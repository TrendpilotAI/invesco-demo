# 230 · NarrativeReactor · Observability — Structured Logging & Tracing

**Status:** pending  
**Priority:** medium  
**Project:** NarrativeReactor  
**Created:** 2026-02-27

---

## Task Description

NarrativeReactor uses console.log/warn scattered everywhere. No structured logging, no request IDs, no distributed tracing across LLM calls. Add pino for structured JSON logging + request correlation IDs + basic OpenTelemetry spans for flow execution timing.

---

## Coding Prompt (agent-executable)

```
Working in /data/workspace/projects/NarrativeReactor/src/:

1. Install: npm i pino pino-http uuid
            npm i -D @types/uuid pino-pretty

2. Create src/lib/logger.ts:
   import pino from 'pino';
   export const logger = pino({
     level: process.env.LOG_LEVEL || 'info',
     ...(process.env.NODE_ENV !== 'production' && { transport: { target: 'pino-pretty' } }),
   });
   export function childLogger(context: Record<string, unknown>) { return logger.child(context); }

3. Add request ID middleware in src/middleware/requestId.ts:
   - Generate UUID v4 per request
   - Set X-Request-ID response header
   - Attach req.requestId for downstream use

4. Add pino-http middleware in src/index.ts:
   import pinoHttp from 'pino-http';
   app.use(pinoHttp({ logger, customProps: (req) => ({ requestId: req.requestId }) }));

5. Replace key console.log calls with structured logger calls:
   - All flows (content-generation, orchestration, integrations, compliance)
   - costTracker service (log each LLM call with cost + model + tokens)
   - publisher services (log each publish attempt with platform + postId)

6. Add flow execution timing:
   - Wrap Genkit flow calls with logger.info({ flowName, durationMs, inputHash })
   - Log LLM model used, token counts, cost estimate per call

7. Update /health endpoint to return logLevel + nodeVersion

8. Add LOG_LEVEL to .env.example
```

---

## Dependencies

- 229 (env validation — LOG_LEVEL from validated env)

## Effort Estimate

4–5 hours

## Acceptance Criteria

- [ ] All requests have X-Request-ID header
- [ ] JSON logs in production, pretty logs in dev
- [ ] Flow execution time logged for every Genkit flow call
- [ ] LLM cost logged per request
- [ ] Zero console.log calls in flows/ and core services/
- [ ] Log level configurable via env var
