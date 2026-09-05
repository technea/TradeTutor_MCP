from dataclasses import dataclass


@dataclass(frozen=True)
class TradePlan:
    symbol: str
    side: str
    entry_price: float
    stop_price: float
    target_price: float
    risk_amount: float
    position_size: float
    risk_reward: float


def _validate_side(side: str) -> str:
    side = side.lower()
    if side not in {"long", "short"}:
        raise ValueError("side must be 'long' or 'short'")
    return side


def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_price: float,
) -> float:
    if account_balance <= 0 or risk_percent <= 0:
        raise ValueError("account_balance and risk_percent must be positive")
    if entry_price <= 0 or stop_price <= 0 or entry_price == stop_price:
        raise ValueError("entry and stop prices must be positive and different")
    risk_amount = account_balance * risk_percent / 100
    return risk_amount / abs(entry_price - stop_price)


def calculate_risk_reward(
    entry_price: float,
    stop_price: float,
    target_price: float,
    side: str = "long",
) -> float:
    side = _validate_side(side)
    if min(entry_price, stop_price, target_price) <= 0:
        raise ValueError("prices must be positive")
    if side == "long":
        risk = entry_price - stop_price
        reward = target_price - entry_price
    else:
        risk = stop_price - entry_price
        reward = entry_price - target_price
    if risk <= 0 or reward < 0:
        raise ValueError("prices do not form a valid trade plan for the selected side")
    return reward / risk


def build_trade_plan(
    symbol: str,
    side: str,
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_price: float,
    target_price: float,
) -> TradePlan:
    side = _validate_side(side)
    position_size = calculate_position_size(account_balance, risk_percent, entry_price, stop_price)
    risk_amount = account_balance * risk_percent / 100
    risk_reward = calculate_risk_reward(entry_price, stop_price, target_price, side)
    return TradePlan(symbol, side, entry_price, stop_price, target_price, risk_amount, position_size, risk_reward)
