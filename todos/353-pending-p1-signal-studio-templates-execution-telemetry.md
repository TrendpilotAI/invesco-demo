# TODO 353: Add Template Execution Telemetry

**Repo:** signal-studio-templates  
**Priority:** P1 (Revenue enablement — usage-based billing)  
**Effort:** M (4-6 hours)  
**Status:** pending

---

## Problem / Opportunity

There is currently no tracking of which templates are executed, by whom, how often, or how fast. This data is essential for:
- Usage-based billing (Invesco SLA reporting)
- Product analytics (which templates are most valuable)
- Performance monitoring
- Future per-seat or per-execution pricing

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates/engine/template-engine.ts:

1. Add telemetry hook to TemplateEngine.execute():
   - Before execution: record start time
   - After execution: write to telemetry store
   
2. Create types/telemetry.ts:
   interface TemplateExecutionRecord {
     id: string;           // uuid
     template_id: string;
     tenant_id?: string;
     user_id?: string;
     parameters: Record<string, unknown>;
     param_hash: string;   // sha256 of JSON.stringify(parameters)
     row_count: number;
     execution_time_ms: number;
     had_ai_talking_points: boolean;
     timestamp: Date;
     error?: string;
   }

3. Create utils/telemetry.ts with:
   - TelemetryStore interface (pluggable — DB, console, or noop)
   - ConsoleTelemetryStore (default, for development)
   - DatabaseTelemetryStore (writes to signal_template_executions table)

4. TemplateEngine constructor should accept optional TelemetryStore

5. Add the DB schema migration SQL in schema/migrations/001_telemetry.sql

6. Add tests in __tests__/telemetry.test.ts verifying execution records are written.
```

## Acceptance Criteria

- [ ] TemplateEngine records execution telemetry on every execute() call
- [ ] TelemetryStore is pluggable (noop / console / DB)
- [ ] DatabaseTelemetryStore writes correct records
- [ ] Tests cover telemetry capture including error cases
- [ ] No performance regression (telemetry is async/non-blocking)

## Dependencies

- TODO 351 (SQL fix) should be done first
- TODO 352 (ESM build) can be parallel
