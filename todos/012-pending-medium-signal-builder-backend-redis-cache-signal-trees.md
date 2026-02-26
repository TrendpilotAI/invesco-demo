---
status: pending
priority: medium
issue_id: "012"
tags: [signal-builder-backend, performance, caching, redis, signal-tree]
dependencies: []
---

# TODO 012 — Redis Caching Layer for Signal Tree Data

**Status:** pending  
**Priority:** medium  
**Repo:** signal-builder-backend  
**Effort:** M (2-3 days)

## Problem Statement

Signal tree read operations (fetching signal node trees for translation and display) hit the database on every request. These trees are:
- Read far more often than written
- Often unchanged between requests (users preview the same signal repeatedly)
- Expensive to reassemble from normalized relational data

There is no caching layer between the API and the database. Redis is already in the stack but used only for Celery task queuing.

## Findings

- Redis is in `Pipfile` (`redis = "*"`) and used by Celery (`core/celery.py`)
- `apps/signals/` has `storages/`, `services/`, `cases/` — clean architecture layers
- Signal tree read path: router → cases → services → storages → DB
- The `cases/` layer is the ideal injection point for a cache-aside pattern
- No existing cache utilities in `core/` or `core/shared/`

## Proposed Solutions

### Option A: Cache-Aside in Cases Layer (Recommended)
Wrap signal tree fetch in Cases with Redis get/set. Cache key: `signal_tree:{org_id}:{signal_id}`. TTL: 300s. Invalidate on write/update/delete.

**Pros:** Clean separation, cache logic stays in use-case layer  
**Cons:** Must carefully invalidate on mutations

### Option B: FastAPI Response Caching Middleware
Cache entire HTTP responses for GET endpoints.

**Pros:** Simple  
**Cons:** Coarse-grained, hard to invalidate per-signal, ignores auth context

**Recommendation:** Option A — cache-aside in the Cases layer with explicit invalidation.

## Coding Prompt

```
You are adding a Redis caching layer for signal tree data to signal-builder-backend.

Repository: /data/workspace/projects/signal-builder-backend/
Stack: FastAPI, SQLAlchemy 2.0, Redis, dependency-injector

TASK: Implement cache-aside pattern for signal tree read operations.

1. Create core/shared/cache.py:
   - Class: RedisCache
   - Constructor: accepts redis_url: str
   - Methods:
     - async get(key: str) -> Optional[dict]
     - async set(key: str, value: dict, ttl: int = 300)
     - async delete(key: str)
     - async delete_pattern(pattern: str)  # for bulk invalidation
   - Serialization: json.dumps/loads (use jsonpickle for complex objects)
   - Connection: use aioredis or redis.asyncio (Python redis client async interface)
   - Handle connection errors gracefully — log warning, return None (cache miss)

2. Create core/shared/cache_keys.py:
   - Constants for cache key patterns:
     SIGNAL_TREE = "signal_tree:{org_id}:{signal_id}"
     SIGNAL_LIST = "signal_list:{org_id}"
   - Function: make_signal_tree_key(org_id: int, signal_id: int) -> str
   - Function: make_signal_list_key(org_id: int) -> str

3. Update core/internals/containers.py (or wherever DI containers are configured):
   - Register RedisCache as a singleton provider
   - Inject REDIS_URL from settings

4. Update apps/signals/cases/ (signal read cases):
   - Inject RedisCache via DI
   - In get_signal_tree case:
     a. Try cache.get(key) → return deserialized tree if hit
     b. On cache miss → fetch from DB → cache.set(key, result, ttl=300)
   - In create/update/delete signal cases:
     - Call cache.delete(signal_tree_key) after successful DB write
     - Call cache.delete_pattern(signal_list_key) after list-affecting operations

5. Add REDIS_URL and CACHE_TTL_SIGNAL_TREE settings:
   - REDIS_URL: str (from env, fallback "redis://localhost:6379")
   - CACHE_TTL_SIGNAL_TREE: int (from env, default 300)

6. Create tests/test_signal_tree_cache.py:
   - Test cache hit path (Redis returns value → DB not called)
   - Test cache miss path (Redis empty → DB called → cached)
   - Test cache invalidation on signal update
   - Test graceful degradation when Redis is unavailable (returns DB result)
   - Use unittest.mock to mock Redis client

7. Add cache hit/miss logging:
   - Log at DEBUG level: "Cache hit for {key}" / "Cache miss for {key}"
   - Include cache hit rate metric (increment counters in Redis itself)

8. Run: python -m pytest tests/test_signal_tree_cache.py -v

Constraints:
- Cache must be opt-out via CACHE_ENABLED=false env var
- Never cache error responses
- Cache keys must include org_id to prevent cross-tenant data leaks
- Deserialization errors must fall through to DB (fail-safe)
- TTL must be configurable per cache key type
```

## Acceptance Criteria

- [ ] `core/shared/cache.py` created with async Redis client wrapper
- [ ] `core/shared/cache_keys.py` defines all cache key patterns
- [ ] RedisCache registered in DI container
- [ ] Signal tree GET operations served from cache on cache hit
- [ ] Cache invalidated on signal create/update/delete
- [ ] Graceful degradation when Redis is down (serves from DB)
- [ ] Cache keys always include `org_id` (no cross-tenant leakage)
- [ ] `CACHE_ENABLED=false` disables caching without code change
- [ ] `tests/test_signal_tree_cache.py` passes with mocked Redis

## Dependencies

None — Redis already available.

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Identified signal tree read as hot path with no caching
- Redis already in stack via Celery — zero new infrastructure cost
- Designed cache-aside at Cases layer to maintain clean architecture

**Learnings:**
- Cache keys MUST include org_id — multi-tenant SaaS, cross-tenant leak risk
- Graceful degradation is required — cache failures must not cause outages
