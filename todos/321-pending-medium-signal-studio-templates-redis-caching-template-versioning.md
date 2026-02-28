# 321 — Redis Result Caching + Template Versioning (Semver)

**Priority:** MEDIUM  
**Effort:** M  
**Status:** pending

---

## Task Description

Two related features that enable production reliability and client safety:
1. **Redis caching** — cache SQL query results by `templateId + params hash` with TTL policies per template category. Massive perf win for frequently-run signals.
2. **Template versioning** — add semver (`version`) to each template, surfaced in the API so Invesco can pin to specific versions and opt-in to upgrades. Prevents breaking live signals on template updates.

---

## Autonomous Coding Prompt

```
REPO: /data/workspace/projects/signal-studio-templates

TASK: Add Redis result caching and semver versioning to all templates.

PREREQUISITE: TODO 320 (Postgres DataProvider wired up) should be complete first.

PART 1 — Template Versioning:

1. Add version field to SignalTemplate type in src/types/index.ts:
   version: string;  // semver: "1.0.0"
   changelog?: Array<{ version: string; date: string; changes: string[] }>;

2. Update all 20 templates: add version: "1.0.0" and a minimal changelog entry.

3. Update REST API:
   - GET /templates → include version in each template's metadata response
   - POST /templates/:id/execute → accept optional X-Template-Version header
     * If provided, validate requested version matches installed version
     * If mismatch: return 409 { error: 'Version mismatch', installed: '1.0.0', requested: '2.0.0' }
   - GET /templates/:id → include full changelog

4. Add version to audit logs (see security section of BRAINSTORM — log templateId, version, userId, duration).

PART 2 — Redis Caching:

5. Install: pnpm add ioredis
   pnpm add -D @types/ioredis (if needed)

6. Create src/cache/RedisCache.ts:
   - Connect to process.env.REDIS_URL (Railway Redis)
   - Implement CacheProvider interface:
       get(key: string): Promise<T | null>
       set(key: string, value: T, ttlSeconds: number): Promise<void>
       invalidate(key: string): Promise<void>
       invalidatePattern(pattern: string): Promise<void>
   - Handle connection failures gracefully: log warning, continue without cache (don't throw)
   - Use ioredis with reconnect strategy

7. Cache key strategy in src/cache/cacheKey.ts:
   - generateCacheKey(templateId: string, params: Record<string, unknown>): string
     * SHA256 of `${templateId}:${JSON.stringify(sortKeys(params))}`
     * sortKeys ensures { a: 1, b: 2 } and { b: 2, a: 1 } produce the same key

8. TTL policy map in src/cache/ttlPolicy.ts:
   export const TTL_POLICY: Record<TemplateCategory, number> = {
     'meeting-prep': 4 * 60 * 60,        // 4 hours
     'sales-intelligence': 1 * 60 * 60,  // 1 hour
     'risk-compliance': 15 * 60,          // 15 minutes
     'management': 1 * 60 * 60,          // 1 hour
     'territory': 30 * 60,               // 30 minutes
   };

9. Update TemplateEngine.execute():
   - Before running SQL: check cache → if hit, return cached result
   - After SQL: store result in cache with appropriate TTL
   - Add cacheHit: boolean to the execution result type
   - Add X-Cache: HIT/MISS response header in the router

10. Stale-while-revalidate pattern (optional, implement if time allows):
    - If cache entry exists but is >80% through its TTL, return it AND trigger
      async background refresh (don't await)

11. Add cache tests in tests/cache/:
    - Unit test generateCacheKey: same params different order → same key
    - Unit test RedisCache with ioredis-mock
    - Integration test: execute template twice → second call returns cached result

12. Export createRedisCacheProvider() from src/index.ts
    Document REDIS_URL env var in README.

ACCEPTANCE: Template executions cache results. Second identical call returns
cacheHit: true with X-Cache: HIT header. Redis unavailable → falls back gracefully,
templates still execute. All new tests pass.
```

---

## Dependencies

- **315** (parameterized queries — cache the safe query results)
- **319** (type safety — version field needs to be in strict SignalTemplate type)
- **320** (Postgres DataProvider — caching wraps real DB calls)

---

## Acceptance Criteria

- [ ] All 20 templates have `version: "1.0.0"` and a changelog entry
- [ ] `GET /templates` returns version in metadata
- [ ] `X-Template-Version` header enforcement works (409 on mismatch)
- [ ] `RedisCache` class created with graceful degradation on connection failure
- [ ] Cache key is deterministic (param order-independent)
- [ ] TTL policy applied per template category
- [ ] `X-Cache: HIT/MISS` header on all `/execute` responses
- [ ] Cache unit tests pass with ioredis-mock
- [ ] `REDIS_URL` env var documented
