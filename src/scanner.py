"""Deterministic multi-symbol market scanner built on supplied observations."""

from dataclasses import dataclass
from typing import Any, Mapping

from .alerts import detect_alerts
from .analytics import MarketScore, score_market, rank_watchlist


@dataclass(frozen=True)
class ScanResult:
    symbol: str
    score: MarketScore
    alerts: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {"symbol": self.symbol, "score": self.score.to_dict(), "alerts": list(self.alerts)}


def scan_markets(markets: Mapping[str, Mapping[str, Any]]) -> list[ScanResult]:
    results: list[ScanResult] = []
    for symbol, observations in markets.items():
        score = score_market(symbol, observations)
        alerts = tuple(a.__dict__ for a in detect_alerts(symbol, observations))
        results.append(ScanResult(symbol=symbol, score=score, alerts=alerts))
    ranked = rank_watchlist([item.score for item in results])
    order = {item.symbol: i for i, item in enumerate(ranked)}
    return sorted(results, key=lambda item: order[item.symbol])
