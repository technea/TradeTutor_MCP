"""Portfolio safety rules for the TradeTutor proposal pipeline."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioLimits:
    max_risk_percent: float = 1.0
    max_daily_loss_percent: float = 3.0
    max_open_positions: int = 3
    kill_switch: bool = False


@dataclass(frozen=True)
class PortfolioState:
    equity: float
    daily_pnl: float = 0.0
    open_positions: int = 0


class PortfolioGuardian:
    """Fail-closed guard that must approve a proposal before execution."""

    def __init__(self, limits: PortfolioLimits | None = None) -> None:
        self.limits = limits or PortfolioLimits()

    def validate(self, state: PortfolioState, risk_percent: float) -> tuple[bool, tuple[str, ...]]:
        reasons: list[str] = []
        if self.limits.kill_switch:
            reasons.append("trading kill switch is enabled")
        if risk_percent <= 0 or risk_percent > self.limits.max_risk_percent:
            reasons.append(f"risk {risk_percent:.2f}% exceeds max {self.limits.max_risk_percent:.2f}%")
        if state.equity <= 0:
            reasons.append("account equity must be positive")
        if state.equity > 0 and state.daily_pnl <= -(state.equity * self.limits.max_daily_loss_percent / 100):
            reasons.append("daily loss limit has been reached")
        if state.open_positions >= self.limits.max_open_positions:
            reasons.append("maximum open positions reached")
        return (not reasons, tuple(reasons))

    def assert_allowed(self, state: PortfolioState, risk_percent: float) -> None:
        allowed, reasons = self.validate(state, risk_percent)
        if not allowed:
            raise PermissionError("Portfolio Guardian blocked execution: " + "; ".join(reasons))
