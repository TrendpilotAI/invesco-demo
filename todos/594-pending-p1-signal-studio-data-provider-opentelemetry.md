# TODO 594 — OpenTelemetry tracing for all providers

**Repo:** signal-studio-data-provider  
**Priority:** P1 (Observability)  
**Effort:** M (1 day)  
**Dependencies:** None

## Task Description
Add OpenTelemetry spans to `execute_query`, `get_schema`, `execute_signal`, and `write_back` across all providers. Emit span attributes: org_id, provider_type, row_count, execution_time_ms, cost (Snowflake credits).

## Autonomous Agent Prompt
```
In /data/workspace/projects/signal-studio-data-provider/:

1. Add opentelemetry-api to pyproject.toml dependencies (optional group):
   [project.optional-dependencies]
   otel = ["opentelemetry-api>=1.20", "opentelemetry-sdk>=1.20"]

2. Create utils/tracing.py:
   - `get_tracer()` returns `opentelemetry.trace.get_tracer("signal_studio_data_provider")`
   - `noop_span()` context manager for when OTEL not configured

3. In each provider (snowflake_provider.py, supabase_provider.py, oracle_provider.py):
   - Wrap execute_query with span: attributes org_id, sql_preview (first 100 chars), row_count, execution_time_ms
   - Wrap get_schema with span: org_id, table_count
   - Wrap execute_signal with span: signal_id, org_id
   - For Snowflake: add cost attribute (credits used)

4. Add pyproject.toml optional group `otel`; fall back gracefully if opentelemetry not installed.

Run pytest tests/ to verify (OTEL not required in tests — should be no-op when not configured).
```

## Acceptance Criteria
- [ ] All provider methods have OTEL spans
- [ ] Span attributes include org_id, timing, row counts
- [ ] Works without OTEL installed (optional dependency, graceful no-op)
- [ ] Tests pass without OTEL installed
