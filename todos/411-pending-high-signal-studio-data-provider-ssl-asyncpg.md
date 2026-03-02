# TODO 411 — Enforce SSL for asyncpg Connection Pool

**Repo:** signal-studio-data-provider  
**Priority:** High  
**Effort:** Small (0.25 days)  
**Status:** pending

## Description
`SupabaseProvider._get_pool()` creates asyncpg pool without SSL enforcement. Credentials transmitted in plaintext if database_url uses non-SSL scheme.

**File:** `providers/supabase_provider.py:41`

## Task
```python
# Before
self._pool = await asyncpg.create_pool(self._sb.database_url, min_size=2, max_size=20)

# After
import ssl as ssl_lib
ssl_ctx = ssl_lib.create_default_context()
self._pool = await asyncpg.create_pool(
    self._sb.database_url, 
    min_size=2, 
    max_size=20,
    ssl=ssl_ctx  # enforce TLS
)
```

Also add `ssl_mode: Literal["require", "prefer", "disable"] = "require"` to `SupabaseConfig` in `config.py` to allow override in test environments.

## Acceptance Criteria
- [ ] SSL enforced by default for Supabase connections
- [ ] Configurable via SupabaseConfig.ssl_mode
- [ ] Tests use ssl_mode="disable" for local test DBs (testcontainers)

## Dependencies
None
