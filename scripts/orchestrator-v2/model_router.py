#!/usr/bin/env python3
"""
Model Router — Intelligent model selection based on task type, complexity, context size, and historical success rates.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional

# Try to import psycopg2 for learning integration
try:
    import psycopg2
    HAS_PG = True
except ImportError:
    HAS_PG = False

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:BtFlrZjz4BV*QcOsd9u*glFKUhAAgqIw@trolley.proxy.rlwy.net:5432/railway"
)

# ── Routing Table ──────────────────────────────────────────────
DEFAULT_MODEL = "anthropic/claude-opus-4-6"

ROUTING_TABLE = [
    # (task_type, complexity, context_threshold, model)
    {"task_type": "heavy_coding",   "complexity": "high", "context": "any",   "model": "anthropic/claude-opus-4-6"},
    {"task_type": "small_coding",   "complexity": "low",  "context": "small", "model": "deepseek/deepseek-chat"},
    {"task_type": "analysis",       "complexity": "any",  "context": "large", "model": "anthropic/claude-opus-4-6"},
    {"task_type": "orchestration",  "complexity": "high", "context": "any",   "model": "anthropic/claude-opus-4-6"},
    {"task_type": "swarm",          "complexity": "any",  "context": "any",   "model": "kimi/kimi-k2.5"},
    {"task_type": "lightweight",    "complexity": "low",  "context": "small", "model": "deepseek/deepseek-chat"},
]

# Keywords for auto-classification
TASK_TYPE_KEYWORDS = {
    "heavy_coding": ["build", "implement", "refactor", "architect", "full stack", "complex code", "system design"],
    "small_coding": ["fix", "patch", "tweak", "small change", "bug", "lint", "format", "quick code"],
    "analysis": ["analyze", "research", "review", "audit", "evaluate", "compare", "summarize document"],
    "orchestration": ["coordinate", "orchestrate", "plan", "decompose", "manage", "oversee"],
    "swarm": ["batch", "bulk", "parallel", "fleet", "many", "swarm", "mass"],
    "lightweight": ["chat", "question", "translate", "simple", "quick", "lookup"],
}


@dataclass
class TaskProfile:
    description: str
    task_type: Optional[str] = None
    complexity: str = "medium"  # low, medium, high
    context_tokens: int = 0
    tags: list = field(default_factory=list)


def classify_task_type(description: str) -> str:
    """Auto-classify task type from description."""
    desc_lower = description.lower()
    scores = {}
    for ttype, keywords in TASK_TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in desc_lower)
        if score > 0:
            scores[ttype] = score
    if scores:
        return max(scores, key=scores.get)
    # Default: if it mentions code-related words, small_coding; else lightweight
    code_words = ["code", "script", "function", "class", "api", "endpoint", "database", "sql"]
    if any(w in desc_lower for w in code_words):
        return "small_coding"
    return "lightweight"


def estimate_complexity(description: str) -> str:
    """Estimate complexity from description length and keywords."""
    high_words = ["complex", "full", "entire", "end-to-end", "production", "architecture", "system"]
    low_words = ["simple", "quick", "small", "tiny", "minor", "trivial"]
    desc_lower = description.lower()
    if any(w in desc_lower for w in high_words) or len(description) > 500:
        return "high"
    if any(w in desc_lower for w in low_words) or len(description) < 100:
        return "low"
    return "medium"


def get_historical_success(task_type: str, model: str) -> Optional[float]:
    """Query Postgres for historical success rate of model on task type."""
    if not HAS_PG:
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE success = true)::float / NULLIF(COUNT(*), 0)
            FROM orchestrator_outcomes
            WHERE task_type = %s AND model = %s
            AND created_at > NOW() - INTERVAL '30 days'
        """, (task_type, model))
        row = cur.fetchone()
        conn.close()
        return row[0] if row and row[0] is not None else None
    except Exception:
        return None


def route(profile: TaskProfile) -> str:
    """Select the best model for a task profile."""
    if profile.task_type is None:
        profile.task_type = classify_task_type(profile.description)
    if profile.complexity == "medium":
        profile.complexity = estimate_complexity(profile.description)

    context_size = "large" if profile.context_tokens > 100_000 else "small"

    # Find matching routes
    candidates = []
    for entry in ROUTING_TABLE:
        if entry["task_type"] == profile.task_type:
            # Check context match
            if entry["context"] != "any" and entry["context"] != context_size:
                continue
            # Check complexity match
            if entry["complexity"] != "any" and entry["complexity"] != profile.complexity:
                continue
            candidates.append(entry["model"])

    if not candidates:
        # Fallback: match by task_type only
        for entry in ROUTING_TABLE:
            if entry["task_type"] == profile.task_type:
                candidates.append(entry["model"])

    if not candidates:
        return "deepseek/deepseek-chat"  # ultimate fallback

    # If multiple candidates, check historical success
    if len(candidates) > 1:
        best_model = candidates[0]
        best_rate = -1.0
        for model in candidates:
            rate = get_historical_success(profile.task_type, model)
            if rate is not None and rate > best_rate:
                best_rate = rate
                best_model = model
        return best_model

    return candidates[0] if candidates else DEFAULT_MODEL


def route_simple(description: str, context_tokens: int = 0) -> str:
    """Simple one-liner route."""
    return route(TaskProfile(description=description, context_tokens=context_tokens))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        desc = " ".join(sys.argv[1:])
        profile = TaskProfile(description=desc)
        model = route(profile)
        print(json.dumps({
            "description": desc,
            "task_type": profile.task_type or classify_task_type(desc),
            "complexity": estimate_complexity(desc),
            "model": model
        }, indent=2))
    else:
        print("Usage: python3 model_router.py <task description>")
