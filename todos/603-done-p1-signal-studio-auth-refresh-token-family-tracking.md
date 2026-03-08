# TODO-603: Refresh Token Family Tracking (Theft Detection)

**Status:** DONE  
**Commit:** ba725e7  
**Repo:** signal-studio-auth  
**Branch:** master  

## What was implemented

- Replaced simple string-based opaque tokens with Redis hash + family SET model
- `rt:{token_id}` HASH: user_id, family_id, parent_id, supabase_token, consumed
- `rt:family:{family_id}` SET: all token_ids in the rotation chain
- On refresh: old token marked `consumed=1` (kept for reuse detection, not deleted)
- On consumed token reuse: entire family revoked (all member hashes + SET deleted) → 401 "Refresh token reuse detected — all sessions revoked"
- Wired into `/auth/refresh` and `/auth/logout` endpoints
- 5 new theft-detection tests added to `tests/test_redis_integration.py`
- All existing tests updated to use `fakeredis(decode_responses=True)` + new hash format
- 93 tests pass, 0 failures

## Acceptance Criteria
- [x] Token reuse triggers full family revocation
- [x] Legitimate rotation still works
- [x] Test: attacker reuses stolen (consumed) token → all sessions revoked
- [x] Test: legitimate user's subsequent refresh after theft attempt → 401
