# TODO-456: Celery Redis Task Lock Guard

**Repo:** signal-builder-backend  
**Priority:** High  
**Effort:** 2h  
**Status:** Pending

## Description
`apps/tasks.py` has two Celery tasks with TODO comments indicating they should skip if already running. Without a concurrency guard, overlapping task runs can cause duplicate analytical DB syncs, data corruption, or race conditions.

## Files
- `apps/tasks.py` (lines 13, 24)
- Potentially: `core/celery/` config

## Coding Prompt
```
Add Redis-based task locking to prevent concurrent Celery task execution.

1. In apps/tasks.py, implement a Redis lock using celery-once or a manual Redis SET NX pattern:
   - For `update_analytical_db_for_all_orgs`: acquire lock with key "celery:lock:all_orgs", TTL=30min
   - For `update_analytical_db_for_org`: acquire lock with key "celery:lock:org:{org_id}", TTL=10min
   
2. If lock is already held, log a warning and return early (don't raise).

3. Ensure lock is always released in a finally block.

4. Add unit tests for the lock behavior (mock Redis).

Pattern example:
```python
import redis
from core.settings import REDIS_URL

def with_lock(key, ttl, fn):
    r = redis.from_url(REDIS_URL)
    lock = r.lock(key, timeout=ttl)
    if lock.acquire(blocking=False):
        try:
            fn()
        finally:
            lock.release()
    else:
        logger.warning(f"Task {key} already running, skipping")
```
```

## Acceptance Criteria
- [ ] Both Celery tasks skip gracefully if already running
- [ ] Lock TTL is set appropriately per task
- [ ] Unit tests cover lock contention scenario
- [ ] No duplicate analytical DB syncs in production
