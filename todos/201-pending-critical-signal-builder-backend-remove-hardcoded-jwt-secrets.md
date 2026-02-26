# TODO 201 — Remove Hardcoded JWT Secrets (CRITICAL)

**Project:** signal-builder-backend  
**Priority:** CRITICAL  
**Estimated Effort:** 1 hour  
**Status:** pending  
**Dependencies:** none  

---

## Task Description

`settings/common.py` contains a hardcoded JWT secret key that defaults to `'very_secure_secret'`. This is a catastrophic security issue — any attacker who knows this default can forge valid JWT tokens and authenticate as any user, including admins.

**Root cause file:** `settings/common.py`  
**Pattern:** `AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "very_secure_secret")`

**Fix:**
1. Remove the insecure default value entirely.
2. Require the env var to be set — fail fast on startup if it's missing.
3. Generate a cryptographically strong secret and set it in Railway env vars for all environments.
4. Add a startup validator that checks secret strength (length ≥ 32 chars).

---

## Coding Prompt (Autonomous Agent)

```
TASK: Remove hardcoded JWT secret default in signal-builder-backend

REPO: /data/workspace/projects/signal-builder-backend/

STEPS:

1. Open `settings/common.py`. Find all secret key settings. Look for patterns like:
   - `AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "very_secure_secret")`
   - Any other key with a weak or hardcoded default string

2. For each secret key:
   a. Remove the hardcoded default
   b. Make it REQUIRED — raise on missing:
   ```python
   AUTH_SECRET_KEY: str = os.environ["AUTH_SECRET_KEY"]  # KeyError on missing = intentional
   ```
   OR use a validator:
   ```python
   _raw_secret = os.getenv("AUTH_SECRET_KEY", "")
   if not _raw_secret or len(_raw_secret) < 32:
       raise RuntimeError(
           "AUTH_SECRET_KEY env var must be set to a random string of at least 32 characters. "
           "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
       )
   AUTH_SECRET_KEY: str = _raw_secret
   ```

3. Also check `settings/local.py`, `settings/test.py` — for test environments, it's acceptable to
   have a fixed test secret, but it must be clearly labeled:
   ```python
   # settings/test.py
   AUTH_SECRET_KEY = "test-only-secret-do-not-use-in-production-xxxxxxxxxxxxxxxx"
   ```

4. Search for any other hardcoded secrets:
   ```bash
   grep -rn "secret\|password\|token\|key" settings/ --include="*.py" | grep -v "os.getenv\|os.environ\|#"
   ```
   Fix any found.

5. Generate a production-strength secret and document how to set it:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Add this command to README.md under "Initial Setup" or "Environment Variables".

6. Update `.env.example`:
   ```
   # REQUIRED: Generate with: python -c "import secrets; print(secrets.token_hex(32))"
   AUTH_SECRET_KEY=
   ```

7. Check if `fastapi-jwt-auth` uses the secret for both signing and verification.
   If symmetric (HS256), one key is enough. If asymmetric (RS256), document both
   `PRIVATE_KEY` and `PUBLIC_KEY` env vars.

8. Add a test in `tests/test_settings.py` (create if missing):
   ```python
   def test_auth_secret_key_cannot_be_default():
       from settings import common
       assert common.AUTH_SECRET_KEY != "very_secure_secret"
       assert len(common.AUTH_SECRET_KEY) >= 32
   ```

9. Commit: "security: require AUTH_SECRET_KEY env var, remove insecure hardcoded default"

VERIFICATION:
- `grep -r "very_secure_secret" .` should return nothing
- App startup without AUTH_SECRET_KEY env var should raise a clear RuntimeError
- App startup with a valid AUTH_SECRET_KEY should succeed
```

---

## Dependencies

- None — can be executed immediately

## Acceptance Criteria

- [ ] No hardcoded secret defaults exist in any settings file (except clearly-labeled test-only files)
- [ ] App raises `RuntimeError` on startup if `AUTH_SECRET_KEY` is missing or too short
- [ ] `.env.example` documents the variable with instructions to generate it
- [ ] `grep -r "very_secure_secret" .` returns no results
- [ ] README documents how to generate a secure key
- [ ] Test validates the key cannot be the insecure default
- [ ] Committed and pushed
