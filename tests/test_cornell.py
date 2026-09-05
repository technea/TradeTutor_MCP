from src.cornell import CornellAnalysis, build_cornell_analysis


def test_cornell_analysis() -> None:
    result = build_cornell_analysis(
        "Should BTCUSDT be considered for a trade?",
        {"trend": "bullish", "volume": "rising", "price": 100000},
        analysis_points=["Bullish structure is present."],
        risk_points=["Invalidate below support."],
        decision="potential_setup",
        summary="Setup may be valid if invalidation holds.",
    )
    assert isinstance(result, CornellAnalysis)
    assert result.decision == "potential_setup"
    markdown = result.to_markdown()
    for section in ("Question", "Cues", "Notes", "Analysis", "Risk", "Decision", "Summary"):
        assert f"## {section}" in markdown


def test_invalid_decision() -> None:
    try:
        build_cornell_analysis("Question", {}, decision="buy", summary="Test")
    except ValueError as exc:
        assert "decision" in str(exc)
    else:
        raise AssertionError("Expected invalid decision to raise")
