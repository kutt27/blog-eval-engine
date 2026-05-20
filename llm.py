"""Groq LLM wrapper for the blog evaluator.

Returns a ``dict`` matching the ``EvaluationResult`` schema so the caller
in ``server.py`` can validate it with Pydantic and stay free of import
cycles. JSON-mode is requested via ``response_format`` so the model is
forced to emit a single JSON object.

Implements a fallback chain: if the primary model fails, tries the
fallback before raising an error. The model selection also adapts to
the requested feedback depth.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Tuple


_DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
_FALLBACK_MODEL = os.getenv("GROQ_FALLBACK_MODEL", "llama-3.1-8b-instant")

# Model selection by depth: cheaper model for quick evaluations.
# Fallback model defaults to ``_FALLBACK_MODEL``. If primary == fallback
# (e.g. Quick depth with default env), the chain runs a single attempt.
_DEPTH_MODELS: Dict[str, Tuple[str, str]] = {
    "Quick": ("llama-3.1-8b-instant", _FALLBACK_MODEL),
    "Standard": (_DEFAULT_MODEL, _FALLBACK_MODEL),
    "Deep Audit": (_DEFAULT_MODEL, _FALLBACK_MODEL),
}

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

You will receive:
1. The author's evaluation configuration (audience, style, purpose, blog
   type, platform, feedback depth, optional custom focus).
2. PRE-COMPUTED content metrics (these are ground-truth numbers — do NOT
   recompute them yourself).
3. Retrieved excerpts from internal rubrics — quality standards, audience
   personas, style guides, blog-type blueprints, platform rules, technical
   excellence standards, SEO rubrics. Treat these as ground truth.
4. The blog content itself.

---

## Required Reasoning Process

Before producing the final JSON, reason through these THREE phases
INTERNALLY (model will see only one response, but structure your
thinking in this order):

### Phase 1: ANALYZE
- Identify the dominant blog type (Tutorial, Comparison, Opinion, Review,
  News, or hybrid). Does it match the user's selection? Note mismatches.
- Identify the target audience signal (Developer, Manager, or Beginner)
  from the text itself. Does it match the user's selection?
- Identify the primary structure (Inverted Pyramid, Storytelling,
  Problem-Solution, Listicle, or hybrid).
- Check Tone Consistency across Intro → Body → Conclusion.

### Phase 2: SCORE
For each dimension in the score_breakdown, evaluate against the
retrieved rubrics. Reference specific rubric concepts in your
rationale. Use the pre-computed metrics (Flesch-Kincaid, passive
voice ratio, jargon density, code-to-text-ratio) as ground truth —
do not second-guess them.

### Phase 3: GENERATE
Based on your Phase 1 analysis and Phase 2 scores:
- Derive strengths from what the content does well.
- Derive improvement priorities from rubric violations and missing elements.
- Write specific line edits (quote verbatim from content in `before`).
- Write comparative analysis (use the pre-computed metrics for
  objective comparisons against platform norms).

---

## Output Schema

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

## Critical Rules

- Ground every judgment in the retrieved rubric excerpts; reference the
  specific rubric concept in rationales when relevant.
- For `line_edits.before`, quote text verbatim from the blog content.
- Item counts MUST follow the "Item count directive" in the config:
    Quick      -> exactly 3-5 items per list, 1-2 line_edits
    Standard   -> 6-10 items per list, 3-5 line_edits
    Deep Audit -> 10-15 items per list, 5+ line_edits, exhaustive
- `overall_score` is a weighted reflection of `score_breakdown`.
- Be specific and actionable; avoid generic praise like "good job" or
  "needs improvement." Instead say *what* specifically is good or bad
  and *why* it matters for the given audience/platform.
- Pay attention to the "Item count directive" and the pre-computed
  metrics — they are ground truth.
"""


def _call_llm(user_prompt: str, model: str, temperature: float) -> dict:
    """Make a single LLM call and return parsed JSON."""
    client = _get_client()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=temperature,
    )
    raw = resp.choices[0].message.content or "{}"
    return json.loads(raw)


def evaluate(user_prompt: str, model: Optional[str] = None,
             temperature: float = 0.3, depth: str = "Standard") -> dict:
    """Send the assembled prompt to Groq and parse the JSON response.

    Implements:
    - Fallback chain: primary → fallback → error.
    - Consistency check for Deep Audit: makes a second call at a different
      temperature and compares overall_score. If variance > 10 points,
      the result includes a ``confidence_warning`` key.

    Args:
        user_prompt: The assembled evaluation prompt.
        model: Override model name. If None, selected by depth.
        temperature: Sampling temperature (0.0-1.0).
        depth: Feedback depth for model selection (Quick → 8B, else 70B).

    Returns:
        Parsed JSON dict matching the EvaluationResult schema, with an
        optional ``confidence_warning`` key for low-consistency results.

    Raises:
        RuntimeError: if the API key is missing.
        Exception: if all models in the chain fail.
    """
    if not is_configured():
        raise RuntimeError("GROQ_API_KEY is not set")

    models_to_try: List[str]
    if model:
        models_to_try = [model]
    else:
        primary, fallback = _DEPTH_MODELS.get(depth, (_DEFAULT_MODEL, _FALLBACK_MODEL))
        models_to_try = [primary, fallback] if primary != fallback else [primary]

    # --- Primary call with fallback chain ---
    last_error: Optional[Exception] = None
    result: Optional[dict] = None
    for attempt_idx, attempt_model in enumerate(models_to_try):
        try:
            temp = temperature if attempt_idx == 0 else min(temperature + 0.1, 0.5)
            result = _call_llm(user_prompt, attempt_model, temp)
            break
        except Exception as exc:
            last_error = exc
            continue

    if result is None:
        raise RuntimeError(f"All models failed. Last error: {last_error}")

    # --- Consistency check (only for Deep Audit or Standard) ---
    if depth in ("Deep Audit", "Standard"):
        try:
            consistency_temp = 0.5 if depth == "Deep Audit" else 0.4
            result2 = _call_llm(
                user_prompt,
                models_to_try[0],
                consistency_temp,
            )
            score1 = result.get("overall_score", 0)
            score2 = result2.get("overall_score", 0)
            variance = abs(score1 - score2)
            if variance > 10:
                result["confidence_warning"] = (
                    f"Low confidence: two evaluations differed by {variance} points "
                    f"({score1} vs {score2}). Consider re-running."
                )
            elif variance > 5:
                # Minor variance — average the scores for stability
                result["overall_score"] = round((score1 + score2) / 2)
        except Exception:
            pass  # Consistency check is best-effort; don't fail the whole request

    return result
