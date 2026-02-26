---
status: pending
priority: medium
issue_id: "016"
tags: [signal-builder-backend, celery, monitoring, flower, observability, railway]
dependencies: ["013"]
---

# TODO 016 — Celery Task Monitoring with Flower

**Status:** pending  
**Priority:** medium  
**Repo:** signal-builder-backend  
**Effort:** S (0.5-1 day)

## Problem Statement

Celery workers run analytical DB sync tasks in the background. There is no visibility into:
- Currently running tasks
- Failed tasks and error messages  
- Task queue depth (backlog)
- Worker health and concurrency
- Historical task duration and failure rate

The existing code even has TODOs acknowledging this gap:
```python
# TODO: if task is already running -- skip task
```

Without monitoring, duplicate task execution, hung workers, and queue backlogs go undetected until users report sync failures.

## Findings

- `core/celery.py` defines the Celery app
- `apps/tasks.py` has `update_analytical_db_for_all_orgs` and `update_analytical_db_for_org`
- `bitbucket-pipelines.yml` and `railway.json` manage deployments
- Redis is used as Celery broker
- Flower is the standard Celery monitoring dashboard

## Proposed Solutions

### Option A: Flower as Railway Service (Recommended)
Add Flower as a separate Railway service, password-protected, behind the existing deployment.

**Pros:** Real-time dashboard, no code changes, standard tool  
**Cons:** Exposes task data — needs auth

### Option B: Custom /admin/celery endpoint
Build a minimal status endpoint into the FastAPI app using `celery.control.inspect()`.

**Pros:** Integrated with existing app  
**Cons:** More code, less feature-rich than Flower

**Recommendation:** Option A — Flower + password auth is production-ready in minutes. Add task instrumentation in Option B style as supplementary.

## Coding Prompt

```
You are adding Celery task monitoring to signal-builder-backend.

Repository: /data/workspace/projects/signal-builder-backend/
Stack: Celery, Redis, FastAPI, Railway deployment

TASK: Deploy Flower for Celery monitoring + add task instrumentation.

PART 1: Flower Setup

1. Add to Pipfile [packages]:
   flower = "*"

2. Add Pipfile script:
   [scripts]
   flower = "celery -A core.celery.celery_app flower --port=5555 --basic_auth=${FLOWER_USER}:${FLOWER_PASSWORD}"

3. Create docker/flower.dockerfile (for Railway):
   FROM python:3.11-slim
   WORKDIR /app
   COPY Pipfile Pipfile.lock ./
   RUN pip install pipenv && pipenv install --system --deploy
   COPY . .
   CMD ["celery", "-A", "core.celery.celery_app", "flower",
        "--port=5555",
        "--basic_auth=${FLOWER_USER}:${FLOWER_PASSWORD}",
        "--broker_api=redis://:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}/0",
        "--persistent=True",
        "--db=/tmp/flower.db"]

4. Add environment variables (document in README):
   FLOWER_USER=admin
   FLOWER_PASSWORD=<strong-random-password>

PART 2: Task Instrumentation

5. Update apps/tasks.py to add task deduplication:
   import hashlib
   from redis import Redis

   def _is_task_running(redis_client: Redis, task_key: str) -> bool:
       return redis_client.exists(f"celery_lock:{task_key}") > 0
   
   def _acquire_task_lock(redis_client: Redis, task_key: str, ttl: int = 3600) -> bool:
       return redis_client.set(f"celery_lock:{task_key}", "1", ex=ttl, nx=True)
   
   def _release_task_lock(redis_client: Redis, task_key: str):
       redis_client.delete(f"celery_lock:{task_key}")

   In update_analytical_db_for_all_orgs:
   - Acquire lock "all_orgs" before running
   - Skip if lock exists (resolve the TODO comment)
   - Release lock in finally block

   In update_analytical_db_for_org:
   - Acquire lock f"org_{org_id}" before running
   - Skip if lock exists
   - Release lock in finally block

6. Add task result tracking:
   In core/celery.py:
   - Set result_backend = settings.REDIS_URL
   - Enable task_track_started = True
   - Enable task_send_sent_event = True
   - Set task_acks_late = True (retry on worker crash)

7. Create apps/analytical_db/routers/ endpoint: GET /admin/celery/status
   - Requires admin auth
   - Returns: active tasks, reserved tasks, scheduled tasks
   - Uses: celery_app.control.inspect().active()
   - Response schema:
     {
       "active_tasks": [...],
       "reserved_tasks": [...],
       "worker_stats": {...},
       "queue_length": 0
     }

8. Add task duration logging:
   In each Celery task, wrap with timing:
   start = time.time()
   try:
       ... task body ...
   finally:
       duration = time.time() - start
       logger.info(f"Task {task_name} completed in {duration:.2f}s for org_id={org_id}")

9. Create tests/test_celery_tasks.py:
   - Test deduplication: second call skipped when lock held
   - Test lock released on success
   - Test lock released on failure (finally block)
   - Mock Redis lock operations

10. Update README.md:
    - Flower access URL and credentials setup
    - How to monitor tasks in development (flower --url-prefix=/flower)
    - Alert thresholds (queue depth > 100, task failures)

Constraints:
- Flower must be password-protected (FLOWER_USER + FLOWER_PASSWORD env vars required)
- Task locks must have TTL (no infinite lock on worker crash)
- Lock TTL must be longer than max expected task duration
- Admin status endpoint must require admin permission (not user-level auth)
```

## Acceptance Criteria

- [ ] `flower` added to Pipfile
- [ ] `pipenv run flower` starts Flower dashboard on port 5555
- [ ] Flower is password-protected via env vars
- [ ] Task deduplication locks implemented for all Celery tasks
- [ ] Lock always released in `finally` block (crash-safe)
- [ ] `GET /admin/celery/status` endpoint returns task queue status
- [ ] Task duration logged with loguru on completion
- [ ] `tests/test_celery_tasks.py` verifies deduplication behavior
- [ ] README updated with Flower access instructions
- [ ] Existing `# TODO: if task is already running` comment resolved

## Dependencies

- TODO 013 (Sentry) — task failures should be reported to Sentry. Implement after 013 or add Sentry capture in the except block here.

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Found `# TODO: if task is already running -- skip task` inline in tasks.py
- Scoped to Flower + task deduplication as high-impact quick wins
- Designed Redis-based task lock with TTL for crash safety

**Learnings:**
- Task locks must use `nx=True` (atomic set-if-not-exists) to prevent race conditions
- TTL on lock keys is critical — worker crashes leave locks held without TTL
