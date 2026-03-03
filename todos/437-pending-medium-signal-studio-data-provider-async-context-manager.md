# TODO-437: Add Async Context Manager Support to Providers

**Repo:** signal-studio-data-provider  
**Priority:** P2 — Developer Experience  
**Effort:** S (1h)  
**Status:** pending

## Task

Add `__aenter__`/`__aexit__` to all three providers and update factory to support `async with`:

```python
# Desired usage:
async with get_provider(config) as provider:
    result = await provider.execute_query(...)
# connection auto-closed on exit

# In each provider:
async def __aenter__(self):
    return self

async def __aexit__(self, exc_type, exc_val, exc_tb):
    await self.close()
    return False
```

Also update `get_provider()` to optionally return an async context manager wrapper.

## Acceptance Criteria

- All 3 providers support `async with`
- `close()` called automatically on context exit
- Tests verify connection cleanup on normal exit and exception
