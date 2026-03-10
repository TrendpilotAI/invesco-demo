# TODO-829: OpenTelemetry Distributed Tracing

**Repo:** signal-builder-backend  
**Priority:** HIGH  
**Effort:** M (2 days)  
**Status:** pending

## Problem

No distributed tracing across the signal execution pipeline (FastAPI → SQL translation → Celery → DB). Debugging Invesco signal failures requires log tailing across multiple systems. OpenTelemetry would give end-to-end trace visibility.

## Solution

1. Add OTEL SDK + auto-instrumentation for FastAPI, SQLAlchemy, Celery
2. Configure OTLP exporter (Honeycomb or Grafana Tempo — check which Nathan prefers)
3. Add custom spans around `transform_signal_nodes_to_sql()` (the hot path)
4. Add custom attributes: `signal_id`, `org_id`, `node_count` to traces

## Coding Prompt

```bash
# Add to Pipfile:
opentelemetry-sdk = ">=1.20"
opentelemetry-instrumentation-fastapi = "*"
opentelemetry-instrumentation-sqlalchemy = "*"
opentelemetry-instrumentation-celery = "*"
opentelemetry-exporter-otlp-proto-http = "*"
```

```python
# core/telemetry.py (new file):
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor

def setup_telemetry(app, engine):
    provider = TracerProvider()
    exporter = OTLPSpanExporter(endpoint=settings.OTEL_ENDPOINT)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    
    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=engine)
    CeleryInstrumentor().instrument()

# In apps/translators/main.py, wrap the hot path:
tracer = trace.get_tracer(__name__)

def transform_signal_nodes_to_sql(signal_nodes, org_id):
    with tracer.start_as_current_span("sql_translation") as span:
        span.set_attribute("node_count", len(signal_nodes))
        span.set_attribute("org_id", org_id)
        # ... existing translation logic
```

Add `OTEL_ENDPOINT` and `OTEL_SERVICE_NAME=signal-builder-backend` to `.env.example`.

## Acceptance Criteria
- Traces visible in configured OTEL backend for signal run requests
- `transform_signal_nodes_to_sql` shows as child span with node_count attribute
- Celery tasks appear as linked spans
- `OTEL_ENDPOINT` defaults to disabled (no-op exporter) if not set
- No performance regression in tests (OTEL overhead < 5ms p99)
