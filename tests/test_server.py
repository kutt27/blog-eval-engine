"""Tests for the server module — prompt building, depth mapping."""

from pathlib import Path
import sys

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from server import _depth_to_k, _depth_to_items


def test_depth_to_k():
    assert _depth_to_k("Quick") == 3
    assert _depth_to_k("Standard") == 6
    assert _depth_to_k("Deep Audit") == 10


def test_depth_to_k_default():
    assert _depth_to_k("Unknown") == 6


def test_depth_to_items_quick():
    items = _depth_to_items("Quick")
    assert "3-5" in items
    assert "1-2" in items


def test_depth_to_items_standard():
    items = _depth_to_items("Standard")
    assert "6-10" in items


def test_depth_to_items_deep():
    items = _depth_to_items("Deep Audit")
    assert "10-15" in items
    assert "5+ line_edits" in items or "exhaustive" in items.lower()
