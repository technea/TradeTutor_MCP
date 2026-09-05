# TradeTutor-MCP

> **Explainable, human-in-the-loop trading education and execution powered by Binance MCP.**

TradeTutor-MCP transforms a market question into a controlled, explainable workflow:

```text
MCP Market Context
       ↓
Scan / Score / Alerts
       ↓
Cornell Market Analysis
       ↓
Risk Plan + Portfolio Guardian
       ↓
Trade Proposal
       ↓
Human Confirmation
       ↓
Paper or Authorized Binance MCP Execution
       ↓
Trade Journal
       ↓
Post-Trade Coach
```

## 🎯 What is TradeTutor?

TradeTutor is an agentic trading assistant designed to help users **research, understand, plan, and review trades** instead of blindly executing orders.

The key idea is simple:

> **Research → Explain → Assess Risk → Ask Permission → Execute → Record → Learn**

It combines **MCP**, structured **Cornell Notes**, transparent risk calculations, portfolio protection, human confirmation, and post-trade learning into one workflow.

## ✨ Key Features

- 🤖 **Agentic market research** — turns market context into structured analysis.
- 🔌 **Binance MCP integration** — uses the connected MCP environment for permitted market/account/trading capabilities.
- 🧠 **Cornell-style reasoning** — separates the question, cues, notes, analysis, risk, and decision.
- 📊 **Market scanner** — ranks supplied multi-symbol observations.
- 🚨 **Market alerts** — detects price, volume, and liquidity warnings without trading.
- 🛡️ **Portfolio Guardian** — checks configured max-risk, daily-loss, open-position, and kill-switch rules.
- 🧮 **Risk planning** — calculates position size and risk/reward from explicit trade parameters.
- 👤 **Human-in-the-loop execution** — live execution remains blocked until explicit confirmation reaches the adapter.
- 📝 **Trade journal** — preserves the thesis and execution context.
- 🎓 **Post-trade coach** — compares the original thesis with the realized outcome and produces lessons.
- 🧪 **Paper trading** — safe in-memory simulation that never calls Binance write tools.
- 🔍 **Capability discovery** — reports available MCP capabilities instead of assuming permissions.
- 🔐 **Credential-safe design** — no Binance API keys, signed REST order implementation, seed phrases, or private keys are stored in this repository.

## 🧠 Cornell Trading Framework

Every market setup can be organized into:

| Section | Purpose |
|---|---|
| **Question** | What trading question are we trying to answer? |
| **Cues** | Trend, momentum, volume, support/resistance, liquidity, and other signals |
| **Notes** | Relevant market and permitted account context |
| **Analysis** | Bullish evidence vs. bearish evidence |
| **Risk** | Entry, stop/invalidation, position size, and risk/reward |
| **Decision** | `potential_setup`, `wait`, or `no_trade` |
| **Summary** | A concise, understandable thesis |

This makes the agent's reasoning easier to inspect and review.

## 🏗️ Architecture

```text
┌───────────────┐
│     User      │
└───────┬───────┘
        │ Market question
        ▼
┌───────────────────────┐
│    TradeTutor Agent   │
│                       │
│ Scanner / Analysis    │
│ Cornell / Risk        │
│ Explain / Propose     │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Portfolio Guardian  │
│  Risk / Loss / Limits │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Human Confirmation  │
└───────────┬───────────┘
            │
       ┌────┴────┐
       ▼         ▼
┌───────────┐ ┌────────────────┐
│   Paper   │ │ Authorized     │
│ Execution │ │ Binance MCP    │
└─────┬─────┘ └───────┬────────┘
      └───────┬───────┘
              ▼
       ┌──────────────┐
       │ Trade Journal│
       └──────┬───────┘
              ▼
       ┌──────────────┐
       │ Post-Trade   │
       │ Coach        │
       └──────────────┘
```

## 📁 Project Structure

```text
TradeTutor_MCP/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── demo.py
├── src/
│   ├── agent.py
│   ├── analytics.py
│   ├── alerts.py
│   ├── binance_mcp.py
│   ├── coach.py
│   ├── cornell.py
│   ├── explain.py
│   ├── journal.py
│   ├── journal_stats.py
│   ├── mcp_capabilities.py
│   ├── paper_trading.py
│   ├── portfolio_guardian.py
│   ├── risk.py
│   ├── runtime.py
│   └── scanner.py
└── tests/
    └── ...
```

## 🔌 Binance MCP Market Tools

The adapter can map permitted spot market context to Binance MCP capabilities such as:

| Purpose | MCP capability |
|---|---|
| Current price | `get_spot_symbol_price_ticker` |
| Best bid/ask | `get_spot_symbol_order_book_ticker` |
| Candles | `get_spot_kline_candlestick_data` |
| 24h statistics | `get_spot_24hr_ticker_price_change_statistics` |

Account and order capabilities are discovered at runtime. The project does **not** assume that a private or changing write-tool name exists.

## ⚙️ End-to-End Runtime

```python
runtime = TradeTutorRuntime(mcp)

# 1. Scan supplied market observations; no trading occurs.
ranked = runtime.scan(markets)

# 2. Build evidence-backed Cornell analysis.
analysis = runtime.analyze_market("BTCUSDT")

# 3. Portfolio Guardian protects proposal creation.
proposal = runtime.create_proposal(
    "BTCUSDT",
    risk_percent=1.0,
    side="long",
    entry_price=100000,
    stop_price=99000,
    target_price=102000,
    rationale="Illustrative setup rationale",
)

# 4A. Safe demo path: paper execution.
runtime.paper_execute(proposal)

# 4B. Live path: only after explicit confirmation.
result = runtime.execute_after_confirmation(proposal)

# 5. Post-trade review.
review = runtime.review_trade(
    thesis="Trend continuation",
    expected="bullish",
    outcome="bullish",
    r_multiple=1.8,
)
```

**Note:** the example prices are illustrative only and are not current quotes or trading recommendations.

## 🧪 Development

### Install

```bash
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
```

### Run tests

```bash
pytest
```

### Run the demo

```bash
python demo.py
```

## 🔐 Security Architecture

TradeTutor is intentionally designed to fail safely around trading execution:

1. Market data is evidence, not a guaranteed recommendation.
2. Scanner and alerts are read-only.
3. Portfolio Guardian is fail-closed for configured risk limits.
4. Paper trading is isolated from live execution.
5. Live execution requires explicit confirmation.
6. Authentication and secrets stay outside the repository.
7. No credentials are hard-coded.
8. If a compatible order-write capability is unavailable, the adapter stops rather than inventing an endpoint.
9. Post-trade reviews explain outcomes and lessons; they do not guarantee future performance.

## 🔗 Connect the Real Binance MCP Runtime

The Binance MCP host/client remains responsible for authentication and transport.

The intended integration flow is:

1. Connect an authorized Binance MCP environment.
2. Inject the permitted tool caller and capability lister into `BinanceMCPAdapter`.
3. Retrieve permitted market/account context.
4. Generate Cornell analysis and a risk-aware proposal.
5. Ask the user for explicit confirmation.
6. Execute only through the authorized MCP capability.
7. Record the execution result.
8. Run the post-trade coach.

**Never place Binance API secrets, passwords, seed phrases, or private keys in this repository.**

## 🏆 Hackathon Demo Story

TradeTutor's strongest demo path is a visible end-to-end loop:

**MCP market data → intelligent scanning → Cornell reasoning → explainable risk plan → portfolio protection → human confirmation → paper/live execution boundary → journal intelligence → post-trade coaching.**

The project is designed to show that an agent can be useful **without hiding its reasoning or removing the user from the final trading decision**.

## 🛣️ Roadmap

- [x] Cornell analysis architecture
- [x] Risk-management calculations
- [x] Market scanning and scoring
- [x] Alerts
- [x] Portfolio Guardian
- [x] Paper-trading path
- [x] MCP capability discovery boundary
- [x] Human-confirmation execution boundary
- [x] Trade journaling and statistics
- [x] Post-trade coaching
- [ ] Connect final live MCP tool caller in the target runtime
- [ ] Demo dashboard
- [ ] Submission video and screenshots

## ⚠️ Disclaimer

TradeTutor-MCP is an experimental software project for educational and hackathon purposes. Cryptocurrency markets are volatile and unpredictable. Analysis, risk calculations, and generated trade proposals can be wrong. Nothing in this repository is financial advice or a guarantee of trading performance. Users are responsible for reviewing and authorizing their own actions.

## 📜 License

MIT

## 🔗 Repository

urlTradeTutor_MCP on GitHubhttps://github.com/technea/TradeTutor_MCP
