# TODO-399: NarrativeReactor — Redis Caching Layer for AI Calls

**Priority:** high
**Repo:** NarrativeReactor
**Effort:** M (2-3 days)

## Description
AI calls (Gemini, Claude) for same prompt+brand combo are expensive and slow. Add Redis caching with TTL.

## Coding Prompt
```
Add Redis caching to NarrativeReactor at /data/workspace/projects/NarrativeReactor/

1. Add ioredis to dependencies
2. Create src/lib/cache.ts with:
   - connect() using REDIS_URL env var (fallback to no-cache in dev)
   - get(key: string): Promise<T | null>
   - set(key: string, value: T, ttlSeconds: number): Promise<void>
   - invalidate(pattern: string): Promise<void>

3. Add cache to these flows:
   - Brand voice analysis (TTL: 1 hour) — same brand rarely changes
   - Compliance check (TTL: 30 min)
   - Competitor analysis (TTL: 4 hours)
   - Trend fetching (TTL: 15 min)

4. Cache key format: `{tenantId}:{operation}:{hash(params)}`
5. Add REDIS_URL to .env.example and README
6. Add cache hit/miss metrics to costTracker
```

## Acceptance Criteria
- [ ] Cache hit reduces AI call latency by >80%
- [ ] Cache miss fallback works transparently
- [ ] App still works when Redis is unavailable (graceful degradation)
- [ ] Cache invalidation works on brand update

## Dependencies
- TODO-397 (multi-tenancy) for tenant-scoped cache keys
