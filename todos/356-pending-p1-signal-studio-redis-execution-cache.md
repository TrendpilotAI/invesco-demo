# TODO-356: Add Redis Caching for Signal Execution Results

**Priority:** P1
**Effort:** M
**Repo:** signal-studio
**Status:** pending

## Description
Repeated identical signal queries re-execute against Oracle 23ai each time. Caching results in Redis would dramatically reduce latency for repeated queries and Oracle load.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Check Redis is configured: grep -rn "redis\|REDIS" lib/ app/ --include="*.ts" | head -10

2. Create lib/cache/signal-cache.ts:
```typescript
import { createClient } from 'redis'

const redis = createClient({ url: process.env.REDIS_URL })
redis.connect()

const SIGNAL_CACHE_TTL = 300 // 5 minutes

export async function getCachedResult(signalId: string, params: Record<string, unknown>) {
  const key = `signal:${signalId}:${hashParams(params)}`
  const cached = await redis.get(key)
  return cached ? JSON.parse(cached) : null
}

export async function setCachedResult(
  signalId: string, 
  params: Record<string, unknown>, 
  result: unknown
) {
  const key = `signal:${signalId}:${hashParams(params)}`
  await redis.setEx(key, SIGNAL_CACHE_TTL, JSON.stringify(result))
}

export async function invalidateSignalCache(signalId: string) {
  const keys = await redis.keys(`signal:${signalId}:*`)
  if (keys.length) await redis.del(keys)
}

function hashParams(params: Record<string, unknown>): string {
  // Simple deterministic hash
  return Buffer.from(JSON.stringify(params, Object.keys(params).sort())).toString('base64').slice(0, 16)
}
```

3. Integrate into signal execution API route (app/api/signals/run/route.ts):
   - Before execution: check getCachedResult
   - If hit: return cached result immediately with X-Cache: HIT header
   - If miss: execute, then setCachedResult, return with X-Cache: MISS header

4. Add cache invalidation when signal definition changes (PUT /api/signals/[id])

5. Add Redis health check to /api/health endpoint

6. Commit: "feat(perf): add Redis caching for signal execution results (5-min TTL)"
```

## Dependencies
- TODO-354 (signal execution must be wired first)

## Acceptance Criteria
- Repeated signal queries return from cache
- Cache TTL is 5 minutes
- X-Cache header indicates HIT/MISS
- Cache invalidated when signal is modified
- Redis health check in /api/health
