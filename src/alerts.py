"""Rule-based monitoring helpers for TradeTutor.

The monitor emits events from caller-supplied observations. Scheduling and
live data transport remain the responsibility of the MCP/agent host.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class Alert:
    symbol: str
    kind: str
    message: str
    severity: str = "info"

    def to_dict(self) -> dict[str, str]:
        return {
            "symbol": self.symbol,
            "kind": self.kind,
            "message": self.message,
            "severity": self.severity,
        }


def detect_alerts(symbol: str, observations: Mapping[str, Any], *, price_change_threshold: float = 3.0, volume_ratio_threshold: float = 2.0, spread_threshold: float = 0.30) -> list[Alert]:
    """Detect explainable conditions; no trade action is taken."""
    alerts: list[Alert] = []
    change = float(observations.get("change_percent", 0.0))
    volume = float(observations.get("volume_ratio", 1.0))
    spread = float(observations.get("spread_percent", 0.0))

    if abs(change) >= price_change_threshold:
        direction = "up" if change > 0 else "down"
        alerts.append(Alert(symbol, "price_move", f"Price moved {change:.2f}% ({direction})", "warning"))
    if volume >= volume_ratio_threshold:
        alerts.append(Alert(symbol, "volume_spike", f"Volume is {volume:.2f}x baseline", "warning"))
    if spread >= spread_threshold:
        alerts.append(Alert(symbol, "liquidity", f"Bid/ask spread is {spread:.3f}%", "high"))
    return alerts
