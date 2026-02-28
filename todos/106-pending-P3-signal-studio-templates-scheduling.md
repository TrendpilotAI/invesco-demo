# TODO 106 — Template Scheduling (Recurring Signals) (P3)

**Repo:** signal-studio-templates  
**Priority:** P3  
**Effort:** L (3-5 days)  
**Status:** pending

---

## Autonomous Coding Prompt

```
Add template scheduling to /data/workspace/projects/signal-studio-templates/

This extends the library with a ScheduledTemplate concept — run a template on a cron
schedule and deliver results via webhook or email.

SCHEMA ADDITIONS (schema/signal-template.ts):
  export interface ScheduledRun {
    id: string;
    templateId: string;
    parameters: Record<string, any>;
    schedule: string; // cron expression e.g. "0 9 * * 1" (Monday 9am)
    timezone: string; // "America/New_York"
    deliveryWebhook?: string; // POST results here
    deliveryEmail?: string[];
    lastRunAt?: Date;
    nextRunAt?: Date;
    enabled: boolean;
  }

ENGINE ADDITIONS (engine/schedule-engine.ts):
  class ScheduleEngine {
    constructor(engine: TemplateEngine, store: ScheduleStore) {}
    
    async schedule(config: Omit<ScheduledRun, 'id' | 'lastRunAt' | 'nextRunAt'>): Promise<ScheduledRun>
    async unschedule(id: string): Promise<void>
    async listSchedules(templateId?: string): Promise<ScheduledRun[]>
    async runNow(id: string): Promise<ExecutionResult>
    async tick(): Promise<void> // call from cron job — runs due schedules
  }

  export interface ScheduleStore {
    save(schedule: ScheduledRun): Promise<void>
    load(id: string): Promise<ScheduledRun | null>
    listDue(now: Date): Promise<ScheduledRun[]>
    listAll(templateId?: string): Promise<ScheduledRun[]>
    delete(id: string): Promise<void>
  }

API ADDITIONS (api/schedules.ts):
  POST /templates/:id/schedule — create schedule
  DELETE /schedules/:id — delete schedule
  GET /schedules — list all schedules
  POST /schedules/:id/run — trigger immediate run

DELIVERY:
  After each tick(), if deliveryWebhook set: POST result as JSON
  If deliveryEmail set: format as HTML table, send via email provider interface

Keep ScheduleStore as an interface — consumer provides implementation (Postgres, Redis, etc.)
```

## Acceptance Criteria
- [ ] ScheduledRun schema defined
- [ ] ScheduleEngine implemented with tick() method
- [ ] API routes added
- [ ] Unit tests for schedule creation and tick()
- [ ] Store interface documented

## Dependencies
- TODO 100, 101, 102 must be complete first
