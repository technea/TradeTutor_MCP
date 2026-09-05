from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class TradeJournalEntry:
    timestamp: str
    symbol: str
    side: str
    thesis: str
    decision: str
    entry_price: float | None = None
    stop_price: float | None = None
    target_price: float | None = None
    outcome: str = "Pending"
    lessons: str = ""

    @classmethod
    def now(cls, symbol: str, side: str, thesis: str, decision: str, **kwargs):
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(),
            symbol=symbol,
            side=side,
            thesis=thesis,
            decision=decision,
            **kwargs,
        )

    def to_markdown(self) -> str:
        return (
            f"### {self.timestamp} — {self.symbol}\n"
            f"- **Side:** {self.side}\n"
            f"- **Decision:** {self.decision}\n"
            f"- **Thesis:** {self.thesis}\n"
            f"- **Entry:** {self.entry_price if self.entry_price is not None else 'N/A'}\n"
            f"- **Stop:** {self.stop_price if self.stop_price is not None else 'N/A'}\n"
            f"- **Target:** {self.target_price if self.target_price is not None else 'N/A'}\n"
            f"- **Outcome:** {self.outcome}\n"
            f"- **Lessons:** {self.lessons or 'N/A'}\n\n"
        )


def append_trade_entry(path: str | Path, entry: TradeJournalEntry) -> None:
    journal_path = Path(path)
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    if not journal_path.exists():
        journal_path.write_text("# Trade Journal\n\n", encoding="utf-8")
    with journal_path.open("a", encoding="utf-8") as file:
        file.write(entry.to_markdown())
