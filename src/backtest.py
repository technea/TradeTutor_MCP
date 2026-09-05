"""Small deterministic backtesting utilities for educational demos."""

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class BacktestResult:
    trades: int
    wins: int
    losses: int
    win_rate: float
    total_r_multiple: float


def evaluate_signals(signals: Sequence[str]) -> BacktestResult:
    """Evaluate a sequence containing 'win'/'loss' labels.

    This is deliberately a result evaluator, not a claim of historical
    profitability. Real OHLC data and strategy rules should be supplied by
    the caller for a meaningful backtest.
    """
    normalized = [str(item).lower() for item in signals]
    wins = normalized.count("win")
    losses = normalized.count("loss")
    trades = wins + losses
    win_rate = wins / trades if trades else 0.0
    total_r = float(wins - losses)
    return BacktestResult(trades, wins, losses, win_rate, total_r)
