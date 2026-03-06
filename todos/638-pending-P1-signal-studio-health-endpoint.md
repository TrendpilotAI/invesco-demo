# TODO-638: Create /api/health/db Health Check Endpoint

**Priority:** P1  
**Effort:** XS (1hr)  
**Repo:** signal-studio  
**Category:** Operations / Infrastructure  

## Problem

Railway uses HTTP health checks to determine pod readiness and liveness. Signal Studio has no unified health endpoint that validates all service dependencies (Postgres, Oracle, rate limiter).

## Coding Prompt (Autonomous Execution)

```
Create /data/workspace/projects/signal-studio/app/api/health/db/route.ts:

import { NextResponse } from 'next/server'
import { logger } from '@/lib/logger'

export async function GET() {
  const checks: Record<string, 'ok' | 'error'> = {}
  
  // Check Postgres
  try {
    const { db } = await import('@/lib/db')
    await db.execute('SELECT 1')
    checks.postgres = 'ok'
  } catch (e) {
    logger.error({ err: e }, 'Health check: Postgres failed')
    checks.postgres = 'error'
  }

  // Check Oracle (connection test)
  try {
    const { testConnection } = await import('@/lib/oracle-service')
    await testConnection()
    checks.oracle = 'ok'
  } catch (e) {
    logger.warn({ err: e }, 'Health check: Oracle unavailable (non-critical)')
    checks.oracle = 'error'
  }

  const allOk = checks.postgres === 'ok'  // Oracle is non-critical
  const status = allOk ? 200 : 503

  return NextResponse.json(
    { status: allOk ? 'healthy' : 'degraded', checks, ts: new Date().toISOString() },
    { status }
  )
}
```

Also update railway.json or next.config.mjs to expose this route as the health check URL.

## Acceptance Criteria

- [ ] GET /api/health/db returns 200 with `{ status: 'healthy', checks: { postgres: 'ok', oracle: 'ok' } }`
- [ ] Returns 503 if Postgres is down
- [ ] Oracle failure returns `oracle: 'error'` but doesn't make overall status 503 (non-critical)
- [ ] Route is NOT protected by auth middleware (health checks must be unauthenticated)
- [ ] Railway health check configured to hit this endpoint

## Dependencies

None
