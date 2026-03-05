# TODO-584: Signal Execution History Table + API Endpoints

**Priority:** P1 (High Value)
**Repo:** signal-builder-backend
**Effort:** M (4-8 hours)
**Status:** Pending

## Problem
No `signal_runs` table exists. Clients cannot see historical execution results, debug failures, or track performance trends over time.

## Task
1. Create `signal_runs` table with: id, signal_id, org_id, status, started_at, completed_at, duration_ms, row_count, error_message, triggered_by
2. Write a run record on every signal execution (success and failure)
3. Add API endpoints:
   - `GET /signals/{id}/runs` — paginated run history
   - `GET /signals/{id}/runs/{run_id}` — individual run details
4. Add to admin panel

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend/:

1. Create Alembic migration for signal_runs table:
   pipenv run auto_migration "add_signal_runs_table"
   Columns: id (pk), signal_id (fk→signals), org_id, status (enum: pending/running/success/failed),
            started_at (timestamp), completed_at (timestamp), duration_ms (int),
            row_count (int, nullable), error_message (text, nullable), triggered_by (str)

2. Create ORM model: apps/signals/models/signal_run.py
3. Create storage: apps/signals/storages/signal_run.py
4. Update apps/signals/cases/signal.py to write signal_run records around execution
5. Add router endpoints in apps/signals/routers_v1.py:
   GET /signals/{id}/runs (paginated, most recent first)
   GET /signals/{id}/runs/{run_id}
6. Add tests for the new endpoints
```

## Acceptance Criteria
- [ ] signal_runs table created via migration
- [ ] Every signal execution creates a run record (success + failure)
- [ ] GET /signals/{id}/runs returns paginated history
- [ ] Org scoping enforced on run access
- [ ] Tests cover happy path + failure capture
