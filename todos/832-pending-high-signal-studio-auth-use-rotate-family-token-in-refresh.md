# TODO-832: Use _rotate_family_token() in /refresh Route (Eliminate Duplication)

**Repo:** signal-studio-auth
**Priority:** P1 (High)
**Effort:** 1 hour
**Status:** pending
**Dependencies:** None
**Created:** 2026-03-10

## Problem

`routes/auth_routes.py` has a well-designed `_rotate_family_token()` function (lines ~188-239) that handles:
- Looking up the old token in Redis
- Detecting theft (consumed token reuse → revoke entire family)
- Marking old token as consumed
- Issuing a new child token in the same family

However, the `/refresh` route (lines ~332-395) **duplicates all of this logic inline** instead of calling `_rotate_family_token()`. The route reimplements:
- Token lookup (line ~340: `r.hgetall(...)`)
- Theft detection (lines ~343-358: consumed check + family revocation)
- Consumed marking (line ~360: `r.hset(...)`)
- Child token issuance (lines ~375-380: `_issue_family_token(...)`)

This means `_rotate_family_token()` is effectively dead code — never called from any route.

## Files to Change

- `routes/auth_routes.py` — Refactor `/refresh` route to call `_rotate_family_token()`

## Coding Prompt

```
Open /data/workspace/projects/signal-studio-auth/routes/auth_routes.py

Refactor the /refresh route handler to use _rotate_family_token(). The new flow should be:

1. Extract old_token_id from body
2. Get the supabase_token from Redis (needed to call Supabase refresh)
   - If Redis unavailable, treat opaque token as supabase token directly
   - If token not found in Redis, raise 401
3. Call Supabase /auth/v1/token?grant_type=refresh_token with the supabase_token
4. Call _rotate_family_token(old_token_id, new_supabase_refresh_token) to handle rotation
5. Return response with new opaque token

The tricky part: _rotate_family_token() currently marks consumed AFTER looking up data,
but the /refresh route needs the supabase_token BEFORE calling Supabase. So we need a
small refactor:

Option A (recommended): Extract a _get_token_data() helper that returns the Redis hash
data without marking consumed. Then _rotate_family_token() handles the rest after
Supabase returns.

Option B: Split _rotate_family_token into _validate_and_consume() + _issue_child().

Go with Option A:

def _get_token_data(token_id: str) -> tuple[dict | None, str]:
    """
    Look up token in Redis. Returns (token_data_dict, supabase_token).
    Raises 401 if token not found or already consumed (theft).
    Returns (None, token_id) if Redis unavailable.
    """
    r = get_redis()
    if r is None:
        return None, token_id
    data = r.hgetall(f"rt:{token_id}")
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    if data.get("consumed") == "1":
        # theft detection — revoke family
        family_id = data.get("family_id", "")
        if family_id:
            family_members = r.smembers(f"rt:family:{family_id}")
            pipe = r.pipeline()
            for mid in family_members:
                pipe.delete(f"rt:{mid}")
            pipe.delete(f"rt:family:{family_id}")
            pipe.execute()
        logger.warning("Refresh token theft detected: token_id=%s family=%s user=%s",
                       token_id, family_id, data.get("user_id", ""))
        raise HTTPException(status_code=401, detail="Refresh token reuse detected — all sessions revoked")
    return data, data["supabase_token"]

Then update _rotate_family_token() to accept token_data dict (avoid double Redis lookup):

def _rotate_family_token(old_token_id: str, new_supabase_token: str, token_data: dict) -> str:
    r = get_redis()
    if r is None:
        return str(uuid.uuid4())
    r.hset(f"rt:{old_token_id}", "consumed", "1")
    return _issue_family_token(
        supabase_token=new_supabase_token,
        user_id=token_data.get("user_id", ""),
        parent_id=old_token_id,
        family_id=token_data.get("family_id"),
    )

Then /refresh becomes:
    token_data, supabase_refresh = _get_token_data(old_token_id)
    # call Supabase
    resp = await client.post(...)
    if token_data is None:
        return _wrap_with_opaque_token(supabase_data)
    new_token_id = _rotate_family_token(old_token_id, new_supabase_rt, token_data)
    result["refresh_token"] = new_token_id
    return result

Run: cd /data/workspace/projects/signal-studio-auth && python -m pytest -v
All existing tests (especially test_redis_integration.py and test_rate_limit_and_tokens.py) must pass.
```

## Acceptance Criteria

- [ ] `/refresh` route calls `_rotate_family_token()` instead of duplicating logic
- [ ] Theft detection still works (test with consumed token → 401 + family revocation)
- [ ] Token rotation still works (new opaque token returned, old marked consumed)
- [ ] No-Redis fallback still works
- [ ] Net code reduction of ~30 lines
- [ ] All existing tests pass unchanged
