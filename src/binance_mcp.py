from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class TradeProposal:
    symbol: str
    side: str
    quantity: float
    entry_price: float
    stop_price: float
    target_price: float
    rationale: str


class BinanceMCPAdapter:
    """Boundary for an authorized Binance MCP/Agent OS runtime.

    This repository intentionally does not contain API-key handling or signed
    REST order code. A connected MCP runtime should provide the actual tools.
    """

    def get_market_context(self, symbol: str) -> Mapping[str, Any]:
        raise NotImplementedError("Supply market data through the authorized Binance MCP runtime.")

    def get_account_context(self) -> Mapping[str, Any]:
        raise NotImplementedError("Supply account data through the authorized Binance MCP runtime.")

    def execute_confirmed_order(self, proposal: TradeProposal, *, confirmed: bool) -> Mapping[str, Any]:
        if not confirmed:
            raise PermissionError("Explicit user confirmation is required before execution.")
        raise NotImplementedError("Delegate order execution to the connected authorized Binance MCP runtime.")
