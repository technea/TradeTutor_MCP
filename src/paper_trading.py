"""Safe paper-trading simulator. It never calls Binance write tools."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PaperTrade:
    symbol: str
    side: str
    quantity: float
    entry_price: float
    stop_price: float
    target_price: float

    @property
    def risk_per_unit(self) -> float:
        return abs(self.entry_price - self.stop_price)

    @property
    def reward_per_unit(self) -> float:
        return abs(self.target_price - self.entry_price)

    @property
    def risk_reward(self) -> float:
        risk = self.risk_per_unit
        return self.reward_per_unit / risk if risk else 0.0


class PaperBroker:
    """In-memory simulator for demos and tests."""

    def __init__(self) -> None:
        self.trades: list[PaperTrade] = []

    def submit(self, trade: PaperTrade) -> PaperTrade:
        if trade.quantity <= 0 or trade.entry_price <= 0:
            raise ValueError("quantity and entry price must be positive")
        self.trades.append(trade)
        return trade

    def close(self, index: int, exit_price: float) -> float:
        trade = self.trades[index]
        if exit_price <= 0:
            raise ValueError("exit price must be positive")
        direction = 1 if trade.side.upper() == "BUY" else -1
        return (exit_price - trade.entry_price) * trade.quantity * direction
