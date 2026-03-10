"""
Bragi Scheduler — Content scheduling engine.
Maps approved posts to optimal time slots and publishes via Blotato.
"""

import json
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

from content_rules import POSTING_SCHEDULE, ACCOUNTS
from blotato_client import BlotatoClient


class ContentScheduler:
    def __init__(self, client: Optional[BlotatoClient] = None):
        self.client = client or BlotatoClient()
        self.schedule = POSTING_SCHEDULE
        self._used_slots: dict[str, set[str]] = {}  # platform -> set of ISO times

    def get_next_slot(self, platform: str, after: Optional[datetime] = None) -> datetime:
        """Get the next available posting time for a platform.

        Args:
            platform: Platform key (twitter, threads, linkedin, tiktok).
            after: Find slots after this time. Defaults to now.

        Returns:
            datetime in the platform's timezone.
        """
        config = self.schedule.get(platform)
        if not config:
            raise ValueError(f"No schedule for platform: {platform}")

        tz = ZoneInfo(config["timezone"])
        now = after or datetime.now(tz)
        if now.tzinfo is None:
            now = now.replace(tzinfo=tz)
        else:
            now = now.astimezone(tz)

        used = self._used_slots.get(platform, set())

        # Check today's remaining slots, then tomorrow's
        for day_offset in range(0, 7):
            check_date = now.date() + timedelta(days=day_offset)
            for time_str in config["times"]:
                hour, minute = map(int, time_str.split(":"))
                slot = datetime(
                    check_date.year, check_date.month, check_date.day,
                    hour, minute, 0, tzinfo=tz,
                )
                if slot > now and slot.isoformat() not in used:
                    return slot

        # Fallback: next week's first slot
        next_week = now + timedelta(days=7)
        first_time = config["times"][0]
        h, m = map(int, first_time.split(":"))
        return datetime(
            next_week.year, next_week.month, next_week.day,
            h, m, 0, tzinfo=tz,
        )

    def schedule_approved_posts(self, approved_posts: list[dict]) -> list[dict]:
        """Take approved posts and schedule them via Blotato.

        Args:
            approved_posts: List of post dicts with status='approved'.

        Returns:
            List of results with scheduling info.
        """
        results = []

        for post in approved_posts:
            if post.get("status") != "approved":
                results.append({**post, "schedule_error": "Post not approved"})
                continue

            platform = post.get("platform", "twitter")
            account_id = post.get("account_id")

            if not account_id:
                account = ACCOUNTS.get(platform)
                if account:
                    account_id = account["id"]
                else:
                    results.append({**post, "schedule_error": f"No account for {platform}"})
                    continue

            try:
                # Get next available slot
                slot = self.get_next_slot(platform)
                slot_iso = slot.isoformat()

                # Mark slot as used
                if platform not in self._used_slots:
                    self._used_slots[platform] = set()
                self._used_slots[platform].add(slot_iso)

                # Schedule via Blotato
                result = self.client.create_post(
                    account_ids=[str(account_id)],
                    text=post["text"],
                    scheduled_time=slot_iso,
                    use_next_free_slot=False,
                )

                results.append({
                    **post,
                    "status": "scheduled",
                    "scheduled_time": slot_iso,
                    "blotato_response": result,
                })

            except Exception as e:
                results.append({
                    **post,
                    "status": "schedule_error",
                    "schedule_error": str(e),
                })

        return results

    def schedule_with_next_free_slot(self, approved_posts: list[dict]) -> list[dict]:
        """Schedule using Blotato's useNextFreeSlot feature (simpler)."""
        results = []

        for post in approved_posts:
            if post.get("status") != "approved":
                continue

            account_id = post.get("account_id")
            if not account_id:
                continue

            try:
                result = self.client.create_post(
                    account_ids=[str(account_id)],
                    text=post["text"],
                    use_next_free_slot=True,
                )
                results.append({
                    **post,
                    "status": "scheduled",
                    "blotato_response": result,
                })
            except Exception as e:
                results.append({
                    **post,
                    "status": "schedule_error",
                    "schedule_error": str(e),
                })

        return results


def load_drafts(path: str = "drafts.json") -> list[dict]:
    """Load drafts from JSON file."""
    with open(path) as f:
        data = json.load(f)
    return data.get("drafts", [])


def save_drafts(drafts: list[dict], path: str = "drafts.json"):
    """Save drafts back to JSON file."""
    from datetime import timezone
    with open(path, "w") as f:
        json.dump({
            "drafts": drafts,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2)
