# TODO-573: Replace File Sessions with Redis — forwardlane_advisor

**Repo:** forwardlane_advisor  
**Priority:** P1  
**Status:** pending

## Description
Currently using `session-file-store` for session persistence. Replace with Redis for scalability.

## Steps
1. `npm install connect-redis ioredis`
2. Remove `session-file-store`
3. Update `app.js` session config to use RedisStore
4. Add `REDIS_URL` env variable support
5. Add Redis service to `docker-compose.yml`
6. Add Redis to Dockerfile healthcheck

## Acceptance Criteria
- Sessions persist across app restarts
- Multiple app instances can share sessions
- Session TTL is configurable via env var

## Dependencies
None (independent improvement)
