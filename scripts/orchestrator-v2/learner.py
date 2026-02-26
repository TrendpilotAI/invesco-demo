#!/usr/bin/env python3
"""
Learner — Track outcomes in Postgres, analyze patterns, feed back into model_router.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Optional, List, Dict

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:BtFlrZjz4BV*QcOsd9u*glFKUhAAgqIw@trolley.proxy.rlwy.net:5432/railway"
)

try:
    import psycopg2
    import psycopg2.extras
    HAS_PG = True
except ImportError:
    HAS_PG = False


# ── Schema ─────────────────────────────────────────────────────

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS orchestrator_outcomes (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(64) NOT NULL,
    goal TEXT,
    task_description TEXT NOT NULL,
    task_type VARCHAR(32),
    model VARCHAR(128) NOT NULL,
    effort VARCHAR(16),
    success BOOLEAN NOT NULL,
    duration_seconds FLOAT,
    retries INT DEFAULT 0,
    error TEXT,
    result_summary TEXT,
    context_tokens INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_outcomes_task_type ON orchestrator_outcomes(task_type);
CREATE INDEX IF NOT EXISTS idx_outcomes_model ON orchestrator_outcomes(model);
CREATE INDEX IF NOT EXISTS idx_outcomes_created ON orchestrator_outcomes(created_at);

CREATE TABLE IF NOT EXISTS orchestrator_goals (
    id SERIAL PRIMARY KEY,
    goal TEXT NOT NULL,
    total_tasks INT,
    completed_tasks INT,
    failed_tasks INT,
    skipped_tasks INT,
    duration_seconds FLOAT,
    success BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""


def get_conn():
    if not HAS_PG:
        raise RuntimeError("psycopg2 not installed. Run: pip install psycopg2-binary")
    return psycopg2.connect(DATABASE_URL)


def init_schema():
    """Create tables if they don't exist."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print("✅ Schema initialized")


def record_outcome(task_id: str, goal: str, description: str, task_type: str,
                   model: str, effort: str, success: bool, duration: float = 0,
                   retries: int = 0, error: str = None, result_summary: str = None,
                   context_tokens: int = 0):
    """Record a task outcome."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO orchestrator_outcomes 
        (task_id, goal, task_description, task_type, model, effort, success,
         duration_seconds, retries, error, result_summary, context_tokens)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (task_id, goal, description, task_type, model, effort, success,
          duration, retries, error, result_summary, context_tokens))
    conn.commit()
    conn.close()


def record_goal(goal: str, total: int, completed: int, failed: int,
                skipped: int, duration: float, success: bool):
    """Record a goal-level outcome."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO orchestrator_goals
        (goal, total_tasks, completed_tasks, failed_tasks, skipped_tasks,
         duration_seconds, success)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (goal, total, completed, failed, skipped, duration, success))
    conn.commit()
    conn.close()


def get_model_stats(days: int = 30) -> List[Dict]:
    """Get model performance stats."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT 
            model,
            task_type,
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE success) as successes,
            ROUND(AVG(duration_seconds)::numeric, 1) as avg_duration,
            ROUND((COUNT(*) FILTER (WHERE success)::float / NULLIF(COUNT(*), 0) * 100)::numeric, 1) as success_rate,
            ROUND(AVG(retries)::numeric, 1) as avg_retries
        FROM orchestrator_outcomes
        WHERE created_at > NOW() - INTERVAL '%s days'
        GROUP BY model, task_type
        ORDER BY success_rate DESC, total DESC
    """ % days)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_model_recommendations() -> Dict[str, str]:
    """Based on history, recommend best model per task type."""
    stats = get_model_stats()
    recommendations = {}
    for row in stats:
        tt = row["task_type"]
        if tt not in recommendations or float(row["success_rate"] or 0) > float(recommendations[tt].get("success_rate", 0)):
            recommendations[tt] = row
    return {k: v["model"] for k, v in recommendations.items()}


def generate_report(days: int = 30) -> str:
    """Generate a human-readable learning report."""
    stats = get_model_stats(days)
    if not stats:
        return "No data yet. Execute some tasks first."

    lines = [
        f"📊 Orchestrator Learning Report (last {days} days)",
        "=" * 55,
        "",
        f"{'Model':<35} {'Type':<15} {'Rate':>6} {'N':>4} {'Avg(s)':>7}",
        "-" * 70,
    ]
    for s in stats:
        lines.append(
            f"{s['model']:<35} {s['task_type'] or 'unknown':<15} "
            f"{s['success_rate'] or 0:>5.1f}% {s['total']:>4} {s['avg_duration'] or 0:>7.1f}"
        )

    lines.extend(["", "🎯 Recommendations:"])
    recs = get_model_recommendations()
    for tt, model in recs.items():
        lines.append(f"  {tt} → {model}")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 learner.py <init|report|stats>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "init":
        init_schema()
    elif cmd == "report":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        print(generate_report(days))
    elif cmd == "stats":
        stats = get_model_stats()
        print(json.dumps(stats, indent=2, default=str))
    else:
        print(f"Unknown command: {cmd}")
