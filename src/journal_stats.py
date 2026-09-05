"""Small, dependency-free trade journal analytics layer."""

from collections import Counter
from typing import Any, Iterable, Mapping


def summarize_journal(entries: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(entries)
    outcomes = [str(row.get("outcome", "")).lower() for row in rows]
    wins = sum(x == "win" for x in outcomes)
    losses = sum(x == "loss" for x in outcomes)
    rs = [float(row["r_multiple"]) for row in rows if row.get("r_multiple") is not None]
    lessons = [str(row["lesson"]) for row in rows if row.get("lesson")]
    return {
        "trades": len(rows),
        "wins": wins,
        "losses": losses,
        "win_rate": wins / len(rows) if rows else 0.0,
        "average_r_multiple": sum(rs) / len(rs) if rs else 0.0,
        "total_r_multiple": sum(rs),
        "recurring_lessons": Counter(lessons).most_common(5),
    }
