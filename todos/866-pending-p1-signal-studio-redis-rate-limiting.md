# 866 — Replace In-Memory Rate Limiter with Redis (Upstash)

**Repo:** signal-studio  
**Priority:** P1 — High  
**Effort:** 0.5 day  
**Status:** pending

## Problem
`lib/rate-limit.ts` uses an in-process LRU cache. On Railway with multiple instances or after any restart, the cache resets and rate limiting state is lost. This means:
- Users can bypass rate limits by hitting different instances
- DDoS protection is ineffective in multi-instance deployments
- LLM cost protection is unreliable

## Solution
Replace with `@upstash/ratelimit` backed by Upstash Redis (available as Railway plugin or via Upstash cloud free tier).

## Coding Prompt (for autonomous agent)
```bash
# 1. Install Upstash ratelimit
cd /data/workspace/projects/signal-studio
pnpm add @upstash/ratelimit @upstash/redis

# 2. Rewrite lib/rate-limit.ts to use Upstash when UPSTASH_REDIS_REST_URL is set,
#    falling back to LRU cache for local dev:

import { Ratelimit } from "@upstash/ratelimit"
import { Redis } from "@upstash/redis"
import { LRUCache } from "lru-cache"

// Use Upstash in production, LRU in dev (when env var not set)
const useRedis = !!process.env.UPSTASH_REDIS_REST_URL

let upstashRatelimit: Ratelimit | null = null
if (useRedis) {
  upstashRatelimit = new Ratelimit({
    redis: Redis.fromEnv(),
    limiter: Ratelimit.slidingWindow(20, "60 s"),
    analytics: true,
  })
}

// Keep existing LRU logic as fallback for local dev
// ... existing LRU code ...

export async function isRateLimited(key: string, options: RateLimitOptions = {}) {
  if (upstashRatelimit) {
    const { success, limit, remaining, reset } = await upstashRatelimit.limit(key)
    return {
      limited: !success,
      remaining,
      resetMs: Math.max(0, reset - Date.now()),
    }
  }
  // Fall back to LRU for local dev
  return isRateLimitedLocal(key, options)
}

# 3. Add to .env.example:
UPSTASH_REDIS_REST_URL=https://your-upstash-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-upstash-token

# 4. Update middleware.ts to use async isRateLimited if needed
# 5. Add Railway env vars: UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN
```

## Acceptance Criteria
- [ ] Rate limiting state survives app restart
- [ ] Rate limiting works correctly across multiple Railway instances
- [ ] Local dev still works without Upstash env vars (LRU fallback)
- [ ] Existing rate limit tests pass
- [ ] No increase in API latency >10ms

## Dependencies
- None (independent change)

## Notes
- Upstash free tier: 10,000 commands/day — sufficient for dev
- Railway Redis plugin also works as alternative
