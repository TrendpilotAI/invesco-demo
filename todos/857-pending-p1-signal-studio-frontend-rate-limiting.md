# Add Rate Limiting to AI Chat API Routes

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (2 hours)

## Description
No rate limiting on `/api/chat/` routes. Authenticated users can make unlimited AI inference calls, leading to unbounded OpenAI/Anthropic costs and DoS potential.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend:
1. pnpm add @upstash/ratelimit @upstash/redis
2. Create lib/rate-limit.ts:
   import { Ratelimit } from '@upstash/ratelimit'
   import { Redis } from '@upstash/redis'
   
   export const chatRateLimit = new Ratelimit({
     redis: Redis.fromEnv(),
     limiter: Ratelimit.slidingWindow(10, '1 m'),
     analytics: true,
     prefix: 'signal-studio:chat',
   })

3. Add to app/api/chat/ai-sdk/route.ts and app/api/chat/insights/route.ts:
   const identifier = user.id  // from auth check
   const { success, limit, reset, remaining } = await chatRateLimit.limit(identifier)
   if (!success) {
     return NextResponse.json(
       { error: 'Rate limit exceeded', reset },
       { status: 429, headers: { 'X-RateLimit-Limit': limit.toString(), 'X-RateLimit-Remaining': remaining.toString() } }
     )
   }

4. Add UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN to .env.example
5. Commit: "feat: add rate limiting to AI chat routes (10 req/min per user)"
```

## Acceptance Criteria
- [ ] AI chat routes return 429 after 10 req/min per user
- [ ] Rate limit headers in response
- [ ] Graceful degradation if Redis unavailable

## Dependencies
- 853 (auth must be in place to identify user for rate limiting)
