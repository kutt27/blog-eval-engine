"""Tests for the RAG retrieval module."""

from pathlib import Path
import sys
import tempfile

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from rag import _extract_h1, _chunk_file, build_query


def test_extract_h1_found():
    text = "# My Document Title\n\nSome content here."
    assert _extract_h1(text) == "My Document Title"


def test_extract_h1_missing():
    text = "No heading here.\n\nJust plain text."
    assert _extract_h1(text) == "(no title)"


def test_extract_h1_multiple():
    text = "# First Title\n\nContent\n\n# Second Title\n\nMore content"
    assert _extract_h1(text) == "First Title"


def test_build_query_full():
    q = build_query(
        audience=["Beginner", "Senior"],
        style=["Technical"],
        purpose="Educate",
        blog_type="How-to",
        platform="Dev.to",
        custom="Focus on code examples",
    )
    assert "Audience: Beginner, Senior" in q
    assert "Style: Technical" in q
    assert "Purpose: Educate" in q
    assert "Blog type: How-to" in q
    assert "Platform: Dev.to" in q
    assert "Focus: Focus on code examples" in q
    assert "|" in q


def test_build_query_empty():
    q = build_query([], [], "", "", "", "")
    assert q == "blog quality evaluation rubrics"


def test_build_query_partial():
    q = build_query(
        audience=["Mid-level"],
        style=[],
        purpose="",
        blog_type="Comparison",
        platform="",
        custom="",
    )
    assert "Audience: Mid-level" in q
    assert "Blog type: Comparison" in q
    assert "|" in q


def test_chunk_file_basic():
    """Verify _chunk_file creates chunks with source metadata."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("# Test Rubric\n\n## Section One\n\nContent for section one.\n\n")
        f.write("## Section Two\n\nContent for section two.\n")
        fname = f.name

    try:
        chunks = _chunk_file(Path(fname))
        assert len(chunks) >= 2, f"Expected at least 2 chunks, got {len(chunks)}"
        for c in chunks:
            assert "source" in c, "Chunk missing 'source' key"
            assert "text" in c, "Chunk missing 'text' key"
            assert Path(fname).name in c["source"], f"Expected filename in source, got: {c['source']}"
    finally:
        Path(fname).unlink(missing_ok=True)


def test_chunk_file_hierarchy():
    """Verify chunk sources include H1 hierarchy."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("# My Rubric\n\nIntroductory text.\n\n## Section\n\nContent.\n")
        fname = f.name

    try:
        chunks = _chunk_file(Path(fname))
        sources = [c["source"] for c in chunks]
        # At least one chunk should reference the H1 title
        assert any("My Rubric" in s for s in sources), f"H1 not in sources: {sources}"
    finally:
        Path(fname).unlink(missing_ok=True)
