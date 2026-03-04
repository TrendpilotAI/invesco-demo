# Oracle Provider Async Blocking Audit — DONE

**Commit:** `0442e3c`  
**Branch:** `master`  
**Repo:** TrendpilotAI/signal-studio-data-provider  

## What Was Done

### Audit Findings
All three blocking DB operations in `oracle_provider.py` were already correctly wrapped in `asyncio.to_thread()`:
- `execute_query()` → calls `_execute_query_sync()` via `asyncio.to_thread()`
- `test_connection()` → calls `_test_connection_sync()` via `asyncio.to_thread()`
- `write_back()` → calls `_write_back_sync()` via `asyncio.to_thread()`

### Fix Applied: Thread-Safe Pool Initialization
**Problem:** `_get_pool()` had a TOCTOU race condition — multiple `asyncio.to_thread()` workers could simultaneously see `self._pool is None` and each call `oracledb.create_pool()`, creating duplicate pools and leaking connections.

**Fix:** Added `threading.Lock` (`_pool_lock`) with double-checked locking pattern:
```python
self._pool_lock = threading.Lock()  # added in __init__

def _get_pool(self):
    if self._pool is None:
        with self._pool_lock:
            if self._pool is None:  # double-checked locking
                import oracledb
                self._pool = oracledb.create_pool(...)
    return self._pool
```

### Tests Added
- `test_oracle_get_pool_thread_safe` — spawns 10 threads concurrently calling `_get_pool()`, asserts `_pool_lock` is a `threading.Lock`, no errors raised
- Existing `to_thread` tests already present: `test_oracle_execute_query_uses_to_thread`, `test_oracle_test_connection_uses_to_thread`, `test_oracle_write_back_uses_to_thread`

## Files Changed
- `providers/oracle_provider.py` — added `import threading`, `_pool_lock`, double-checked locking in `_get_pool()`
- `tests/test_providers.py` — added `test_oracle_get_pool_thread_safe`
