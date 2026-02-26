# TODO 006 — Fix Hardcoded Fallback Secrets in signal-builder-backend

**Status:** pending  
**Priority:** high  
**Repo:** signal-builder-backend  
**Effort:** S (2-4 hours)

## Problem

In `settings/common.py`, both JWT and auth secrets default to the literal string `'very_secure_secret'`:

```python
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", 'very_secure_secret')
AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY', 'very_secure_secret')
```

If these env vars are not set in a production deployment, the app silently uses a well-known weak secret, making all JWT tokens forgeable by anyone who reads the source code.

## Files Affected

- `settings/common.py` (lines ~14, ~34)
- `settings/production.py` (add enforcement)
- `.env.example` (ensure JWT_SECRET_KEY and AUTH_SECRET_KEY are documented)

## Coding Prompt

```
You are fixing a critical security vulnerability in signal-builder-backend.

In /data/workspace/projects/signal-builder-backend/settings/common.py:
1. Change JWT_SECRET_KEY to raise ValueError if env var is missing AND ENV != 'development':
   JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
   if not JWT_SECRET_KEY:
       if ENV == 'production':
           raise ValueError("JWT_SECRET_KEY env var must be set in production")
       JWT_SECRET_KEY = 'dev_only_insecure_secret'

2. Do the same for AUTH_SECRET_KEY.

3. In settings/production.py, add explicit assertions that both secrets are set and have length >= 32 chars.

4. Update .env.example to add:
   JWT_SECRET_KEY=your-256-bit-secret-here
   AUTH_SECRET_KEY=your-256-bit-secret-here

5. Add a comment near each setting explaining why weak defaults are not allowed in production.

Do NOT change any other settings. Run the existing tests after to verify nothing is broken.
```

## Acceptance Criteria

- [ ] Starting the app in production without JWT_SECRET_KEY raises a clear ValueError
- [ ] Development mode still works with a dev-only placeholder
- [ ] `.env.example` documents both required secrets
- [ ] No test regressions

## Dependencies

None — can be done immediately.
