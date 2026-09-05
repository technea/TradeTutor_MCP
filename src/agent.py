from .binance_mcp import BinanceMCPAdapter, TradeProposal
from .cornell import CornellAnalysis, build_cornell_analysis
from .journal import TradeJournalEntry, append_trade_entry
from .risk import TradePlan, build_trade_plan


class TradeTutor:
    """Orchestrates analysis, risk planning, confirmation, and journaling."""

    def __init__(self, binance: BinanceMCPAdapter | None = None):
        self.binance = binance or BinanceMCPAdapter()

    def analyze(self, symbol: str, market_context: dict) -> CornellAnalysis:
        return build_cornell_analysis(
            question=f"Should {symbol} be considered for a trade?",
            cues=market_context.get("cues", []),
            notes=market_context.get("notes", []),
            analysis=market_context.get("analysis", []),
            risk=market_context.get("risk", []),
            decision=market_context.get("decision", "wait"),
            summary=market_context.get("summary", "No conclusion supplied."),
        )

    def create_trade_plan(self, **kwargs) -> TradePlan:
        return build_trade_plan(**kwargs)

    def prepare_proposal(self, plan: TradePlan, rationale: str) -> TradeProposal:
        return TradeProposal(
            symbol=plan.symbol,
            side=plan.side,
            quantity=plan.position_size,
            entry_price=plan.entry_price,
            stop_price=plan.stop_price,
            target_price=plan.target_price,
            rationale=rationale,
        )

    def execute(self, proposal: TradeProposal, confirmed: bool = False):
        return self.binance.execute_confirmed_order(proposal, confirmed=confirmed)

    def record_trade(self, journal_path: str, entry: TradeJournalEntry) -> None:
        append_trade_entry(journal_path, entry)
