# TODO-895: Migrate Persistence Layer to asyncpg (Async PostgreSQL)

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** M (2-3 hours)  
**Status:** pending

## Problem

FastAPI is built on async I/O. `psycopg2` is a **synchronous** driver — every DB call blocks the event loop thread, reducing throughput under concurrent load. While `ThreadedConnectionPool` mitigates this by running DB ops in threads, this is a workaround, not a solution.

`asyncpg` provides native async PostgreSQL access with connection pooling, proper `await` syntax, and significantly better performance under load.

## Fix

Replace `psycopg2-binary` with `asyncpg` in `requirements.txt` and rewrite `persistence.py` using async functions.

## Coding Prompt

```
1. Edit /data/workspace/projects/core-entityextraction/requirements.txt:
   - Remove: psycopg2-binary>=2.9.0
   - Add: asyncpg>=0.29.0

2. Rewrite /data/workspace/projects/core-entityextraction/persistence.py:

"""PostgreSQL persistence for entity store — async write-through cache.
Uses asyncpg connection pool for non-blocking I/O with FastAPI.
"""
import asyncio
import logging
import os
from typing import Dict, List, Optional, Set

import asyncpg

LOGGER = logging.getLogger("entity_extraction.persistence")

POOL_MIN = int(os.environ.get("DB_POOL_MIN", 2))
POOL_MAX = int(os.environ.get("DB_POOL_MAX", 10))

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS entities (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(40) NOT NULL,
    entity_value VARCHAR(256) NOT NULL,
    UNIQUE(entity_type, entity_value)
);
"""

_pool: Optional[asyncpg.Pool] = None


async def init_pool() -> bool:
    global _pool
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        LOGGER.warning("No DATABASE_URL set — entity persistence disabled (in-memory only)")
        return False
    try:
        _pool = await asyncpg.create_pool(db_url, min_size=POOL_MIN, max_size=POOL_MAX)
        LOGGER.info("asyncpg connection pool created (min=%d, max=%d).", POOL_MIN, POOL_MAX)
        return True
    except Exception as exc:
        LOGGER.warning("Could not create asyncpg pool: %s", exc)
        return False


async def init_db() -> bool:
    if not await init_pool():
        return False
    try:
        async with _pool.acquire() as conn:
            await conn.execute(CREATE_TABLE_SQL)
        LOGGER.info("Entity persistence table ready.")
        return True
    except Exception as exc:
        LOGGER.error("Failed to init DB: %s", exc)
        return False


async def load_all(entity_store: Dict[str, Set[str]]) -> int:
    if _pool is None:
        return 0
    try:
        async with _pool.acquire() as conn:
            rows = await conn.fetch("SELECT entity_type, entity_value FROM entities")
        loaded = 0
        for row in rows:
            if row["entity_type"] in entity_store:
                entity_store[row["entity_type"]].add(row["entity_value"])
                loaded += 1
        LOGGER.info("Loaded %d entities from Postgres.", loaded)
        return loaded
    except Exception as exc:
        LOGGER.error("Failed to load entities: %s", exc)
        return 0


async def save_entities(entity_type: str, values: List[str]) -> int:
    if not values or _pool is None:
        return 0
    try:
        rows = [(entity_type, v) for v in values]
        async with _pool.acquire() as conn:
            result = await conn.executemany(
                "INSERT INTO entities (entity_type, entity_value) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                rows,
            )
        return len(rows)
    except Exception as exc:
        LOGGER.error("Failed to save entities: %s", exc)
        return 0


async def delete_entities(entity_types_list: Optional[List[str]] = None, all_entities: bool = False) -> int:
    if _pool is None:
        return 0
    try:
        async with _pool.acquire() as conn:
            if all_entities:
                result = await conn.execute("DELETE FROM entities")
            elif entity_types_list:
                result = await conn.execute(
                    "DELETE FROM entities WHERE entity_type = ANY($1::text[])",
                    entity_types_list,
                )
            else:
                return 0
        return int(result.split()[-1]) if result else 0
    except Exception as exc:
        LOGGER.error("Failed to delete entities: %s", exc)
        return 0


3. Update main.py startup_event to use async:
   Change `@app.on_event("startup")` to `async def startup_event():` 
   and await persistence calls:
   
   @app.on_event("startup")
   async def startup_event():
       _load_ml_model()  # sync OK, runs in startup before requests
       enable_spacy = os.environ.get("ENABLE_SPACY_ENTITY_EXTRACTION", "").lower() in ("1", "true", "yes")
       if enable_spacy:
           _load_spacy_model()
       if await persistence.init_db():
           loaded = await persistence.load_all(entity_store)
           LOGGER.info("Loaded %d entities from Postgres on startup.", loaded)
           _invalidate_pattern_cache()
       LOGGER.info("Entity Extraction Service v2.0.0 ready.")

4. Update the fixed_lists endpoints to await persistence calls:
   await persistence.save_entities(entity_type, list(values))
   await persistence.delete_entities(entity_types_list=...)
   await persistence.delete_entities(all_entities=True)

5. Update conftest.py to mock async persistence functions properly:
   monkeypatch.setattr("persistence.save_entities", AsyncMock(return_value=0))
   monkeypatch.setattr("persistence.delete_entities", AsyncMock(return_value=0))
   monkeypatch.setattr("persistence.init_db", AsyncMock(return_value=False))
   monkeypatch.setattr("persistence.load_all", AsyncMock(return_value=0))

Run: pytest tests/ -x -q
```

## Acceptance Criteria
- [ ] `psycopg2-binary` removed from requirements.txt
- [ ] `asyncpg>=0.29.0` added to requirements.txt
- [ ] All persistence functions are `async`
- [ ] `startup_event` properly awaits persistence calls
- [ ] All existing tests pass with AsyncMock stubs
- [ ] No blocking DB calls in async context

## Dependencies
- TODO-893 (fix connection leak first — simpler to resolve before rewrite)

## Notes
If asyncpg migration is too risky for production, an intermediate step is to use `databases` library which wraps asyncpg/aiosqlite with SQLAlchemy-compatible async interface.
