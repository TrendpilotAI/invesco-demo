"""
Bragi Blotato Client — API wrapper for Blotato social media scheduling.
"""

import os
import json
import requests
from typing import Optional


class BlotatoClient:
    BASE_URL = "https://backend.blotato.com"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ["BLOTATO_API_KEY"]
        self.session = requests.Session()
        self.session.headers.update({
            "blotato-api-key": self.api_key,
            "Content-Type": "application/json",
        })

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """Make an authenticated request to the Blotato API."""
        url = f"{self.BASE_URL}{path}"
        resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        try:
            return resp.json()
        except (json.JSONDecodeError, ValueError):
            return {"status": resp.status_code, "text": resp.text}

    # ── Accounts ─────────────────────────────────────────────────────────────

    def list_accounts(self) -> list[dict]:
        """List all connected social media accounts."""
        data = self._request("GET", "/v2/users/me/accounts")
        # API returns { items: [...] }
        if isinstance(data, list):
            return data
        return data.get("items", data.get("accounts", data.get("data", [data])))

    # ── Posts ────────────────────────────────────────────────────────────────

    def create_post(
        self,
        account_ids: list[str],
        text: str,
        media_urls: Optional[list[str]] = None,
        scheduled_time: Optional[str] = None,
        use_next_free_slot: bool = True,
    ) -> dict:
        """Create or schedule a post.

        Args:
            account_ids: List of account ID strings.
            text: Post text content.
            media_urls: Optional list of media URLs to attach.
            scheduled_time: ISO 8601 datetime string for scheduling.
            use_next_free_slot: If True, auto-schedule to next available slot.
        """
        payload = {
            "accountIds": [str(aid) for aid in account_ids],
            "text": text,
        }

        if scheduled_time:
            payload["scheduledTime"] = scheduled_time
            payload["useNextFreeSlot"] = False
        elif use_next_free_slot:
            payload["useNextFreeSlot"] = True

        if media_urls:
            payload["mediaUrls"] = media_urls

        return self._request("POST", "/v2/posts", json=payload)

    def schedule_post(
        self,
        account_ids: list[str],
        text: str,
        scheduled_time: str,
    ) -> dict:
        """Schedule a post for a specific time."""
        return self.create_post(
            account_ids=account_ids,
            text=text,
            scheduled_time=scheduled_time,
            use_next_free_slot=False,
        )

    def get_post_status(self, post_id: str) -> dict:
        """Get the status of a post."""
        return self._request("GET", f"/v2/posts/{post_id}")

    # ── Media ────────────────────────────────────────────────────────────────

    def upload_media(self, url_or_base64: str) -> dict:
        """Upload media for use in posts.

        Args:
            url_or_base64: Either a URL to the media or a base64-encoded string.
        """
        payload = {}
        if url_or_base64.startswith(("http://", "https://")):
            payload["url"] = url_or_base64
        else:
            payload["base64"] = url_or_base64

        return self._request("POST", "/v2/media", json=payload)


# ── Quick test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    client = BlotatoClient()
    print("Testing Blotato API connectivity...")
    try:
        accounts = client.list_accounts()
        print(f"✅ Connected! Found {len(accounts)} accounts:")
        for acc in accounts:
            if isinstance(acc, dict):
                name = acc.get("fullname") or acc.get("username") or acc.get("name", "?")
                platform = acc.get("platform", acc.get("type", "?"))
                aid = acc.get("id", "?")
                print(f"   • {platform}: {name} (id: {aid})")
            else:
                print(f"   • {acc}")
    except Exception as e:
        print(f"❌ Error: {e}")
