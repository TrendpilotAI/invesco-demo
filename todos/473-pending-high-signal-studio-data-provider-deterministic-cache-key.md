---
id: "473"
status: pending
priority: high
repo: signal-studio-data-provider
title: "Fix non-deterministic cache key in SnowflakeProvider"
effort: S
dependencies: []
created: "2026-03-04"
---

## Task Description

`providers/snowflake_provider.py:101`:
```python
cache_key = f"{sql}|{params}"
```

`dict.__repr__()` is not stable — `{"a":1,"b":2}` and `{"b":2,"a":1}` have different repr but are semantically identical. This causes unnecessary cache misses and potentially stale cache hits if dict ordering changes between Python versions.

## Coding Prompt

In `providers/snowflake_provider.py`, update `execute_query()` cache key generation:

```python
import json

# Replace:
cache_key = f"{sql}|{params}"

# With:
cache_key = f"{sql}|{json.dumps(params, sort_keys=True, default=str) if params else 'null'}"
```

Also update the docstring on `execute_query()` to note that params dict ordering doesn't affect caching.

Add a test:
```python
def test_snowflake_cache_key_stable_across_param_order(snowflake_provider):
    """Same params in different order should hit the same cache entry."""
    sql = "SELECT * FROM t WHERE a = %(a)s AND b = %(b)s"
    params_v1 = {"a": 1, "b": 2}
    params_v2 = {"b": 2, "a": 1}
    
    key1 = snowflake_provider._make_cache_key(sql, params_v1)
    key2 = snowflake_provider._make_cache_key(sql, params_v2)
    assert key1 == key2
```

(Extract cache key logic to a private `_make_cache_key()` method for testability.)

## Acceptance Criteria
- [ ] Cache key uses `json.dumps(params, sort_keys=True)`
- [ ] `_make_cache_key()` private method extracted for testability
- [ ] Test proves same params in different order → same cache key
- [ ] CI passes
