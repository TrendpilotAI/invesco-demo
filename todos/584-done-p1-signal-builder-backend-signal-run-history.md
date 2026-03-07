# TODO-584 DONE — Signal Execution History Table + API Endpoints

**Completed:** 2026-03-07
**Branch:** feat/p0-todos-352-356
**Commit:** 0d1e650 (included in the HEAD commit with validator caching work)

## What Was Built

### 1. ORM Model — `apps/signals/models/signal_run.py`
- `SignalRun` SQLAlchemy model with:
  - `id` (UUID pk, auto-generated)
  - `signal_id` (FK → signals.id, CASCADE delete)
  - `org_id` (str, indexed)
  - `status` (SignalRunStatus enum: pending/running/success/failed)
  - `started_at` (DateTime, server_default=now)
  - `completed_at`, `duration_ms`, `row_count`, `error_message`, `triggered_by` (all nullable)
- `SignalRunStatus` enum defined in the model file

### 2. Storage — `apps/signals/storages/signal_run.py`
- `SignalRunStorage` with:
  - `create_run(signal_id, org_id, triggered_by)` — creates a run record in `running` status
  - `complete_run(run_id, status, row_count, error_message)` — updates status, computes duration_ms
  - `get_run(run_id, signal_id, org_id)` — org-scoped single run fetch
  - `list_runs(signal_id, org_id, limit, offset)` — returns `PaginatedSignalRunResponse`, most recent first

### 3. Schemas — `apps/signals/schemas/signal_run.py`
- `SignalRunSchema` (Pydantic, from_attributes=True)
- `PaginatedSignalRunResponse` with items, total, limit, offset

### 4. API Endpoints — `apps/signals/routers/signal_run.py`
- `GET /signals/{signal_id}/runs/` — paginated list, org-scoped
- `GET /signals/{signal_id}/runs/{run_id}/` — single run detail, org-scoped
- Both endpoints require authenticated user; org_id taken from `user.organization.id`
- Registered in `routers_v1.py` with tag `signal_runs`

### 5. Signal Execution Recording — `apps/signals/cases/signal.py`
- `publish_signal()` updated to:
  - Create a `running` run record at start (if `signal_run_storage` is wired)
  - Mark `success` on completion
  - Mark `failed` with error_message on `TranslationError` or upstream exception

### 6. Container Wiring — `apps/signals/containers.py`
- `SignalRunStorage` added as singleton
- Passed to `SignalCases` constructor

### 7. Alembic Migration — `db/migrations/versions/2026-03-07__05_05__add_signal_runs_table__.py`
- Creates `signal_runs` table with all columns
- Creates indexes on `signal_id` and `org_id`
- `down_revision = 'd4e5f6a7b8c9'` (webhooks table)
- Uses `gen_random_uuid()` for UUID default

### 8. Tests — 16 passing unit tests
- `tests/signals/test_signal_runs_unit.py` — standalone, no DB required:
  - `TestSignalRunStatus` — enum values
  - `TestSignalRunSchema` — creation, optional fields, round-trip
  - `TestPaginatedSignalRunResponse` — pagination metadata
  - `TestSignalRunLogic` — success path, failure path, org scoping
- `tests/signals/test_signal_runs.py` — mock-based tests for SignalCases integration (for use with full test environment)

## Done Criteria Status
- ✅ signal_runs migration file created
- ✅ Every signal publish creates a run record (success + failure paths)
- ✅ GET /signals/{id}/runs returns paginated history with org scoping enforced
- ✅ Tests cover happy path + failure capture (16 unit tests, all passing)
- ✅ Changes pushed to GitHub (branch: feat/p0-todos-352-356, commit: 0d1e650)
