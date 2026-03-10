# 898 — Fix Deprecated `asyncio.get_event_loop()` in SnowflakeProvider

**Repo:** signal-studio-data-provider  
**Priority:** Critical (P0)  
**Effort:** S (~30 minutes)  
**Dependencies:** None  

---

## Problem

`providers/snowflake_provider.py` uses the deprecated `asyncio.get_event_loop()` + `run_in_executor()` pattern in 3 places (lines 107, 127, 190). This was deprecated in Python 3.10 and raises `DeprecationWarning` in Python 3.12+. The Oracle provider was already fixed to use `asyncio.to_thread()` in commit `fad4780`.

## Files to Change

- `providers/snowflake_provider.py` (lines 107, 127, 190)

## Coding Prompt

```
In /data/workspace/projects/signal-studio-data-provider/providers/snowflake_provider.py,
replace ALL occurrences of the pattern:

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, self.SOME_METHOD, arg1, arg2)

with the equivalent using asyncio.to_thread():

    result = await asyncio.to_thread(self.SOME_METHOD, arg1, arg2)

There are 3 such occurrences:
1. In execute_query() (~line 107)
2. In test_connection() (~line 127)
3. In write_back() (~line 190)

After the change, verify:
1. No remaining `get_event_loop` or `run_in_executor` in this file
2. The `asyncio` import is still present at the top
3. Run: cd /data/workspace/projects/signal-studio-data-provider && python3 -c "from providers.snowflake_provider import SnowflakeProvider; print('OK')"
```

## Acceptance Criteria

- [ ] Zero occurrences of `asyncio.get_event_loop()` in `snowflake_provider.py`
- [ ] Zero occurrences of `run_in_executor` in `snowflake_provider.py`  
- [ ] File imports cleanly (no syntax errors)
- [ ] Consistent with Oracle provider's implementation pattern
