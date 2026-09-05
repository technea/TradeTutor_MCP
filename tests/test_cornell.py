import pytest

from src.cornell import build_cornell_analysis


def test_cornell_analysis_and_markdown():
    analysis = build_cornell_analysis(
        question="Should BTCUSDT be considered for a trade?",
        cues=["Higher-timeframe trend is bullish"],
        notes=["Price is above the observed support"],
        analysis=["Bullish evidence outweighs bearish evidence"],
        risk=["Invalidation below support"],
        decision="potential_setup",
        summary="Potential setup, subject to confirmation and risk limits.",
    )

    markdown = analysis.to_markdown()
    assert "## Question" in markdown
    assert "## Cues" in markdown
    assert "potential_setup" in markdown
    assert "Potential setup" in markdown


def test_question_is_required():
    with pytest.raises(ValueError):
        build_cornell_analysis(question="", summary="No trade")


def test_invalid_decision_is_rejected():
    with pytest.raises(ValueError):
        build_cornell_analysis(question="Test", decision="buy", summary="Test")
