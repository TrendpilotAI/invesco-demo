# 337 — Confirm Railway Production Env Vars

**Priority:** CRITICAL
**Repo:** forwardlane-backend
**Effort:** S (30 min)
**Category:** Security / Infrastructure

## Description
Security features were implemented but are env-gated — they only activate when specific
Railway environment variables are set. These MUST be confirmed before Invesco demo goes live.

## Required Railway Env Vars

| Variable | Required Value | Activates |
|----------|---------------|-----------|
| `DJANGO_ENV` | `production` | HTTPS redirect, HSTS, secure cookies, X-Frame-Options |
| `REDIS_URL` | Railway Redis internal URL | Redis cache backend (currently falls back to LocMemCache) |
| `ALLOWED_HOSTS` | `api.forwardlane.com` (or prod domain) | Prevents host header injection |
| `CORS_ALLOW_ALL` | NOT SET or `false` | Prevents open CORS |

## Verification Steps
1. Log into Railway dashboard for forwardlane-backend service
2. Check Environment Variables tab
3. Confirm each variable above is set correctly
4. Deploy and verify: `curl -I https://api.forwardlane.com/healthz` should return `Strict-Transport-Security` header
5. Verify Redis cache: check logs for `django_redis` cache backend initialization

## Files Referenced
- `forwardlane/settings/base.py` — HTTPS/HSTS settings (activated by DJANGO_ENV=production)
- `forwardlane/settings/cache.py` — Redis settings (activated by REDIS_URL)
- `forwardlane/settings/cors.py` — CORS settings

## Acceptance Criteria
- [ ] `DJANGO_ENV=production` confirmed in Railway prod
- [ ] `REDIS_URL` confirmed in Railway prod
- [ ] `ALLOWED_HOSTS` set to production domain
- [ ] `curl -I https://<prod-domain>/healthz` returns `Strict-Transport-Security` header
- [ ] No `CORS_ALLOW_ALL=true` in Railway prod env
