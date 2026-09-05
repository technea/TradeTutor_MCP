"""Safe local check for an authorized Binance MCP client bridge.

This script does not authenticate, place orders, transfer funds, or print
secrets. The MCP host must provide the authorized call_tool/list_tools
functions when embedding this module.
"""

from src.mcp_runtime import AuthorizedBinanceRuntime


def run_check(call_tool, list_tools):
    runtime = AuthorizedBinanceRuntime(call_tool=call_tool, list_tools=list_tools)
    result = runtime.check_connection()
    print("Binance MCP runtime connected:", result["connected"])
    print("Discovered tools:", result["tool_count"])
    print("Market capabilities:", result["market_capabilities"])
    print("Account capabilities:", result["account_capabilities"])
    print("Trading capabilities:", result["trading_capabilities"])
    print("SAFE CHECK ONLY: no order or transfer was submitted.")
    return result


if __name__ == "__main__":
    raise SystemExit(
        "This checker must be embedded in an MCP host that supplies call_tool and list_tools. "
        "It intentionally does not accept Binance credentials or execute trades."
    )
