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
- `src/binance_mcp.py` maps live spot market context to the published Binance market-data tool names and discovers account/order tools from the connected MCP server.
- `tests/test_binance_mcp.py` verifies market-tool mapping and the confirmation gate.
- `demo.py` remains a safe local demo and cannot place a real order.
- No Binance API keys, signed REST order implementation, or credentials are stored in this repository.
- Execution is blocked unless `confirmed=True` reaches the adapter.

## Binance MCP market tools

The adapter uses these Binance MCP tool names for spot market evidence:

| Purpose | MCP tool |
|---|---|
| Current price | `get_spot_symbol_price_ticker` |
| Best bid/ask | `get_spot_symbol_order_book_ticker` |
| Candles | `get_spot_kline_candlestick_data` |
| 24h statistics | `get_spot_24hr_ticker_price_change_statistics` |

These provide the raw observations used by the Cornell workflow. The application does not claim that raw market data is itself a trading recommendation.

## Connect the real Binance MCP runtime

The Binance MCP host/client remains responsible for authentication and transport. Inject two functions into `BinanceMCPAdapter`:

```python
from src.binance_mcp import BinanceMCPAdapter
from src.runtime import TradeTutorRuntime


def call_tool(tool_name, arguments):
    # Delegate to your already-authorized Binance MCP client.
    return your_mcp_client.call_tool(tool_name, arguments)


def list_tools():
    # Return MCP tool definitions with at least `name`, `description`, and
    # `inputSchema` where available.
    return your_mcp_client.list_tools()

mcp = BinanceMCPAdapter(call_tool=call_tool, list_tools=list_tools)
runtime = TradeTutorRuntime(mcp)
```

The adapter calls the four market tools above directly. Account and order tools are **discovered at runtime** from the connected Binance MCP server rather than guessed or hard-coded, because MCP tool names can differ between server/runtime versions.

## Required Track B execution sequence

1. Call `runtime.analyze_market("BTCUSDT")` to retrieve live market evidence through Binance MCP.
2. Build the Cornell analysis from that evidence.
3. Call `runtime.create_proposal(...)` after the user has supplied/approved the intended risk parameters.
4. Display the resulting symbol, side, quantity, entry, stop, target, risk/reward, and rationale.
5. Ask for an explicit confirmation from the user.
6. Only after confirmation call `runtime.execute_after_confirmation(proposal)`.
7. Record the authorized execution response in the trade journal.

The adapter's order discovery requires an MCP tool definition whose name/description identifies an order/trade operation and whose input schema exposes symbol, side, and quantity. If the connected MCP server does not expose a compatible write tool, TradeTutor stops instead of guessing an order endpoint.

## Example integration shape

```python
analysis = runtime.analyze_market("BTCUSDT")
print(analysis.cornell_markdown)

proposal = runtime.create_proposal(
    "BTCUSDT",
    risk_percent=1.0,
    side="long",
    entry_price=100000,
    stop_price=99000,
    target_price=102000,
    rationale="User-approved setup rationale",
)

# Present proposal to user here. Do not auto-confirm.
result = runtime.execute_after_confirmation(proposal)
print(result)
```

**Important:** the example prices above are illustrative only. They are not a current BTC quote or a recommendation.

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

The project is designed around a visible Track B workflow: **MCP market data → structured reasoning → risk-controlled proposal → human confirmation → authorized MCP execution → journal**.

## License

MIT
