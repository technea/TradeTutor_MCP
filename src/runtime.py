"""Live-runtime workflow boundary for an authorized Binance MCP connection."""

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
    """Orchestrates MCP context -> analysis -> proposal -> confirmed execution.

    The actual Binance tools remain outside this repository and are supplied by
    the connected authorized MCP/Agent OS runtime.
    """

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
        return AnalysisResult(symbol=symbol, cornell_markdown=analysis.to_markdown(), proposal=None)

    def execute_after_confirmation(self, proposal: TradeProposal) -> Mapping[str, Any]:
        """Execute only when the caller explicitly confirms the proposal."""
        return self.agent.execute(proposal, confirmed=True)
