"""Semantic retrieval over the markdown rubrics in ``semantic-rag/``.

Chunks each file on H2 boundaries, embeds the chunks once with a local
ONNX model via ``fastembed``, and caches the result on disk keyed by a
hash of the source files. ``retrieve()`` returns the top-k snippets for
a query.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import List, Optional

import numpy as np


_HERE = Path(__file__).parent
_RAG_DIR = _HERE / "semantic-rag"
_CACHE_FILE = _HERE / ".rag_cache.npz"
_MODEL_NAME = "BAAI/bge-small-en-v1.5"  # fastembed default; 384-dim, ONNX

# Lazy singletons so importing this module is cheap.
_model = None
_chunks: Optional[List[dict]] = None
_embeddings: Optional[np.ndarray] = None


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


def _chunk_file(path: Path) -> List[dict]:
    """Split a markdown file on H2 headings; preserve filename + heading."""
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.M)
    chunks: List[dict] = []

    intro = parts[0].strip()
    if intro:
        chunks.append({"source": f"{path.name} > (intro)", "text": intro})

    for section in parts[1:]:
        header, _, body = section.partition("\n")
        header = header.strip()
        body = body.strip()
        full = f"## {header}\n{body}" if body else f"## {header}"
        chunks.append({"source": f"{path.name} > {header}", "text": full})
    return chunks


def _content_hash() -> str:
    h = hashlib.sha256()
    for path in sorted(_RAG_DIR.glob("*.md")):
        h.update(path.name.encode())
        h.update(path.read_bytes())
    h.update(_MODEL_NAME.encode())
    return h.hexdigest()


def _load_or_build() -> None:
    """Populate the module-level chunk + embedding singletons."""
    global _chunks, _embeddings
    if _chunks is not None and _embeddings is not None:
        return

    expected = _content_hash()
    if _CACHE_FILE.exists():
        try:
            data = np.load(_CACHE_FILE, allow_pickle=False)
            if str(data["hash"]) == expected:
                _chunks = json.loads(str(data["chunks"]))
                _embeddings = data["embeddings"].astype(np.float32)
                return
        except Exception:
            pass  # fall through to rebuild

    all_chunks: List[dict] = []
    for path in sorted(_RAG_DIR.glob("*.md")):
        all_chunks.extend(_chunk_file(path))

    embs = _embed([c["text"] for c in all_chunks])

    _chunks = all_chunks
    _embeddings = embs
    np.savez_compressed(
        _CACHE_FILE,
        embeddings=embs,
        chunks=np.array(json.dumps(all_chunks)),
        hash=np.array(expected),
    )


def retrieve(query: str, k: int = 6) -> List[dict]:
    """Return the top-k chunks for ``query`` sorted by cosine similarity."""
    _load_or_build()
    assert _chunks is not None and _embeddings is not None

    q = _embed([query])
    scores = (_embeddings @ q.T).flatten()
    top_idx = np.argsort(-scores)[:k]
    return [
        {
            "source": _chunks[i]["source"],
            "text": _chunks[i]["text"],
            "score": float(scores[i]),
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
