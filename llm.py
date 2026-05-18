"""Groq LLM wrapper for the blog evaluator.

Returns a ``dict`` matching the ``EvaluationResult`` schema so the caller
in ``server.py`` can validate it with Pydantic and stay free of import
cycles. JSON-mode is requested via ``response_format`` so the model is
forced to emit a single JSON object.
"""

from __future__ import annotations

import json
import os
from typing import Optional


_DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Lazy singleton.
_client = None


def is_configured() -> bool:
    """Whether a Groq API key is present in the environment."""
    return bool(os.getenv("GROQ_API_KEY"))


def _get_client():
    global _client
    if _client is None:
        from groq import Groq  # imported lazily so missing dep doesn't crash startup
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


SYSTEM_PROMPT = """You are a senior editor evaluating a Markdown blog post.

You receive:
1. The author's evaluation configuration (audience, style, purpose, blog
   type, platform, feedback depth, optional custom focus).
2. Retrieved excerpts from internal rubrics — quality standards, audience
   personas, style guides, blog-type blueprints, platform rules, technical
   excellence standards. Treat these as ground truth.
3. The blog content itself.

Respond with a SINGLE JSON object (no prose, no markdown fences) matching
this schema EXACTLY:

{
  "overall_score": <int 0-100>,
  "summary": <str, 1-2 sentences>,
  "score_breakdown": [
    {"name": <str>, "score": <int 0-100>, "rationale": <str>}
  ],
  "strengths": [<str>],
  "improvement_priorities": [
    {"priority": "high"|"medium"|"low", "title": <str>, "description": <str>}
  ],
  "line_edits": [
    {"before": <str>, "after": <str>, "rationale": <str>}
  ],
  "comparative_analysis": [<str>],
  "word_count": <int>
}

Rules:
- Ground every judgment in the retrieved rubric excerpts; reference the
  specific rubric concept in rationales when relevant.
- For `line_edits.before`, quote text verbatim from the blog content.
- Item counts by feedback depth:
    Quick      -> 3-5 items per list
    Standard   -> 6-10 items per list
    Deep Audit -> 10+ items per list, multiple line edits
- `overall_score` is a weighted reflection of `score_breakdown`.
- Be specific and actionable; avoid generic praise.
"""


def evaluate(user_prompt: str, model: Optional[str] = None,
             temperature: float = 0.3) -> dict:
    """Send the assembled prompt to Groq and parse the JSON response.

    Raises:
        RuntimeError: if the API key is missing.
        json.JSONDecodeError: if the model returns invalid JSON.
        Exception: any error from the underlying Groq client.
    """
    if not is_configured():
        raise RuntimeError("GROQ_API_KEY is not set")

    client = _get_client()
    resp = client.chat.completions.create(
        model=model or _DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=temperature,
    )
    raw = resp.choices[0].message.content or "{}"
    return json.loads(raw)
