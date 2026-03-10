# TODO-830: Explicit SQLAlchemy Connection Pool Configuration

**Repo:** signal-builder-backend  
**Priority:** MEDIUM  
**Effort:** XS (2 hours)  
**Status:** pending

## Problem

SQLAlchemy engine likely uses default pool settings (pool_size=5, max_overflow=10). Under Invesco load with concurrent signal runs, connection exhaustion is a risk. No explicit pool configuration visible in settings.

## Fix

Add explicit pool config to the SQLAlchemy engine creation in `db/` or `settings/`:

```python
# db/engine.py or wherever create_engine/create_async_engine is called:
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,           # max persistent connections
    max_overflow=10,        # burst connections above pool_size
    pool_pre_ping=True,     # verify connections before use (handles stale connections)
    pool_timeout=30,        # seconds to wait for connection from pool
    pool_recycle=1800,      # recycle connections after 30 min (Railway resets)
    echo=False,
)
```

Also add `SQLALCHEMY_POOL_SIZE`, `SQLALCHEMY_MAX_OVERFLOW` to `.env.example` for environment-specific tuning.

## Coding Prompt

```
1. Find where create_engine or create_async_engine is called in:
   - db/
   - core/
   - settings/
   
2. Add: pool_size=20, max_overflow=10, pool_pre_ping=True, pool_timeout=30, pool_recycle=1800

3. Add to settings/common.py:
   SQLALCHEMY_POOL_SIZE: int = 20
   SQLALCHEMY_MAX_OVERFLOW: int = 10
   
4. Update engine call to use settings values

5. Add to .env.example:
   SQLALCHEMY_POOL_SIZE=20
   SQLALCHEMY_MAX_OVERFLOW=10
```

## Acceptance Criteria
- Engine config uses explicit pool settings loaded from environment
- `pool_pre_ping=True` prevents stale connection errors after Railway restarts
- Settings are documented in `.env.example`
- All tests pass (pool config doesn't affect test behavior with SQLite/in-memory)
