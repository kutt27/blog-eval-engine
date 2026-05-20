"""Semantic retrieval over the markdown rubrics in ``semantic-rag/``.

Chunks each file on H2 boundaries, embeds the chunks once with a local
ONNX model via ``fastembed``, and caches the result on disk keyed by a
hash of the source files. ``retrieve()`` returns the top-k snippets for
a query using hybrid dense + sparse (BM25) retrieval.

Improvements (Tier 1):
- H1 hierarchy tracking in chunk source names
- Overlapping chunks for long sections (> 500 chars)
- Hybrid retrieval blending dense embeddings with BM25 sparse scores
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import List, Optional

import numpy as np

from rank_bm25 import BM25Okapi


_HERE = Path(__file__).parent
_RAG_DIR = _HERE / "semantic-rag"
_CACHE_FILE = _HERE / ".rag_cache.npz"
_MODEL_NAME = "BAAI/bge-small-en-v1.5"  # fastembed default; 384-dim, ONNX
_CHUNK_VERSION = 2  # increment to invalidate cache when chunking strategy changes

# Lazy singletons so importing this module is cheap.
_model = None
_chunks: Optional[List[dict]] = None
_embeddings: Optional[np.ndarray] = None
_bm25: Optional[BM25Okapi] = None


def _load_model():
    global _model
    if _model is None:
        from fastembed import TextEmbedding
        _model = TextEmbedding(model_name=_MODEL_NAME)
    return _model


def _embed(texts: List[str]) -> np.ndarray:
    """Run texts through the model and return an L2-normalized float32 matrix."""
    model = _load_model()
    vectors = np.asarray(list(model.embed(texts)), dtype=np.float32)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


def _extract_h1(text: str) -> str:
    """Extract the first H1 heading from markdown text."""
    match = re.search(r"^# (.+)", text, re.M)
    return match.group(1).strip() if match else "(no title)"


def _split_into_overlapping(text: str, max_chars: int = 500, overlap: int = 100) -> List[str]:
    """Split text into overlapping paragraph-aligned chunks."""
    paragraphs = re.split(r"\n\n+", text.strip())
    if not paragraphs:
        return [text] if text else []

    # Remove empty paragraphs
    paragraphs = [p for p in paragraphs if p.strip()]

    chunks: List[str] = []
    current: List[str] = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)
        if current_len + para_len > max_chars and current:
            chunk_text = "\n\n".join(current)
            chunks.append(chunk_text)

            # Carry overlap from the end of current
            overlap_text = ""
            acc = 0
            for p in reversed(current):
                overlap_text = p + "\n\n" + overlap_text
                acc += len(p)
                if acc >= overlap:
                    break
            current = [overlap_text.strip(), para]
            current_len = len(overlap_text) + para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks if chunks else [text]


def _chunk_file(path: Path) -> List[dict]:
    """Split a markdown file on H2 headings; track H1 hierarchy.

    For sections longer than 500 characters, creates overlapping
    sub-chunks aligned to paragraph boundaries.
    """
    text = path.read_text(encoding="utf-8")
    h1_title = _extract_h1(text)

    # Remove H1 line so it doesn't interfere with H2 splitting
    text_no_h1 = re.sub(r"^# .+\n?", "", text, count=1).strip()

    parts = re.split(r"^## ", text_no_h1, flags=re.M)
    chunks: List[dict] = []

    intro = parts[0].strip()
    if intro:
        chunks.append({
            "source": f"{path.name} > {h1_title} > (intro)",
            "text": intro,
        })

    for section in parts[1:]:
        header, _, body = section.partition("\n")
        header = header.strip()
        body = body.strip()
        full = f"## {header}\n{body}" if body else f"## {header}"

        # For long sections, create overlapping sub-chunks
        if len(full) > 500:
            body_only = body if body else ""
            sub_texts = _split_into_overlapping(body_only, max_chars=500, overlap=100)
            for i, sub in enumerate(sub_texts):
                chunks.append({
                    "source": f"{path.name} > {h1_title} > {header} (part {i + 1}/{len(sub_texts)})",
                    "text": f"## {header}\n{sub}",
                })
        else:
            chunks.append({
                "source": f"{path.name} > {h1_title} > {header}",
                "text": full,
            })
    return chunks


def _content_hash() -> str:
    h = hashlib.sha256()
    for path in sorted(_RAG_DIR.glob("*.md")):
        h.update(path.name.encode())
        h.update(path.read_bytes())
    h.update(_MODEL_NAME.encode())
    h.update(str(_CHUNK_VERSION).encode())  # invalidate cache when strategy changes
    return h.hexdigest()


def _load_or_build() -> None:
    """Populate the module-level chunk + embedding + BM25 singletons."""
    global _chunks, _embeddings, _bm25
    if _chunks is not None and _embeddings is not None and _bm25 is not None:
        return

    expected = _content_hash()
    if _CACHE_FILE.exists():
        try:
            data = np.load(_CACHE_FILE, allow_pickle=False)
            if str(data["hash"]) == expected:
                _chunks = json.loads(str(data["chunks"]))
                _embeddings = data["embeddings"].astype(np.float32)
                _build_bm25()  # rebuild BM25 from chunks (not cached in npz)
                return
        except Exception:
            pass  # fall through to rebuild

    all_chunks: List[dict] = []
    for path in sorted(_RAG_DIR.glob("*.md")):
        all_chunks.extend(_chunk_file(path))

    embs = _embed([c["text"] for c in all_chunks])

    _chunks = all_chunks
    _embeddings = embs
    _build_bm25()

    np.savez_compressed(
        _CACHE_FILE,
        embeddings=embs,
        chunks=np.array(json.dumps(all_chunks)),
        hash=np.array(expected),
    )


def _build_bm25() -> None:
    """Build BM25 index from the current chunk corpus."""
    global _bm25
    if _chunks is None:
        _bm25 = None
        return
    tokenized_corpus = [c["text"].lower().split() for c in _chunks]
    _bm25 = BM25Okapi(tokenized_corpus)


def retrieve(query: str, k: int = 6, alpha: float = 0.7) -> List[dict]:
    """
    Return the top-k chunks using hybrid retrieval.

    Blends dense (cosine) and sparse (BM25) scores:
    - alpha=0.7 → 70% dense, 30% BM25 weight
    """
    _load_or_build()
    assert _chunks is not None and _embeddings is not None and _bm25 is not None

    # --- Dense retrieval ---
    q = _embed([query])
    dense_scores = (_embeddings @ q.T).flatten()

    # --- BM25 retrieval ---
    tokenized_query = query.lower().split()
    bm25_scores = np.array(_bm25.get_scores(tokenized_query), dtype=np.float64)

    # --- Normalize both to [0, 1] ---
    dense_norm = dense_scores.copy()
    d_max = dense_norm.max()
    if d_max > 0:
        dense_norm /= d_max

    bm25_norm = bm25_scores.copy()
    b_max = bm25_norm.max()
    if b_max > 0:
        bm25_norm /= b_max

    # --- Blend ---
    blended = alpha * dense_norm + (1.0 - alpha) * bm25_norm
    top_idx = np.argsort(-blended)[:k]

    return [
        {
            "source": _chunks[i]["source"],
            "text": _chunks[i]["text"],
            "score": float(blended[i]),
        }
        for i in top_idx
    ]


def build_query(
    audience: List[str],
    style: List[str],
    purpose: str,
    blog_type: str,
    platform: str,
    custom: str,
) -> str:
    """Assemble a retrieval query from the evaluation config."""
    parts: List[str] = []
    if audience:
        parts.append(f"Audience: {', '.join(audience)}")
    if style:
        parts.append(f"Style: {', '.join(style)}")
    if purpose:
        parts.append(f"Purpose: {purpose}")
    if blog_type:
        parts.append(f"Blog type: {blog_type}")
    if platform:
        parts.append(f"Platform: {platform}")
    if custom:
        parts.append(f"Focus: {custom}")
    return " | ".join(parts) if parts else "blog quality evaluation rubrics"
