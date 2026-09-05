"""Human-readable explanations for TradeTutor decisions."""

from typing import Any, Mapping


def explain_decision(*, symbol: str, decision: str, score: int, risk_reward: float | None = None, warnings: list[str] | None = None) -> Mapping[str, Any]:
    warnings = warnings or []
    reasons: list[str] = [f"Directional score for {symbol}: {score}.", f"Workflow decision: {decision}."]
    if risk_reward is not None:
        reasons.append(f"Planned risk/reward: {risk_reward:.2f}R.")
    if warnings:
        reasons.append("Risk warnings: " + "; ".join(warnings))
    return {
        "decision": decision,
        "reasons": reasons,
        "disclaimer": "This explanation summarizes supplied evidence; it is not a guarantee or financial advice.",
    }
