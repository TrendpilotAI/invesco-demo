# TODO 200 — Fix CORS Wildcard (CRITICAL)

**Project:** signal-builder-backend  
**Priority:** CRITICAL  
**Estimated Effort:** 1 hour  
**Status:** complete  
**Dependencies:** none  

---

## Task Description

The FastAPI backend (`get_application.py`) configures CORS middleware with `allow_origins=["*"]` (wildcard). Combined with `allow_credentials=True`, this is a critical security misconfiguration — it allows **any origin** to make authenticated, credential-carrying requests to the API. In a financial data API serving multi-tenant adviser data, this is unacceptable.

**Root cause file:** `apps/get_application.py`  
**Settings file:** `settings/common.py`

**Fix:**
1. Add `CORS_ALLOWED_ORIGINS` to settings, read from an environment variable.
2. Replace the wildcard in `get_application.py` with the settings value.
3. Update Railway environment variables to include the correct allowed origins.

---

## Coding Prompt (Autonomous Agent)

```
TASK: Fix CORS wildcard misconfiguration in signal-builder-backend

REPO: /data/workspace/projects/signal-builder-backend/

STEPS:

1. Open `settings/common.py`. Add the following setting:
   ```python
   import os
   CORS_ALLOWED_ORIGINS: list[str] = os.getenv(
       "CORS_ALLOWED_ORIGINS",
       "https://app.forwardlane.com"
   ).split(",")
   ```
   Place it near other security/auth settings. Strip whitespace from each origin:
   ```python
   CORS_ALLOWED_ORIGINS: list[str] = [
       o.strip() for o in os.getenv(
           "CORS_ALLOWED_ORIGINS",
           "https://app.forwardlane.com"
       ).split(",")
       if o.strip()
   ]
   ```

2. Open `apps/get_application.py`. Find the CORSMiddleware configuration.
   Replace:
   ```python
   allow_origins=["*"]
   ```
   With:
   ```python
   allow_origins=settings.CORS_ALLOWED_ORIGINS
   ```
   Ensure `settings` is imported at the top of the file.

3. Verify `allow_credentials=True` is kept — this is correct behavior once origins are restricted.

4. Add a startup log line so it's visible what origins are allowed:
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.info(f"CORS allowed origins: {settings.CORS_ALLOWED_ORIGINS}")
   ```

5. Update `.env.example` (if present) to document:
   ```
   CORS_ALLOWED_ORIGINS=https://app.forwardlane.com,https://signal-studio.forwardlane.com
   ```

6. Check all settings environment files (settings/local.py, settings/production.py, settings/qa.py) to ensure no hardcoded `allow_origins` overrides.

7. Write or update a test in `tests/` that verifies:
   - A request from an allowed origin gets CORS headers back
   - A request from a disallowed origin does NOT get `Access-Control-Allow-Origin` header

8. Commit: "security: restrict CORS to configured allowed origins (fixes wildcard)"

VERIFICATION:
- `grep -r 'allow_origins' apps/` should not contain `"*"`
- `grep -r 'CORS_ALLOWED_ORIGINS' settings/` should show the new setting
```

---

## Dependencies

- None — can be executed immediately

## Acceptance Criteria

- [ ] `get_application.py` no longer contains `allow_origins=["*"]`
- [ ] `CORS_ALLOWED_ORIGINS` is a configurable env var in `settings/common.py`
- [ ] Default value is a specific ForwardLane origin, not `*`
- [ ] `.env.example` documents the variable
- [ ] App still starts and serves requests from allowed origins
- [ ] Test proves CORS headers are not returned for disallowed origins
- [ ] Committed and pushed to the feature branch
