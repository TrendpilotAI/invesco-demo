# TODO-816: Replace in-memory rate limiter with Redis (Upstash)

**Priority**: HIGH (P1)
**Repo**: signal-studio
**Source**: AUDIT.md → AUDIT-002, BRAINSTORM.md → 4.3

## Description
The current LRU cache rate limiter is process-local. In a multi-replica Railway deployment, each instance has an independent counter, making rate limiting ineffective. Replace with Upstash Redis for distributed, multi-instance correctness.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Install: pnpm add @upstash/ratelimit @upstash/redis

2. Rewrite lib/rate-limit.ts to use Upstash:
   import { Ratelimit } from "@upstash/ratelimit"
   import { Redis } from "@upstash/redis"
   
   const redis = new Redis({
     url: process.env.UPSTASH_REDIS_REST_URL!,
     token: process.env.UPSTASH_REDIS_REST_TOKEN!,
   })
   
   export const rateLimiter = new Ratelimit({
     redis,
     limiter: Ratelimit.slidingWindow(20, "1 m"),
   })
   
   Keep the withRateLimit() HOF interface identical so callers don't change.

3. Add to .env.example:
   UPSTASH_REDIS_REST_URL=https://...upstash.io
   UPSTASH_REDIS_REST_TOKEN=...

4. Add Railway env vars: UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN

5. Update __tests__/lib/rate-limit.test.ts to mock Upstash Redis.

6. Ensure graceful degradation: if Redis is unavailable, allow requests through (fail open) and log error.
```

## Acceptance Criteria
- [ ] Rate limiter uses Upstash Redis
- [ ] Works correctly across multiple Railway replicas
- [ ] Fails open (allows traffic) if Redis unavailable
- [ ] Unit tests pass with mocked Redis

## Effort
4 hours

## Dependencies
Requires Upstash account + Redis database creation
