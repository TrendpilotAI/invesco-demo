# TODO 314 — Add asyncpg Connection Pool to SupabaseProvider

**Priority:** P1 🟠  
**Repo:** signal-studio-data-provider  
**File:** providers/supabase_provider.py  
**Effort:** M (2-4 hours)  
**Status:** pending

---

## Description

`SupabaseProvider` creates a new asyncpg connection per query. Under concurrent signal execution (multiple orgs or parallel signal runs), this creates excessive connection overhead and can exhaust Postgres connection limits.

---

## Coding Prompt

```
Upgrade SupabaseProvider in /data/workspace/projects/signal-studio-data-provider/providers/supabase_provider.py
to use asyncpg connection pooling:

1. Replace single-connection logic with an async pool:

import asyncpg

class SupabaseProvider:
    def __init__(self, config: OrgConfig) -> None:
        ...
        self._pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                dsn=self._supabase.database_url,
                min_size=2,
                max_size=10,
                command_timeout=30,
            )
        return self._pool

    async def execute_query(self, sql: str, params: dict | None = None) -> QueryResult:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            if self._jwt:
                await conn.execute(
                    "SET LOCAL request.jwt.claims = $1",
                    json.dumps({"sub": self._jwt})
                )
            # convert dict params to positional list for asyncpg $1,$2...
            param_list = list(params.values()) if params else []
            t0 = time.time()
            rows = await conn.fetch(sql, *param_list)
            elapsed = (time.time() - t0) * 1000
        ...

2. Update close() to properly drain the pool:
    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

3. Handle the lazy pool init in test fixtures (use pytest-asyncio).
```

---

## Dependencies

- TODO 311 (JWT fix) — JWT must be fixed before pooling to avoid cross-connection JWT leakage

## Acceptance Criteria

- [ ] Pool created lazily on first use
- [ ] Pool properly closed in `close()`
- [ ] JWT set per connection acquire (not per instance)
- [ ] Concurrent `execute_query` calls don't block each other
- [ ] Tests updated to handle async pool lifecycle
