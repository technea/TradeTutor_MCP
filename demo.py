"""Safe local demo of the TradeTutor workflow.

This demo uses supplied sample market context. It does not place orders.
Live market/account context must come from the authorized Binance MCP runtime.
"""

from src.agent import TradeTutor
from src.binance_mcp import BinanceMCPAdapter


def main() -> None:
    agent = TradeTutor(BinanceMCPAdapter())
    sample_context = {
        "trend": "Sample bullish trend",
        "momentum": "Sample positive momentum",
        "volume": "Sample above-average volume",
        "support": "Sample support zone",
        "resistance": "Sample resistance zone",
        "market_condition": "Demo data only",
    }

    analysis = agent.analyze(
        "BTCUSDT",
        sample_context,
        decision="wait",
        analysis_points=[
            "Bullish evidence should be verified against live permitted market data.",
            "A breakout should be confirmed rather than assumed from sample data.",
        ],
        risk_points=[
            "Define invalidation before considering an order.",
            "Keep position risk within the user's predefined limit.",
        ],
        summary="Demo only: wait for live confirmation before considering any trade.",
    )

    print(analysis.to_markdown())
    print("\nNo order was submitted. Connect the authorized Binance MCP runtime for live execution.")


if __name__ == "__main__":
    main()
