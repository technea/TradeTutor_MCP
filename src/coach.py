"""Post-trade review helpers for thesis/outcome comparison."""

from typing import Any, Mapping


def review_trade(*, thesis: str, expected: str, outcome: str, r_multiple: float | None = None) -> Mapping[str, Any]:
    matched = expected.strip().lower() == outcome.strip().lower()
    if r_multiple is not None and r_multiple < 0:
        lesson = "The thesis did not survive the realized outcome; review invalidation and risk sizing."
    elif matched:
        lesson = "The realized outcome matched the stated expectation; review what evidence was most useful."
    else:
        lesson = "The realized outcome differed from the expectation; identify which assumption changed."
    return {
        "thesis": thesis,
        "expected": expected,
        "outcome": outcome,
        "r_multiple": r_multiple,
        "thesis_correct": matched,
        "lesson": lesson,
    }
