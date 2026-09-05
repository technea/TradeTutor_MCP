"""Runtime bridge for an already-authorized Binance MCP session.

TradeTutor deliberately does not implement Binance authentication or store API
keys. A supported MCP host (ChatGPT, Claude, Codex, VS Code, or a compatible
MCP client) owns the authorization and transport, then injects its tool caller
and tool discovery functions into BinanceMCPAdapter.

Binance MCP endpoint:
    https://agent.binance.com/mcp/agentic
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from .binance_mcp import BinanceMCPAdapter, TradeProposal

ToolCaller = Callable[[str, Mapping[str, Any]], Mapping[str, Any]]
ToolLister = Callable[[], Sequence[Mapping[str, Any]]]


@dataclass
class AuthorizedBinanceRuntime:
    """Bind TradeTutor to an externally authorized Binance MCP session."""

    call_tool: ToolCaller
    list_tools: ToolLister

    def adapter(self) -> BinanceMCPAdapter:
        return BinanceMCPAdapter(self.call_tool, list_tools=self.list_tools)

    def check_connection(self) -> Mapping[str, Any]:
        """Discover capabilities without placing an order or moving funds."""
        tools = list(self.list_tools())
        names = [str(tool.get("name", "")) for tool in tools]
        account = []
        order = []
        for tool in tools:
            name = str(tool.get("name", ""))
            description = str(tool.get("description", "")).lower()
            text = f"{name.lower()} {description}"
            if "account" in text or "balance" in text or "position" in text:
                account.append(name)
            if "order" in text or "trade" in text or "place" in text:
                order.append(name)
        return {
            "connected": True,
            "tool_count": len(names),
            "account_capabilities": sorted(set(account)),
            "trading_capabilities": sorted(set(order)),
            "market_capabilities": [
                name for name in names
                if any(word in name.lower() for word in ("ticker", "kline", "order_book", "price"))
            ],
        }

    def execute(self, proposal: TradeProposal, *, confirmed: bool) -> Mapping[str, Any]:
        """Execute only through the authorized MCP session after confirmation."""
        return self.adapter().execute_confirmed_order(proposal, confirmed=confirmed)
