"""Live workflow boundary: Binance MCP -> analysis -> proposal -> confirmation -> execution."""

from dataclasses import dataclass
from typing import Any, Mapping

from .agent import TradeTutor
from .binance_mcp import BinanceMCPAdapter, TradeProposal


@dataclass(frozen=True)
class AnalysisResult:
    symbol: str
    cornell_markdown: str
    proposal: TradeProposal | None


class TradeTutorRuntime:
    """Orchestrate the human-in-the-loop trading workflow."""

    def __init__(self, mcp: BinanceMCPAdapter | None = None) -> None:
        self.mcp = mcp or BinanceMCPAdapter()
        self.agent = TradeTutor(self.mcp)

    def analyze_market(
        self,
        symbol: str,
        *,
        decision: str = "wait",
        analysis_points: list[str] | None = None,
        risk_points: list[str] | None = None,
        summary: str = "No final thesis supplied.",
    ) -> AnalysisResult:
        context: Mapping[str, Any] = self.mcp.get_market_context(symbol)
        analysis = self.agent.analyze(
            symbol,
            context,
            decision=decision,
            analysis_points=analysis_points,
            risk_points=risk_points,
            summary=summary,
        )
        return AnalysisResult(
            symbol=symbol,
            cornell_markdown=analysis.to_markdown(),
            proposal=None,
        )

    def create_proposal(
        self,
        symbol: str,
        *,
        risk_percent: float,
        side: str,
        entry_price: float,
        stop_price: float,
        target_price: float,
        rationale: str,
    ) -> TradeProposal:
        account = self.mcp.get_account_context()
        balance = float(account["balance"])
        plan = self.agent.create_trade_plan(
            balance,
            risk_percent,
            side,
            entry_price,
            stop_price,
            target_price,
        )
        return self.agent.prepare_proposal(symbol, plan, rationale)

    def execute_after_confirmation(self, proposal: TradeProposal) -> Mapping[str, Any]:
        """Execute only after the caller has explicitly confirmed the proposal."""
        return self.agent.execute(proposal, confirmed=True)
