# TODO-433: Fix JWT RLS Race Condition in SupabaseProvider

**Repo:** signal-studio-data-provider  
**Priority:** P0 — Critical Security  
**Effort:** S (1-2h)  
**Status:** pending

## Problem

`SupabaseProvider.set_jwt()` stores JWT on the instance (`self._jwt`). Under concurrent async requests, Request A's JWT can bleed into Request B's connection context — a multi-tenant data breach.

Additionally, only `request.jwt.claim.sub` is set, but Supabase RLS policies typically check `request.jwt.claims` (full JSON).

## Task

1. Remove `self._jwt` instance variable
2. Add `jwt: str | None = None` parameter to `execute_query()`, `execute_signal()`, `write_back()`
3. Within the connection context manager, set:
   ```python
   import json
   await conn.execute(
       "SELECT set_config('request.jwt.claims', $1, true)",
       json.dumps({"sub": jwt, "role": "authenticated"})
   )
   ```
4. Remove `set_jwt()` method (or deprecate)
5. Update all callers in tests
6. Add test: concurrent requests with different JWTs don't cross-contaminate

## Acceptance Criteria

- `set_jwt()` method removed or deprecated
- JWT passed per-call, scoped to connection
- `request.jwt.claims` set as full JSON object
- Test passes for concurrent multi-tenant scenario
