# 228 — Add PostgreSQL Connection Pooling to persistence.py

**Repo:** core-entityextraction  
**Priority:** P0 (Critical — production stability)  
**Effort:** 4 hours  
**Dependencies:** None

## Description
`persistence.py` opens a new `psycopg2.connect()` on every DB call. Under concurrent load this exhausts Postgres connections and adds 20-100ms latency per request. Replace with `psycopg2.pool.ThreadedConnectionPool`.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/persistence.py:

1. Add import: from psycopg2 import pool as psycopg2_pool

2. Create a module-level pool variable:
   _pool: Optional[psycopg2_pool.ThreadedConnectionPool] = None

3. Add init_pool() function called during FastAPI startup:
   def init_pool() -> bool:
       global _pool
       db_url = os.environ.get("DATABASE_URL")
       if not db_url:
           return False
       try:
           _pool = psycopg2_pool.ThreadedConnectionPool(minconn=1, maxconn=10, dsn=db_url)
           LOGGER.info("Postgres connection pool initialized (1-10 connections).")
           return True
       except Exception as exc:
           LOGGER.error("Failed to init connection pool: %s", exc)
           return False

4. Replace _get_conn() to use the pool:
   def _get_conn():
       if _pool is None:
           return None
       try:
           return _pool.getconn()
       except Exception as exc:
           LOGGER.warning("Could not get connection from pool: %s", exc)
           return None

5. Add _put_conn(conn) to return connections to pool:
   def _put_conn(conn):
       if _pool and conn:
           _pool.putconn(conn)

6. Update all functions (load_all, save_entities, delete_entities, init_db) 
   to use _put_conn(conn) in finally blocks instead of conn.close().

7. In main.py startup_event(), call persistence.init_pool() before persistence.init_db().
```

## Acceptance Criteria
- [ ] No new connections created per request (verified via Postgres pg_stat_activity)
- [ ] Pool min=1, max=10 configurable via env vars
- [ ] Connections properly returned to pool in all code paths (success + exception)
- [ ] init_pool() called before init_db() in startup
- [ ] Existing behavior preserved (graceful fallback if DATABASE_URL not set)
