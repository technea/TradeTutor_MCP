from dataclasses import dataclass, field
from typing import Mapping


DECISIONS = {"potential_setup", "wait", "no_trade"}


@dataclass
class CornellAnalysis:
    question: str
    cues: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    analysis: list[str] = field(default_factory=list)
    risk: list[str] = field(default_factory=list)
    decision: str = "wait"
    summary: str = ""

    def __post_init__(self) -> None:
        if not self.question.strip():
            raise ValueError("question is required")
        if self.decision not in DECISIONS:
            raise ValueError(f"decision must be one of {sorted(DECISIONS)}")
        if not self.summary.strip():
            raise ValueError("summary is required")

    def to_markdown(self) -> str:
        def bullets(items: list[str]) -> str:
            return "\n".join(f"- {item}" for item in items) or "- None recorded"

        return "\n".join([
            "## Question", self.question, "",
            "## Cues", bullets(self.cues), "",
            "## Notes", bullets(self.notes), "",
            "## Analysis", bullets(self.analysis), "",
            "## Risk", bullets(self.risk), "",
            "## Decision", self.decision, "",
            "## Summary", self.summary, "",
        ])


def build_cornell_analysis(
    question: str,
    market_context: Mapping[str, object],
    *,
    analysis_points: list[str] | None = None,
    risk_points: list[str] | None = None,
    decision: str = "wait",
    summary: str = "",
) -> CornellAnalysis:
    cues = []
    notes = []
    for key, value in market_context.items():
        notes.append(f"{key}: {value}")
        if key.lower() in {"trend", "momentum", "volume", "support", "resistance", "market_condition"}:
            cues.append(f"{key}: {value}")

    return CornellAnalysis(
        question=question,
        cues=cues,
        notes=notes,
        analysis=analysis_points or [],
        risk=risk_points or [],
        decision=decision,
        summary=summary or "No final thesis supplied.",
    )
