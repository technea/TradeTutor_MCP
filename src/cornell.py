from dataclasses import dataclass, field
from typing import Iterable

VALID_DECISIONS = {"potential_setup", "wait", "no_trade"}


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
        self.question = self.question.strip()
        self.summary = self.summary.strip()
        if not self.question:
            raise ValueError("question is required")
        if self.decision not in VALID_DECISIONS:
            raise ValueError(f"decision must be one of {sorted(VALID_DECISIONS)}")
        if not self.summary:
            raise ValueError("summary is required")

    def to_markdown(self) -> str:
        sections = [
            ("Question", [self.question]),
            ("Cues", self.cues),
            ("Notes", self.notes),
            ("Analysis", self.analysis),
            ("Risk", self.risk),
            ("Decision", [self.decision]),
            ("Summary", [self.summary]),
        ]
        output = []
        for title, items in sections:
            output.append(f"## {title}")
            if len(items) == 1:
                output.append(items[0])
            else:
                output.extend(f"- {item}" for item in items) if items else output.append("- None recorded")
            output.append("")
        return "\n".join(output).strip() + "\n"


def _clean(items: Iterable[str] | None) -> list[str]:
    return [str(item).strip() for item in (items or []) if str(item).strip()]


def build_cornell_analysis(
    question: str,
    cues: Iterable[str] | None = None,
    notes: Iterable[str] | None = None,
    analysis: Iterable[str] | None = None,
    risk: Iterable[str] | None = None,
    decision: str = "wait",
    summary: str = "",
) -> CornellAnalysis:
    return CornellAnalysis(
        question=question,
        cues=_clean(cues),
        notes=_clean(notes),
        analysis=_clean(analysis),
        risk=_clean(risk),
        decision=decision,
        summary=summary,
    )
