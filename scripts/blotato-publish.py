#!/usr/bin/env python3
"""
Blotato Publishing Script — NarrativeReactor → Blotato Bridge

Usage:
    # List connected accounts
    python3 blotato-publish.py accounts

    # Publish immediately
    python3 blotato-publish.py post --platform twitter --text "Your post here"

    # Schedule for next free slot
    python3 blotato-publish.py post --platform linkedin --text "Your post" --next-slot

    # Schedule for specific time
    python3 blotato-publish.py post --platform twitter --text "Your post" --schedule "2026-03-04T14:00:00Z"

    # Post with media
    python3 blotato-publish.py post --platform linkedin --text "Check this out" --media "https://example.com/image.png"

    # Twitter thread
    python3 blotato-publish.py thread --text "First tweet" --replies "Second tweet" "Third tweet"

    # Cross-post to all connected platforms
    python3 blotato-publish.py crosspost --text "Your post" --next-slot

    # Check post status
    python3 blotato-publish.py status --id <postSubmissionId>
"""

import argparse
import json
import os
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_URL = "https://backend.blotato.com/v2"
API_KEY = os.environ.get("BLOTATO_API_KEY", "")

SUPPORTED_PLATFORMS = [
    "twitter", "linkedin", "facebook", "instagram",
    "pinterest", "tiktok", "threads", "bluesky", "youtube"
]


def api(method, path, data=None):
    """Make authenticated Blotato API call."""
    url = f"{BASE_URL}{path}"
    headers = {
        "blotato-api-key": API_KEY,
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        err = e.read().decode()
        print(f"❌ API error {e.code}: {err}", file=sys.stderr)
        sys.exit(1)


def cmd_accounts(args):
    """List connected social accounts."""
    result = api("GET", "/users/me/accounts")
    items = result.get("items", [])
    if not items:
        print("⚠️  No social accounts connected.")
        print("→  Go to https://my.blotato.com/settings to connect accounts.")
        return
    print(f"📱 {len(items)} connected account(s):\n")
    for acc in items:
        print(f"  {acc['platform']:12s}  @{acc.get('username', 'N/A'):20s}  id: {acc['id']}")


def get_account_id(platform):
    """Get account ID for a platform, or exit with helpful error."""
    result = api("GET", f"/users/me/accounts?platform={platform}")
    items = result.get("items", [])
    if not items:
        print(f"❌ No {platform} account connected. Go to https://my.blotato.com/settings")
        sys.exit(1)
    if len(items) > 1:
        print(f"Multiple {platform} accounts found:")
        for acc in items:
            print(f"  @{acc.get('username', 'N/A')}  id: {acc['id']}")
        print("Using first one.")
    return items[0]["id"]


def cmd_post(args):
    """Publish or schedule a single post."""
    account_id = args.account_id or get_account_id(args.platform)

    media_urls = []
    if args.media:
        media_urls = args.media if isinstance(args.media, list) else [args.media]

    payload = {
        "post": {
            "accountId": account_id,
            "content": {
                "text": args.text,
                "mediaUrls": media_urls,
                "platform": args.platform,
            },
            "target": {
                "targetType": args.platform,
            },
        }
    }

    # LinkedIn/Facebook page posting
    if args.page_id:
        payload["post"]["target"]["pageId"] = args.page_id

    # Scheduling
    if args.schedule:
        payload["scheduledTime"] = args.schedule
    elif args.next_slot:
        payload["useNextFreeSlot"] = True

    result = api("POST", "/posts", payload)
    sub_id = result.get("postSubmissionId", "unknown")
    print(f"✅ Post submitted to {args.platform}!")
    print(f"   Submission ID: {sub_id}")

    if not args.no_poll:
        print("   Polling status...")
        poll_status(sub_id)

    return sub_id


def cmd_thread(args):
    """Publish a Twitter/Threads/Bluesky thread."""
    platform = args.platform or "twitter"
    account_id = args.account_id or get_account_id(platform)

    additional = [{"text": r, "mediaUrls": []} for r in args.replies]

    payload = {
        "post": {
            "accountId": account_id,
            "content": {
                "text": args.text,
                "mediaUrls": [],
                "platform": platform,
                "additionalPosts": additional,
            },
            "target": {
                "targetType": platform,
            },
        }
    }

    if args.next_slot:
        payload["useNextFreeSlot"] = True
    elif args.schedule:
        payload["scheduledTime"] = args.schedule

    result = api("POST", "/posts", payload)
    sub_id = result.get("postSubmissionId", "unknown")
    print(f"✅ Thread ({1 + len(args.replies)} posts) submitted to {platform}!")
    print(f"   Submission ID: {sub_id}")

    if not args.no_poll:
        poll_status(sub_id)


def cmd_crosspost(args):
    """Post to all connected platforms."""
    result = api("GET", "/users/me/accounts")
    items = result.get("items", [])
    if not items:
        print("❌ No accounts connected.")
        sys.exit(1)

    print(f"📤 Cross-posting to {len(items)} platform(s)...\n")
    for acc in items:
        platform = acc["platform"]
        payload = {
            "post": {
                "accountId": acc["id"],
                "content": {
                    "text": args.text,
                    "mediaUrls": args.media or [],
                    "platform": platform,
                },
                "target": {
                    "targetType": platform,
                },
            }
        }
        if args.next_slot:
            payload["useNextFreeSlot"] = True

        try:
            result = api("POST", "/posts", payload)
            print(f"  ✅ {platform:12s} → submitted (id: {result.get('postSubmissionId', '?')})")
        except SystemExit:
            print(f"  ❌ {platform:12s} → failed")


def cmd_status(args):
    """Check post submission status."""
    poll_status(args.id, max_polls=1)


def poll_status(submission_id, max_polls=10):
    """Poll post status until published or failed."""
    for i in range(max_polls):
        result = api("GET", f"/posts/{submission_id}")
        status = result.get("status", "unknown")
        print(f"   Status: {status}")
        if status in ("published", "failed", "error"):
            if status != "published":
                print(f"   ⚠️  Details: {json.dumps(result, indent=2)}")
            return result
        if i < max_polls - 1:
            time.sleep(3)
    return result


def main():
    if not API_KEY:
        print("❌ BLOTATO_API_KEY not set. Export it first.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Blotato Publishing CLI")
    subs = parser.add_subparsers(dest="command", required=True)

    # accounts
    subs.add_parser("accounts", help="List connected accounts")

    # post
    p = subs.add_parser("post", help="Publish a single post")
    p.add_argument("--platform", required=True, choices=SUPPORTED_PLATFORMS)
    p.add_argument("--text", required=True)
    p.add_argument("--media", nargs="*", help="Media URLs")
    p.add_argument("--account-id", help="Override account ID")
    p.add_argument("--page-id", help="Page ID for LinkedIn/Facebook")
    p.add_argument("--schedule", help="ISO 8601 timestamp")
    p.add_argument("--next-slot", action="store_true")
    p.add_argument("--no-poll", action="store_true")

    # thread
    t = subs.add_parser("thread", help="Publish a thread")
    t.add_argument("--platform", choices=["twitter", "threads", "bluesky"], default="twitter")
    t.add_argument("--text", required=True, help="First post")
    t.add_argument("--replies", nargs="+", required=True, help="Reply posts")
    t.add_argument("--account-id", help="Override account ID")
    t.add_argument("--schedule", help="ISO 8601 timestamp")
    t.add_argument("--next-slot", action="store_true")
    t.add_argument("--no-poll", action="store_true")

    # crosspost
    c = subs.add_parser("crosspost", help="Post to all platforms")
    c.add_argument("--text", required=True)
    c.add_argument("--media", nargs="*")
    c.add_argument("--next-slot", action="store_true")

    # status
    s = subs.add_parser("status", help="Check post status")
    s.add_argument("--id", required=True, help="Post submission ID")

    args = parser.parse_args()

    commands = {
        "accounts": cmd_accounts,
        "post": cmd_post,
        "thread": cmd_thread,
        "crosspost": cmd_crosspost,
        "status": cmd_status,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
