# TODO 351 — Fix Hardcoded/Empty JWT Secret Fallbacks
**Repo:** signal-studio-auth
**Priority:** CRITICAL
**Effort:** 30 minutes
**Status:** pending

## Description
`config/supabase_config.py` has two dangerous secret fallbacks:
1. `FORWARDLANE_JWT_SECRET` defaults to `"very_secure_secret"` — a known weak secret
2. `SUPABASE_JWT_SECRET` defaults to `""` — empty string causes PyJWT to accept ANY token signature

## Coding Prompt
In `/data/workspace/projects/signal-studio-auth/config/supabase_config.py`:

1. Replace the SUPABASE_JWT_SECRET line with:
```python
SUPABASE_JWT_SECRET: str = os.environ.get("SUPABASE_JWT_SECRET", "")
```

2. Replace the FORWARDLANE_JWT_SECRET line with:
```python
FORWARDLANE_JWT_SECRET: str = os.environ.get("AUTH_SECRET_KEY", "")
```

3. Add a validation function after the config vars:
```python
def validate_config() -> None:
    """Raise RuntimeError if critical config is missing. Call at app startup."""
    import sys
    env = os.environ.get("ENVIRONMENT", "development").lower()
    if env == "production":
        if not SUPABASE_JWT_SECRET:
            raise RuntimeError("SUPABASE_JWT_SECRET must be set in production")
        if AUTH_MODE in (AuthMode.FORWARDLANE, AuthMode.DUAL) and not FORWARDLANE_JWT_SECRET:
            raise RuntimeError("AUTH_SECRET_KEY must be set when AUTH_MODE includes forwardlane")
    elif not SUPABASE_JWT_SECRET:
        import warnings
        warnings.warn("SUPABASE_JWT_SECRET is empty — all Supabase tokens will be rejected", stacklevel=2)
```

4. Create `.env.example` at the repo root with all required variables documented.

## Acceptance Criteria
- [ ] No hardcoded secret strings in config.py
- [ ] `validate_config()` raises `RuntimeError` in production when secrets are missing
- [ ] `.env.example` created with all required env vars documented
- [ ] Existing tests still pass
