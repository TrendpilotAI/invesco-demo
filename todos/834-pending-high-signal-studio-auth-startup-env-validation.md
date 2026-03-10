# TODO-834: Add Startup Environment Variable Validation

**Repo:** signal-studio-auth
**Priority:** P1 (High)
**Effort:** 45 minutes
**Status:** pending
**Dependencies:** None
**Created:** 2026-03-10

## Problem

The app starts silently with missing critical env vars. `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, and `SUPABASE_JWT_SECRET` default to empty strings in `config/supabase_config.py` (lines 46-48). If they're missing:
- Every Supabase API call fails with a cryptic `httpx` error
- JWT validation fails silently
- No clear error message tells the operator what's wrong

`AUTH_SECRET_KEY` already has `_require_secret()` validation (good), but the Supabase vars have none.

## Files to Change

- `config/supabase_config.py` lines 46-48 — Add validation for SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_JWT_SECRET
- `config/redis_config.py` — Add optional warning if REDIS_URL is not set

## Coding Prompt

```
Open /data/workspace/projects/signal-studio-auth/config/supabase_config.py

Add validation after the env var loading (after line 48). Use the existing _TESTING guard pattern:

# After line 48, add:
def _require_env(var_name: str) -> str:
    """Load a required env var. Raises RuntimeError in non-test environments if missing."""
    value = os.environ.get(var_name, "")
    if not _TESTING and not value:
        raise RuntimeError(
            f"[signal-studio-auth] FATAL: {var_name} is required but not set. "
            f"Set it in your environment or .env file before starting the service."
        )
    return value

Then change lines 46-48 from:
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
    SUPABASE_JWT_SECRET: str = os.environ.get("SUPABASE_JWT_SECRET", "")
    SUPABASE_SERVICE_KEY: str = os.environ.get("SUPABASE_SERVICE_KEY", "")
To:
    SUPABASE_URL: str = _require_env("SUPABASE_URL")
    SUPABASE_JWT_SECRET: str = _require_env("SUPABASE_JWT_SECRET")
    SUPABASE_SERVICE_KEY: str = _require_env("SUPABASE_SERVICE_KEY")

Open /data/workspace/projects/signal-studio-auth/config/redis_config.py

Add a startup warning (not fatal — Redis is optional with in-memory fallback):
    import logging
    _logger = logging.getLogger(__name__)
    if not REDIS_URL:
        _logger.warning(
            "REDIS_URL not set — rate limiting and refresh token rotation "
            "will use in-memory fallback (not safe for multi-replica deployments)"
        )

Run: cd /data/workspace/projects/signal-studio-auth && python -m pytest -v
Tests should still pass because _TESTING guard bypasses validation.
```

## Acceptance Criteria

- [ ] App raises `RuntimeError` on startup if `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, or `SUPABASE_JWT_SECRET` are missing (non-test)
- [ ] Error messages clearly name the missing variable
- [ ] Tests still pass (validation bypassed when `pytest` is in `sys.modules`)
- [ ] Warning logged if `REDIS_URL` is not set
- [ ] Existing `_require_secret()` for `AUTH_SECRET_KEY` is unchanged
