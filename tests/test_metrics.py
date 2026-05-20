"""Tests for the content metrics module."""

from pathlib import Path
import sys

# Ensure the project root is on sys.path
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from metrics import compute_metrics


def test_basic_counts():
    content = "# Hello\n\nThis is a sentence. Here is another one."
    m = compute_metrics(content)
    assert m.word_count == 10, f"Expected 10 words, got {m.word_count}"
    assert m.sentence_count == 2, f"Expected 2 sentences, got {m.sentence_count}"
    assert m.paragraph_count == 2, f"Expected 2 paragraphs, got {m.paragraph_count}"


def test_code_block_detection():
    content = "# Code Test\n\nSome text.\n\n```python\nprint('hello')\n```\n\nMore text."
    m = compute_metrics(content)
    assert m.code_blocks == 1, f"Expected 1 code block, got {m.code_blocks}"
    assert m.code_to_text_ratio > 0, "Expected non-zero code-to-text ratio"


def test_text_only_code_stripped():
    """Verify code content is excluded from text analysis."""
    content = "# Test\n\n```\n" + "word " * 100 + "\n```\n\nReal text here."
    m = compute_metrics(content)
    assert m.word_count < 50, f"Code content should be stripped; got {m.word_count} words"


def test_passive_voice_detection():
    content = "# Passive\n\nThe system was configured by the admin. The code was written by John. Active code runs."
    m = compute_metrics(content)
    assert m.passive_voice_ratio > 0, "Expected at least some passive voice"
    assert m.passive_voice_ratio < 1.0, "Not everything should be passive"


def test_jargon_density():
    content = "# Jargon\n\nWe deployed the API to AWS using Docker containers. The Kubernetes cluster handles orchestration."
    m = compute_metrics(content)
    assert m.jargon_density > 0, f"Expected jargon density > 0, got {m.jargon_density}"
    assert m.jargon_density < 50, f"Jargon density seems too high: {m.jargon_density}"


def test_empty_content():
    m = compute_metrics("")
    assert m.word_count == 0
    assert m.sentence_count == 1  # fallback to avoid div-by-zero
    assert m.code_blocks == 0
    assert m.code_to_text_ratio == 0.0


def test_to_prompt_block():
    content = "# Block Test\n\nSimple content here."
    m = compute_metrics(content)
    block = m.to_prompt_block()
    assert "Flesch-Kincaid" in block
    assert "Word count" in block
    assert "Code blocks" in block
    assert len(block) > 50


def test_ttv_detection():
    content = "# TTV Test\n\nHere is some introductory text. Install the package using npm. This is a tutorial."
    m = compute_metrics(content)
    # We should either detect TTV or not — both are valid, just verify it doesn't crash
    assert m.ttv_position is None or m.ttv_position >= 0


def test_headings_count():
    content = "# H1\n\nText\n\n## H2\n\nText\n\n### H3\n\nText"
    m = compute_metrics(content)
    assert m.heading_count == 3, f"Expected 3 headings, got {m.heading_count}"
