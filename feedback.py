"""
Feedback loop — SQLite persistence for evaluations and user corrections.

Stores every evaluation request + result, plus optional user feedback
(corrections, ratings). A summary endpoint exposes what the LLM
consistently gets wrong, which can be injected into the system prompt
to improve future evaluations.
"""

from __future__ import annotations

import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger("blog-evaluator.feedback")

_DB_PATH = Path(__file__).parent / ".evaluation_history.db"


# ---------- Schema ----------

_SCHEMA = """
CREATE TABLE IF NOT EXISTS evaluations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   REAL NOT NULL,
    config_json TEXT NOT NULL,            -- serialized EvaluationRequest
    snippets    TEXT,                     -- serialized retrieved snippets
    result_json TEXT NOT NULL,            -- serialized EvaluationResult
    latency_ms  REAL,
    mode        TEXT DEFAULT 'live',
    confidence  TEXT DEFAULT 'ok'         -- 'ok', 'low', 'warning'
);

CREATE TABLE IF NOT EXISTS feedback (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluation_id   INTEGER REFERENCES evaluations(id),
    timestamp       REAL NOT NULL,
    feedback_type   TEXT NOT NULL,        -- 'correction', 'rating', 'flag'
    payload_json    TEXT NOT NULL,         -- arbitrary JSON payload
    notes           TEXT
);

CREATE INDEX IF NOT EXISTS idx_eval_timestamp ON evaluations(timestamp);
CREATE INDEX IF NOT EXISTS idx_eval_config ON evaluations(config_json);
CREATE INDEX IF NOT EXISTS idx_feedback_eval ON feedback(evaluation_id);
"""


# ---------- Connection management ----------


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(_SCHEMA)
    return conn


# ---------- Public API ----------


def store_evaluation(
    config: dict,
    snippets: Optional[List[dict]],
    result: dict,
    latency_ms: Optional[float] = None,
    confidence: str = "ok",
) -> int:
    """Store an evaluation and return its ID."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            """
            INSERT INTO evaluations (timestamp, config_json, snippets, result_json, latency_ms, mode, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                time.time(),
                json.dumps(config),
                json.dumps(snippets) if snippets else None,
                json.dumps(result),
                latency_ms,
                result.get("mode", "live"),
                confidence,
            ),
        )
        conn.commit()
        return cur.lastrowid  # type: ignore[return-value]
    finally:
        conn.close()


def store_feedback(
    evaluation_id: int,
    feedback_type: str,
    payload: dict,
    notes: Optional[str] = None,
) -> int:
    """Store user feedback for a previous evaluation."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            """
            INSERT INTO feedback (evaluation_id, timestamp, feedback_type, payload_json, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (evaluation_id, time.time(), feedback_type, json.dumps(payload), notes),
        )
        conn.commit()
        return cur.lastrowid  # type: ignore[return-value]
    finally:
        conn.close()


def get_recent_evaluations(limit: int = 20) -> List[Dict[str, Any]]:
    """Return the most recent evaluations."""
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM evaluations ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_feedback_summary() -> str:
    """Generate a human-readable summary of common issues from feedback.

    This summary is designed to be injected into the LLM system prompt
    so it learns from past corrections.
    """
    conn = _get_conn()
    try:
        # Get counts of corrections grouped by common patterns
        rows = conn.execute(
            """
            SELECT e.config_json, f.payload_json, f.notes
            FROM feedback f
            JOIN evaluations e ON e.id = f.evaluation_id
            WHERE f.feedback_type = 'correction'
            ORDER BY f.timestamp DESC
            LIMIT 20
            """
        ).fetchall()

        if not rows:
            return "No corrections recorded yet."

        summaries: List[str] = []
        for r in rows:
            payload = json.loads(r["payload_json"])
            notes = r["notes"] or ""
            if "field" in payload and "expected" in payload:
                summaries.append(
                    f"- {payload['field']}: user expected ~{payload['expected']}, "
                    f"got ~{payload.get('actual', '?')}. {notes}"
                )

        if not summaries:
            return ""

        return (
            "## Learning from past corrections\n\n"
            "The following issues were flagged by users in previous evaluations. "
            "Pay extra attention to these areas:\n\n"
            + "\n".join(summaries)
        )
    finally:
        conn.close()


def get_common_weaknesses(min_occurrences: int = 3) -> str:
    """Analyze evaluation history for recurring low scores and patterns.

    Returns a block of text that can be injected into the system prompt.
    """
    conn = _get_conn()
    try:
        rows = conn.execute(
            """
            SELECT result_json FROM evaluations
            WHERE mode = 'live'
            ORDER BY timestamp DESC
            LIMIT 100
            """
        ).fetchall()

        if len(rows) < min_occurrences:
            return ""

        # Track dimension scores
        dimension_scores: Dict[str, List[int]] = {}
        for r in rows:
            result = json.loads(r["result_json"])
            for dim in result.get("score_breakdown", []):
                name = dim.get("name", "unknown")
                score = dim.get("score", 50)
                if name not in dimension_scores:
                    dimension_scores[name] = []
                dimension_scores[name].append(score)

        weak_spots: List[str] = []
        for name, scores in dimension_scores.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < 65 and len(scores) >= min_occurrences:
                weak_spots.append(
                    f"- **{name}** — average score {avg_score:.0f}/100 "
                    f"across {len(scores)} evaluations. Be extra rigorous here."
                )

        if not weak_spots:
            return ""

        return (
            "## Historical evaluation patterns\n\n"
            "Based on past evaluations, these dimensions consistently score low. "
            "Scrutinize them carefully:\n\n"
            + "\n".join(weak_spots)
        )
    finally:
        conn.close()
