import pytest

from src.risk import calculate_position_size, calculate_risk_reward, build_trade_plan


def test_position_size_uses_defined_risk():
    assert calculate_position_size(1000, 1, 100, 95) == pytest.approx(2)


def test_long_risk_reward():
    assert calculate_risk_reward(100, 95, 110, "long") == pytest.approx(2)


def test_short_risk_reward():
    assert calculate_risk_reward(100, 105, 90, "short") == pytest.approx(2)


def test_trade_plan():
    plan = build_trade_plan("BTCUSDT", "long", 1000, 1, 100, 95, 110)
    assert plan.position_size == pytest.approx(2)
    assert plan.risk_reward == pytest.approx(2)


def test_invalid_prices():
    with pytest.raises(ValueError):
        calculate_position_size(1000, 1, 100, 100)
