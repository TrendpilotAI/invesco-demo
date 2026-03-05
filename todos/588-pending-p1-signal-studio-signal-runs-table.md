# TODO-588: Create signal_runs Postgres table + run history UI

**Repo:** signal-studio
**Priority:** P1
**Effort:** M (half day)
**Status:** pending

## Problem
Every signal execution is ephemeral — no history stored. This is a compliance gap and UX issue.
Users can't see past runs, debug failures, or audit what ran when.

## Task
1. Add migration to create `signal_runs` table in Postgres
2. Wire `/api/signals/run` route to INSERT a row on each execution
3. Add GET `/api/signals/[id]/runs` endpoint
4. Show run history in signal detail drawer/panel

## Coding Prompt
```
In /data/workspace/projects/signal-studio:
1. Create migration file scripts/migrations/001-signal-runs.sql:
   CREATE TABLE IF NOT EXISTS signal_runs (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     signal_id TEXT NOT NULL,
     user_id TEXT NOT NULL,
     status TEXT NOT NULL CHECK (status IN ('pending','running','completed','failed')),
     result JSONB,
     error TEXT,
     duration_ms INT,
     created_at TIMESTAMPTZ DEFAULT now(),
     updated_at TIMESTAMPTZ DEFAULT now()
   );
   CREATE INDEX idx_signal_runs_signal_id ON signal_runs(signal_id);
   CREATE INDEX idx_signal_runs_user_id ON signal_runs(user_id);
   CREATE INDEX idx_signal_runs_created_at ON signal_runs(created_at DESC);

2. Update app/api/signals/run/route.ts to:
   - INSERT pending row before execution
   - UPDATE to completed/failed with result/error after
   - Return run_id in response

3. Create app/api/signals/[id]/runs/route.ts → SELECT last 20 runs for signal
4. Add RunHistory component showing status, duration, timestamp, result preview
5. Wire into signal detail view
```

## Acceptance Criteria
- [ ] Migration runs cleanly against Postgres
- [ ] Each signal run creates a row
- [ ] Status updates (pending→running→completed/failed)
- [ ] Run history visible in UI
- [ ] API returns 200 with runs array

## Dependencies
- Postgres credentials in `.env.local`
