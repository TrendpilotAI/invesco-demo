#!/usr/bin/env python3
"""
Compound Learning CLI — Record learnings, search, query metrics.

Usage:
    python3 cli.py learn --category model_selection --title "GPT 5.4 bad" --content "..." --impact high
    python3 cli.py decide --title "Use Sonnet" --description "..." --reasoning "..."
    python3 cli.py model-perf --model sonnet --task-type coding --success --time-ms 12000
    python3 cli.py feedback --session abc --action "Used GPT 5.4" --correction "Should have used Sonnet"
    python3 cli.py search "sql injection"
    python3 cli.py best-model coding
    python3 cli.py metrics [--date 2026-03-10]
    python3 cli.py update-metrics
    python3 cli.py consolidate
"""

import argparse
import json
import sys
import os
from datetime import date, datetime

# Allow running from the script directory or as a module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compound_learning.client import CompoundLearningClient
from compound_learning.hooks import on_cron_consolidate


def cmd_learn(args):
    with CompoundLearningClient() as cl:
        tags = args.tags.split(",") if args.tags else []
        lid = cl.record_learning(
            category=args.category,
            title=args.title,
            content=args.content,
            impact=args.impact,
            project=args.project,
            subcategory=args.subcategory,
            agent=args.agent,
            model=args.model,
            trigger=args.trigger or "cli",
            confidence=args.confidence,
            tags=tags,
        )
        if lid:
            print(f"✅ Learning #{lid} recorded [{args.impact}] — {args.title}")
        else:
            print("⚠️  Learning recorded to fallback (DB unavailable)")


def cmd_decide(args):
    with CompoundLearningClient() as cl:
        alts = args.alternatives.split("|") if args.alternatives else []
        tags = args.tags.split(",") if args.tags else []
        did = cl.record_decision(
            title=args.title,
            description=args.description,
            reasoning=args.reasoning,
            alternatives=alts,
            project=args.project,
            stakeholder=args.stakeholder,
            decided_by=args.decided_by,
            reversible=not args.irreversible,
            tags=tags,
        )
        if did:
            print(f"✅ Decision #{did} logged — {args.title}")
        else:
            print("⚠️  Decision logged to fallback")


def cmd_model_perf(args):
    with CompoundLearningClient() as cl:
        pid = cl.record_model_performance(
            model=args.model,
            task_type=args.task_type,
            completion_time_ms=args.time_ms,
            tokens_in=args.tokens_in,
            tokens_out=args.tokens_out,
            cost_usd=args.cost,
            quality_score=args.quality,
            success=args.success,
            project=args.project,
            notes=args.notes,
        )
        status = "✅" if args.success else "❌"
        print(f"{status} Model perf #{pid} — {args.model} on {args.task_type}")


def cmd_feedback(args):
    with CompoundLearningClient() as cl:
        fid = cl.record_feedback(
            session_key=args.session,
            agent_action=args.action,
            human_correction=args.correction,
            severity=args.severity,
        )
        print(f"✅ Feedback #{fid} recorded [{args.severity}]")


def cmd_search(args):
    with CompoundLearningClient() as cl:
        results = cl.search_learnings(
            query=args.query,
            category=args.category,
            project=args.project,
            impact=args.impact,
            limit=args.limit,
        )
        if not results:
            print("No learnings found.")
            return
        print(f"Found {len(results)} learnings:\n")
        for r in results:
            tags_str = " ".join(f"[{t}]" for t in (r.get("tags") or []))
            print(f"  #{r['id']} [{r['impact'].upper()}] {r['category']}")
            print(f"    {r['title']}")
            print(f"    {r['content'][:120]}...")
            if r.get("project"):
                print(f"    project: {r['project']}")
            if tags_str:
                print(f"    tags: {tags_str}")
            print(f"    {r['created_at']}")
            print()


def cmd_best_model(args):
    with CompoundLearningClient() as cl:
        result = cl.get_best_model(args.task_type)
        if not result:
            print(f"No model data for task type '{args.task_type}' (need 3+ records in 30 days)")
            return
        print(f"🏆 Best model for '{args.task_type}': {result['recommended']}\n")
        print(f"{'Model':<30} {'Tasks':>6} {'Success':>8} {'Quality':>8} {'Avg ms':>8} {'Avg $':>8}")
        print("-" * 76)
        for c in result["candidates"]:
            q = f"{c['avg_quality']:.2f}" if c.get("avg_quality") else "N/A"
            print(
                f"{c['model']:<30} {c['total_tasks']:>6} "
                f"{c['success_rate']:>7.0%} {q:>8} "
                f"{c['avg_time_ms']:>7.0f} {float(c['avg_cost']):>7.4f}"
            )


def cmd_metrics(args):
    with CompoundLearningClient() as cl:
        target = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
        m = cl.get_daily_metrics(target)
        if not m:
            print(f"No metrics for {target}. Run 'update-metrics' first.")
            return
        print(f"📊 Compound Metrics for {target}")
        print(f"  Learnings:  {m['total_learnings']}")
        print(f"  Decisions:  {m['total_decisions']}")
        print(f"  Tasks:      {m['total_tasks']}")
        print(f"  Feedback:   {m['total_feedback']}")
        print(f"  Patterns:   {m['patterns_detected']}")
        print(f"  Avg Quality:{m['avg_quality_score'] or 'N/A'}")
        print(f"  Total Cost: ${float(m['total_cost_usd']):.4f}")
        print(f"  Tokens:     {m['total_tokens']:,}")
        print(f"  Top Model:  {m['top_model'] or 'N/A'}")
        print(f"  Top Task:   {m['top_task_type'] or 'N/A'}")
        cats = m.get("learnings_by_category")
        if cats and isinstance(cats, dict) and cats:
            print(f"  Categories: {cats}")


def cmd_update_metrics(args):
    with CompoundLearningClient() as cl:
        m = cl.update_daily_metrics()
        if m:
            print(f"✅ Metrics updated for {m['date']}: {m['total_learnings']} learnings, {m['total_tasks']} tasks")
        else:
            print("⚠️  Failed to update metrics")


def cmd_consolidate(args):
    print("🔄 Running consolidation...")
    on_cron_consolidate()
    print("✅ Consolidation complete")


def main():
    parser = argparse.ArgumentParser(description="Compound Learning CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # learn
    p = sub.add_parser("learn", help="Record a learning")
    p.add_argument("--category", "-c", required=True)
    p.add_argument("--title", "-t", required=True)
    p.add_argument("--content", required=True)
    p.add_argument("--impact", default="medium", choices=["low", "medium", "high", "critical"])
    p.add_argument("--project", "-p")
    p.add_argument("--subcategory")
    p.add_argument("--agent", default="honey")
    p.add_argument("--model", default="unknown")
    p.add_argument("--trigger", default="cli")
    p.add_argument("--confidence", type=float, default=0.8)
    p.add_argument("--tags", help="Comma-separated tags")

    # decide
    p = sub.add_parser("decide", help="Log a decision")
    p.add_argument("--title", "-t", required=True)
    p.add_argument("--description", "-d", required=True)
    p.add_argument("--reasoning", "-r", required=True)
    p.add_argument("--alternatives", help="Pipe-separated alternatives")
    p.add_argument("--project", "-p")
    p.add_argument("--stakeholder")
    p.add_argument("--decided-by", default="honey")
    p.add_argument("--irreversible", action="store_true")
    p.add_argument("--tags", help="Comma-separated tags")

    # model-perf
    p = sub.add_parser("model-perf", help="Record model performance")
    p.add_argument("--model", "-m", required=True)
    p.add_argument("--task-type", required=True)
    p.add_argument("--time-ms", type=int, default=0)
    p.add_argument("--tokens-in", type=int, default=0)
    p.add_argument("--tokens-out", type=int, default=0)
    p.add_argument("--cost", type=float, default=0.0)
    p.add_argument("--quality", type=float)
    p.add_argument("--success", action="store_true", default=True)
    p.add_argument("--failure", dest="success", action="store_false")
    p.add_argument("--project", "-p")
    p.add_argument("--notes")

    # feedback
    p = sub.add_parser("feedback", help="Log human feedback")
    p.add_argument("--session", "-s", required=True)
    p.add_argument("--action", "-a", required=True)
    p.add_argument("--correction", "-c", required=True)
    p.add_argument("--severity", default="important", choices=["minor", "important", "critical"])

    # search
    p = sub.add_parser("search", help="Search learnings")
    p.add_argument("query", nargs="?")
    p.add_argument("--category", "-c")
    p.add_argument("--project", "-p")
    p.add_argument("--impact")
    p.add_argument("--limit", "-n", type=int, default=20)

    # best-model
    p = sub.add_parser("best-model", help="Get best model for a task type")
    p.add_argument("task_type")

    # metrics
    p = sub.add_parser("metrics", help="Show daily metrics")
    p.add_argument("--date", help="YYYY-MM-DD (default: today)")

    # update-metrics
    sub.add_parser("update-metrics", help="Recalculate today's metrics")

    # consolidate
    sub.add_parser("consolidate", help="Run hourly consolidation (detect patterns, update metrics)")

    args = parser.parse_args()
    cmd_map = {
        "learn": cmd_learn,
        "decide": cmd_decide,
        "model-perf": cmd_model_perf,
        "feedback": cmd_feedback,
        "search": cmd_search,
        "best-model": cmd_best_model,
        "metrics": cmd_metrics,
        "update-metrics": cmd_update_metrics,
        "consolidate": cmd_consolidate,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
