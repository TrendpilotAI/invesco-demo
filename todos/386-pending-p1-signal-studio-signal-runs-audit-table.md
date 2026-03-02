# TODO-386: Add signal_runs Audit Table for Execution History

**Repo:** signal-studio
**Priority:** P1 (compliance + UX)
**Effort:** M (1-2 days)
**Status:** pending
**Audit ref:** NEW-002

## Description
Signal executions produce results but nothing is persisted. No audit trail, no history UI, no debugging capability. For a financial platform this is a compliance gap and a product gap — users want to see their signal history.

## Task
1. Create Postgres migration: `signal_runs` table
2. Update `/api/signals/run` to persist run record (before + after execution)
3. Create `/api/signals/[id]/runs` GET endpoint (paginated history)
4. Add "Run History" tab to signal detail drawer in UI
5. Show: timestamp, status, duration, result summary, error if failed

## Schema
```sql
CREATE TABLE signal_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  signal_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending','running','completed','failed')),
  params JSONB,
  result JSONB,
  error TEXT,
  duration_ms INT,
  created_at TIMESTAMPTZ DEFAULT now(),
  completed_at TIMESTAMPTZ
);
CREATE INDEX ON signal_runs (signal_id, created_at DESC);
CREATE INDEX ON signal_runs (user_id, created_at DESC);
```

## Coding Prompt (autonomous execution)
```
In /data/workspace/projects/signal-studio/:
1. Create scripts/migrations/002-signal-runs.sql with schema above
2. In app/api/signals/run/route.ts:
   - Before execution: INSERT signal_run with status='running', get run_id
   - After success: UPDATE run SET status='completed', result=..., duration_ms=...
   - On error: UPDATE run SET status='failed', error=...
3. Create app/api/signals/[id]/runs/route.ts:
   - GET with pagination (limit/offset query params)
   - Return runs sorted by created_at DESC
4. In signal detail component, add "History" tab showing run list
5. Add test: __tests__/api/signal-runs.test.ts
```

## Acceptance Criteria
- [ ] Migration SQL created and documented
- [ ] Every signal run is persisted to DB
- [ ] History API returns paginated results
- [ ] UI shows run history tab
- [ ] Failed runs show error message

## Dependencies
TODO-384 (fix build errors first for clean TS)
