#!/usr/bin/env python3
"""
Seed the compound learning database with learnings from MEMORY.md.

Usage:
    python3 seed.py              # Seed all
    python3 seed.py --dry-run    # Preview without writing
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compound_learning.client import CompoundLearningClient

# ============================================================
# Seed data — extracted from MEMORY.md and operational history
# ============================================================

SEED_LEARNINGS = [
    # 1
    {
        "category": "model_selection",
        "title": "GPT 5.4 not suited for long coding subagent tasks",
        "content": "GPT 5.4 completes in 1-6 seconds, barely writes code. Fast but shallow — unsuitable for complex coding subagent work that needs deep reasoning and large code output.",
        "impact": "high",
        "project": None,
        "tags": ["model_routing", "coding", "gpt5"],
    },
    # 2
    {
        "category": "architecture",
        "title": "Apex should be thin API client, not reimplemented logic",
        "content": "ForwardLane's Apex layer should be a thin client wrapping the Django backend API, not reimplementing business logic. Duplication creates drift and bugs. Single source of truth in Django.",
        "impact": "high",
        "project": "signal-studio",
        "tags": ["architecture", "forwardlane", "apex", "django"],
    },
    # 3
    {
        "category": "client_insight",
        "title": "Craig Lieb rejected chat interfaces for Invesco",
        "content": "Craig Lieb (Invesco) explicitly said NO to chat interfaces and complex dashboards. Wants: Salesforce-embedded 'easy buttons', meeting prep briefs, mobile-first. Brian Kiley is the key user. 2-3 week demo window.",
        "impact": "critical",
        "project": "invesco-demo",
        "tags": ["client", "invesco", "craig_lieb", "ux", "salesforce"],
    },
    # 4
    {
        "category": "model_selection",
        "title": "DeepSeek handles git-sync at 1/10th Claude cost",
        "content": "DeepSeek can handle routine git-sync and simple automation tasks at roughly 1/10th the cost of Claude. Good for low-complexity, high-volume tasks. Route accordingly.",
        "impact": "high",
        "project": None,
        "tags": ["model_routing", "cost_optimization", "deepseek"],
    },
    # 5
    {
        "category": "security",
        "title": "NEXT_PUBLIC_SKIP_AUTH=true was in production",
        "content": "Discovered NEXT_PUBLIC_SKIP_AUTH=true deployed to production in Signal Studio. Authentication was completely bypassed. Critical security incident — always audit env vars before deploy, never trust SKIP_AUTH flags.",
        "impact": "critical",
        "project": "signal-studio",
        "tags": ["security", "auth", "production_incident", "env_vars"],
    },
    # 6
    {
        "category": "security",
        "title": "SQLAlchemy parameterization prevents SQL injection",
        "content": "Always use SQLAlchemy parameterized queries, never string interpolation for SQL. The NL→SQL engine must validate and parameterize all generated SQL before execution. $0.01/query cost makes this non-negotiable.",
        "impact": "critical",
        "project": "signal-studio",
        "tags": ["security", "sql_injection", "sqlalchemy", "nl2sql"],
    },
    # 7
    {
        "category": "process",
        "title": "Quality over quantity — 350+ TODOs, zero CI pipelines",
        "content": "System was a mile wide and an inch deep. 350+ TODO files, zero CI pipelines, zero git hooks, agents pushing to main. Obsessively planning and barely closing loops. New principle: stop generating plans, start closing loops.",
        "impact": "critical",
        "project": None,
        "tags": ["process", "quality", "ci", "self_critique"],
    },
    # 8
    {
        "category": "architecture",
        "title": "CLI-first, MCP-never",
        "content": "Unless no CLI exists AND requires persistent state AND called >10x/session, always prefer CLI tools over MCP servers. MCP adds complexity, latency, and failure modes. CLI is simpler, more debuggable, more composable.",
        "impact": "high",
        "project": None,
        "tags": ["architecture", "tooling", "cli", "mcp", "principle"],
    },
    # 9
    {
        "category": "engineering",
        "title": "Compound Intelligence Architecture is core identity",
        "content": "Every task makes Honey smarter. Kimi K2.5 Swarms as judge agents, compound engineering docs/skills updated continuously, hourly cron consolidates learnings, daily cron re-scores projects. Ultimate north star: maximum concurrent tokens/sec × minimum cost × maximum uptime × perfect fault tolerance.",
        "impact": "critical",
        "project": None,
        "tags": ["architecture", "compound_learning", "north_star", "identity"],
    },
    # 10
    {
        "category": "engineering",
        "title": "NL→SQL engine works with full Invesco schema",
        "content": "Natural language to SQL engine tested and working with full Invesco schema: 200+ columns, 22 tables. Cost ~$0.01 per signal generation. This is the core IP of Signal Studio.",
        "impact": "high",
        "project": "signal-studio",
        "tags": ["nl2sql", "invesco", "core_ip"],
    },
    # 11
    {
        "category": "engineering",
        "title": "ForwardLane Django backend has 150 models, 2000+ PRs",
        "content": "The legacy ForwardLane Django backend is massive: 150 models, 2000+ PRs, Python 3.9, Django 3.2. Victor Presnyackiy is the active developer. 5 frontend generations over 10 years. 13 repos analyzed, 3 worth absorbing, 10 skip.",
        "impact": "medium",
        "project": "forwardlane",
        "tags": ["legacy", "django", "codebase_analysis"],
    },
    # 12
    {
        "category": "business",
        "title": "Ultrafone is a hidden consumer product at 75% completion",
        "content": "AI phone receptionist with real-time social engineering detection. Pipecat + Groq + Fish Audio + Deepgram stack. 75% complete. Market = everyone with a phone. Hidden gem in the portfolio.",
        "impact": "medium",
        "project": "ultrafone",
        "tags": ["product", "consumer", "ai_voice", "opportunity"],
    },
    # 13
    {
        "category": "infrastructure",
        "title": "Railway infrastructure: 39 services across 5 projects",
        "content": "As of Feb 2026: 39 Railway services across 5 projects. Temporal connected at temporal.railway.internal:7233. 50 subagent concurrency, 20 children/parent, 3 depth levels. 9 cron jobs with self-healing hooks. Ultrafone has redundant services flagged for cleanup.",
        "impact": "medium",
        "project": None,
        "tags": ["infrastructure", "railway", "inventory"],
    },
    # 14
    {
        "category": "process",
        "title": "Self-critique before shipping prevents overengineered theater",
        "content": "First draft of quality-check.sh was overengineered theater — checking for things that didn't matter while missing real issues. Rebuilt as single pragmatic script. Every failure must be a real issue, no false positives. Self-review catches what auto-review misses.",
        "impact": "high",
        "project": None,
        "tags": ["process", "quality", "self_critique", "shipping"],
    },
    # 15
    {
        "category": "engineering",
        "title": "Data Waterfall Pipeline: 7-provider lead enrichment",
        "content": "Built multi-provider enrichment for Signal Studio: Hunter → FindyMail → Icypeas → QuickEnrich → Forager → Wiza → LeadIQ. Two-tier caching (Redis + DB, 30-day TTL), short-circuit when fields filled, batch via Celery, full audit logging. Code complete, needs API keys.",
        "impact": "medium",
        "project": "signal-studio",
        "tags": ["enrichment", "data_waterfall", "lead_gen"],
    },
    # 16
    {
        "category": "model_selection",
        "title": "48 models across 8 providers in allowlist",
        "content": "Model allowlist expanded to 48 models across 8 providers: OpenAI, Anthropic, Google, Grok, Groq, MiniMax, Kimi, DeepSeek. Kimi K2.5 and MiniMax still blocked at gateway level (provider adapter missing).",
        "impact": "medium",
        "project": None,
        "tags": ["model_routing", "infrastructure", "providers"],
    },
    # 17
    {
        "category": "client_insight",
        "title": "Invesco is a $300K retention account",
        "content": "Invesco account worth $300K. Craig Lieb meeting Feb 17. Demo window 2-3 weeks. Brian Kiley (new hire) is key user. Must demonstrate value quickly with Salesforce-embedded tools, not chat interfaces.",
        "impact": "critical",
        "project": "invesco-demo",
        "tags": ["client", "invesco", "revenue", "retention"],
    },
    # 18
    {
        "category": "architecture",
        "title": "Nathan's vision: Private AI mesh network on Railway",
        "content": "Nathan wants a private AI mesh on Railway — multiple specialized AI agents as 'colleagues' on private networking (*.railway.internal). Honey + specialized agents collaborate, share work, specialize. Think AI team, not single assistant.",
        "impact": "high",
        "project": None,
        "tags": ["vision", "architecture", "mesh", "railway", "multi_agent"],
    },
    # 19
    {
        "category": "engineering",
        "title": "Signal Studio deployed: Next.js 15 + Django + dual Postgres",
        "content": "Signal Studio fully deployed on Railway in 2.5 hours: Next.js 15 frontend, Django backend with 150+ models, dual PostgreSQL (default + analytical), Redis, Celery Worker + Beat. The biggest overnight build.",
        "impact": "high",
        "project": "signal-studio",
        "tags": ["deployment", "railway", "milestone"],
    },
    # 20
    {
        "category": "process",
        "title": "Coverage ratchet: start at current, can only go up",
        "content": "Don't set arbitrary coverage targets (like 70% on day 1). Start at current coverage level and enforce it can only go up. Ratchet mechanism prevents regression while being realistic about starting points.",
        "impact": "medium",
        "project": None,
        "tags": ["process", "testing", "coverage", "principle"],
    },
]

SEED_DECISIONS = [
    {
        "title": "Established Honey identity",
        "description": "Named the AI assistant Honey — a proactive multi-hyphenate operator, not a chatbot.",
        "reasoning": "Nathan wanted an AI with personality, opinions, and operational capability across all business domains. The name reflects warmth + effectiveness.",
        "project": None,
        "decided_by": "nathan+honey",
        "tags": ["identity", "foundational"],
    },
    {
        "title": "CLI-first, MCP-never architecture",
        "description": "Default to CLI tools over MCP servers for all tool integrations.",
        "reasoning": "MCP adds complexity, latency, and failure modes. CLI is simpler, more debuggable, composable. Only use MCP if no CLI exists AND requires persistent state AND called >10x/session.",
        "project": None,
        "decided_by": "nathan+honey",
        "tags": ["architecture", "tooling", "principle"],
    },
    {
        "title": "Compound Learning Pipeline as core infrastructure",
        "description": "Build persistent learning system (Postgres + Convex) so every task makes Honey smarter.",
        "reasoning": "Without persistent learning, each session starts from scratch. Compound intelligence requires: recording learnings, detecting patterns, routing models based on performance data, and self-correcting from feedback.",
        "project": None,
        "decided_by": "nathan+honey",
        "tags": ["architecture", "compound_learning", "foundational"],
    },
]


def seed(dry_run: bool = False):
    """Seed the database with historical learnings and decisions."""
    if dry_run:
        print(f"🔍 DRY RUN — would seed {len(SEED_LEARNINGS)} learnings + {len(SEED_DECISIONS)} decisions\n")
        for i, l in enumerate(SEED_LEARNINGS, 1):
            print(f"  [{i}] [{l['impact'].upper()}] {l['category']}: {l['title']}")
        print()
        for i, d in enumerate(SEED_DECISIONS, 1):
            print(f"  [D{i}] {d['title']}")
        return

    cl = CompoundLearningClient()
    try:
        # Check if already seeded
        existing = cl.search_learnings(limit=1)
        if existing:
            print(f"⚠️  Database already has {len(existing)}+ learnings. Seeding anyway (idempotent by title check)...")
            existing_titles = {r["title"] for r in cl.search_learnings(limit=500)}
        else:
            existing_titles = set()

        learned = 0
        skipped = 0
        for item in SEED_LEARNINGS:
            if item["title"] in existing_titles:
                skipped += 1
                continue
            lid = cl.record_learning(
                category=item["category"],
                title=item["title"],
                content=item["content"],
                impact=item["impact"],
                project=item.get("project"),
                agent="honey",
                model="seed",
                trigger="seed",
                confidence=0.9,
                tags=item.get("tags", []),
            )
            if lid:
                print(f"  ✅ #{lid} [{item['impact']}] {item['title'][:60]}")
                learned += 1
            else:
                print(f"  ⚠️  fallback: {item['title'][:60]}")
                learned += 1

        decided = 0
        for item in SEED_DECISIONS:
            did = cl.record_decision(
                title=item["title"],
                description=item["description"],
                reasoning=item["reasoning"],
                project=item.get("project"),
                decided_by=item.get("decided_by", "honey"),
                tags=item.get("tags", []),
            )
            if did:
                print(f"  📋 Decision #{did}: {item['title'][:60]}")
                decided += 1

        # Update metrics
        cl.update_daily_metrics()

        print(f"\n🍯 Seed complete: {learned} learnings ({skipped} skipped), {decided} decisions")

    finally:
        cl.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed compound learning database")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()
    seed(dry_run=args.dry_run)
