# TODO-827: Signal Scheduling via Celery Beat

**Repo:** signal-builder-backend  
**Priority:** HIGH  
**Effort:** L (3-4 days)  
**Status:** pending  
**Dependencies:** TODO-826 (fix optional storage params first)

## Problem

Signals can only be run manually via API. Invesco use case requires signals to run automatically on schedules (daily close prices, weekly portfolio updates). No scheduling mechanism exists.

## Proposed Solution

1. **DB migration:** Add `schedule` field to `signals` table:
   ```sql
   schedule_cron VARCHAR(100) NULL,  -- e.g. "0 18 * * 1-5" (weekdays at 6pm ET)
   schedule_enabled BOOLEAN DEFAULT FALSE,
   schedule_timezone VARCHAR(50) DEFAULT 'America/New_York',
   last_scheduled_run_at TIMESTAMP WITH TIME ZONE NULL,
   ```

2. **Celery Beat dynamic schedule:** Add a beat task `sync_signal_schedules` that runs every 60s and dynamically updates the Celery Beat schedule from the database:
   ```python
   @celery_app.on_after_configure.connect
   def setup_periodic_tasks(sender, **kwargs):
       sender.add_periodic_task(60.0, sync_signal_schedules.s(), name='sync-schedules')
   ```

3. **Celery task:** `run_scheduled_signal(signal_id, org_id)` — runs the signal and records the run in `signal_run`.

4. **API endpoints:**
   - `PATCH /v1/signals/{id}/schedule` — set cron expression + enable/disable
   - Validate cron expression using `croniter` library

5. **Admin panel:** Add schedule toggle/cron field to sqladmin signal view.

## Coding Prompt

```
In apps/signals/:
1. Add migration: alembic revision --autogenerate -m "add signal scheduling fields"
   Fields: schedule_cron (nullable varchar), schedule_enabled (bool), schedule_timezone (varchar), last_scheduled_run_at (timestamptz)

2. Add to Signal SQLAlchemy model (apps/signals/models/signal.py)

3. Create apps/signals/tasks/scheduler.py with:
   - sync_signal_schedules() Celery task
   - run_scheduled_signal(signal_id: str, org_id: str) Celery task
   Both decorated with @celery_app.task

4. Add PATCH /v1/signals/{id}/schedule endpoint in apps/signals/routers/
   Accepts: {"cron": "0 18 * * 1-5", "enabled": true, "timezone": "America/New_York"}
   Validate cron with: from croniter import croniter; croniter.is_valid(cron)

5. Add croniter to Pipfile

6. Write tests: tests/test_signal_scheduling.py
   - test_set_schedule_valid_cron
   - test_set_schedule_invalid_cron_returns_422
   - test_disable_schedule
```

## Acceptance Criteria
- Signals can have a cron schedule set/unset via API
- Celery Beat picks up enabled schedules within 60 seconds
- `signal_run` records are created for scheduled runs
- Invalid cron expressions return HTTP 422
- Tests cover happy path and invalid input
