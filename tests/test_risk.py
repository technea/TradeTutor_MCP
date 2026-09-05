from src.risk import calculate_position_size, calculate_risk_reward, build_trade_plan


def test_position_size() -> None:
    assert calculate_position_size(1000, 1, 100, 95) == 2


def test_long_risk_reward() -> None:
    assert calculate_risk_reward(100, 95, 110, "long") == 2


def test_short_risk_reward() -> None:
    assert calculate_risk_reward(100, 105, 90, "short") == 2


def test_trade_plan() -> None:
    plan = build_trade_plan(1000, 1, "long", 100, 95, 110)
    assert plan.risk_amount == 10
    assert plan.position_size == 2
    assert plan.risk_reward == 2
