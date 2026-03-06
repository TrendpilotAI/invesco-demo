# TODO-639: Create signal_runs Persistence Table

**Priority:** P1  
**Effort:** S (4hrs)  
**Repo:** signal-studio  
**Category:** Data / Compliance  

## Problem

Signal executions are fire-and-forget. No database record is created when a signal runs. This is:
- A **compliance gap** (no audit trail — SOC2 blocker)
- A **UX gap** (users can't see run history)
- A **debugging gap** (no way to inspect failed runs)

## Task Description

1. Create SQL migration for `signal_runs` table
2. Insert record in `/api/signals/run/route.ts` on each execution
3. Create GET endpoint for signal run history
4. Add run history UI component to signal detail page

## Coding Prompt (Autonomous Execution)

```sql
-- Create in scripts/migrations/002-signal-runs.sql
CREATE TABLE IF NOT EXISTS signal_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  signal_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('running', 'success', 'error')),
  input_params JSONB,
  result_summary JSONB,
  error_message TEXT,
  duration_ms INTEGER,
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_signal_runs_signal_id ON signal_runs(signal_id);
CREATE INDEX idx_signal_runs_user_id ON signal_runs(user_id);
CREATE INDEX idx_signal_runs_started_at ON signal_runs(started_at DESC);
```

Then in `app/api/signals/run/route.ts`:
- Before executing: INSERT with status='running'
- On success: UPDATE with status='success', result_summary, duration_ms, completed_at
- On error: UPDATE with status='error', error_message, completed_at

Add `app/api/signals/[id]/runs/route.ts` GET endpoint returning paginated run history.

## Acceptance Criteria

- [ ] Migration SQL file created and documented
- [ ] Every signal execution creates a row in signal_runs
- [ ] Failed runs record error_message
- [ ] GET /api/signals/:id/runs returns paginated history (limit 20, cursor-based)
- [ ] Signal detail page shows last 5 runs with status + timestamp

## Dependencies

None. But pairs well with TODO-638 (health check should verify signal_runs table accessible).
