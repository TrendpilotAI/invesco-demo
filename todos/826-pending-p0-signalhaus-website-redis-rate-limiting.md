# TODO-826: Fix In-Memory Rate Limiter → Upstash Redis
**Repo:** signalhaus-website  
**Priority:** P0 (Critical)  
**Status:** pending  
**Effort:** 1 day

## Problem
`/src/app/api/contact/route.ts` uses an in-memory `Map` for rate limiting (line 12). In Vercel's serverless environment, each Lambda invocation is isolated — the Map is empty on cold starts. Rate limiting doesn't work in production, making the contact form vulnerable to spam/abuse.

## Task
Replace the in-memory rate limiter with Upstash Redis using the official `@upstash/ratelimit` package.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website:

1. Install dependencies:
   npm install @upstash/ratelimit @upstash/redis

2. Create /src/lib/ratelimit.ts:
   ```typescript
   import { Ratelimit } from "@upstash/ratelimit"
   import { Redis } from "@upstash/redis"
   
   export const ratelimit = new Ratelimit({
     redis: Redis.fromEnv(),
     limiter: Ratelimit.slidingWindow(5, "15 m"),
     analytics: true,
   })
   ```

3. Update /src/app/api/contact/route.ts:
   - Remove: const rateLimitStore = new Map<string, RateEntry>() (line 12)
   - Remove: the RateEntry interface, RATE_LIMIT, WINDOW_MS consts
   - Remove: checkRateLimit() function
   - Import ratelimit from "@/lib/ratelimit"
   - Replace rate limit check with:
     ```typescript
     const { success, reset } = await ratelimit.limit(ip)
     if (!success) {
       return NextResponse.json(
         { error: "Too many requests. Please try again later." },
         { status: 429, headers: { "Retry-After": String(Math.ceil((reset - Date.now()) / 1000)) } }
       )
     }
     ```

4. Create .env.example with:
   RESEND_API_KEY=re_xxxx
   CONTACT_EMAIL=hello@signalhaus.ai
   SLACK_WEBHOOK_URL=https://hooks.slack.com/...
   NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
   NEXT_PUBLIC_CLARITY_ID=xxxxxxxxx
   NEXT_PUBLIC_LI_PARTNER_ID=123456
   UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
   UPSTASH_REDIS_REST_TOKEN=xxxx

5. Update DEPLOY.md with Upstash setup instructions
```

## Acceptance Criteria
- Rate limiter works correctly in Vercel serverless (stateless, shared state via Redis)
- 5 requests per 15 min per IP are allowed; 6th returns 429
- `.env.example` documents all required env vars
- No memory leak from unbounded Map growth

## Dependencies
- Upstash account (free tier: 10k requests/day)
