# TODO-313: Activate Redis + HTTPS in Railway Production — forwardlane-backend

**Priority:** HIGH  
**Effort:** S  
**Repo:** forwardlane-backend  
**Status:** pending

## Description
INFRA-004 hardening is code-complete but NOT yet activated in Railway production. Three env vars must be set to enable HTTPS redirect, HSTS, Redis caching, and confirm CORS lock-down.

## Task Steps
1. In Railway production environment (Signal Studio project), set:
   - `DJANGO_ENV=production` — enables HTTPS redirect, HSTS, secure cookies
   - `REDIS_URL=redis://default:n0cCnXT!P~Deqag~_R-ycmL30-4Jx79E@Redis.railway.internal:6379` — activates django-redis caching
   - Verify `ALLOWED_HOSTS` is set tightly (not `*`)
   - Confirm `CORS_ALLOW_ALL` is NOT set or is `false`
2. After setting, trigger a Railway redeploy
3. Verify: `curl -I https://<prod-url>/api/v1/healthz/` returns 200 with HTTPS redirect chain
4. Verify: Redis connection in Django logs (look for cache HIT/MISS on MeetingPrepView calls)

## Acceptance Criteria
- [ ] `DJANGO_ENV=production` set in Railway
- [ ] `REDIS_URL` set pointing to internal Redis
- [ ] HTTPS redirect working (HTTP → HTTPS 301)
- [ ] No `CORS_ALLOW_ALL=true` in production env
- [ ] Redis cache active (confirmed via logs or cache hit on MeetingPrep)

## Dependencies
- TODO-311 (Django 4.2 compat must pass before activating prod)
