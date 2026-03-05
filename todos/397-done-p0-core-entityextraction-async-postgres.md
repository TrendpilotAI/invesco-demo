# TODO-397: Migrate persistence.py to Async Postgres (asyncpg)

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** M (3-4 hours)  
**Status:** pending

## Description
`persistence.py` uses synchronous `psycopg2.ThreadedConnectionPool` which blocks FastAPI's async event loop on every DB call. This degrades throughput under load — while a psycopg2 call waits for Postgres, no other async requests can be processed.

Call sites: startup `init_db()`/`load_all()`, `POST /fixed_lists` → `save_entities()`, `DELETE /fixed_lists` → `delete_entities()`.

## Coding Prompt
```
Migrate /data/workspace/projects/core-entityextraction/persistence.py from psycopg2 to asyncpg:

1. Add asyncpg to requirements.txt (remove psycopg2-binary)
2. Rewrite persistence.py using asyncpg:
   - Use asyncpg.create_pool() in FastAPI lifespan context manager (replace @app.on_event("startup"))
   - Store pool in app.state.db_pool
   - All functions become async: async def init_db(), async def load_all(), async def save_entities(), async def delete_entities()
   - Use asyncpg's executemany() for batch inserts
   - Handle ON CONFLICT with asyncpg syntax: INSERT ... ON CONFLICT DO NOTHING
3. Update main.py:
   - Replace @app.on_event("startup") with async context manager via lifespan=
   - Make /fixed_lists endpoints async (they already are) and await persistence calls
   - Pass request.app.state.db_pool to persistence functions
4. Short-term alternative if asyncpg is too risky: wrap all persistence calls in asyncio.to_thread():
   await asyncio.to_thread(persistence.save_entities, entity_type, values)

Test: ensure service starts without DATABASE_URL (in-memory only mode still works).
```

## Dependencies
None — but do after TODO-396 (dead code removal)

## Acceptance Criteria
- No synchronous psycopg2 calls in async request handlers
- Service starts cleanly with and without DATABASE_URL
- Entity loading at startup works
- /fixed_lists POST and DELETE persist correctly
