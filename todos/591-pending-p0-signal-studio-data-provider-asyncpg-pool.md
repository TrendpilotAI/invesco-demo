# TODO 591 — Add asyncpg connection pool to SupabaseProvider

**Repo:** signal-studio-data-provider  
**Priority:** P0 (Performance/Stability)  
**Effort:** S (half day)  
**Dependencies:** 590 (SecretStr)

## Task Description
The SupabaseProvider uses `database_url` for direct asyncpg queries but likely creates a new connection per query. This is slow and will exhaust DB connection limits under load. Implement a proper `asyncpg.Pool` initialized once per provider instance.

## Changes Required
In `providers/supabase_provider.py`:
1. Add `_pool: asyncpg.Pool | None = None` instance variable
2. Add `async def _get_pool(self) -> asyncpg.Pool` lazy initializer using `asyncpg.create_pool(dsn, min_size=2, max_size=10)`
3. Wrap all `asyncpg.connect()` calls to use pool instead: `async with pool.acquire() as conn:`
4. In `close()`, call `await self._pool.close()` if pool exists

## Autonomous Agent Prompt
```
In /data/workspace/projects/signal-studio-data-provider/providers/supabase_provider.py:

1. Add asyncpg connection pooling:
   - Add `self._pool: asyncpg.Pool | None = None` in `__init__`
   - Add `async def _get_pool(self) -> asyncpg.Pool` that lazily calls `asyncpg.create_pool(dsn, min_size=2, max_size=10)` using `self._config.supabase.database_url.get_secret_value()`
   - Replace any direct `asyncpg.connect()` calls with `async with (await self._get_pool()).acquire() as conn:`
   - In `close()`, add `if self._pool: await self._pool.close(); self._pool = None`

2. Update tests/test_providers.py to mock asyncpg.Pool instead of asyncpg.connect.

Run `pytest tests/` to verify.
```

## Acceptance Criteria
- [ ] `asyncpg.Pool` used for all DB connections in SupabaseProvider
- [ ] Pool initialized lazily on first use
- [ ] `close()` properly tears down pool
- [ ] Tests updated and passing
