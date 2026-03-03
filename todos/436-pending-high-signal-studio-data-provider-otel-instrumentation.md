# TODO-436: Add OpenTelemetry Instrumentation

**Repo:** signal-studio-data-provider  
**Priority:** P1 — Observability  
**Effort:** M (3-4h)  
**Status:** pending

## Task

Add OTEL spans to all DataProvider methods for production tracing and cost attribution.

```python
# In each provider's execute_query():
from opentelemetry import trace
tracer = trace.get_tracer("signal_studio.data_provider")

with tracer.start_as_current_span("data_provider.execute_query") as span:
    span.set_attribute("db.system", "snowflake")  # or postgresql/oracle
    span.set_attribute("db.org_id", org_id)
    span.set_attribute("db.statement", sql[:200])  # truncate for safety
    span.set_attribute("db.row_count", result.row_count)
    span.set_attribute("db.execution_time_ms", result.execution_time_ms)
    if result.cost:
        span.set_attribute("db.cost_credits", result.cost)
```

Add `opentelemetry-api` as optional dep. Core works without it (no-op tracer).

## Acceptance Criteria

- Spans emitted for execute_query, get_schema, write_back
- OTEL is optional — no import error if not installed  
- org_id, timing, row_count attributes present
- SQL truncated to 200 chars in span (never full query for security)
