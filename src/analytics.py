"""Explainable market-scoring utilities for TradeTutor.

These functions score supplied market observations; they do not fetch data or
claim to predict prices. They are intentionally deterministic so the scoring
can be tested and shown transparently in a hackathon demo.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class MarketScore:
    symbol: str
    score: int
    regime: str
    confidence: str
    bullish_evidence: tuple[str, ...]
    bearish_evidence: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def label(self) -> str:
        if self.score >= 3:
            return "bullish_bias"
        if self.score <= -3:
            return "bearish_bias"
        return "neutral"

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "score": self.score,
            "label": self.label,
            "regime": self.regime,
            "confidence": self.confidence,
            "bullish_evidence": list(self.bullish_evidence),
            "bearish_evidence": list(self.bearish_evidence),
            "warnings": list(self.warnings),
        }


def score_market(symbol: str, observations: Mapping[str, Any]) -> MarketScore:
    """Create a transparent score from normalized observations.

    Supported optional numeric keys: change_percent, volume_ratio,
    spread_percent, trend_strength (0..1), and volatility_percent.
    """
    change = float(observations.get("change_percent", 0.0))
    volume_ratio = float(observations.get("volume_ratio", 1.0))
    spread = float(observations.get("spread_percent", 0.0))
    trend = float(observations.get("trend_strength", 0.0))
    volatility = float(observations.get("volatility_percent", 0.0))

    score = 0
    bullish: list[str] = []
    bearish: list[str] = []
    warnings: list[str] = []

    if change >= 1.0:
        score += 2
        bullish.append(f"24h change is positive ({change:.2f}%)")
    elif change <= -1.0:
        score -= 2
        bearish.append(f"24h change is negative ({change:.2f}%)")

    if volume_ratio >= 1.25:
        score += 1 if change >= 0 else -1
        (bullish if change >= 0 else bearish).append(
            f"volume is elevated ({volume_ratio:.2f}x baseline)"
        )

    if trend >= 0.7:
        score += 1 if change >= 0 else -1
        (bullish if change >= 0 else bearish).append("trend strength is high")

    if spread > 0.20:
        warnings.append(f"wide bid/ask spread ({spread:.3f}%)")
        score -= 1

    if volatility >= 6.0:
        warnings.append(f"high observed volatility ({volatility:.2f}%)")

    if score >= 3:
        regime = "trend_up"
    elif score <= -3:
        regime = "trend_down"
    else:
        regime = "mixed_or_range"

    confidence = "high" if abs(score) >= 4 and not warnings else "medium" if abs(score) >= 2 else "low"

    return MarketScore(
        symbol=symbol,
        score=score,
        regime=regime,
        confidence=confidence,
        bullish_evidence=tuple(bullish),
        bearish_evidence=tuple(bearish),
        warnings=tuple(warnings),
    )


def rank_watchlist(results: list[MarketScore]) -> list[MarketScore]:
    """Rank symbols by absolute directional score, then confidence."""
    confidence_rank = {"high": 2, "medium": 1, "low": 0}
    return sorted(results, key=lambda item: (abs(item.score), confidence_rank[item.confidence]), reverse=True)
