"""
Content metrics pre-processor for the blog evaluator.

Computes objective, measurable attributes of a blog post *before* the
LLM sees it.  The LLM is notoriously bad at arithmetic (readability
scores, ratios, counts), so we offload those to deterministic functions
and inject the results into the prompt as ground-truth data.

Metrics computed:
- Flesch-Kincaid Grade Level & Reading Ease
- Passive voice ratio
- Jargon density
- Word / sentence / paragraph counts
- Code-to-text ratio
- Hook strength (first 100 words)
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

try:
    import textstat
except ImportError:
    textstat = None  # type: ignore[assignment]


# ---------- Helpers ----------

_CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```", re.M)
_INLINE_CODE_RE = re.compile(r"`[^`]+`")
_HEADING_RE = re.compile(r"^#{1,6}\s+", re.M)
_PASSIVE_VOICE_RE = re.compile(
    r"\b(am|is|are|was|were|be|being|been|get|gets|got|gotten)\s+"
    r"(\w+ed|said|done|made|taken|known|shown|seen|given|built|written|"
    r"found|kept|put|set|run|cut|bought|caught|taught|thought|sent|"
    r"brought|sold|led|held|meant|kept|paid|won|lost|hit|fed|"
    r"drawn|driven|grown|broken|frozen|chosen|hidden|ridden|"
    r"written|taken|given|seen|known|begun|fallen|risen)\b",
    re.IGNORECASE,
)

# A small heuristic set of domain-specific jargon terms common in
# technical/developer writing.  In production you might load this from
# a config file or compute it dynamically from the rubric corpus.
_TECH_JARGON = {
    "api", "async", "aws", "backend", "bottleneck", "cache", "ci/cd",
    "cli", "cloud", "containerization", "cors", "crud", "daemon", "db",
    "dependency", "deploy", "docker", "dto", "ec2", "endpoint", "eventual",
    "framework", "frontend", "gpu", "graphql", "http", "idempotent",
    "immutable", "infrastructure", "instance", "iot", "jwt", "kubernetes",
    "latency", "library", "load balancer", "middleware", "migration",
    "mikroservices", "monolith", "mvp", "namespace", "nosql", "observability",
    "orm", "pipeline", "polyfill", "polyrepo", "postgres", "promise",
    "prototype", "proxy", "pwa", "queue", "redis", "refactor", "rest",
    "s3", "saas", "scalability", "schema", "sdk", "serverless", "shard",
    "sla", "sql", "ssh", "stateful", "stateless", "subscription", "svm",
    "tailwind", "terraform", "throughput", "tls", "typescript", "ui",
    "uuid", "ux", "vpc", "webhook", "websocket", "webpack",
    "algorithm", "bandwidth", "checksum", "compiler", "concurrency",
    "ecosystem", "exception", "expression",
    "footgun", "interface",
    "iterative", "metadata", "nullable", "optimization",
    "overhead", "pagination", "polymorphism", "recursion", "refactoring",
    "regression", "repository", "resolution", "serialization",
    "singleton", "snippet", "syntax", "throttling", "tokenize",
    "transpiler", "typesafe",
}


# ---------- Public API ----------


class ContentMetrics:
    """Container for all pre-computed metrics about a piece of content."""

    __slots__ = (
        "word_count",
        "sentence_count",
        "paragraph_count",
        "avg_sentence_length",
        "long_sentence_count",
        "flesch_reading_ease",
        "flesch_kincaid_grade",
        "passive_voice_ratio",
        "jargon_density",
        "code_blocks",
        "code_to_text_ratio",
        "ttv_position",
        "has_tweetable_quote",
        "heading_count",
    )

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self) -> dict:
        return {s: getattr(self, s) for s in self.__slots__}

    def to_prompt_block(self) -> str:
        """Format metrics as a markdown block for injection into the LLM prompt."""
        lines = [
            "## Pre-computed content metrics",
            "",
            f"- **Word count:** {self.word_count}",
            f"- **Sentence count:** {self.sentence_count}",
            f"- **Paragraph count:** {self.paragraph_count}",
            f"- **Average sentence length:** {self.avg_sentence_length:.1f} words",
            f"- **Sentences > 35 words:** {self.long_sentence_count}",
            f"- **Flesch Reading Ease:** {self.flesch_reading_ease:.1f}",
            f"- **Flesch-Kincaid Grade Level:** {self.flesch_kincaid_grade:.1f}",
            f"- **Passive voice ratio:** {self.passive_voice_ratio:.1%}",
            f"- **Jargon density:** {self.jargon_density:.2f} terms/100 words",
            f"- **Code-to-text ratio:** {self.code_to_text_ratio:.1%}",
            f"- **Code blocks:** {self.code_blocks}",
            f"- **Headings:** {self.heading_count}",
        ]
        if self.ttv_position:
            lines.append(f"- **Time-to-value position:** ~word {self.ttv_position}")
        if self.has_tweetable_quote:
            lines.append("- **Tweetable quote found:** Yes")
        return "\n".join(lines)


def compute_metrics(content: str) -> ContentMetrics:
    """Compute all deterministic metrics for *content* (raw markdown)."""
    text_only = _strip_markdown_code(content)

    # --- Basic counts ---
    words = _tokenize(text_only)
    sentences = _split_sentences(text_only)
    paragraphs = _split_paragraphs(text_only)
    word_count = len(words)

    # --- Code analysis ---
    code_blocks, code_chars = _count_code_blocks(content)
    total_chars = len(content) or 1
    code_to_text_ratio = code_chars / total_chars

    # --- Readability (requires textstat, best-effort) ---
    flesch_re = 0.0
    fk_grade = 0.0
    if textstat is not None and word_count >= 3:
        try:
            flesch_re = textstat.flesch_reading_ease(text_only)
            fk_grade = textstat.flesch_kincaid_grade(text_only)
        except Exception:
            pass  # textstat can raise on edge-case content

    # --- Sentence stats ---
    sentence_count = len(sentences) or 1
    avg_sentence_length = word_count / sentence_count
    long_sentence_count = sum(1 for s in sentences if len(s.split()) > 35)

    # --- Passive voice ---
    passive_matches = _PASSIVE_VOICE_RE.findall(text_only)
    passive_voice_ratio = len(passive_matches) / sentence_count

    # --- Jargon density ---
    jargon_count = sum(1 for w in words if w.lower() in _TECH_JARGON)
    jargon_density = jargon_count / max(word_count, 1) * 100

    # --- Headings ---
    heading_count = len(_HEADING_RE.findall(content))

    # --- Engagement metrics ---
    ttv_position = _estimate_ttv(content)
    has_tweetable = _has_tweetable_quote(content)

    return ContentMetrics(
        word_count=word_count,
        sentence_count=sentence_count,
        paragraph_count=len(paragraphs),
        avg_sentence_length=round(avg_sentence_length, 1),
        long_sentence_count=long_sentence_count,
        flesch_reading_ease=round(flesch_re, 1),
        flesch_kincaid_grade=round(fk_grade, 1),
        passive_voice_ratio=round(passive_voice_ratio, 4),
        jargon_density=round(jargon_density, 2),
        code_blocks=code_blocks,
        code_to_text_ratio=round(code_to_text_ratio, 4),
        ttv_position=ttv_position,
        has_tweetable_quote=has_tweetable,
        heading_count=heading_count,
    )


# ---------- Internal helpers ----------


def _strip_markdown_code(text: str) -> str:
    """Remove fenced code blocks and inline code for text analysis."""
    text = _CODE_BLOCK_RE.sub(" ", text)
    text = _INLINE_CODE_RE.sub(" ", text)
    return text


def _tokenize(text: str) -> List[str]:
    return text.split()


def _split_sentences(text: str) -> List[str]:
    """A rough sentence splitter — good enough for metrics, not NLP-grade."""
    # Split on sentence-ending punctuation followed by space or end-of-string.
    parts = re.split(r"(?<=[.!?:;])\s+", text.strip())
    return [p for p in parts if len(p.strip()) > 1]


def _split_paragraphs(text: str) -> List[str]:
    parts = re.split(r"\n\s*\n+", text.strip())
    return [p for p in parts if p.strip()]


def _count_code_blocks(content: str) -> Tuple[int, int]:
    """Return (number_of_code_blocks, total_characters_in_code_blocks)."""
    blocks = _CODE_BLOCK_RE.findall(content)
    total_chars = sum(len(b) for b in blocks)
    return len(blocks), total_chars


def _estimate_ttv(content: str) -> Optional[int]:
    """Estimate Time-to-Value: word position of first actionable content.

    Looks for the first code block, bullet list, or actionable phrase
    within the first 500 words. Returns word index or None.
    """
    words = content.split()
    if not words:
        return None

    # Check first code block position
    code_match = _CODE_BLOCK_RE.search(content)
    if code_match:
        prefix_words = len(content[: code_match.start()].split())
        if prefix_words < 500:
            return prefix_words

    # Check for actionable markers
    actionable = re.compile(
        r"\b(install|run|create|set up|download|clone|configure|build|"
        r"deploy|implement|tutorial|step|guide|example)\b",
        re.IGNORECASE,
    )
    for i, w in enumerate(words[:100]):
        if actionable.search(w):
            return i

    return None


def _has_tweetable_quote(content: str) -> bool:
    """Check if any sentence is ≤120 chars and reads like a standalone takeaway."""
    sentences = _split_sentences(_strip_markdown_code(content))
    for s in sentences:
        clean = s.strip().strip('"').strip("'")
        if 40 < len(clean) <= 120 and "?" not in clean[:20]:
            return True
    return False
