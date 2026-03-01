# TODO-358: Add OpenTelemetry Tracing via @vercel/otel

**Priority:** P1
**Effort:** M
**Repo:** signal-studio
**Status:** pending

## Description
No observability in production. Can't debug latency issues, Oracle query performance, or AI call failures. Blind in production is risky for a financial platform.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Install: pnpm add @vercel/otel @opentelemetry/sdk-trace-node

2. Create instrumentation.ts in project root:
```typescript
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel({
    serviceName: 'signal-studio',
    traceExporter: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ? 'otlp' : 'console',
  })
}
```

3. Add OTEL env vars to .env.example:
   OTEL_EXPORTER_OTLP_ENDPOINT=
   OTEL_SERVICE_NAME=signal-studio

4. Add custom spans to critical paths in lib/:
```typescript
import { trace } from '@opentelemetry/api'
const tracer = trace.getTracer('signal-studio')

// Wrap Oracle queries:
const span = tracer.startSpan('oracle.query', { attributes: { 'db.statement': sql.slice(0, 100) } })
try {
  const result = await executeOracleQuery(sql)
  span.setStatus({ code: SpanStatusCode.OK })
  return result
} catch (e) {
  span.recordException(e as Error)
  span.setStatus({ code: SpanStatusCode.ERROR })
  throw e
} finally {
  span.end()
}
```

5. Instrument: Oracle queries, AI/LLM calls, signal execution, auth middleware

6. Commit: "feat(observability): add OpenTelemetry tracing via @vercel/otel"
```

## Dependencies
- TODO-353 (structured logging should come first)

## Acceptance Criteria
- instrumentation.ts exists and registered
- Oracle queries traced with spans
- AI/LLM calls traced  
- Traces visible in console (dev) or OTLP endpoint (prod)
- No performance regression
