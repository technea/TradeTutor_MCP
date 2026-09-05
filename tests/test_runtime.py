from src.binance_mcp import BinanceMCPAdapter
from src.runtime import TradeTutorRuntime


def test_runtime_builds_confirmation_ready_proposal() -> None:
    calls = []

    def call_tool(name, arguments):
        calls.append((name, arguments))
        if name == "market":
            return {"price": 100, "trend": "bullish", "volume": "rising"}
        if name == "account":
            return {"balance": 1000}
        raise AssertionError(f"unexpected tool: {name}")

    adapter = BinanceMCPAdapter(
        call_tool,
        market_tool="market",
        account_tool="account",
        order_tool="order",
    )
    runtime = TradeTutorRuntime(adapter)

    analysis = runtime.analyze_market("BTCUSDT", summary="Wait for confirmation.")
    assert analysis.symbol == "BTCUSDT"
    assert "## Question" in analysis.cornell_markdown
    assert "## Risk" in analysis.cornell_markdown

    proposal = runtime.create_proposal(
        "BTCUSDT",
        risk_percent=1,
        side="long",
        entry_price=100,
        stop_price=95,
        target_price=110,
        rationale="Demo thesis only.",
    )
    assert proposal.symbol == "BTCUSDT"
    assert proposal.quantity == 2.0
    assert calls[0][0] == "market"
    assert calls[1][0] == "account"


def test_runtime_execution_requires_confirmed_proposal() -> None:
    calls = []

    def call_tool(name, arguments):
        calls.append((name, arguments))
        return {"order_id": "demo-123"}

    adapter = BinanceMCPAdapter(call_tool, order_tool="order")
    runtime = TradeTutorRuntime(adapter)
    proposal = runtime.agent.prepare_proposal(
        "BTCUSDT",
        runtime.agent.create_trade_plan(1000, 1, "long", 100, 95, 110),
        "Demo thesis.",
    )

    result = runtime.execute_after_confirmation(proposal)
    assert result["order_id"] == "demo-123"
    assert calls[0][0] == "order"
