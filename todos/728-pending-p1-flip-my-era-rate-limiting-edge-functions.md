# TODO-728: Rate Limiting on Story Generation Edge Functions

**Repo:** flip-my-era  
**Priority:** P1  
**Effort:** Low-Medium (2-4 hours)  
**Status:** pending

## Description
No per-user rate limiting exists on story generation. Free users could drain API costs by spamming generation requests even before credit checks. Paid users could accidentally (or maliciously) trigger excessive Groq/Runware calls.

## Coding Prompt
```
In /data/workspace/projects/flip-my-era/supabase/functions/:

1. Create a rate-limit utility (supabase/functions/_shared/rate-limit.ts)
   - Uses Supabase DB table: rate_limits (user_id, action, count, window_start)
   - Function: checkRateLimit(userId, action, maxPerHour, maxPerDay)
   - Returns: { allowed: boolean, remaining: number, resetAt: Date }

2. Create migration: supabase/migrations/xxx_add_rate_limits_table.sql
   CREATE TABLE rate_limits (
     user_id uuid NOT NULL,
     action text NOT NULL,
     count integer DEFAULT 0,
     window_start timestamptz DEFAULT now(),
     PRIMARY KEY (user_id, action)
   );
   -- Index for cleanup
   CREATE INDEX ON rate_limits (window_start);

3. Add rate limit checks to these edge functions:
   - groq-api/index.ts: 20 requests/hour, 100/day per user
   - stream-chapters/index.ts: 10 requests/hour, 50/day per user
   - groq-storyline/index.ts: 20 requests/hour, 100/day per user

4. Return 429 Too Many Requests with Retry-After header when limit exceeded

5. Add cron cleanup (supabase/functions/cleanup-rate-limits/):
   - Delete rate_limit rows older than 24 hours
   - Schedule: daily via pg_cron or Supabase scheduled function

6. Frontend: handle 429 response in story generation hooks
   - Show toast: "You've hit your generation limit. Try again in X minutes."
```

## Acceptance Criteria
- [ ] Generating 21 stories in an hour returns 429 on the 21st
- [ ] 429 response includes Retry-After header
- [ ] Frontend shows friendly rate limit message
- [ ] Rate limit table auto-cleans old entries
- [ ] Admin (service role) bypasses rate limits
