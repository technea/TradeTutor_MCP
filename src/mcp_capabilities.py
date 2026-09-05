"""Capability inspection for connected MCP tools; never assumes write access."""

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class MCPCapabilities:
    market_read: tuple[str, ...]
    account_read: tuple[str, ...]
    order_write: tuple[str, ...]

    @property
    def can_trade(self) -> bool:
        return bool(self.order_write)

    def to_dict(self) -> dict[str, Any]:
        return {"market_read": list(self.market_read), "account_read": list(self.account_read), "order_write": list(self.order_write), "can_trade": self.can_trade}


def inspect_tools(tools: Iterable[Mapping[str, Any]]) -> MCPCapabilities:
    market: list[str] = []
    account: list[str] = []
    orders: list[str] = []
    for tool in tools:
        name = str(tool.get("name", ""))
        text = (name + " " + str(tool.get("description", ""))).lower()
        if any(k in text for k in ("ticker", "kline", "candlestick", "order book", "orderbook", "market")):
            market.append(name)
        if any(k in text for k in ("account", "balance", "position")):
            account.append(name)
        if any(k in text for k in ("place order", "create order", "new order", "submit order", "trade")):
            orders.append(name)
    return MCPCapabilities(tuple(dict.fromkeys(market)), tuple(dict.fromkeys(account)), tuple(dict.fromkeys(orders)))
