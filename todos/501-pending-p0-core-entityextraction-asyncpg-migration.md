# TODO-501: Migrate from psycopg2 to asyncpg

**Repo:** core-entityextraction
**Priority:** P0
**Effort:** M (4-8h)
**Dependencies:** None
**Blocks:** TODO-502 (regex caching benefits more with async), TODO-510 (Redis caching)

## Description
The current `persistence.py` uses `psycopg2.pool.ThreadedConnectionPool` which blocks the FastAPI async event loop on every DB call. Migrate to `asyncpg` with a proper async connection pool for true non-blocking I/O.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Replace psycopg2 with asyncpg in requirements.txt
2. Rewrite persistence.py:
   - Replace ThreadedConnectionPool with asyncpg.create_pool()
   - Convert all DB functions (init_db, upsert_entities, delete_entities, load_entities) to async
   - Use `async with pool.acquire() as conn:` pattern
   - Keep same env vars: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
   - Add DB_POOL_MIN (default 2), DB_POOL_MAX (default 10), DB_STATEMENT_TIMEOUT (default 30s)
   - Log pool exhaustion events
3. Update main.py:
   - Change startup_event() to use `await` for all DB calls
   - Update all route handlers that call persistence functions to await them
4. Update schema.sql if needed (asyncpg uses $1 params not %s)
5. Run existing tests if any, verify app starts with `uvicorn main:app`
```

## Acceptance Criteria
- [ ] All DB operations are truly async (no sync pool)
- [ ] App starts and serves requests with asyncpg
- [ ] Connection pool is configurable via env vars
- [ ] Pool exhaustion is logged
- [ ] No psycopg2 import remains in codebase
