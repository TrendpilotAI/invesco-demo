---
id: "470"
status: pending
priority: high
repo: signal-studio-data-provider
title: "Fix factory provider cache concurrent creation race — add asyncio.Lock"
effort: S
dependencies: []
created: "2026-03-04"
---

## Task Description

`factory.py` has a race condition: two concurrent coroutines calling `get_provider()` for the same `org_id` can both pass the cache-miss check, create duplicate providers (two connection pools), and leak one pool.

## Coding Prompt

In `factory.py`:

1. Replace the module-level dict with a lock registry:
```python
import asyncio

_provider_cache: dict[str, DataProvider] = {}
_provider_locks: dict[str, asyncio.Lock] = {}
_registry_lock = asyncio.Lock()  # protect _provider_locks dict itself
```

2. Rewrite `get_provider()` as async (it already returns sync but callers are async):
```python
async def get_provider(org_config: OrgConfig, *, cached: bool = True) -> DataProvider:
    if not cached:
        return _create_provider(org_config)
    
    if org_config.org_id in _provider_cache:
        return _provider_cache[org_config.org_id]
    
    # Get or create per-org lock
    async with _registry_lock:
        if org_config.org_id not in _provider_locks:
            _provider_locks[org_config.org_id] = asyncio.Lock()
    
    async with _provider_locks[org_config.org_id]:
        # Double-check after acquiring lock
        if org_config.org_id in _provider_cache:
            return _provider_cache[org_config.org_id]
        provider = _create_provider(org_config)
        _provider_cache[org_config.org_id] = provider
        return provider


def _create_provider(org_config: OrgConfig) -> DataProvider:
    match org_config.data_tier:
        case "enterprise":
            return SnowflakeProvider(org_config)
        case "self-serve":
            return SupabaseProvider(org_config)
        case "legacy":
            return OracleProvider(org_config)
        case _:
            raise ValueError(f"Unknown data tier: {org_config.data_tier}")
```

3. Update `close_all()` to also clear the locks dict:
```python
async def close_all() -> None:
    for provider in _provider_cache.values():
        await provider.close()
    _provider_cache.clear()
    _provider_locks.clear()
```

4. Add test in `tests/test_factory.py`:
```python
async def test_concurrent_get_provider_creates_one_instance(org_config):
    results = await asyncio.gather(*[get_provider(org_config) for _ in range(10)])
    assert len(set(id(r) for r in results)) == 1  # all same instance
```

## Acceptance Criteria
- [ ] `get_provider()` uses per-org asyncio.Lock to prevent duplicate creation
- [ ] Double-checked locking pattern implemented
- [ ] `close_all()` clears locks dict
- [ ] Concurrency test passes (10 concurrent calls → 1 provider instance)
