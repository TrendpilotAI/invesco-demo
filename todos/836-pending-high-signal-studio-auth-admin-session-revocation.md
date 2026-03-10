# TODO-836: Add Admin Session Revocation Endpoint

**Repo:** signal-studio-auth
**Priority:** P1 (High)
**Effort:** 2 hours
**Status:** pending
**Dependencies:** TODO-828 (rate limiter singleton — need Redis working cleanly)
**Created:** 2026-03-10

## Problem

No admin endpoint exists to revoke all sessions for a specific user. If a user's credentials are compromised, an admin must:
1. Manually connect to Redis
2. Find and delete all `rt:*` keys for that user
3. Call Supabase admin API to invalidate sessions

This should be a single API call.

## Files to Change

- `routes/auth_routes.py` — Add `DELETE /auth/admin/users/{user_id}/sessions` route

## Coding Prompt

```
Open /data/workspace/projects/signal-studio-auth/routes/auth_routes.py

Add a new route after the existing /update-password route:

@router.delete("/admin/users/{user_id}/sessions")
async def revoke_user_sessions(user_id: str, request: Request):
    """
    Admin-only: revoke ALL refresh tokens for a user.
    
    Scans Redis for rt:* keys belonging to the user, deletes them all,
    and calls Supabase admin API to invalidate server-side sessions.
    """
    # Require admin role
    caller = getattr(request.state, "user", None)
    if not caller or not caller.is_authenticated:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    caller_role = _get_caller_role(request)
    if caller_role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    
    revoked_count = 0
    r = get_redis()
    if r is not None:
        # Scan all rt:* keys and check user_id field
        cursor = 0
        keys_to_delete = []
        families_to_clean = set()
        while True:
            cursor, keys = r.scan(cursor, match="rt:*", count=100)
            for key in keys:
                # Skip family set keys
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
        
        if keys_to_delete or families_to_clean:
            pipe = r.pipeline()
            for k in keys_to_delete:
                pipe.delete(k)
            for fid in families_to_clean:
                pipe.delete(f"rt:family:{fid}")
            pipe.execute()
            revoked_count = len(keys_to_delete)
    
    # Also call Supabase admin logout
    try:
        async with _http_client(request) as client:
            await client.post(
                f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}/logout",
                headers=_supabase_headers(service=True),
            )
    except Exception as exc:
        logger.warning("Admin session revocation — Supabase logout failed: %s", exc)
    
    logger.info("Admin revoked %d sessions for user %s", revoked_count, user_id)
    return {"detail": f"Revoked {revoked_count} refresh tokens", "user_id": user_id}

Add tests in tests/test_rbac.py or a new test_admin.py:
- Test 401 if not authenticated
- Test 403 if not admin
- Test successful revocation (mock Redis with test tokens, verify all deleted)
- Test that user's existing refresh token returns 401 after revocation

Run: cd /data/workspace/projects/signal-studio-auth && python -m pytest -v
```

## Acceptance Criteria

- [ ] `DELETE /auth/admin/users/{user_id}/sessions` endpoint exists
- [ ] Returns 401 if not authenticated
- [ ] Returns 403 if caller is not admin
- [ ] Scans Redis and deletes all `rt:*` tokens for the target user
- [ ] Cleans up corresponding `rt:family:*` sets
- [ ] Calls Supabase admin logout API
- [ ] Returns count of revoked tokens
- [ ] Tests cover auth checks + successful revocation
