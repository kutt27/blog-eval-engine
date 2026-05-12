"""Blog Evaluator API server.

Exposes a single POST /evaluate endpoint that accepts the frontend's
evaluation config as JSON plus an optional `prompt_injection` string for
augmenting the LLM prompt during evaluation.

LLM + semantic-RAG wiring is intentionally stubbed for now; this layer
defines and validates the request contract.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Literal, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


# ---------- Request / response models ----------

class EvaluationRequest(BaseModel):
    """Payload sent by the frontend when the user clicks Run Evaluation."""

    content: str = Field(..., min_length=1, description="Markdown blog content to evaluate.")
    audience: List[str] = Field(default_factory=list)
    style: List[str] = Field(default_factory=list)
    purpose: str = ""
    platform: str = ""
    depth: Literal["Quick", "Standard", "Deep Audit"] = "Standard"
    custom: str = ""

    # Hook for callers (and future admin/test surfaces) to inject extra
    # instructions or override fragments into the LLM prompt.
    prompt_injection: Optional[str] = None


class EvaluationResponse(BaseModel):
    status: str
    received: EvaluationRequest
    word_count: int
    prompt_preview: str


# ---------- App setup ----------

app = FastAPI(title="Blog Evaluator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Prompt assembly (stub) ----------

def build_prompt(req: EvaluationRequest) -> str:
    """Assemble the evaluation prompt. Real RAG retrieval lands later."""
    parts = [
        "You are evaluating a blog post.",
        f"Target audience: {', '.join(req.audience) or 'unspecified'}",
        f"Writing style: {', '.join(req.style) or 'unspecified'}",
        f"Primary purpose: {req.purpose or 'unspecified'}",
        f"Platform: {req.platform or 'unspecified'}",
        f"Feedback depth: {req.depth}",
    ]
    if req.custom:
        parts.append(f"Custom focus: {req.custom}")
    if req.prompt_injection:
        parts.append(f"Additional instructions: {req.prompt_injection}")
    parts.append("---")
    parts.append(req.content)
    return "\n".join(parts)


# ---------- Routes ----------

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate(req: EvaluationRequest) -> EvaluationResponse:
    prompt = build_prompt(req)
    word_count = len(req.content.split())
    preview = prompt if len(prompt) <= 500 else prompt[:500] + "..."
    return EvaluationResponse(
        status="received",
        received=req,
        word_count=word_count,
        prompt_preview=preview,
    )


# ---------- Static frontend ----------
# Serve index.html, app.js, style.css from the project root so the whole
# app runs from one process during development.

_ROOT = Path(__file__).parent
app.mount("/", StaticFiles(directory=str(_ROOT), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
