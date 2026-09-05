import pytest

from src.binance_mcp import BinanceMCPAdapter, TradeProposal


def test_adapter_delegates_to_configured_tools() -> None:
    calls = []

    def call_tool(name, arguments):
        calls.append((name, dict(arguments)))
        if name == "market":
            return {"symbol": arguments["symbol"], "price": 100}
        if name == "account":
            return {"balance": 1000}
        return {"order_id": "demo-1"}

    adapter = BinanceMCPAdapter(
        call_tool,
        market_tool="market",
        account_tool="account",
        order_tool="order",
    )

    assert adapter.get_market_context("BTCUSDT")["price"] == 100
    assert adapter.get_account_context()["balance"] == 1000

    proposal = TradeProposal("BTCUSDT", "BUY", 0.01, 100, 95, 110, "test")
    result = adapter.execute_confirmed_order(proposal, confirmed=True)

    assert result["order_id"] == "demo-1"
    assert calls[-1][0] == "order"
    assert calls[-1][1]["symbol"] == "BTCUSDT"


def test_execution_requires_confirmation() -> None:
    adapter = BinanceMCPAdapter(lambda *_: {"ok": True}, order_tool="order")
    proposal = TradeProposal("BTCUSDT", "BUY", 0.01, 100, 95, 110, "test")

    with pytest.raises(PermissionError):
        adapter.execute_confirmed_order(proposal, confirmed=False)
