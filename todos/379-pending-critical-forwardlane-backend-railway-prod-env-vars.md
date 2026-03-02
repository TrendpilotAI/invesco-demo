# 379 — Set Railway Production Env Vars

**Repo:** forwardlane-backend  
**Priority:** critical  
**Effort:** S (30min)  
**Status:** pending

## Description
Security hardening (INFRA-004) added HTTPS redirect, HSTS, Redis caching, and secure cookies — but all are gated behind env vars that must be set in Railway. Until they are set, production runs without HTTPS enforcement and without Redis caching.

## Steps
1. In Railway project → forwardlane-backend service → Variables:
   - Set `DJANGO_ENV=production` (enables HTTPS redirect, HSTS, secure cookies, X_FRAME_OPTIONS=DENY)
   - Set `REDIS_URL=<railway-redis-internal-url>` (activates django-redis cache)
   - Verify `ALLOWED_HOSTS` is set and tight (e.g., `api.forwardlane.com`)
   - Verify `CORS_ALLOW_ALL` is NOT set or is `false`
2. Trigger a Railway redeploy
3. Test: curl -I http://api.forwardlane.com — should get 301 redirect to HTTPS
4. Test: verify Redis cache hits in logs for NL→SQL and meeting prep endpoints

## Acceptance Criteria
- HTTP → HTTPS redirect active in production
- Redis cache active (check Django logs for cache hits)
- No `CORS_ALLOW_ALL=true` in production env
