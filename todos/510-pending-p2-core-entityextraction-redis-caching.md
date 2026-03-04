# TODO-510: Redis Caching Layer

**Repo:** core-entityextraction
**Priority:** P2
**Effort:** M (4-6h)
**Dependencies:** TODO-501 (asyncpg, for consistent async patterns)
**Blocks:** None

## Description
Cache entity store snapshot in Redis to bypass Postgres on every extraction request. Major performance win for high-traffic deployments.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Add redis[hiredis] to requirements.txt
2. Create cache.py:
   - Use redis.asyncio client
   - REDIS_URL env var (default: None = caching disabled)
   - Cache entity store with TTL=300s (5 min)
   - Cache key: "entity_store:{entity_type}"
   - Invalidate on PUT/DELETE /fixed_lists

3. Update extraction logic:
   - Try Redis first → fallback to Postgres → populate Redis
   - Log cache hits/misses

4. Add Prometheus metrics: cache_hit_total, cache_miss_total

5. Graceful degradation: if Redis is down, fall through to Postgres silently
```

## Acceptance Criteria
- [ ] Entity store cached in Redis with 5min TTL
- [ ] Cache invalidated on store updates
- [ ] Graceful fallback when Redis unavailable
- [ ] Cache hit/miss metrics exposed
- [ ] Optional (disabled if REDIS_URL not set)
