# TODO-387: Add /api/health/db Connection Pool Health Check

**Repo:** signal-studio
**Priority:** P1 (reliability)
**Effort:** S (3-4 hours)
**Status:** pending
**Audit ref:** NEW-005

## Description
No database health check endpoint exists. Railway's health check hits `/` (Next.js page) which doesn't verify DB connectivity. Pool exhaustion or Oracle outages would be invisible until users hit errors.

## Task
1. Create `app/api/health/db/route.ts`
2. Check: Postgres connection, Oracle 23ai connection, Redis ping
3. Return structured JSON with status per service
4. Wire into Railway health check URL setting

## Response Format
```json
{
  "status": "healthy"|"degraded"|"unhealthy",
  "timestamp": "2026-03-02T08:00:00Z",
  "services": {
    "postgres": { "status": "ok", "latencyMs": 12 },
    "oracle": { "status": "ok", "latencyMs": 45 },
    "redis": { "status": "error", "error": "ECONNREFUSED" }
  }
}
```
HTTP 200 if all OK, HTTP 503 if any critical service down.

## Coding Prompt (autonomous execution)
```
In /data/workspace/projects/signal-studio/app/api/health/db/route.ts:
1. Create GET handler (no auth required — Railway internal only)
2. Check Postgres: run SELECT 1, measure latency
3. Check Oracle: run SELECT 1 FROM dual, measure latency (wrap in try/catch — Oracle optional)
4. Check Redis: redis.ping(), measure latency (wrap in try/catch — Redis optional)
5. Return 200 JSON if all OK, 503 if postgres fails (Oracle/Redis degraded only)
6. In railway.json: set healthcheckPath to /api/health/db
```

## Acceptance Criteria
- [ ] `/api/health/db` returns JSON with all service statuses
- [ ] 503 returned when Postgres is down
- [ ] Oracle/Redis failures return 200 with `degraded` status
- [ ] Railway healthcheckPath updated
- [ ] Latency measured per service

## Dependencies
None.
