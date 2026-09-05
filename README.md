# TradeTutor-MCP

> **Explainable, human-in-the-loop trading education and execution powered by Binance MCP.**

TradeTutor-MCP turns a market question into a controlled workflow:

```text
Binance MCP market context
        ↓
Cornell Notes analysis
        ↓
Risk / trade plan
        ↓
Trade proposal
        ↓
Explicit user confirmation
        ↓
Authorized Binance MCP execution
        ↓
Trade journal / review
```

## Current implementation

- `src/runtime.py` orchestrates market context, Cornell analysis, account-aware proposal creation, and confirmed execution.
- `src/binance_mcp.py` is a clean MCP adapter. It accepts an injected MCP `call_tool(tool_name, arguments)` function and configurable tool names.
- `demo.py` remains a safe local demo and cannot place a real order.
- No Binance API keys, signed REST order implementation, or credentials are stored in this repository.
- Execution is blocked unless `confirmed=True` reaches the adapter.

## Connect the real Binance MCP runtime

The connected Binance Agent OS/MCP client should inject its tool caller into `BinanceMCPAdapter`:

```python
from src.binance_mcp import BinanceMCPAdapter
from src.runtime import TradeTutorRuntime


def call_tool(tool_name, arguments):
    # Delegate to the already-authorized Binance MCP client.
    return your_mcp_client.call_tool(tool_name, arguments)

mcp = BinanceMCPAdapter(
    call_tool,
    market_tool="<actual-market-tool-name>",
    account_tool="<actual-account-tool-name>",
    order_tool="<actual-order-tool-name>",
)

runtime = TradeTutorRuntime(mcp)
```

The exact tool names are intentionally not guessed: they must match the tools exposed by the connected Binance MCP server. They can also be supplied through `BINANCE_MCP_MARKET_TOOL`, `BINANCE_MCP_ACCOUNT_TOOL`, and `BINANCE_MCP_ORDER_TOOL`.

### Required execution sequence

1. Request market context through the authorized MCP tool.
2. Build Cornell analysis.
3. Fetch account context when sizing a proposal.
4. Present the trade proposal to the user.
5. Obtain explicit confirmation.
6. Only then call `execute_after_confirmation()`.
7. Record the result in the journal.

## Development

```bash
python -m venv .venv
pip install -r requirements.txt
pytest
python demo.py
```

## Security

- Never commit Binance API keys, secrets, passwords, seed phrases, or private keys.
- Authentication and signing belong to the authorized Binance Agent OS/MCP environment.
- Never bypass the confirmation gate.
- Never present trading outcomes as guaranteed.
- This is a hackathon prototype, not financial advice.

## Hackathon focus

The MVP demonstrates a transparent, human-in-the-loop trading workflow rather than a black-box "buy/sell" command. The next integration step is to inject the real Binance MCP client and map its currently exposed market, account, and order tool names into the adapter.

## License

MIT
