"""TradeTutor orchestration: scan -> analyze -> guard -> confirm -> execute/review."""

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .agent import TradeTutor
from .binance_mcp import BinanceMCPAdapter, TradeProposal
from .coach import review_trade
from .mcp_capabilities import inspect_tools
from .paper_trading import PaperBroker, PaperTrade
from .portfolio_guardian import PortfolioGuardian, PortfolioState
from .scanner import scan_markets


@dataclass(frozen=True)
class AnalysisResult:
    symbol: str
    cornell_markdown: str
    proposal: TradeProposal | None


class TradeTutorRuntime:
    """Single application boundary for the human-in-the-loop workflow."""

    def __init__(self, mcp: BinanceMCPAdapter | None = None, *, guardian: PortfolioGuardian | None = None) -> None:
        self.mcp = mcp or BinanceMCPAdapter()
        self.agent = TradeTutor(self.mcp)
        self.guardian = guardian or PortfolioGuardian()
        self.paper_broker = PaperBroker()

    def scan(self, markets: Mapping[str, Mapping[str, Any]]) -> list[Any]:
        return scan_markets(markets)

    def capabilities(self, tools: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
        return inspect_tools(tools).to_dict()

    def analyze_market(self, symbol: str, *, decision: str = "wait", analysis_points: list[str] | None = None,
                       risk_points: list[str] | None = None, summary: str = "No final thesis supplied.") -> AnalysisResult:
        context = self.mcp.get_market_context(symbol)
        analysis = self.agent.analyze(symbol, context, decision=decision, analysis_points=analysis_points,
                                      risk_points=risk_points, summary=summary)
        return AnalysisResult(symbol=symbol, cornell_markdown=analysis.to_markdown(), proposal=None)

    def create_proposal(self, symbol: str, *, risk_percent: float, side: str, entry_price: float,
                        stop_price: float, target_price: float, rationale: str,
                        daily_pnl: float = 0.0, open_positions: int = 0) -> TradeProposal:
        account = self.mcp.get_account_context()
        balance = float(account["balance"])
        state = PortfolioState(equity=balance, daily_pnl=daily_pnl, open_positions=open_positions)
        self.guardian.assert_allowed(state, risk_percent)
        plan = self.agent.create_trade_plan(balance, risk_percent, side, entry_price, stop_price, target_price)
        return self.agent.prepare_proposal(symbol, plan, rationale)

    def paper_execute(self, proposal: TradeProposal, *, fill_price: float | None = None) -> PaperTrade:
        trade = PaperTrade(proposal.symbol, proposal.side, proposal.quantity, proposal.entry_price,
                           proposal.stop_price, proposal.target_price)
        self.paper_broker.submit(trade)
        if fill_price is not None:
            self.paper_broker.close(len(self.paper_broker.trades) - 1, fill_price)
        return trade

    def execute_after_confirmation(self, proposal: TradeProposal) -> Mapping[str, Any]:
        """Live execution remains behind explicit caller confirmation."""
        return self.agent.execute(proposal, confirmed=True)

    def review_trade(self, *, thesis: str, expected: str, outcome: str,
                     r_multiple: float | None = None) -> Mapping[str, Any]:
        return review_trade(thesis=thesis, expected=expected, outcome=outcome, r_multiple=r_multiple)
