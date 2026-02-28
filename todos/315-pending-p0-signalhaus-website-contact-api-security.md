# TODO 315: SignalHaus Website — Contact API Security (Rate Limiting + Validation)

**Priority:** P0 (Security)
**Effort:** S (2-4 hours)
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Description
The `/api/contact` route has no rate limiting and no input validation. Any bot can spam the form, and malformed data goes straight to Resend.

## Acceptance Criteria
- [ ] Zod validation on name (min 2 chars), email (valid format), message (min 10 chars)
- [ ] Rate limiting: max 3 submissions per IP per 15 minutes
- [ ] Returns 400 with field-level errors on invalid input
- [ ] Returns 429 on rate limit exceeded
- [ ] No change to happy path behavior

## Coding Prompt

```
In /data/workspace/projects/signalhaus-website/src/app/api/contact/route.ts:

1. Add Zod validation:
   - Install: cd /data/workspace/projects/signalhaus-website && npm install zod
   - Schema: { name: z.string().min(2).max(100), email: z.string().email(), message: z.string().min(10).max(2000) }
   - Parse request body with schema.safeParse(), return 400 with errors if invalid

2. Add rate limiting using a simple in-memory Map (edge-compatible) or @upstash/ratelimit if UPSTASH_REDIS_REST_URL is configured:
   - Key: X-Forwarded-For header or "unknown"
   - Limit: 3 requests per 900 seconds (15 min)
   - Return 429 { error: "Too many requests. Please wait before submitting again." } if exceeded

3. Add explicit CORS headers:
   - Access-Control-Allow-Origin: https://www.signalhaus.ai
   - Access-Control-Allow-Methods: POST, OPTIONS
```

## Dependencies
None

## Notes
- Simple in-memory rate limiting is fine for a low-traffic site (resets on cold start)
- If Upstash Redis is available, use @upstash/ratelimit for persistent rate limiting
