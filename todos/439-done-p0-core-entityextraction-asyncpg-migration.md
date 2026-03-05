# TODO-439: Migrate persistence.py from psycopg2 to asyncpg

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** M (4-8h)  
**Status:** pending

## Problem
`persistence.py` uses psycopg2 `ThreadedConnectionPool` which performs blocking I/O. In FastAPI's async context, every DB call blocks the event loop, degrading throughput under load.

## Task
Replace psycopg2 with asyncpg for non-blocking async database operations.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/persistence.py:

1. Replace imports: remove psycopg2/psycopg2.pool, add asyncpg
2. Replace ThreadedConnectionPool with asyncpg.create_pool() returning an AsyncPool
3. Change all DB functions to async:
   - init_db() → async def init_db()
   - upsert_entities() → async def upsert_entities()
   - delete_entities() → async def delete_entities()
   - load_all_entities() → async def load_all_entities()
4. Use asyncpg's executemany() for bulk upserts
5. In main.py, update startup_event to use lifespan context manager (FastAPI 0.110+):
   @asynccontextmanager
   async def lifespan(app: FastAPI):
       await persistence.init_db()
       await persistence.load_all_entities(entity_store)
       yield
       await persistence.close_pool()
6. Update all route handlers to await persistence calls
7. Update requirements.txt: remove psycopg2-binary, add asyncpg>=0.29.0
8. Test: all entity endpoints still work, DB writes confirmed in Postgres
```

## Acceptance Criteria
- [ ] No psycopg2 imports remain
- [ ] asyncpg pool created at startup, closed at shutdown
- [ ] All DB operations are async
- [ ] `pytest tests/test_persistence.py` passes
- [ ] Load test shows >2x throughput improvement under concurrent requests

## Dependencies
- TODO-399 (pytest suite) should be done first or in parallel
