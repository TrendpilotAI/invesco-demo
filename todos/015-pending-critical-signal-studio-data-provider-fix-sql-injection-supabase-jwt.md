---
status: pending
priority: p1
issue_id: "015"
tags: [python, security, sql-injection, supabase, postgresql, signal-studio-data-provider]
dependencies: []
---

# Fix SQL Injection: JWT String Interpolation in SupabaseProvider

## Problem Statement

`SupabaseProvider.execute_query()` sets the RLS (Row-Level Security) context using an f-string that directly interpolates the JWT token value into a SQL `SET` statement:

```python
await conn.execute(f"SET request.jwt.claim.sub = '{self._jwt}'")
```

An attacker who controls the JWT value (or a misconfigured caller) can inject arbitrary SQL by crafting a value like `'; DROP TABLE users; --`. This bypasses PostgreSQL RLS entirely and can lead to data exfiltration or destruction. This is a **critical security vulnerability** that must be fixed before any production deployment.

## Findings

**Vulnerable code** in `providers/supabase_provider.py`, `execute_query()`:
```python
if self._jwt:
    await conn.execute(f"SET request.jwt.claim.sub = '{self._jwt}'")
```

**Attack vector:**
```python
provider.set_jwt("' ; SELECT pg_read_file('/etc/passwd') ; --")
# Results in: SET request.jwt.claim.sub = '' ; SELECT pg_read_file('/etc/passwd') ; --'
```

**Impact:** Complete RLS bypass, potential database read of arbitrary files, privilege escalation in multi-tenant environment where each org has its own RLS policy.

**Additional injection points also in this file:**
- `vector_search()`: `f"SELECT *, ({column} <=> $1::vector)"` — column name from caller
- `write_back()`: table name and column names from caller

## Proposed Solutions

### Option A: Use `set_config()` with Parameterized Call (Recommended)
```python
# Safe replacement:
await conn.execute(
    "SELECT set_config('request.jwt.claim.sub', $1, true)",
    self._jwt
)
```
`set_config(setting, value, is_local)` is the PostgreSQL function for session config. With `is_local=true`, it's scoped to the current transaction. asyncpg parameterizes the value safely.

### Option B: Validate JWT Before Setting
Parse the JWT, extract the `sub` claim, and only set that validated value. But this requires a JWT library and is more complex. Combine with Option A.

## Recommended Action

1. Replace the f-string SET with `set_config()` parameterized call
2. Add input validation in `set_jwt()` to reject non-string or overlong values
3. Fix `vector_search()` table/column name injection (see TODO-018)
4. Add a security test that verifies injected values are handled safely

## Acceptance Criteria

- [ ] `execute_query()` uses `SELECT set_config('request.jwt.claim.sub', $1, true)` with parameterized JWT value
- [ ] `set_jwt()` validates input: must be string, max 4096 chars, raises `ValueError` on invalid input
- [ ] Test `test_jwt_injection_is_safe` verifies that a malicious JWT string does NOT result in SQL execution
- [ ] No f-string interpolation of user-controlled values into SQL strings anywhere in SupabaseProvider
- [ ] mypy passes on modified file

## Coding Prompt

```
TASK: Fix SQL injection vulnerability in SupabaseProvider in signal-studio-data-provider.

REPO: /data/workspace/projects/signal-studio-data-provider/

FILES TO MODIFY:
  - providers/supabase_provider.py
  - tests/test_providers.py

CHANGES:

1. In execute_query(), replace:
     await conn.execute(f"SET request.jwt.claim.sub = '{self._jwt}'")
   With:
     await conn.execute(
         "SELECT set_config('request.jwt.claim.sub', $1, true)",
         self._jwt
     )

2. In set_jwt(), add validation:
     def set_jwt(self, jwt: str) -> None:
         if not isinstance(jwt, str):
             raise ValueError("JWT must be a string")
         if len(jwt) > 4096:
             raise ValueError("JWT exceeds maximum length")
         self._jwt = jwt

3. Add tests in tests/test_providers.py:
   - test_set_jwt_rejects_non_string: pass an int, verify ValueError
   - test_set_jwt_rejects_overlong: pass string of 4097 chars, verify ValueError
   - test_execute_query_uses_set_config: mock asyncpg conn, verify execute called with 
     "SELECT set_config..." and NOT with f-string pattern
   - test_jwt_injection_chars_safe: set jwt to "'; DROP TABLE users; --", verify
     the set_config call receives it as a parameter value (not interpolated)

IMPORTANT: Do not change the public API of set_jwt() or execute_query(). Only fix the internal implementation.
```

## Dependencies

None — standalone security fix.

## Estimated Effort

S (hours)

## Work Log

### 2026-02-26 — Initial triage

**By:** Planning Agent

**Actions:**
- Identified f-string SQL injection in SupabaseProvider.execute_query()
- Confirmed set_config() is the correct PostgreSQL parameterized alternative
- Noted additional injection risks in vector_search() and write_back() (separate TODO)

**Learnings:**
- PostgreSQL SET command does not support parameterized values via protocol-level params
- set_config() is the correct workaround: it's a regular function call that asyncpg can parameterize
- The `is_local=true` parameter scopes the setting to the transaction, which is safer than session-level
