from dataclasses import dataclass


@dataclass(frozen=True)
class TradePlan:
    side: str
    entry_price: float
    stop_price: float
    target_price: float
    risk_amount: float
    position_size: float
    risk_reward: float


def _validate_prices(entry_price: float, stop_price: float, target_price: float) -> None:
    if min(entry_price, stop_price, target_price) <= 0:
        raise ValueError("prices must be greater than zero")


def calculate_position_size(account_balance: float, risk_percent: float, entry_price: float, stop_price: float) -> float:
    if account_balance <= 0:
        raise ValueError("account_balance must be greater than zero")
    if risk_percent <= 0:
        raise ValueError("risk_percent must be greater than zero")
    if entry_price <= 0 or stop_price <= 0 or entry_price == stop_price:
        raise ValueError("entry and stop prices must be positive and different")
    risk_amount = account_balance * risk_percent / 100
    return risk_amount / abs(entry_price - stop_price)


def calculate_risk_reward(entry_price: float, stop_price: float, target_price: float, side: str = "long") -> float:
    _validate_prices(entry_price, stop_price, target_price)
    side = side.lower()
    if side == "long":
        risk = entry_price - stop_price
        reward = target_price - entry_price
    elif side == "short":
        risk = stop_price - entry_price
        reward = entry_price - target_price
    else:
        raise ValueError("side must be 'long' or 'short'")
    if risk <= 0:
        raise ValueError("stop price must define positive risk for the selected side")
    if reward < 0:
        raise ValueError("target price must define non-negative reward")
    return reward / risk


def build_trade_plan(account_balance: float, risk_percent: float, side: str, entry_price: float, stop_price: float, target_price: float) -> TradePlan:
    risk_amount = account_balance * risk_percent / 100
    return TradePlan(side=side.lower(), entry_price=entry_price, stop_price=stop_price, target_price=target_price, risk_amount=risk_amount, position_size=calculate_position_size(account_balance, risk_percent, entry_price, stop_price), risk_reward=calculate_risk_reward(entry_price, stop_price, target_price, side))
