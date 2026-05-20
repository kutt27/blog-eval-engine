"""Blog Evaluator API server.

Exposes a single POST /evaluate endpoint that accepts the frontend's
evaluation config as JSON plus an optional `prompt_injection` string for
augmenting the LLM prompt during evaluation.

Retrieval runs against the local rubric corpus via ``rag.py``; the LLM
call is delegated to ``llm.py`` (Groq). If either dependency is missing or
``GROQ_API_KEY`` is unset the route returns a hardcoded mock so the
frontend remains functional.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import List, Literal, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ValidationError

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

log = logging.getLogger("blog-evaluator")


# ---------- Request / response models ----------

class EvaluationRequest(BaseModel):
    """Payload sent by the frontend when the user clicks Run Evaluation."""

    content: str = Field(..., min_length=1, description="Markdown blog content to evaluate.")
    audience: List[str] = Field(default_factory=list)
    style: List[str] = Field(default_factory=list)
    purpose: str = ""
    blog_type: str = ""
    platform: str = ""
    depth: Literal["Quick", "Standard", "Deep Audit"] = "Standard"
    custom: str = ""

    # Hook for callers (and future admin/test surfaces) to inject extra
    # instructions or override fragments into the LLM prompt.
    prompt_injection: Optional[str] = None


# Structured evaluation result. This is the contract the LLM must satisfy
# once it replaces the mock implementation in /evaluate.

class ScoreDimension(BaseModel):
    name: str
    score: int = Field(..., ge=0, le=100)
    rationale: str


class ImprovementItem(BaseModel):
    priority: Literal["high", "medium", "low"]
    title: str
    description: str


class LineEdit(BaseModel):
    before: str
    after: str
    rationale: str


class EvaluationResult(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    summary: str
    score_breakdown: List[ScoreDimension] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    improvement_priorities: List[ImprovementItem] = Field(default_factory=list)
    line_edits: List[LineEdit] = Field(default_factory=list)
    comparative_analysis: List[str] = Field(default_factory=list)
    word_count: int = 0
    # Indicates whether the response came from the live LLM or the mock.
    mode: Literal["live", "mock"] = "live"
    # Populated by the consistency check when score variance exceeds threshold.
    confidence_warning: str | None = None


# ---------- App setup ----------

app = FastAPI(title="Blog Evaluator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Prompt assembly (stub) ----------

def _depth_to_k(depth: str) -> int:
    """Map evaluation depth to number of RAG snippets to retrieve."""
    mapping = {"Quick": 3, "Standard": 6, "Deep Audit": 10}
    return mapping.get(depth, 6)


def _retrieve_context(req: EvaluationRequest) -> List[dict]:
    """Pull top-k rubric snippets via the local RAG store. Empty on failure.

    The number of snippets is determined by the ``depth`` field:
    - Quick → 3
    - Standard → 6
    - Deep Audit → 10
    """
    try:
        import rag
        k = _depth_to_k(req.depth)
        query = rag.build_query(
            audience=req.audience,
            style=req.style,
            purpose=req.purpose,
            blog_type=req.blog_type,
            platform=req.platform,
            custom=req.custom,
        )
        return rag.retrieve(query, k=k)
    except Exception as exc:  # missing deps, model download failure, etc.
        log.warning("RAG retrieval unavailable: %s", exc)
        return []


def _depth_to_items(depth: str) -> str:
    """Return a human-readable item count directive for the LLM prompt."""
    mapping = {
        "Quick": "Generate exactly 3-5 items in every list. Limit line_edits to 1-2.",
        "Standard": "Generate 6-10 items in every list. 3-5 line_edits expected.",
        "Deep Audit": "Generate 10-15 items in every list. At least 5 line_edits expected. Be exhaustive.",
    }
    return mapping.get(depth, mapping["Standard"])


def _compute_metrics(content: str) -> Optional[str]:
    """Compute deterministic content metrics; return prompt block or empty."""
    try:
        from metrics import compute_metrics as _cm
        return _cm(content).to_prompt_block()
    except Exception as exc:
        log.debug("Content metrics unavailable: %s", exc)
        return None


def build_prompt(req: EvaluationRequest, snippets: List[dict]) -> str:
    """Assemble the user-turn prompt: config + retrieved rubrics + content metrics + content."""
    lines: List[str] = ["## Evaluation configuration"]
    lines.append(f"- Target audience: {', '.join(req.audience) or 'unspecified'}")
    lines.append(f"- Writing style: {', '.join(req.style) or 'unspecified'}")
    lines.append(f"- Primary purpose: {req.purpose or 'unspecified'}")
    lines.append(f"- Blog type: {req.blog_type or 'unspecified'}")
    lines.append(f"- Platform: {req.platform or 'unspecified'}")
    lines.append(f"- Feedback depth: {req.depth}")
    lines.append(f"- Item count directive: {_depth_to_items(req.depth)}")
    if req.custom:
        lines.append(f"- Custom focus: {req.custom}")
    if req.prompt_injection:
        lines.append(f"- Additional instructions: {req.prompt_injection}")

    # Pre-computed metrics block (ground truth — LLM should not compute these)
    metrics_block = _compute_metrics(req.content)
    if metrics_block:
        lines.append(f"\n{metrics_block}")

    if snippets:
        lines.append("\n## Reference rubrics (retrieved)")
        for s in snippets:
            lines.append(f"\n### [{s['source']}]")
            lines.append(s["text"])

    lines.append("\n## Blog content")
    lines.append(req.content)
    return "\n".join(lines)


# ---------- Mock evaluator ----------
# Hardcoded result used until the real LLM call is wired in. Shape is
# locked to EvaluationResult so the frontend can be validated end-to-end.

def _mock_result(req: EvaluationRequest) -> EvaluationResult:
    word_count = len(req.content.split())
    return EvaluationResult(
        overall_score=78,
        summary=(
            "Solid draft with a clear thesis and good technical grounding. "
            "Tighten the introduction and add one concrete example to lift it "
            "into the top tier for your selected audience."
        ),
        score_breakdown=[
            ScoreDimension(name="Structure", score=82,
                           rationale="Headings follow a logical hierarchy; intro could be tighter."),
            ScoreDimension(name="Depth", score=75,
                           rationale="Covers the main concepts but skips a key edge case."),
            ScoreDimension(name="Clarity", score=80,
                           rationale="Sentences are readable; a few passive constructions remain."),
            ScoreDimension(name="Evidence", score=68,
                           rationale="Examples are anecdotal — add a benchmark or citation."),
            ScoreDimension(name="Engagement", score=84,
                           rationale="Strong hook and a clear call-to-action at the close."),
        ],
        strengths=[
            "Opening paragraph establishes the problem in under 50 words.",
            "Code snippets are runnable and well-commented.",
            "Closing CTA aligns with the stated purpose.",
        ],
        improvement_priorities=[
            ImprovementItem(
                priority="high",
                title="Add quantitative evidence",
                description="Replace the 'much faster' claim in section 2 with a measured benchmark.",
            ),
            ImprovementItem(
                priority="medium",
                title="Trim the introduction",
                description="The first three paragraphs restate the title — collapse them into one.",
            ),
            ImprovementItem(
                priority="low",
                title="Normalize heading case",
                description="Section 4 uses Title Case while others use Sentence case.",
            ),
        ],
        line_edits=[
            LineEdit(
                before="This is something that has been on my mind for a while now.",
                after="I've been thinking about this for months.",
                rationale="Cuts 6 words and removes hedging.",
            ),
            LineEdit(
                before="It is widely known that caching improves performance.",
                after="Caching cut our p99 latency from 240ms to 38ms.",
                rationale="Replaces a truism with concrete evidence.",
            ),
        ],
        comparative_analysis=[
            "Your introduction is 2.1× longer than top-performing posts in this category.",
            f"At {word_count} words, the post sits below the 1,200-word median for "
            f"{req.platform or 'this platform'}.",
        ],
        word_count=word_count,
        mode="mock",
    )


# ---------- Routes ----------

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


class FeedbackRequest(BaseModel):
    """Payload for submitting user feedback on an evaluation."""
    evaluation_id: int
    feedback_type: Literal["correction", "rating", "flag"]
    payload: dict = Field(default_factory=dict)
    notes: str = ""


@app.post("/feedback")
def submit_feedback(fb: FeedbackRequest) -> dict:
    """Store user correction/rating for a previous evaluation."""
    try:
        from feedback import store_feedback
        fid = store_feedback(
            evaluation_id=fb.evaluation_id,
            feedback_type=fb.feedback_type,
            payload=fb.payload,
            notes=fb.notes or None,
        )
        return {"status": "ok", "feedback_id": fid}
    except Exception as exc:
        log.warning("Feedback storage failed: %s", exc)
        return {"status": "error", "detail": str(exc)}


def _force_mock() -> bool:
    return os.getenv("USE_MOCK_LLM", "").lower() in {"1", "true", "yes"}


@app.post("/evaluate", response_model=EvaluationResult)
def evaluate(req: EvaluationRequest) -> EvaluationResult:
    snippets = _retrieve_context(req)
    prompt = build_prompt(req, snippets)

    # Bail out to the mock if the LLM isn't usable in this environment.
    if _force_mock():
        return _mock_result(req)
    try:
        import llm
    except ImportError:
        log.warning("llm module unavailable; returning mock")
        return _mock_result(req)
    if not llm.is_configured():
        log.warning("GROQ_API_KEY not set; returning mock")
        return _mock_result(req)

    import time
    t0 = time.monotonic()
    try:
        raw = llm.evaluate(prompt, depth=req.depth)
        raw.setdefault("word_count", len(req.content.split()))
        raw["mode"] = "live"
        validated = EvaluationResult.model_validate(raw)
        latency_ms = (time.monotonic() - t0) * 1000

        # Persist to feedback loop (best-effort)
        try:
            from feedback import store_evaluation
            store_evaluation(
                config=req.model_dump(),
                snippets=[{k: s.get(k) for k in ("source", "score")} for s in snippets],
                result=raw,
                latency_ms=latency_ms,
                confidence="low" if raw.get("confidence_warning") else "ok",
            )
        except Exception:
            pass

        return validated
    except (ValidationError, ValueError) as exc:
        log.exception("LLM returned malformed result: %s", exc)
        return _mock_result(req)
    except Exception as exc:
        log.exception("LLM call failed: %s", exc)
        return _mock_result(req)


# ---------- Static frontend ----------
# Serve index.html, app.js, style.css from the project root so the whole
# app runs from one process during development.

_ROOT = Path(__file__).parent
app.mount("/", StaticFiles(directory=str(_ROOT), html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
