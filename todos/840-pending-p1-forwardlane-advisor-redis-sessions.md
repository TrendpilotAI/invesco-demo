# TODO-840: Replace File-Based Sessions with Redis (forwardlane_advisor)

**Repo:** forwardlane_advisor  
**Priority:** P1  
**Effort:** Small (4-6 hours)  
**Status:** pending

## Description
forwardlane_advisor uses `session-file-store` for Express sessions — a file-based approach that doesn't scale horizontally, can't be shared across pods, and leaks session data to disk. Replace with Redis (`connect-redis`).

## Coding Prompt
In `/data/workspace/projects/forwardlane_advisor/`:
1. `npm install connect-redis ioredis`
2. In `app.js` or session config, replace `session-file-store` with:
   ```js
   const Redis = require('ioredis');
   const connectRedis = require('connect-redis');
   const RedisStore = connectRedis(session);
   const redisClient = new Redis(process.env.REDIS_URL || 'redis://localhost:6379');
   app.use(session({ store: new RedisStore({ client: redisClient }), ... }));
   ```
3. Add `REDIS_URL` to `.env.example` and environment docs
4. Update Dockerfile to optionally link Redis container
5. Update `pm2.json` / `Procfile` with Redis dependency note
6. Test login → session persistence → logout flow

## Acceptance Criteria
- Sessions stored in Redis (verify with `redis-cli keys "sess:*"`)
- No session files created in filesystem
- Login/logout works correctly
- App restarts don't clear active sessions

## Dependencies
- None
