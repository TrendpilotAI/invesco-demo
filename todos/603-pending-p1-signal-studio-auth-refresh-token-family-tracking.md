# TODO-603: Refresh Token Family Tracking (Theft Detection)

**Repo:** signal-studio-auth  
**Priority:** P1 (MEDIUM)  
**Effort:** 3h  
**Status:** pending

## Problem
Current refresh token rotation detects reuse of a consumed token by returning 401, but does NOT revoke the entire token chain. An attacker who steals a token and rotates it first leaves the legitimate user with a consumed token that returns 401, but the attacker's new token keeps working.

## Fix: Token Family Tracking in Redis

Track parent→child relationships. On reuse of consumed token, revoke the entire family.

```python
# Redis data model:
# rt:{token_id} = {user_id, family_id, parent_id, supabase_refresh_token}
# rt:family:{family_id} = SET of all token_ids in this family

import uuid

async def issue_refresh_token(user_id: str, supabase_token: str, 
                               parent_id: str = None, family_id: str = None) -> str:
    token_id = str(uuid.uuid4())
    family_id = family_id or str(uuid.uuid4())  # new family on initial login
    
    r = get_redis()
    pipe = r.pipeline()
    pipe.hset(f"rt:{token_id}", mapping={
        "user_id": user_id,
        "family_id": family_id,
        "parent_id": parent_id or "",
        "supabase_token": supabase_token,
        "consumed": "0",
    })
    pipe.expire(f"rt:{token_id}", REFRESH_TOKEN_TTL)
    pipe.sadd(f"rt:family:{family_id}", token_id)
    pipe.expire(f"rt:family:{family_id}", REFRESH_TOKEN_TTL)
    await pipe.execute()
    return token_id

async def rotate_refresh_token(old_token_id: str, new_supabase_token: str) -> str:
    r = get_redis()
    data = await r.hgetall(f"rt:{old_token_id}")
    
    if not data:
        raise HTTPException(401, "Invalid refresh token")
    
    if data.get("consumed") == "1":
        # THEFT DETECTED: revoke entire family
        family_id = data.get("family_id")
        if family_id:
            family_members = await r.smembers(f"rt:family:{family_id}")
            pipe = r.pipeline()
            for member_id in family_members:
                pipe.delete(f"rt:{member_id}")
            pipe.delete(f"rt:family:{family_id}")
            await pipe.execute()
        raise HTTPException(401, "Refresh token reuse detected — all sessions revoked")
    
    # Mark old token as consumed
    await r.hset(f"rt:{old_token_id}", "consumed", "1")
    
    # Issue new token in same family
    return await issue_refresh_token(
        user_id=data["user_id"],
        supabase_token=new_supabase_token,
        parent_id=old_token_id,
        family_id=data["family_id"],
    )
```

## Files to Change
- `routes/auth_routes.py` — replace current token rotation logic with family tracking
- `tests/test_redis_integration.py` — add theft detection test cases

## Acceptance Criteria
- [ ] Token reuse triggers full family revocation
- [ ] Legitimate rotation still works
- [ ] Test: attacker reuses stolen (consumed) token → all sessions revoked
- [ ] Test: legitimate user's subsequent refresh after theft attempt → 401

## Dependencies
- TODO-601 (integration tests — add theft detection tests there)
