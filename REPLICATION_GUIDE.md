# TradeTutor Replication Guide

## Overview

TradeTutor is an explainable, human-in-the-loop crypto trading workflow. It retrieves live Binance market data, supports BNB Chain token research and security checks, creates structured risk plans, and provides Cornell-style explanations. Paper trading is available for safe testing.

## Requirements

- Node.js 22 or later
- Python 3.12 or later
- Internet access to Binance public APIs
- A terminal such as PowerShell

## Installation

1. Clone or download the TradeTutor project.
2. Open a terminal in the project directory:

   ```powershell
   cd "E:\trade tutor"
   ```

3. Install the Python dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Start the Agent

Start the local dashboard server:

```powershell
node dashboard_server.mjs
```

Open the dashboard in a browser:

```text
http://127.0.0.1:8787/
```

## Demo Questions

1. What are the top trending tokens on BNB Chain?
2. Which BNB Chain tokens have the highest smart-money inflows?
3. Search BNB Chain for CAKE.
4. Show the current price, liquidity, volume, and holders for CAKE.
5. Is this BNB Chain token safe? `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`
6. Create a risk plan for BNB.

## Security Audit Demo

Use a verified BNB Chain contract address and ask the agent to audit it before trading:

```text
Audit this BNB Chain contract for scam or honeypot risks:
0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c
```

The agent reports contract and trading risks. An unavailable audit must not be treated as proof that a token is safe.

## How the Workflow Operates

1. The user asks a market or token question.
2. The agent retrieves fresh public Binance data.
3. The agent presents the relevant evidence and metrics.
4. Cornell analysis separates the question, cues, notes, risk, and decision.
5. Portfolio and risk checks are applied before a trade recommendation.
6. Paper trading can be used for safe experimentation.
7. Live execution remains blocked until the user explicitly confirms it.

## Testing

Run the automated tests from the project directory:

```powershell
$env:PYTHONPATH = "."
pytest -q
```

## Important Note

The dashboard requires live network access to Binance. If Binance is unavailable, TradeTutor intentionally does not use stale or cached market data and recommends waiting for live data to return.
