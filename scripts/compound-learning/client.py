"""
CompoundLearningClient — Dual-write client: PostgreSQL now, self-hosted Convex target.

Usage:
    from compound_learning.client import CompoundLearningClient
    cl = CompoundLearningClient()
    cl.record_learning("model_selection", "GPT 5.4 bad for coding", "Completes fast but barely writes code", impact="high")
"""

import json
import logging
import os
import sys
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional

import psycopg2
import psycopg2.extras

from .convex_client import ConvexClient

logger = logging.getLogger("compound_learning")

# Fallback file when both Postgres and Convex are down
FALLBACK_LOG = os.path.join(os.path.dirname(__file__), "fallback_learnings.jsonl")


class CompoundLearningClient:
    """Dual-write client: PostgreSQL (primary) + self-hosted Convex (secondary)."""

    def __init__(
        self,
        postgres_url: Optional[str] = None,
        convex_url: Optional[str] = None,
        convex_token: Optional[str] = None,
    ):
        self._pg_url = postgres_url or os.environ.get("COMPOUND_DB_URL") or os.environ.get("DATABASE_URL")
        self._pg_conn: Optional[psycopg2.extensions.connection] = None

        self._convex = ConvexClient(
            url=convex_url or os.environ.get("CONVEX_URL"),
            token=convex_token or os.environ.get("OPENCLAW_CONVEX_SECRET"),
        )

    # ------------------------------------------------------------------
    # PostgreSQL connection (lazy, with reconnect)
    # ------------------------------------------------------------------

    def _pg(self) -> Optional[psycopg2.extensions.connection]:
        """Get or create Postgres connection. Returns None if unavailable."""
        if self._pg_conn and not self._pg_conn.closed:
            try:
                self._pg_conn.isolation_level  # ping
                return self._pg_conn
            except Exception:
                self._pg_conn = None

        if not self._pg_url:
            logger.warning("No PostgreSQL URL configured (set COMPOUND_DB_URL or DATABASE_URL)")
            return None

        try:
            self._pg_conn = psycopg2.connect(self._pg_url, connect_timeout=5)
            self._pg_conn.autocommit = True
            return self._pg_conn
        except Exception as e:
            logger.error("PostgreSQL connection failed: %s", e)
            return None

    def _execute(self, sql: str, params: tuple = ()) -> Optional[List[Dict]]:
        """Execute SQL and return rows as dicts. None on failure."""
        conn = self._pg()
        if not conn:
            return None
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql, params)
                if cur.description:
                    return [dict(row) for row in cur.fetchall()]
                return []
        except Exception as e:
            logger.error("SQL error: %s | %s", e, sql[:120])
            try:
                conn.rollback()
            except Exception:
                pass
            return None

    def _fallback_write(self, record_type: str, data: Dict[str, Any]):
        """Write to local JSONL file when both backends are down."""
        entry = {"_type": record_type, "_ts": datetime.now(timezone.utc).isoformat(), **data}
        try:
            with open(FALLBACK_LOG, "a") as f:
                f.write(json.dumps(entry, default=str) + "\n")
            logger.info("Wrote to fallback log: %s", record_type)
        except Exception as e:
            logger.error("Fallback write failed: %s", e)

    # ------------------------------------------------------------------
    # Record Learning
    # ------------------------------------------------------------------

    def record_learning(
        self,
        category: str,
        title: str,
        content: str,
        *,
        subcategory: Optional[str] = None,
        project: Optional[str] = None,
        task: Optional[str] = None,
        session: Optional[str] = None,
        agent: str = "honey",
        model: str = "unknown",
        trigger: str = "manual",
        confidence: float = 0.8,
        impact: str = "medium",
        tags: Optional[List[str]] = None,
    ) -> Optional[int]:
        """Record a learning. Returns the learning ID or None."""
        tags = tags or []

        # Postgres write
        row = self._execute(
            """
            INSERT INTO compound_learnings
                (category, subcategory, title, content, project, task, session_key,
                 agent, model, trigger, confidence, impact, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (category, subcategory, title, content, project, task, session,
             agent, model, trigger, confidence, impact, tags),
        )

        learning_id = row[0]["id"] if row else None

        # Convex write (best-effort)
        if self._convex.available:
            self._convex.mutation("compoundLearnings:record", {
                "category": category,
                "subcategory": subcategory or "",
                "title": title,
                "content": content,
                "project": project or "",
                "task": task or "",
                "sessionKey": session or "",
                "agent": agent,
                "model": model,
                "trigger": trigger,
                "confidence": confidence,
                "impact": impact,
                "tags": tags,
            })

        # Fallback if Postgres failed
        if learning_id is None and not self._convex.available:
            self._fallback_write("learning", {
                "category": category, "title": title, "content": content,
                "project": project, "impact": impact, "tags": tags,
            })

        return learning_id

    # ------------------------------------------------------------------
    # Record Decision
    # ------------------------------------------------------------------

    def record_decision(
        self,
        title: str,
        description: str,
        reasoning: str,
        *,
        alternatives: Optional[List[str]] = None,
        project: Optional[str] = None,
        stakeholder: Optional[str] = None,
        decided_by: str = "honey",
        reversible: bool = True,
        tags: Optional[List[str]] = None,
    ) -> Optional[int]:
        """Log a significant decision. Returns decision ID or None."""
        alternatives = alternatives or []
        tags = tags or []

        row = self._execute(
            """
            INSERT INTO compound_decisions
                (title, description, reasoning, alternatives, project, stakeholder,
                 decided_by, reversible, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (title, description, reasoning, json.dumps(alternatives),
             project, stakeholder, decided_by, reversible, tags),
        )
        decision_id = row[0]["id"] if row else None

        if self._convex.available:
            self._convex.mutation("compoundDecisions:record", {
                "title": title, "description": description, "reasoning": reasoning,
                "alternatives": alternatives, "project": project or "",
                "stakeholder": stakeholder or "", "decidedBy": decided_by,
                "reversible": reversible, "tags": tags,
            })

        if decision_id is None and not self._convex.available:
            self._fallback_write("decision", {"title": title, "description": description, "reasoning": reasoning})

        return decision_id

    # ------------------------------------------------------------------
    # Record Model Performance
    # ------------------------------------------------------------------

    def record_model_performance(
        self,
        model: str,
        task_type: str,
        *,
        completion_time_ms: int = 0,
        tokens_in: int = 0,
        tokens_out: int = 0,
        cost_usd: float = 0.0,
        quality_score: Optional[float] = None,
        success: bool = True,
        project: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[int]:
        """Track model performance for routing optimization."""
        row = self._execute(
            """
            INSERT INTO compound_model_performance
                (model, task_type, completion_time_ms, tokens_in, tokens_out,
                 cost_usd, quality_score, success, project, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (model, task_type, completion_time_ms, tokens_in, tokens_out,
             cost_usd, quality_score, success, project, notes),
        )

        if self._convex.available:
            self._convex.mutation("compoundModelPerformance:record", {
                "model": model, "taskType": task_type,
                "completionTimeMs": completion_time_ms,
                "tokensIn": tokens_in, "tokensOut": tokens_out,
                "costUsd": cost_usd, "qualityScore": quality_score or 0,
                "success": success, "project": project or "", "notes": notes or "",
            })

        return row[0]["id"] if row else None

    # ------------------------------------------------------------------
    # Record Feedback
    # ------------------------------------------------------------------

    def record_feedback(
        self,
        session_key: str,
        agent_action: str,
        human_correction: str,
        *,
        category: str = "general",
        severity: str = "important",
    ) -> Optional[int]:
        """Log human feedback/correction."""
        row = self._execute(
            """
            INSERT INTO compound_feedback_loop
                (session_key, agent_action, human_correction, category, severity)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (session_key, agent_action, human_correction, category, severity),
        )

        if self._convex.available:
            self._convex.mutation("compoundFeedback:record", {
                "sessionKey": session_key, "agentAction": agent_action,
                "humanCorrection": human_correction, "category": category,
                "severity": severity,
            })

        return row[0]["id"] if row else None

    # ------------------------------------------------------------------
    # Record Pattern
    # ------------------------------------------------------------------

    def record_pattern(
        self,
        name: str,
        description: str,
        recommendation: str,
        *,
        category: str = "general",
        auto_apply: bool = False,
        learning_ids: Optional[List[int]] = None,
    ) -> Optional[int]:
        """Log a detected pattern."""
        learning_ids = learning_ids or []

        # Upsert: increment occurrences if pattern name exists
        row = self._execute(
            """
            INSERT INTO compound_patterns
                (name, description, recommendation, category, auto_apply, learning_ids)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET
                occurrences = compound_patterns.occurrences + 1,
                description = EXCLUDED.description,
                recommendation = EXCLUDED.recommendation,
                learning_ids = compound_patterns.learning_ids || EXCLUDED.learning_ids
            RETURNING id
            """,
            (name, description, recommendation, category, auto_apply, learning_ids),
        )

        if self._convex.available:
            self._convex.mutation("compoundPatterns:record", {
                "name": name, "description": description,
                "recommendation": recommendation, "category": category,
                "autoApply": auto_apply, "learningIds": learning_ids,
            })

        return row[0]["id"] if row else None

    # ------------------------------------------------------------------
    # Search & Query
    # ------------------------------------------------------------------

    def search_learnings(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        project: Optional[str] = None,
        impact: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict]:
        """Search learnings by text, category, project, or impact."""
        conditions = []
        params: list = []

        if query:
            conditions.append("search_vector @@ plainto_tsquery('english', %s)")
            params.append(query)
        if category:
            conditions.append("category = %s")
            params.append(category)
        if project:
            conditions.append("project = %s")
            params.append(project)
        if impact:
            conditions.append("impact = %s")
            params.append(impact)

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"""
            SELECT id, category, subcategory, title, content, project, impact, tags,
                   confidence, agent, model, trigger, created_at
            FROM compound_learnings
            {where}
            ORDER BY created_at DESC
            LIMIT %s
        """
        params.append(limit)
        rows = self._execute(sql, tuple(params))
        return rows or []

    def get_best_model(self, task_type: str) -> Optional[Dict]:
        """Get the best performing model for a task type based on recorded metrics."""
        rows = self._execute(
            """
            SELECT
                model,
                COUNT(*) as total_tasks,
                AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as success_rate,
                AVG(quality_score) FILTER (WHERE quality_score IS NOT NULL) as avg_quality,
                AVG(completion_time_ms) as avg_time_ms,
                AVG(cost_usd) as avg_cost,
                SUM(tokens_in + tokens_out) as total_tokens
            FROM compound_model_performance
            WHERE task_type = %s AND created_at > NOW() - INTERVAL '30 days'
            GROUP BY model
            HAVING COUNT(*) >= 3
            ORDER BY
                AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) DESC,
                AVG(quality_score) FILTER (WHERE quality_score IS NOT NULL) DESC NULLS LAST,
                AVG(cost_usd) ASC
            LIMIT 5
            """,
            (task_type,),
        )
        if not rows:
            return None
        return {
            "recommended": rows[0]["model"],
            "candidates": rows,
        }

    def get_daily_metrics(self, target_date: Optional[date] = None) -> Optional[Dict]:
        """Get compound metrics for a date."""
        target_date = target_date or date.today()
        rows = self._execute(
            "SELECT * FROM compound_daily_metrics WHERE date = %s",
            (target_date,),
        )
        return rows[0] if rows else None

    def update_daily_metrics(self, target_date: Optional[date] = None) -> Optional[Dict]:
        """Recalculate and store today's compound metrics."""
        target_date = target_date or date.today()

        # Gather stats
        stats = {}
        for name, sql in [
            ("learnings", "SELECT COUNT(*) as n FROM compound_learnings WHERE created_at::date = %s"),
            ("decisions", "SELECT COUNT(*) as n FROM compound_decisions WHERE created_at::date = %s"),
            ("tasks", "SELECT COUNT(*) as n FROM compound_model_performance WHERE created_at::date = %s"),
            ("feedback", "SELECT COUNT(*) as n FROM compound_feedback_loop WHERE created_at::date = %s"),
            ("patterns", "SELECT COUNT(*) as n FROM compound_patterns WHERE created_at::date = %s"),
        ]:
            rows = self._execute(sql, (target_date,))
            stats[name] = rows[0]["n"] if rows else 0

        # Aggregates from model performance
        perf = self._execute(
            """
            SELECT
                AVG(quality_score) FILTER (WHERE quality_score IS NOT NULL) as avg_q,
                SUM(cost_usd) as total_cost,
                SUM(tokens_in + tokens_out) as total_tokens
            FROM compound_model_performance
            WHERE created_at::date = %s
            """,
            (target_date,),
        )
        perf_row = perf[0] if perf else {}

        # Top model
        top_model_rows = self._execute(
            """
            SELECT model, COUNT(*) as n FROM compound_model_performance
            WHERE created_at::date = %s GROUP BY model ORDER BY n DESC LIMIT 1
            """,
            (target_date,),
        )
        top_model = top_model_rows[0]["model"] if top_model_rows else None

        # Top task type
        top_task_rows = self._execute(
            """
            SELECT task_type, COUNT(*) as n FROM compound_model_performance
            WHERE created_at::date = %s GROUP BY task_type ORDER BY n DESC LIMIT 1
            """,
            (target_date,),
        )
        top_task = top_task_rows[0]["task_type"] if top_task_rows else None

        # Category breakdown
        cat_rows = self._execute(
            """
            SELECT category, COUNT(*) as n FROM compound_learnings
            WHERE created_at::date = %s GROUP BY category
            """,
            (target_date,),
        )
        cats = {r["category"]: r["n"] for r in (cat_rows or [])}

        # Models used
        model_rows = self._execute(
            """
            SELECT model, COUNT(*) as n FROM compound_model_performance
            WHERE created_at::date = %s GROUP BY model
            """,
            (target_date,),
        )
        models = {r["model"]: r["n"] for r in (model_rows or [])}

        # Upsert
        row = self._execute(
            """
            INSERT INTO compound_daily_metrics
                (date, total_learnings, total_decisions, total_tasks, total_feedback,
                 patterns_detected, avg_quality_score, total_cost_usd, total_tokens,
                 top_model, top_task_type, learnings_by_category, models_used)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (date) DO UPDATE SET
                total_learnings = EXCLUDED.total_learnings,
                total_decisions = EXCLUDED.total_decisions,
                total_tasks = EXCLUDED.total_tasks,
                total_feedback = EXCLUDED.total_feedback,
                patterns_detected = EXCLUDED.patterns_detected,
                avg_quality_score = EXCLUDED.avg_quality_score,
                total_cost_usd = EXCLUDED.total_cost_usd,
                total_tokens = EXCLUDED.total_tokens,
                top_model = EXCLUDED.top_model,
                top_task_type = EXCLUDED.top_task_type,
                learnings_by_category = EXCLUDED.learnings_by_category,
                models_used = EXCLUDED.models_used,
                updated_at = NOW()
            RETURNING *
            """,
            (target_date, stats["learnings"], stats["decisions"], stats["tasks"],
             stats["feedback"], stats["patterns"],
             perf_row.get("avg_q"), perf_row.get("total_cost") or 0,
             perf_row.get("total_tokens") or 0,
             top_model, top_task, json.dumps(cats), json.dumps(models)),
        )
        return row[0] if row else None

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def close(self):
        """Close connections."""
        if self._pg_conn and not self._pg_conn.closed:
            self._pg_conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
