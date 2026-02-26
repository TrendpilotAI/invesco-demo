---
status: pending
priority: high
issue_id: "017"
tags: [signal-builder-backend, reliability, celery, analytical-db, sync, error-handling]
dependencies: ["013", "016"]
---

# TODO 017 — Analytical DB Sync Reliability Improvements

**Status:** pending  
**Priority:** high  
**Repo:** signal-builder-backend  
**Effort:** L (3-5 days)

## Problem Statement

The analytical DB synchronization is a critical background process that keeps the analytical database in sync with the primary database. Current risks:

1. **No retry logic** — if sync fails mid-way, it fails silently
2. **No partial progress tracking** — sync restarts from scratch on retry
3. **No sync status visible to users** — front-end has no way to show sync state
4. **No alerting on sync failures** — engineering doesn't know when sync breaks
5. **Concurrent sync possible** — the `# TODO: if task is already running -- skip task` comment shows this is unresolved
6. **Schema recreation risk** — `should_recreate_schema=True` can wipe analytical data on bug

## Findings

- `apps/tasks.py` has `update_analytical_db_for_all_orgs` and `update_analytical_db_for_org`
- `apps/analytical_db/cases/analytical_db_sync_cases.py` has sync logic
- Both tasks have inline `# TODO: if task is already running -- skip task` comments
- `backoff = "*"` is in Pipfile but likely not applied to sync operations
- No sync status model or table exists

## Proposed Solutions

### Option A: Celery retry + sync status table (Recommended)
Add Celery retry with exponential backoff, create a `SyncJob` model to track progress, expose status via API.

**Pros:** Full visibility and reliability  
**Cons:** DB schema change required

### Option B: Celery retry only
Just add `.retry()` calls without status tracking.

**Pros:** Quick  
**Cons:** No user visibility, hard to debug

**Recommendation:** Option A — status tracking is needed for production quality.

## Coding Prompt

```
You are improving the reliability of the analytical DB sync process in signal-builder-backend.

Repository: /data/workspace/projects/signal-builder-backend/
Stack: Celery, SQLAlchemy 2.0, FastAPI, Redis

TASK: Add retry logic, sync status tracking, and failure alerting.

PART 1: Celery Task Reliability

1. Update apps/tasks.py:

   @celery_app.task(
       bind=True,
       max_retries=3,
       default_retry_delay=60,  # 60s base, exponential backoff
       acks_late=True,           # Don't ack until task completes
       reject_on_worker_lost=True,
   )
   @inject
   def update_analytical_db_for_org(
       self,  # bind=True provides self for retry
       org_id: int,
       sync_job_id: int,  # NEW: track in DB
       should_recreate_schema: bool = False,
       ...
   ):
       try:
           # Update sync job status to RUNNING
           run_coroutine(sync_cases.update_sync_job_status(sync_job_id, "running"))
           run_coroutine(sync_cases.run_synchronization_for_org(org_id, should_recreate_schema))
           run_coroutine(sync_cases.update_sync_job_status(sync_job_id, "completed"))
       except Exception as exc:
           run_coroutine(sync_cases.update_sync_job_status(
               sync_job_id, "failed", error=str(exc)
           ))
           # Retry with exponential backoff using backoff library
           raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

2. Guard against should_recreate_schema misuse:
   - Add validation: should_recreate_schema=True requires explicit admin flag
   - Log a WARNING when should_recreate_schema=True is used
   - Require ALLOW_SCHEMA_RECREATE env var to be "true" as additional safety gate

PART 2: Sync Job Status Model

3. Create apps/analytical_db/models/sync_job.py:
   class SyncJob(Base):
       __tablename__ = "analytical_db_sync_jobs"
       
       id: int (primary key)
       org_id: int (FK → orgs, indexed)
       status: str  # pending | running | completed | failed
       started_at: datetime
       completed_at: datetime (nullable)
       error_message: str (nullable, text)
       rows_synced: int (nullable)
       celery_task_id: str (nullable, for cross-referencing)
       created_at: datetime (auto-now)
       
       Index: (org_id, status), (org_id, created_at DESC)

4. Create Alembic migration:
   pipenv run alembic revision --autogenerate -m "add_analytical_db_sync_jobs_table"
   Review and apply: pipenv run alembic upgrade head

5. Add SyncJob cases in apps/analytical_db/cases/:
   - create_sync_job(org_id: int) -> SyncJob
   - update_sync_job_status(sync_job_id: int, status: str, error: str = None)
   - get_latest_sync_job(org_id: int) -> Optional[SyncJob]
   - get_sync_job_history(org_id: int, limit: int = 10) -> List[SyncJob]

PART 3: Sync Status API Endpoint

6. Add endpoint in apps/analytical_db/routers/:

   GET /analytical-db/sync/status:
   - Returns latest sync job for the authenticated user's org
   - Response: {status, started_at, completed_at, error_message, rows_synced}
   
   GET /analytical-db/sync/history:
   - Returns last 10 sync jobs for the org
   - Useful for debugging intermittent failures

   POST /analytical-db/sync/trigger:
   - Creates a SyncJob record (status=pending)
   - Enqueues update_analytical_db_for_org Celery task
   - Returns: {sync_job_id, status: "pending"}
   - Rate limit: 1 per minute per org (prevent spam)

PART 4: Failure Alerting

7. In the task except handler, after max retries exhausted:
   - Log ERROR with full exception trace
   - If Sentry is configured (TODO 013), it will auto-capture
   - Optionally: send email alert to org admin (use existing email infrastructure if any)

8. Add sync job age alert:
   - Celery beat task: check_stale_sync_jobs (runs every 30 min)
   - Alert if any org has no successful sync in last 24h
   - Log WARNING: "Org {org_id} has not synced successfully in {hours}h"

PART 5: Tests

9. Create tests/analytical_db/test_sync_reliability.py:
   - Test retry: task retries on transient exception
   - Test max retries: task fails and marks job as failed after 3 retries
   - Test status transitions: pending → running → completed
   - Test status transitions: pending → running → failed
   - Test concurrent guard: second task call is skipped if lock held
   - Mock DB and Celery

10. Run: python -m pytest tests/analytical_db/ -v

Constraints:
- should_recreate_schema=True must require explicit env var guard
- Sync jobs older than 30 days may be purged (add cleanup cron task)
- SyncJob table must not grow unbounded — enforce 100-job retention per org
- Retry countdown must be exponential (not fixed) to avoid thundering herd
- Task ID (Celery UUID) stored in SyncJob for cross-reference with Flower
```

## Acceptance Criteria

- [ ] Celery tasks have `max_retries=3` with exponential backoff
- [ ] `analytical_db_sync_jobs` table created via Alembic migration
- [ ] SyncJob status transitions: pending → running → completed/failed
- [ ] Error message stored in SyncJob on failure
- [ ] `GET /analytical-db/sync/status` returns current sync status
- [ ] `POST /analytical-db/sync/trigger` creates job and enqueues task
- [ ] `should_recreate_schema=True` requires `ALLOW_SCHEMA_RECREATE=true` env var
- [ ] Stale sync detection task alerts on orgs without sync in 24h
- [ ] `tests/analytical_db/test_sync_reliability.py` passes
- [ ] Inline `# TODO: if task is already running -- skip task` resolved

## Dependencies

- TODO 013 (Sentry) — failure alerting is enhanced by Sentry integration. Not a hard blocker.
- TODO 016 (Flower) — task lock mechanism from TODO 016 is reused here. Implement TODO 016 first.

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Found 2 inline `# TODO: if task is already running -- skip task` comments in tasks.py
- Identified `should_recreate_schema=True` as data-loss risk
- Designed SyncJob model for full visibility into sync history
- Scoped retry to max_retries=3 with exponential backoff using `backoff` (already in Pipfile)

**Learnings:**
- `backoff` is already in Pipfile but likely unused — apply to sync operations
- Celery `acks_late=True` + `reject_on_worker_lost=True` is critical for at-least-once delivery
