from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .binance_mcp import BinanceMCPAdapter, TradeProposal
from .cornell import CornellAnalysis, build_cornell_analysis
from .journal import TradeJournalEntry, append_trade_entry
from .risk import TradePlan, build_trade_plan


@dataclass
class TradeTutor:
    mcp: BinanceMCPAdapter

    def analyze(self, symbol: str, market_context: Mapping[str, Any], *, decision: str = "wait", analysis_points: list[str] | None = None, risk_points: list[str] | None = None, summary: str = "") -> CornellAnalysis:
        return build_cornell_analysis(
            f"Should {symbol} be considered for a trade?",
            market_context,
            analysis_points=analysis_points,
            risk_points=risk_points,
            decision=decision,
            summary=summary,
        )

    def create_trade_plan(self, account_balance: float, risk_percent: float, side: str, entry_price: float, stop_price: float, target_price: float) -> TradePlan:
        return build_trade_plan(account_balance, risk_percent, side, entry_price, stop_price, target_price)

    def prepare_proposal(self, symbol: str, plan: TradePlan, rationale: str) -> TradeProposal:
        return TradeProposal(symbol=symbol, side=plan.side, quantity=plan.position_size, entry_price=plan.entry_price, stop_price=plan.stop_price, target_price=plan.target_price, rationale=rationale)

    def execute(self, proposal: TradeProposal, *, confirmed: bool) -> Mapping[str, Any]:
        return self.mcp.execute_confirmed_order(proposal, confirmed=confirmed)

    @staticmethod
    def record_trade(path: str | Path, entry: TradeJournalEntry) -> None:
        append_trade_entry(path, entry)
