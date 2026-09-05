from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TradeProposal:
    symbol: str
    side: str
    quantity: float
    entry_price: float | None
    stop_price: float | None
    target_price: float | None
    rationale: str


class BinanceMCPAdapter:
    """Boundary for an authorized Binance MCP/Agent OS runtime.

    This repository deliberately does not contain Binance secrets or pretend
    to execute live orders. The connected MCP runtime is responsible for the
    actual authorized Binance operations.
    """

    def get_market_context(self, symbol: str) -> dict[str, Any]:
        raise NotImplementedError("Supply market data through the authorized Binance MCP runtime")

    def get_account_context(self) -> dict[str, Any]:
        raise NotImplementedError("Supply account data through the authorized Binance MCP runtime")

    def execute_confirmed_order(self, proposal: TradeProposal, confirmed: bool = False) -> Any:
        if not confirmed:
            raise PermissionError("Explicit user confirmation is required before execution")
        raise NotImplementedError("Delegate order execution to the authorized Binance MCP runtime")
