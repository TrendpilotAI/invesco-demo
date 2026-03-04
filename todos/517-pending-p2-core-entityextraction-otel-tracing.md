# TODO-517: OpenTelemetry Tracing

**Repo:** core-entityextraction
**Priority:** P2
**Effort:** M (4h)
**Dependencies:** None
**Blocks:** None

## Description
Add OTEL spans for extraction pipeline stages to debug slow extractions on large texts.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Add opentelemetry-api, opentelemetry-sdk, opentelemetry-instrumentation-fastapi to requirements.txt
2. Configure OTEL exporter via OTEL_EXPORTER_OTLP_ENDPOINT env var
3. Add spans:
   - "entity_extraction.regex" — full regex pipeline
   - "entity_extraction.pattern_build" — pattern compilation
   - "entity_extraction.pattern_match" — matching phase
   - "entity_extraction.ml" — spaCy prediction
   - "entity_extraction.persistence" — DB operations
4. Add trace context propagation headers
5. Graceful no-op if OTEL endpoint not configured
```

## Acceptance Criteria
- [ ] OTEL traces emitted for all extraction stages
- [ ] Configurable via env var
- [ ] No-op when unconfigured
- [ ] No performance impact when disabled
