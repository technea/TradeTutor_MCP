# TradeTutor-MCP

> **Explainable, human-in-the-loop trading education and execution powered by Binance MCP.**

TradeTutor-MCP turns a market question into a controlled workflow:

```text
MCP market context → Scan/Score/Alerts → Cornell analysis → Risk plan
→ Portfolio Guardian → Trade proposal → Human confirmation
→ Paper or authorized Binance MCP execution → Journal → Post-trade coach
```

## Current implementation

- `src/runtime.py` is the main orchestration boundary for scanning, analysis, risk checks, paper execution, capabilities, live confirmation, and post-trade review.
- `src/binance_mcp.py` maps spot market context to Binance market-data tools and discovers account/order tools from the connected MCP server.
- `src/analytics.py` provides transparent market scoring and watchlist ranking.
- `src/alerts.py` detects price, volume, and liquidity warnings without placing trades.
- `src/scanner.py` ranks supplied multi-symbol market observations.
- `src/portfolio_guardian.py` enforces max risk, daily-loss, open-position, and kill-switch rules before proposals are created.
- `src/paper_trading.py` provides an in-memory simulator that never calls Binance write tools.
- `src/mcp_capabilities.py` reports discovered market/account/order capabilities without assuming permissions.
- `src/journal_stats.py` calculates win rate, R-multiples, and recurring lessons from structured journal records.
- `src/coach.py` compares an original thesis with a realized outcome and produces a review lesson.
- `src/explain.py` produces a human-readable decision explanation.
- No Binance API keys, signed REST order implementation, or credentials are stored in this repository.
- Live execution remains blocked unless explicit confirmation reaches the adapter.

## Binance MCP market tools

| Purpose | MCP tool |
|---|---|
| Current price | `get_spot_symbol_price_ticker` |
| Best bid/ask | `get_spot_symbol_order_book_ticker` |
| Candles | `get_spot_kline_candlestick_data` |
| 24h statistics | `get_spot_24hr_ticker_price_change_statistics` |

## End-to-end runtime

```python
runtime = TradeTutorRuntime(mcp)

# 1. Scan supplied market observations; no trading occurs.
ranked = runtime.scan(markets)

# 2. Build evidence-backed Cornell analysis.
analysis = runtime.analyze_market("BTCUSDT")

# 3. Proposal creation is protected by Portfolio Guardian.
proposal = runtime.create_proposal(
    "BTCUSDT",
    risk_percent=1.0,
    side="long",
    entry_price=100000,
    stop_price=99000,
    target_price=102000,
    rationale="User-approved setup rationale",
)

# 4A. Safe demo path: paper execution.
runtime.paper_execute(proposal)

# 4B. Live path: only after an explicit user confirmation.
result = runtime.execute_after_confirmation(proposal)

# 5. Post-trade review.
review = runtime.review_trade(
    thesis="Trend continuation",
    expected="bullish",
    outcome="bullish",
    r_multiple=1.8,
)
```

The example prices are illustrative only and are not current quotes or recommendations.

## Connect the real Binance MCP runtime

The Binance MCP host/client remains responsible for authentication and transport. Inject an authorized tool caller and tool lister into `BinanceMCPAdapter`. The adapter discovers account and order capabilities at runtime rather than guessing private or changing write-tool names.

If no compatible order-write capability is exposed, the adapter stops instead of inventing an endpoint.

## Safety architecture

1. Market data is evidence, not an automatic recommendation.
2. Scanner and alerts are read-only.
3. Portfolio Guardian is fail-closed for configured risk limits.
4. Paper trading is completely separate from live execution.
5. Live orders require explicit confirmation.
6. Authentication/secrets remain outside the repository.
7. Post-trade reviews describe outcomes and lessons; they do not guarantee future performance.

## Development

```bash
python -m venv .venv
pip install -r requirements.txt
pytest
python demo.py
```

## Hackathon focus

The project now demonstrates a complete visible Track B story:

**MCP market data → intelligent scanning → Cornell reasoning → explainable risk plan → portfolio protection → human confirmation → paper/live execution boundary → journal intelligence → post-trade coaching.**

## License

MIT
