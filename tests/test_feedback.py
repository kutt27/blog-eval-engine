"""Tests for the feedback loop module."""

from pathlib import Path
import sys

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from feedback import (
    store_evaluation,
    store_feedback,
    get_recent_evaluations,
    get_feedback_summary,
)


def test_store_and_retrieve_evaluation():
    eval_id = store_evaluation(
        config={"audience": ["Beginner"]},
        snippets=[{"source": "test.md", "text": "test"}],
        result={"overall_score": 85, "mode": "live"},
        latency_ms=1200,
        confidence="ok",
    )
    assert eval_id > 0, f"Expected positive ID, got {eval_id}"

    recent = get_recent_evaluations(limit=5)
    assert len(recent) >= 1
    assert any(r["id"] == eval_id for r in recent)


def test_store_feedback():
    eval_id = store_evaluation(
        config={"depth": "Quick"},
        snippets=None,
        result={"overall_score": 70, "mode": "mock"},
    )

    fb_id = store_feedback(
        evaluation_id=eval_id,
        feedback_type="correction",
        payload={"field": "overall_score", "expected": 80, "actual": 70},
        notes="Score was too low for this content",
    )
    assert fb_id > 0


def test_feedback_summary_no_data():
    # Should return gracefully with no data
    summary = get_feedback_summary()
    assert isinstance(summary, str)


def test_feedback_summary_with_corrections():
    eval_id = store_evaluation(
        config={"audience": ["Senior"]},
        snippets=None,
        result={"overall_score": 65, "mode": "live"},
    )

    store_feedback(
        evaluation_id=eval_id,
        feedback_type="correction",
        payload={"field": "overall_score", "expected": 75, "actual": 65},
        notes="Underestimated technical depth",
    )

    summary = get_feedback_summary()
    assert "corrections" in summary.lower() or "overall_score" in summary
