"""Binance MCP integration boundary.

The connected MCP host owns authentication/transport. TradeTutor receives a
small tool-caller interface and never stores API keys or signed REST requests.

Known public Binance MCP tool names are used for market data. Account and
order tools are discovered from the connected MCP server so this project does
not hard-code a private or changing write-tool name.
"""

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence


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
    def __call__(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]: ...


class MCPToolLister(Protocol):
    def __call__(self) -> Sequence[Mapping[str, Any]]: ...


class BinanceMCPAdapter:
    """Translate TradeTutor operations into Binance MCP calls."""

    PRICE_TOOL = "get_spot_symbol_price_ticker"
    ORDER_BOOK_TOOL = "get_spot_symbol_order_book_ticker"
    KLINE_TOOL = "get_spot_kline_candlestick_data"
    TICKER_24H_TOOL = "get_spot_24hr_ticker_price_change_statistics"

    def __init__(self, call_tool: MCPToolCaller | None = None, *, list_tools: MCPToolLister | None = None) -> None:
        self._call_tool = call_tool
        self._list_tools = list_tools

    def _call(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        if not self._call_tool:
            raise RuntimeError("Inject the connected authorized Binance MCP tool caller.")
        if not tool_name:
            raise RuntimeError("Binance MCP tool name is not configured.")
        result = self._call_tool(tool_name, arguments)
        if not isinstance(result, Mapping):
            raise TypeError("MCP tool result must be a mapping.")
        return result

    def _discover(self, keywords: tuple[str, ...]) -> tuple[str, Mapping[str, Any]]:
        if not self._list_tools:
            raise RuntimeError("MCP tool discovery is required for account/trading operations.")
        matches: list[tuple[int, str, Mapping[str, Any]]] = []
        for tool in self._list_tools():
            name = str(tool.get("name", ""))
            description = str(tool.get("description", "")).lower()
            haystack = f"{name.lower()} {description}"
            score = sum(1 for keyword in keywords if keyword in haystack)
            if score:
                matches.append((score, name, tool))
        if not matches:
            raise RuntimeError(f"No connected Binance MCP tool matched: {keywords}")
        matches.sort(key=lambda item: (-item[0], item[1]))
        _, name, schema = matches[0]
        return name, schema

    def get_market_context(self, symbol: str) -> Mapping[str, Any]:
        return {
            "symbol": symbol,
            "price": self._call(self.PRICE_TOOL, {"symbol": symbol}),
            "order_book": self._call(self.ORDER_BOOK_TOOL, {"symbol": symbol}),
            "candles_1h": self._call(self.KLINE_TOOL, {"symbol": symbol, "interval": "1h", "limit": 50}),
            "ticker_24h": self._call(self.TICKER_24H_TOOL, {"symbol": symbol}),
        }

    def get_account_context(self) -> Mapping[str, Any]:
        tool, _ = self._discover(("account", "balance"))
        return self._call(tool, {})

    @staticmethod
    def _order_arguments(schema: Mapping[str, Any], proposal: TradeProposal) -> dict[str, Any]:
        properties = schema.get("inputSchema", schema)
        if not isinstance(properties, Mapping):
            properties = {}
        properties = properties.get("properties", {}) if isinstance(properties.get("properties", {}), Mapping) else {}
        aliases = {
            "symbol": ("symbol",),
            "side": ("side",),
            "quantity": ("quantity", "qty", "baseQuantity"),
            "type": ("type", "orderType"),
        }
        source = {
            "symbol": proposal.symbol,
            "side": proposal.side.upper(),
            "quantity": proposal.quantity,
            "type": "MARKET",
        }
        result: dict[str, Any] = {}
        for target, names in aliases.items():
            for name in names:
                if name in properties:
                    result[name] = source[target]
                    break
        if "symbol" not in result or "side" not in result:
            raise RuntimeError("Discovered Binance order tool does not expose symbol/side fields.")
        if not any(key in result for key in ("quantity", "qty", "baseQuantity")):
            raise RuntimeError("Discovered Binance order tool does not expose a quantity field.")
        return result

    def execute_confirmed_order(self, proposal: TradeProposal, *, confirmed: bool) -> Mapping[str, Any]:
        if not confirmed:
            raise PermissionError("Explicit user confirmation is required before execution.")
        tool, schema = self._discover(("order", "place", "trade"))
        return self._call(tool, self._order_arguments(schema, proposal))
