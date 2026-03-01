# TODO 355 — Write ForwardLane → Supabase User Migration Script
**Repo:** signal-studio-auth
**Priority:** HIGH
**Effort:** 4 hours
**Status:** pending

## Description
No migration tooling exists to move existing ForwardLane users to Supabase Auth.
This blocks switching from dual-mode to supabase-only mode.

## Coding Prompt
Create `/data/workspace/projects/signal-studio-auth/scripts/migrate_users.py`:

```python
#!/usr/bin/env python3
"""
Migrate ForwardLane users to Supabase Auth.

Usage:
  python scripts/migrate_users.py --dry-run          # Preview without making changes
  python scripts/migrate_users.py --batch-size 50    # Migrate in batches
  python scripts/migrate_users.py --resume-from 100  # Resume after offset

Environment variables required:
  SUPABASE_URL, SUPABASE_SERVICE_KEY
  FORWARDLANE_DB_URL (postgres connection string)
"""
import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any

import asyncpg
import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
FL_DB_URL = os.environ["FORWARDLANE_DB_URL"]

ADMIN_HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
}


async def get_forwardlane_users(conn, offset: int, limit: int) -> list[dict]:
    """Fetch users from ForwardLane Postgres."""
    rows = await conn.fetch(
        """
        SELECT u.id, u.email, u.first_name, u.last_name,
               o.id as org_id, o.name as org_name, o.vertical as org_vertical,
               u.role
        FROM users u
        LEFT JOIN organizations o ON u.organization_id = o.id
        ORDER BY u.id
        OFFSET $1 LIMIT $2
        """,
        offset, limit
    )
    return [dict(r) for r in rows]


async def create_supabase_user(client: httpx.AsyncClient, user: dict, dry_run: bool) -> dict:
    """Create a user in Supabase Auth with legacy metadata."""
    payload = {
        "email": user["email"],
        "email_confirm": True,
        "app_metadata": {
            "legacy_user_id": user["id"],
            "organization_id": user["org_id"],
            "organization_name": user["org_name"],
            "organization_vertical": user["org_vertical"],
            "role": user.get("role", "viewer"),
        },
        "user_metadata": {
            "first_name": user.get("first_name", ""),
            "last_name": user.get("last_name", ""),
        },
    }
    
    if dry_run:
        logger.info(f"[DRY RUN] Would create user: {user['email']}")
        return {"dry_run": True, "email": user["email"]}
    
    resp = await client.post(
        f"{SUPABASE_URL}/auth/v1/admin/users",
        headers=ADMIN_HEADERS,
        json=payload,
    )
    
    if resp.status_code == 422:
        data = resp.json()
        if "already been registered" in str(data):
            logger.info(f"Skipping existing user: {user['email']}")
            return {"skipped": True, "email": user["email"]}
    
    resp.raise_for_status()
    return resp.json()


async def main(dry_run: bool, batch_size: int, resume_from: int):
    conn = await asyncpg.connect(FL_DB_URL)
    results = {"created": 0, "skipped": 0, "failed": 0}
    
    async with httpx.AsyncClient(timeout=30) as client:
        offset = resume_from
        while True:
            users = await get_forwardlane_users(conn, offset, batch_size)
            if not users:
                break
            
            for user in users:
                try:
                    result = await create_supabase_user(client, user, dry_run)
                    if result.get("skipped"):
                        results["skipped"] += 1
                    else:
                        results["created"] += 1
                except Exception as e:
                    logger.error(f"Failed to migrate {user['email']}: {e}")
                    results["failed"] += 1
            
            offset += batch_size
            logger.info(f"Progress: offset={offset}, {results}")
    
    await conn.close()
    logger.info(f"Migration complete: {results}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--resume-from", type=int, default=0)
    args = parser.parse_args()
    asyncio.run(main(args.dry_run, args.batch_size, args.resume_from))
```

Also add `asyncpg>=0.29.0` to `requirements.txt`.

## Acceptance Criteria
- [ ] Script connects to ForwardLane Postgres and paginates all users
- [ ] Creates Supabase users with correct `legacy_user_id` in app_metadata
- [ ] Skips already-migrated users (idempotent)
- [ ] Dry-run mode previews without making changes
- [ ] Resume-from offset for large migrations
- [ ] Logs progress with counts
- [ ] Unit tests for `create_supabase_user` with mocked responses
