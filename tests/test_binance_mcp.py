import pytest

from src.binance_mcp import BinanceMCPAdapter, TradeProposal


def test_market_context_calls_live_binance_tools():
    calls = []

    def call_tool(name, arguments):
        calls.append((name, arguments))
        return {"tool": name, "arguments": arguments}

    adapter = BinanceMCPAdapter(call_tool=call_tool)
    context = adapter.get_market_context("BTCUSDT")

    assert context["symbol"] == "BTCUSDT"
    assert [name for name, _ in calls] == [
        "get_spot_symbol_price_ticker",
        "get_spot_symbol_order_book_ticker",
        "get_spot_kline_candlestick_data",
        "get_spot_24hr_ticker_price_change_statistics",
    ]


def test_order_requires_explicit_confirmation():
    adapter = BinanceMCPAdapter(call_tool=lambda *_: {})
    proposal = TradeProposal("BTCUSDT", "BUY", 0.001, 100000, 99000, 102000, "test")

    with pytest.raises(PermissionError):
        adapter.execute_confirmed_order(proposal, confirmed=False)


def test_order_tool_is_discovered_and_called_after_confirmation():
    calls = []
    tools = [
        {
            "name": "get_account_balance",
            "description": "Get account balances",
            "inputSchema": {"properties": {}},
        },
        {
            "name": "place_spot_order",
            "description": "Place a spot trading order",
            "inputSchema": {
                "properties": {
                    "symbol": {},
                    "side": {},
                    "quantity": {},
                    "type": {},
                }
            },
        },
    ]

    def call_tool(name, arguments):
        calls.append((name, arguments))
        return {"status": "ok"}

    adapter = BinanceMCPAdapter(call_tool=call_tool, list_tools=lambda: tools)
    proposal = TradeProposal("BTCUSDT", "buy", 0.001, 100000, 99000, 102000, "confirmed demo")

    result = adapter.execute_confirmed_order(proposal, confirmed=True)

    assert result == {"status": "ok"}
    assert calls == [("place_spot_order", {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "quantity": 0.001,
        "type": "MARKET",
    })]
