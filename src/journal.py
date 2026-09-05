from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class TradeJournalEntry:
    symbol: str
    side: str
    thesis: str
    decision: str
    entry: float | None = None
    stop: float | None = None
    target: float | None = None
    outcome: str = "Pending"
    lessons: str = ""
    timestamp: str = ""

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_markdown(self) -> str:
        return "\n".join([
            f"### {self.timestamp} — {self.symbol} ({self.side.upper()})",
            f"- **Decision:** {self.decision}",
            f"- **Thesis:** {self.thesis}",
            f"- **Entry:** {self.entry if self.entry is not None else 'N/A'}",
            f"- **Stop:** {self.stop if self.stop is not None else 'N/A'}",
            f"- **Target:** {self.target if self.target is not None else 'N/A'}",
            f"- **Outcome:** {self.outcome}",
            f"- **Lessons:** {self.lessons or 'N/A'}",
            "",
        ])


def append_trade_entry(path: str | Path, entry: TradeJournalEntry) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as file:
        file.write(entry.to_markdown())
