# TODO-458: Add Redis Caching to Signal Validator Methods

**Repo:** signal-builder-backend  
**Priority:** Medium  
**Effort:** 3h  
**Status:** Pending

## Description
Three validator classes have `# TODO: cache` comments indicating DB calls that could be cached. These validators are called on every signal construction/validation request and hit the DB each time.

## Files
- `apps/signals/features/signal_construction/cases/validators/base_validators/base_filter_value_validator.py` (lines 147, 245, 339)
- `apps/signals/features/signal_construction/cases/validators/base_validators/base_ordering_validator.py` (line 214)
- `apps/signals/features/signal_construction/cases/validators/base_validators/base_group_function_filter_value_validator.py` (line 22)

## Coding Prompt
```
Add short-TTL Redis caching to validator DB lookups:

1. Identify the DB queries at each TODO: cache location
2. Wrap each with a Redis cache decorator or manual cache pattern
3. Use TTL of 60-300 seconds (data doesn't change frequently)
4. Cache key should include org_id and relevant entity IDs to avoid cross-tenant data leaks

Use existing core/shared/cache.py if available, or implement:
```python
async def get_cached(cache_key: str, ttl: int, fetch_fn):
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    result = await fetch_fn()
    await redis.setex(cache_key, ttl, json.dumps(result))
    return result
```

Ensure cache is invalidated on relevant entity updates.
```

## Acceptance Criteria
- [ ] DB calls in validators are cached with appropriate TTL
- [ ] Cache keys include tenant/org scope to prevent data leaks
- [ ] Cache invalidation on entity mutations
- [ ] Performance test showing reduced DB calls
