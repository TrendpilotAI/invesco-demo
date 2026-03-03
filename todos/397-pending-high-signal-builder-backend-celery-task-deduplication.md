# TODO-397: Implement Celery Task Deduplication

**Status:** pending
**Priority:** high
**Repo:** signal-builder-backend
**Effort:** S

## Problem
`apps/tasks.py` lines 13 and 24 have `# TODO: if task is already running -- skip task` comments.
Without deduplication, concurrent Celery workers can process the same signal simultaneously, causing race conditions and inconsistent results.

## Task
Implement task deduplication using Redis-based locking so the same signal task isn't processed concurrently.

## Coding Prompt
```
In apps/tasks.py, implement task deduplication for the signal execution tasks at lines 13 and 24.

Steps:
1. Use Redis (already in dependencies: redis==5.0.1) to implement a distributed lock
2. Key format: `task_lock:{task_name}:{signal_id}`
3. If lock already held, log a warning and return early (skip duplicate)
4. Lock TTL should match expected max task duration (configurable via settings)
5. Use try/finally to ensure lock is always released
6. Add unit test: mock Redis, verify second call to same task is skipped

Reference: core/celery/ for existing celery config and Redis connection setup.
```

## Acceptance Criteria
- Concurrent calls to same task with same signal_id are deduplicated
- Lock is always released (even on exception)
- Configurable TTL in settings
- Unit test confirming skip behavior
