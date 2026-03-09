# TODO-863: Add Oracle Connection Pooling

**Repo:** signal-studio-data-provider  
**Priority:** High  
**Effort:** M (2-4 hours)  
**Status:** pending

## Problem
`providers/oracle_provider.py` uses a single `self._conn`. Under concurrent async calls, multiple coroutines share one connection — race condition.

## Fix
Replace `self._conn` with `oracledb.create_pool()`:
```python
self._pool = await oracledb.create_pool_async(
    user=self._oc.user,
    password=self._oc.password,
    dsn=self._oc.dsn,
    min=2, max=10
)
```

## Acceptance Criteria
- [ ] Oracle provider uses connection pool
- [ ] Concurrent queries don't race
- [ ] Pool is closed cleanly in `close()`
