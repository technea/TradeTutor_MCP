# TradeTutor-MCP

> **Explainable, human-in-the-loop trading education and execution powered by Binance MCP.**

TradeTutor-MCP is a Binance Agent OS hackathon project that turns a market question into a structured workflow using **Cornell Notes**, risk planning, explicit user confirmation, Binance MCP execution, and post-trade journaling.

## 🎯 Vision

Instead of simply asking an agent to *"buy BTC"*, TradeTutor makes the reasoning visible:

```text
Market Research
      ↓
Cornell Notes Analysis
      ↓
Risk Assessment
      ↓
Trade Proposal
      ↓
User Confirmation
      ↓
Binance MCP Execution
      ↓
Trade Journal
      ↓
Post-Trade Review
```

The goal is to make agent-assisted trading **structured, explainable, and controlled by the user**.

## 🧠 Cornell Trading Framework

Every proposed setup is organized into six sections:

| Section | Purpose |
|---|---|
| **Question** | What trading decision are we evaluating? |
| **Cues** | Trend, momentum, volume, support/resistance, market conditions |
| **Notes** | Relevant market/account observations |
| **Analysis** | Bullish and bearish evidence |
| **Risk** | Entry, invalidation, position sizing, and risk/reward |
| **Decision** | Potential setup, wait, or no-trade conclusion |

A short **Summary** captures the final thesis.

## 🚀 MVP

### 1. Market Scanner
Collect relevant market information through the authorized Binance MCP environment.

### 2. Cornell Analysis Engine
Convert market observations into a consistent Cornell-style analysis.

### 3. Risk / Trade Plan
Calculate proposed entry, invalidation, position size, risk amount, and risk/reward where sufficient inputs are available.

### 4. Binance MCP Adapter
Keep Binance execution behind a clean adapter boundary. Credentials are never stored in the repository.

### 5. Human Confirmation
The agent explains the proposed action and waits for explicit user confirmation before an execution-capable workflow proceeds.

### 6. Trade Journal
Record the original thesis, decision, execution details, outcome, mistakes, and lessons.

## 📁 Project Structure

```text
TradeTutor_MCP/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── cornell.py
│   ├── risk.py
│   ├── journal.py
│   └── binance_mcp.py
├── notes/
│   └── trade_journal.md
└── tests/
    └── test_cornell.py
```

## 🔐 Security Principles

- Never commit Binance API keys, secrets, passwords, seed phrases, or private keys.
- Use the official Binance authorization / Agent OS / MCP connection for account access.
- Keep execution behind explicit authorization and user confirmation.
- Never present trading outcomes as guaranteed.
- This project is a hackathon prototype and **not financial advice**.

## 🛠️ Local Development

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it and install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

## 🔌 Binance MCP Integration

TradeTutor does not hard-code Binance credentials or implement a fake trading endpoint. The `binance_mcp.py` module provides the application boundary for the authorized Binance MCP environment.

The intended runtime is:

```text
User
  ↓
TradeTutor Agent
  ↓
Authorized Binance MCP
  ↓
Binance capabilities
  ↓
Analysis / Proposal / Confirmation
  ↓
Authorized execution
```

## 🧪 Example User Flow

**User:**

> Analyze BTC/USDT and tell me whether there is a reasonable setup.

**TradeTutor:**

1. Collects permitted market information.
2. Builds Cornell Notes.
3. Separates bullish and bearish evidence.
4. Defines invalidation and risk parameters.
5. Produces a trade proposal or recommends waiting.
6. Requests explicit confirmation before an execution-capable action.
7. Records the decision in the journal.

## 📊 Post-Trade Review

After a completed trade, TradeTutor can compare:

- Original thesis
- Planned setup
- Actual execution
- Market outcome
- What went well
- What went wrong
- Lessons for the next setup

This creates a feedback loop rather than treating each trade as an isolated action.

## 🏆 Hackathon Focus

The first implementation target is a **working MCP trading workflow**. Once the core workflow is stable, the project can be extended with richer Agent OS capabilities and a polished demonstration.

## ⚠️ Disclaimer

TradeTutor-MCP is an experimental hackathon project for educational and demonstration purposes. It does not provide financial advice, guarantee profits, or eliminate trading risk. Users remain responsible for their decisions and should independently evaluate any trade before authorizing execution.

## 📄 License

MIT
