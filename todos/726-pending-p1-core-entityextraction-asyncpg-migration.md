# TODO-726: Migrate persistence.py from psycopg2 to asyncpg

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** M  
**Status:** pending

## Description
`persistence.py` uses `psycopg2.pool.ThreadedConnectionPool` which blocks FastAPI's async event loop on every DB call. This creates thread-blocking under high concurrency and negates FastAPI's async performance benefits.

## Coding Prompt
Migrate `/data/workspace/projects/core-entityextraction/persistence.py` from psycopg2 to asyncpg:

1. Replace `psycopg2-binary` with `asyncpg` in `requirements.txt`
2. Rewrite `persistence.py` using `asyncpg.create_pool()` with an async context manager
3. Change all persistence functions to `async def` with `await pool.fetch/execute/fetchval`
4. Update `main.py` to `await` all persistence calls
5. Use FastAPI `lifespan` context manager (replacing deprecated `@app.on_event`) to init/close the pool
6. Update `schema.sql` if needed; run `pytest tests/ -v` to confirm all tests pass

## Acceptance Criteria
- [ ] No psycopg2 imports remain
- [ ] All persistence functions are async
- [ ] Pool created in lifespan, not module-level
- [ ] All existing tests pass
- [ ] Load test shows no event loop blocking under 50 concurrent requests

## Dependencies
- TODO-735 (replace deprecated on_event with lifespan — can be done together)
