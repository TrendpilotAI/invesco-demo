# TODO: Redis Caching for Signal-to-SQL Translation (signal-builder-backend)

**Priority:** Medium  
**Repo:** signal-builder-backend  
**Effort:** 4 hours  
**Status:** pending

## Description
`transform_signal_nodes_to_sql()` and `PropertiesMapPreparationService` are called per-request with no caching. These are expensive DB + computation operations.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend:

1. Add redis caching decorator utility in core/shared/cache.py:
   ```python
   import redis.asyncio as aioredis
   import json, hashlib
   from functools import wraps
   
   def redis_cache(ttl: int = 300, key_prefix: str = ""):
       def decorator(func):
           @wraps(func)
           async def wrapper(*args, **kwargs):
               cache_key = f"{key_prefix}:{hashlib.md5(str(args).encode()).hexdigest()}"
               cached = await redis_client.get(cache_key)
               if cached:
                   return json.loads(cached)
               result = await func(*args, **kwargs)
               await redis_client.setex(cache_key, ttl, json.dumps(result))
               return result
           return wrapper
       return decorator
   ```

2. Apply to PropertiesMapPreparationService.prepare_properties_map() with TTL=600s

3. Apply to signal_nodes_tree with TTL=60s (invalidate on signal update)

4. Add cache invalidation in signal update/delete storages

5. Add REDIS_URL to settings/common.py (already available since Celery uses Redis)
```

## Dependencies
- 219-pending-high-signal-builder-backend-upgrade-deps.md (for latest redis client)

## Acceptance Criteria
- Repeated signal SQL generation uses cache (< 5ms vs 50ms+ DB call)
- Cache invalidated on signal mutations
- Redis errors gracefully degrade (cache miss, not crash)
