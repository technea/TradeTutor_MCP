"""Adapter boundary for a connected Binance MCP runtime.

The MCP client/Agent OS owns authentication and transport. TradeTutor only
receives a small callable tool registry, so API keys and signed REST requests
never enter this project.
"""

from dataclasses import dataclass
import os
from typing import Any, Callable, Mapping, Protocol


@dataclass(frozen=True)
class TradeProposal:
    symbol: str
    side: str
    quantity: float
    entry_price: float
    stop_price: float
    target_price: float
    rationale: str


class MCPToolCaller(Protocol):
    """Minimal interface implemented by the connected MCP client."""

    def __call__(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]: ...


class BinanceMCPAdapter:
    """Translate TradeTutor operations into connected MCP tool calls.

    Tool names are deliberately configurable because the connected Binance MCP
    server is the source of truth for its currently exposed tool names.
    """

    def __init__(
        self,
        call_tool: MCPToolCaller | None = None,
        *,
        market_tool: str | None = None,
        account_tool: str | None = None,
        order_tool: str | None = None,
    ) -> None:
        self._call_tool = call_tool
        self.market_tool = market_tool or os.getenv("BINANCE_MCP_MARKET_TOOL", "")
        self.account_tool = account_tool or os.getenv("BINANCE_MCP_ACCOUNT_TOOL", "")
        self.order_tool = order_tool or os.getenv("BINANCE_MCP_ORDER_TOOL", "")

    def _call(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        if not self._call_tool:
            raise RuntimeError(
                "No Binance MCP client is connected. Inject call_tool from the "
                "authorized Agent OS/MCP runtime."
            )
        if not tool_name:
            raise RuntimeError("Binance MCP tool name is not configured.")
        result = self._call_tool(tool_name, arguments)
        if not isinstance(result, Mapping):
            raise TypeError("MCP tool result must be a mapping.")
        return result

    def get_market_context(self, symbol: str) -> Mapping[str, Any]:
        return self._call(self.market_tool, {"symbol": symbol})

    def get_account_context(self) -> Mapping[str, Any]:
        return self._call(self.account_tool, {})

    def execute_confirmed_order(
        self, proposal: TradeProposal, *, confirmed: bool
    ) -> Mapping[str, Any]:
        if not confirmed:
            raise PermissionError("Explicit user confirmation is required before execution.")
        return self._call(
            self.order_tool,
            {
                "symbol": proposal.symbol,
                "side": proposal.side,
                "quantity": proposal.quantity,
                "entry_price": proposal.entry_price,
                "stop_price": proposal.stop_price,
                "target_price": proposal.target_price,
                "rationale": proposal.rationale,
            },
        )
