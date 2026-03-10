# TODO-837: Implement Redis Session Scan in update_password()

**Repo:** signal-studio-auth
**Priority:** P1 (High)
**Effort:** 1 hour
**Status:** pending
**Dependencies:** TODO-836 (admin revocation — shares scan logic, DRY opportunity)
**Created:** 2026-03-10

## Problem

The `/update-password` route (line ~520 in `routes/auth_routes.py`) has a comment about revoking all opaque refresh tokens for the user in Redis, but the actual scan is **not implemented**. Currently it only:
1. Calls Supabase admin API to invalidate sessions (line ~524-528)
2. Does NOT scan Redis `rt:*` keys to delete the user's opaque tokens

This means after a password change, the user's old refresh tokens in Redis are still valid until they expire (7 days). An attacker with a stolen refresh token could continue using it.

## Files to Change

- `routes/auth_routes.py` — Add Redis scan in `/update-password` route

## Coding Prompt

```
Open /data/workspace/projects/signal-studio-auth/routes/auth_routes.py

In the /update-password route, after the Supabase password update succeeds (around line 520),
replace the existing Redis/Supabase revocation block with a proper scan.

If TODO-836 (admin revocation) is done first, extract the scan logic into a shared helper:

def _revoke_all_user_tokens(user_id: str) -> int:
    """Scan Redis for all rt:* tokens belonging to user_id and delete them."""
    r = get_redis()
    if r is None or not user_id:
        return 0
    
    cursor = 0
    keys_to_delete = []
    families_to_clean = set()
    while True:
        cursor, keys = r.scan(cursor, match="rt:*", count=100)
        for key in keys:
            key_str = key if isinstance(key, str) else key.decode()
            if key_str.startswith("rt:family:"):
                continue
            data = r.hgetall(key)
            if data.get("user_id") == user_id:
                keys_to_delete.append(key_str)
                fid = data.get("family_id", "")
                if fid:
                    families_to_clean.add(fid)
        if cursor == 0:
            break
    
    if not keys_to_delete and not families_to_clean:
        return 0
    
    pipe = r.pipeline()
    for k in keys_to_delete:
        pipe.delete(k)
    for fid in families_to_clean:
        pipe.delete(f"rt:family:{fid}")
    pipe.execute()
    return len(keys_to_delete)

Then in /update-password, replace the try/except block with:
    revoked = _revoke_all_user_tokens(user_sub or "")
    logger.info("update_password: revoked %d tokens for user %s", revoked, user_sub)
    
    # Also invalidate Supabase sessions
    if user_sub:
        try:
            async with _http_client(request) as client:
                await client.post(
                    f"{SUPABASE_URL}/auth/v1/admin/users/{user_sub}/logout",
                    headers=_supabase_headers(service=True),
                )
        except Exception as exc:
            logger.warning("update_password: Supabase session revocation failed: %s", exc)

Run: cd /data/workspace/projects/signal-studio-auth && python -m pytest -v
```

## Acceptance Criteria

- [ ] `/update-password` scans Redis for all user tokens and deletes them
- [ ] Shared `_revoke_all_user_tokens()` helper usable by both update_password and admin revocation
- [ ] Old refresh tokens are invalidated immediately after password change
- [ ] Supabase admin logout still called
- [ ] Tests verify token revocation after password change
- [ ] All existing tests pass
