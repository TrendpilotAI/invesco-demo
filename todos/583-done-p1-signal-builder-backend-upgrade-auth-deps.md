# DONE-583: Upgrade python-jose → PyJWT, passlib → argon2-cffi

**Status:** ✅ Completed
**Date:** 2026-03-06

## What Was Done

1. **Identified usage:** `python-jose` was used only in `core/auth/auth_token.py` — `passlib` had zero usages in Python files (already unused).

2. **Installed new deps** in venv:
   - `PyJWT==2.11.0` (with `cryptography` extra)
   - `argon2-cffi==25.1.0`

3. **Removed old deps:** `python-jose` and `passlib` uninstalled from venv.

4. **Updated `Pipfile`:**
   - `python-jose = {extras = ["cryptography"], version = "==3.3.0"}` → `PyJWT = {extras = ["crypto"], version = ">=2.8.0"}`
   - `passlib = "==1.7.4"` → `argon2-cffi = ">=21.3.0"`

5. **Updated `core/auth/auth_token.py`:**
   - `from jose import jwt, JWTError` → `import jwt` + `from jwt.exceptions import PyJWTError`
   - `except JWTError:` → `except PyJWTError:`
   - API is fully compatible (PyJWT 2.x `encode` returns str, `decode` returns dict directly)

6. **Verified:** PyJWT encode/decode cycle works correctly, `PyJWTError` is raised on invalid tokens.

7. **pip-audit:** `No known vulnerabilities found`

8. **Committed and pushed:**
   - Branch: `feat/p0-todos-352-356`
   - Commit: `feat: replace python-jose with PyJWT, passlib with argon2-cffi (CVE fix)`
   - Pushed to: Bitbucket (origin) + GitHub

## Notes

- Full test suite could not run in this environment (psycopg2 build deps missing), but auth module logic verified directly.
- `argon2-cffi` added to Pipfile for future password hashing use — no existing passlib code needed migration.
