# TODO-501: Redis Connection Pool for signal-studio-auth

**Priority:** P1  
**Effort:** XS (~1h)  
**Repo:** signal-studio-auth  
**Status:** pending

## Description
`config/redis_config.py` `get_redis()` currently creates a new Redis connection on each call. Under concurrent requests, this wastes connection slots and adds latency.

## Fix
Use `redis.ConnectionPool` shared at module level:

```python
# config/redis_config.py
import redis
import os

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

_pool: redis.ConnectionPool | None = None

def get_redis_pool() -> redis.ConnectionPool:
    global _pool
    if _pool is None:
        _pool = redis.ConnectionPool.from_url(REDIS_URL, max_connections=20)
    return _pool

def get_redis() -> redis.Redis | None:
    try:
        pool = get_redis_pool()
        r = redis.Redis(connection_pool=pool)
        r.ping()
        return r
    except Exception:
        return None
```

## Acceptance Criteria
- [ ] `get_redis()` uses connection pool
- [ ] Pool size configurable via `REDIS_MAX_CONNECTIONS` env var
- [ ] Tests pass with mock Redis
