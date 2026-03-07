# TODO-822: Fix Celery Task Idempotency

**Repo**: signal-builder-backend  
**Priority**: CRITICAL  
**Effort**: Low-Medium (3-5 hours)

## Problem
`apps/tasks.py:13,24` has TODOs noting that if a signal task is already running, it should be skipped. Without this, concurrent triggers cause duplicate signal_run records and potential data corruption.

## Task
1. Add Redis distributed lock at start of each signal Celery task
2. Lock key: `signal_task_lock:{signal_id}`
3. If lock exists: log warning, return early (do not error)
4. If lock acquired: execute task, release lock in `finally` block
5. Set lock TTL to max expected task duration (e.g., 10 minutes)

```python
from redis import Redis
r = Redis.from_url(settings.REDIS_URL)

def execute_signal_task(signal_id, ...):
    lock_key = f"signal_task_lock:{signal_id}"
    with r.lock(lock_key, timeout=600, blocking=False) as lock:
        if not lock:
            logger.warning(f"Signal {signal_id} task already running, skipping")
            return
        # ... existing task logic
```

## Acceptance Criteria
- Concurrent task triggers for same signal_id result in only one execution
- Tests verify idempotency behavior
- No orphaned signal_run records on concurrent trigger
