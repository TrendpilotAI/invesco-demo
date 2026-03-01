# 338 — Migrate persistence.py to Async Postgres (asyncpg)

**Repo:** core-entityextraction  
**Priority:** P1 (Performance)  
**Effort:** 3-4 hours

## Problem
`persistence.py` uses synchronous `psycopg2`. All DB calls block the asyncio event loop in FastAPI, negating async concurrency benefits. Under load, a slow Postgres query stalls all concurrent requests.

## Solution
Replace `psycopg2` with `asyncpg` (or `psycopg[async]`):

```python
import asyncpg

_pool: asyncpg.Pool = None

async def init_db() -> bool:
    global _pool
    try:
        _pool = await asyncpg.create_pool(dsn=os.environ["DATABASE_URL"], min_size=2, max_size=10)
        return True
    except Exception as exc:
        LOGGER.error("DB init failed: %s", exc)
        return False

async def load_all(entity_store: Dict[str, Set[str]]) -> int:
    async with _pool.acquire() as conn:
        rows = await conn.fetch("SELECT entity_type, entity_value FROM entities")
        ...
```

Update `startup_event` in `main.py` to `await init_db()` using `asynccontextmanager` lifespan.

## Dependencies
- None (can be done independently)

## Acceptance Criteria
- [ ] All DB operations are non-blocking
- [ ] Connection pool size configurable via `DB_MIN_CONN`/`DB_MAX_CONN` env vars
- [ ] `/health` endpoint verifies DB connectivity
- [ ] Tests mock asyncpg pool
