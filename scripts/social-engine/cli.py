#!/usr/bin/env python3
"""
Bragi CLI — Content management command line interface.

Usage:
    python3 cli.py generate --topics "topic1,topic2,topic3"
    python3 cli.py generate --persona enterprise --topic "single topic"
    python3 cli.py drafts
    python3 cli.py approve --id <draft_id>
    python3 cli.py approve --all
    python3 cli.py reject --id <draft_id>
    python3 cli.py schedule
    python3 cli.py accounts
    python3 cli.py pipeline --topics "topic1,topic2"
"""

import argparse
import json
import sys
import os

# Ensure we can import sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content_generator import ContentGenerator, save_drafts
from blotato_client import BlotatoClient
from scheduler import ContentScheduler, load_drafts
from content_rules import PERSONAS

DRAFTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drafts.json")


def cmd_generate(args):
    """Generate content."""
    gen = ContentGenerator()

    if args.persona and args.topic:
        # Single post
        post = gen.generate_post(topic=args.topic, persona=args.persona)
        drafts = [post]
    elif args.topics:
        # Daily batch with specific topics
        topics = [t.strip() for t in args.topics.split(",")]
        drafts = gen.generate_daily_batch(topics=topics)
    else:
        # Default daily batch
        drafts = gen.generate_daily_batch()

    # Merge with existing drafts
    existing = []
    if os.path.exists(DRAFTS_FILE):
        try:
            with open(DRAFTS_FILE) as f:
                existing = json.load(f).get("drafts", [])
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    all_drafts = existing + drafts
    save_drafts(all_drafts, DRAFTS_FILE)

    print(f"\n🎯 Generated {len(drafts)} new posts:")
    for d in drafts:
        status = "⚠️" if d.get("violations") else "✅"
        print(f"  {status} [{d.get('persona_label', d.get('persona', '?'))}] {d.get('platform', '?')}")
        text = d.get("text", d.get("error", "?"))
        print(f"     {text[:120]}{'...' if len(text) > 120 else ''}")
    print(f"\nTotal drafts: {len(all_drafts)}")


def cmd_drafts(args):
    """List pending drafts."""
    if not os.path.exists(DRAFTS_FILE):
        print("No drafts found. Run 'generate' first.")
        return

    drafts = load_drafts(DRAFTS_FILE)
    if not drafts:
        print("No drafts found.")
        return

    status_filter = args.status if hasattr(args, "status") and args.status else None

    print(f"\n📋 Drafts ({len(drafts)} total):\n")
    for i, d in enumerate(drafts):
        if status_filter and d.get("status") != status_filter:
            continue
        status_icon = {"draft": "📝", "approved": "✅", "rejected": "❌", "scheduled": "📅"}.get(
            d.get("status", "draft"), "❓"
        )
        print(f"  {status_icon} [{d.get('id', i)}] {d.get('persona_label', '?')} → {d.get('platform', '?')}")
        text = d.get("text", "")
        print(f"     {text[:150]}{'...' if len(text) > 150 else ''}")
        if d.get("violations"):
            print(f"     ⚠️  {d['violations']}")
        print()


def cmd_approve(args):
    """Approve drafts."""
    drafts = load_drafts(DRAFTS_FILE)

    if args.all:
        count = 0
        for d in drafts:
            if d.get("status") == "draft":
                d["status"] = "approved"
                count += 1
        print(f"✅ Approved {count} drafts")
    elif args.id:
        found = False
        for d in drafts:
            if d.get("id") == args.id:
                d["status"] = "approved"
                found = True
                print(f"✅ Approved: {d.get('text', '')[:80]}")
                break
        if not found:
            print(f"❌ Draft not found: {args.id}")
            return
    else:
        print("Specify --id <draft_id> or --all")
        return

    save_drafts(drafts, DRAFTS_FILE)


def cmd_reject(args):
    """Reject a draft."""
    drafts = load_drafts(DRAFTS_FILE)

    found = False
    for d in drafts:
        if d.get("id") == args.id:
            d["status"] = "rejected"
            found = True
            print(f"❌ Rejected: {d.get('text', '')[:80]}")
            break

    if not found:
        print(f"Draft not found: {args.id}")
        return

    save_drafts(drafts, DRAFTS_FILE)


def cmd_schedule(args):
    """Schedule approved posts via Blotato."""
    drafts = load_drafts(DRAFTS_FILE)
    approved = [d for d in drafts if d.get("status") == "approved"]

    if not approved:
        print("No approved posts to schedule. Run 'approve' first.")
        return

    scheduler = ContentScheduler()

    if args.next_slot:
        results = scheduler.schedule_with_next_free_slot(approved)
    else:
        results = scheduler.schedule_approved_posts(approved)

    # Update drafts with results
    result_map = {r["id"]: r for r in results if "id" in r}
    for d in drafts:
        if d.get("id") in result_map:
            d.update(result_map[d["id"]])

    save_drafts(drafts, DRAFTS_FILE)

    scheduled = [r for r in results if r.get("status") == "scheduled"]
    errors = [r for r in results if r.get("schedule_error")]

    print(f"\n📅 Scheduled {len(scheduled)} posts")
    for s in scheduled:
        t = s.get("scheduled_time", "next free slot")
        print(f"  ✅ [{s.get('persona_label', '?')}] {s.get('platform', '?')} → {t}")

    if errors:
        print(f"\n⚠️  {len(errors)} errors:")
        for e in errors:
            print(f"  ❌ [{e.get('persona_label', '?')}] {e.get('schedule_error', '?')}")


def cmd_accounts(args):
    """List connected Blotato accounts."""
    client = BlotatoClient()
    accounts = client.list_accounts()
    print(f"\n📱 Connected accounts ({len(accounts)}):\n")
    for acc in accounts:
        if isinstance(acc, dict):
            name = acc.get("name", acc.get("username", "?"))
            platform = acc.get("platform", acc.get("type", "?"))
            aid = acc.get("id", "?")
            print(f"  • {platform}: {name} (id: {aid})")
        else:
            print(f"  • {acc}")


def cmd_pipeline(args):
    """Full pipeline: generate → show → approve all → schedule."""
    print("🚀 Running full content pipeline...\n")

    # Step 1: Generate
    gen_args = argparse.Namespace(topics=args.topics, persona=None, topic=None)
    cmd_generate(gen_args)

    # Step 2: Show drafts
    print("\n" + "=" * 60)
    cmd_drafts(argparse.Namespace(status=None))

    # Step 3: Info about approval
    print("=" * 60)
    print("\n📋 Next steps:")
    print("  1. Open the approval dashboard: approval_dashboard.html")
    print("  2. Or approve via CLI: python3 cli.py approve --all")
    print("  3. Then schedule: python3 cli.py schedule")


def cmd_clear(args):
    """Clear all drafts."""
    save_drafts([], DRAFTS_FILE)
    print("🗑️  Cleared all drafts")


def main():
    parser = argparse.ArgumentParser(
        description="Bragi — Social Content Engine CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # generate
    gen_parser = subparsers.add_parser("generate", help="Generate content")
    gen_parser.add_argument("--topics", help="Comma-separated topics")
    gen_parser.add_argument("--topic", help="Single topic")
    gen_parser.add_argument("--persona", choices=list(PERSONAS.keys()), help="Specific persona")

    # drafts
    drafts_parser = subparsers.add_parser("drafts", help="List drafts")
    drafts_parser.add_argument("--status", choices=["draft", "approved", "rejected", "scheduled"])

    # approve
    approve_parser = subparsers.add_parser("approve", help="Approve drafts")
    approve_parser.add_argument("--id", help="Draft ID to approve")
    approve_parser.add_argument("--all", action="store_true", help="Approve all drafts")

    # reject
    reject_parser = subparsers.add_parser("reject", help="Reject a draft")
    reject_parser.add_argument("--id", required=True, help="Draft ID to reject")

    # schedule
    sched_parser = subparsers.add_parser("schedule", help="Schedule approved posts")
    sched_parser.add_argument("--next-slot", action="store_true", help="Use Blotato's next free slot")

    # accounts
    subparsers.add_parser("accounts", help="List connected accounts")

    # pipeline
    pipe_parser = subparsers.add_parser("pipeline", help="Full generate → approve → schedule pipeline")
    pipe_parser.add_argument("--topics", help="Comma-separated topics")

    # clear
    subparsers.add_parser("clear", help="Clear all drafts")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "generate": cmd_generate,
        "drafts": cmd_drafts,
        "approve": cmd_approve,
        "reject": cmd_reject,
        "schedule": cmd_schedule,
        "accounts": cmd_accounts,
        "pipeline": cmd_pipeline,
        "clear": cmd_clear,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
