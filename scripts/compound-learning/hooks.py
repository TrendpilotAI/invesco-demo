"""
Compound Learning Hooks — called by cron jobs and session lifecycle.

Usage:
    from compound_learning.hooks import on_session_end, on_task_complete
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .client import CompoundLearningClient

logger = logging.getLogger("compound_learning.hooks")


def _client() -> CompoundLearningClient:
    return CompoundLearningClient()


def on_session_end(
    session_key: str,
    model: str,
    summary: str,
    learnings_list: List[Dict[str, str]],
):
    """Called when a session ends. Records learnings and updates metrics.

    learnings_list: [{"category": "...", "title": "...", "content": "...", "impact": "medium", "tags": [...]}]
    """
    cl = _client()
    try:
        ids = []
        for item in learnings_list:
            lid = cl.record_learning(
                category=item.get("category", "general"),
                title=item["title"],
                content=item["content"],
                session=session_key,
                model=model,
                trigger="session_end",
                impact=item.get("impact", "medium"),
                tags=item.get("tags", []),
            )
            if lid:
                ids.append(lid)

        # Record a meta-learning about the session itself
        if summary:
            cl.record_learning(
                category="session",
                title=f"Session summary: {session_key}",
                content=summary,
                session=session_key,
                model=model,
                trigger="session_end",
                impact="low",
                tags=["session_summary"],
            )

        cl.update_daily_metrics()
        logger.info("Session %s ended: %d learnings recorded", session_key, len(ids))
    finally:
        cl.close()


def on_task_complete(
    task_id: str,
    model: str,
    task_type: str,
    success: bool,
    completion_time_ms: int = 0,
    tokens_in: int = 0,
    tokens_out: int = 0,
    cost_usd: float = 0.0,
    quality_score: Optional[float] = None,
    project: Optional[str] = None,
    notes: Optional[str] = None,
):
    """Called when a sub-agent task completes. Records model performance."""
    cl = _client()
    try:
        cl.record_model_performance(
            model=model,
            task_type=task_type,
            completion_time_ms=completion_time_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost_usd,
            quality_score=quality_score,
            success=success,
            project=project,
            notes=f"task:{task_id} | {notes or ''}",
        )

        # Auto-learn from failures
        if not success:
            cl.record_learning(
                category="model_selection",
                title=f"{model} failed on {task_type}",
                content=f"Task {task_id} failed. Model: {model}, Type: {task_type}. {notes or 'No details.'}",
                model=model,
                trigger="auto",
                impact="medium",
                project=project,
                tags=["failure", "auto_detected", task_type],
            )

        logger.info("Task %s complete: model=%s success=%s", task_id, model, success)
    finally:
        cl.close()


def on_human_feedback(
    session_key: str,
    agent_action: str,
    correction: str,
    severity: str = "important",
):
    """Called when Nathan corrects Honey. Records feedback and generates learning."""
    cl = _client()
    try:
        fb_id = cl.record_feedback(
            session_key=session_key,
            agent_action=agent_action,
            human_correction=correction,
            severity=severity,
        )

        # Auto-generate a learning from the feedback
        cl.record_learning(
            category="feedback",
            title=f"Correction: {correction[:80]}",
            content=f"Action: {agent_action}\nCorrection: {correction}\nSeverity: {severity}",
            session=session_key,
            trigger="feedback",
            impact="high" if severity == "critical" else "medium",
            tags=["human_feedback", severity],
        )

        logger.info("Feedback recorded: session=%s severity=%s", session_key, severity)
    finally:
        cl.close()


def on_cron_consolidate():
    """Called by hourly-consolidate cron. Detects patterns, updates metrics.

    This is the compound learning loop:
    1. Look at recent learnings for repeated categories/themes
    2. Detect patterns (3+ learnings in same category with similar content)
    3. Update daily metrics
    """
    cl = _client()
    try:
        # Update today's metrics
        cl.update_daily_metrics()

        # Detect patterns: categories with 3+ recent learnings
        rows = cl._execute(
            """
            SELECT category, COUNT(*) as n,
                   array_agg(id) as ids,
                   array_agg(DISTINCT title) as titles
            FROM compound_learnings
            WHERE created_at > NOW() - INTERVAL '7 days'
            GROUP BY category
            HAVING COUNT(*) >= 3
            ORDER BY n DESC
            """
        )

        patterns_found = 0
        for row in (rows or []):
            cat = row["category"]
            n = row["n"]
            titles = row["titles"][:5]  # top 5 titles
            ids = row["ids"]

            cl.record_pattern(
                name=f"recurring_{cat}",
                description=f"{n} learnings in '{cat}' category in the last 7 days: {', '.join(str(t) for t in titles)}",
                recommendation=f"High activity in '{cat}' — review and consolidate learnings, consider automation.",
                category=cat,
                learning_ids=ids[:10],  # cap at 10
            )
            patterns_found += 1

        # Detect model failure patterns
        fail_rows = cl._execute(
            """
            SELECT model, task_type, COUNT(*) as failures
            FROM compound_model_performance
            WHERE NOT success AND created_at > NOW() - INTERVAL '7 days'
            GROUP BY model, task_type
            HAVING COUNT(*) >= 2
            """
        )
        for row in (fail_rows or []):
            cl.record_pattern(
                name=f"model_failure_{row['model']}_{row['task_type']}",
                description=f"{row['model']} failed {row['failures']} times on {row['task_type']} tasks in 7 days",
                recommendation=f"Consider routing {row['task_type']} tasks away from {row['model']}",
                category="model_selection",
            )
            patterns_found += 1

        logger.info("Cron consolidate complete: %d patterns detected/updated", patterns_found)
    finally:
        cl.close()
