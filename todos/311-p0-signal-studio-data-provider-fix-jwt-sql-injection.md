# TODO 311 — Fix JWT SQL Injection in SupabaseProvider

**Priority:** P0 🔴  
**Repo:** signal-studio-data-provider  
**File:** providers/supabase_provider.py  
**Effort:** S (< 1 hour)  
**Status:** pending

---

## Description

`SupabaseProvider.set_jwt()` sets a Postgres session variable by directly interpolating the JWT string into SQL:

```python
await conn.execute(f"SET request.jwt.claim.sub = '{self._jwt}'")
```

This is a SQL injection vulnerability. A malicious JWT payload containing a single quote could break out of the string literal and execute arbitrary SQL.

Additionally, JWT is stored as instance state (`self._jwt`), meaning if the same provider instance is reused across requests (which the factory's `cached=True` enables), user A's JWT persists to user B's queries.

---

## Coding Prompt

```
Fix SQL injection in /data/workspace/projects/signal-studio-data-provider/providers/supabase_provider.py:

1. Replace the f-string JWT injection:
   BEFORE: await conn.execute(f"SET request.jwt.claim.sub = '{self._jwt}'")
   AFTER:  await conn.execute("SET LOCAL request.jwt.claims = $1", json.dumps({"sub": self._jwt}))
   
   Note: SET LOCAL scopes the variable to the current transaction only.
   Import json at the top.

2. Ensure JWT is set per connection acquire, not cached on the instance.
   Wherever the pool acquires a connection, set the JWT claim before executing the actual query.
   Pattern:
   async with self._pool.acquire() as conn:
       if self._jwt:
           await conn.execute("SET LOCAL request.jwt.claims = $1", json.dumps({"sub": self._jwt}))
       result = await conn.fetch(sql, *params)

3. Add a test in tests/test_providers.py that verifies:
   - A JWT containing single quotes does not cause a syntax error
   - A JWT containing SQL metacharacters ('; DROP TABLE users; --) is safely handled
```

---

## Dependencies

None — fix in isolation first.

## Acceptance Criteria

- [ ] No f-string SQL interpolation in supabase_provider.py
- [ ] JWT is scoped to connection acquire block (SET LOCAL)
- [ ] Security test passes with adversarial JWT inputs
- [ ] All existing tests still pass
