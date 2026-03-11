# signal-studio-auth remediation status

Date: 2026-03-11 UTC
Repo: `/data/workspace/projects/signal-studio-auth`
Default branch verified: `master`

## Executive summary

The Tier 3 header-conflict claim was **historically valid**, but it is **already fixed on the default branch**.

Specifically:
- the duplicate/competing inline security-header middleware referenced in the audit docs is **not present** on current `master`
- the fix landed earlier in commit **`67b68c3`** (`fix: P0 auth cleanups — remove dup headers, rotate_family_token refactor, field_validator fix (#831 #832 #833)`)
- current `main.py` only installs **one** security-header path: `app.add_middleware(SecurityHeadersMiddleware)`
- current production header policy is **not being downgraded** by a competing middleware on `master`

I still made a small hardening follow-up branch to reduce regression risk and improve maintainability/documentation.

## Verification results

### 1) Duplicate security-header middleware on active/default branch

Result: **No duplicate middleware on current `master`**.

Evidence:
- `main.py` contains `app.add_middleware(SecurityHeadersMiddleware)`
- `main.py` does **not** contain the prior inline `@app.middleware("http")` security header function
- grep confirmed no non-test inline app middleware remains for header injection in the app entrypoint

Historical note:
- repository planning/audit docs (`AUDIT.md`, `BRAINSTORM.md`, `PLAN.md`) correctly describe the earlier bug state
- that bug was remediated in commit `67b68c3`

### 2) X-Frame-Options or related headers being downgraded by competing middleware

Result: **No active downgrade on current `master`**.

Current canonical header values on the app:
- `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'; form-action 'self'`
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()`
- `X-XSS-Protection: 1; mode=block`

Conclusion:
- `X-Frame-Options` is **not** being downgraded
- CSP protections such as `frame-ancestors 'none'` and `form-action 'self'` are **present** and not clobbered on the current branch
- the earlier downgrade described in audit artifacts is no longer live on `master`

## Follow-up remediation completed

Even though the primary bug was already fixed upstream, I completed a focused follow-up branch to lock the fix in.

### Branch created and pushed

- Branch: **`fix/header-policy-regression-readme`**
- Commit: **`1e2073b`**
- Remote: **pushed to `origin`**

### Changes in follow-up branch

1. **Centralized security-header policy**
   - introduced `SECURITY_HEADERS` in `middleware/security_headers.py`
   - middleware now applies headers from a single canonical mapping
   - this reduces the chance of value drift across tests/docs/code

2. **Added app-level header regression tests**
   - extended `tests/test_security_headers.py`
   - new tests validate:
     - canonical header map values
     - real `main.app` `/health` responses use the exact final header policy
     - no duplicated or downgraded header values are present in the final response

3. **Added missing test dependency**
   - pinned `fakeredis==2.32.0` in `requirements.txt`
   - broader Redis/token tests depended on it but it was not previously listed

4. **Added comprehensive README**
   - created `README.md` covering:
     - service purpose and architecture
     - auth endpoints and flows
     - Redis usage
     - rate limiting behavior
     - refresh token rotation and reuse detection
     - environment variables
     - local development and deployment notes
     - security header policy

## Validation run

Using a clean virtualenv (`.venv2`), I ran:

```bash
python -m pytest -q \
  tests/test_security_headers.py \
  tests/test_connection_pool.py \
  tests/test_rate_limit_and_tokens.py \
  tests/test_auth.py \
  tests/test_password_reset.py \
  tests/test_rbac.py \
  tests/test_security.py \
  tests/test_redis_integration.py
```

Result:
- **107 passed**
- no failures

## Important nuance for the main agent

The right way to report this upstream is:

> The Tier 3 duplicate security-header issue was real historically, but it is **already fixed on the current default branch** via commit `67b68c3`. I did **not** remove a live duplicate path because none remained. Instead, I added a small hardening branch (`fix/header-policy-regression-readme`, commit `1e2073b`) that centralizes the canonical header policy, adds app-level regression tests, documents the service comprehensively, and fixes the missing `fakeredis` test dependency.
