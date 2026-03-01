# 373 — Add Per-Endpoint Rate Limiting for /api/generate and /api/video

## Task Description
Global rate limiting (100 req/15min/IP) exists but AI generation endpoints are expensive. `/api/generate` and `/api/video` should have tighter per-route limits (e.g., 10 req/15min) to prevent cost abuse and API quota exhaustion.

## Coding Prompt
You are working on the NarrativeReactor repo at `/data/workspace/projects/NarrativeReactor/`.

Read `src/index.ts` and any route files to understand current rate limiting setup. The global limiter uses `express-rate-limit`.

Add stricter per-route limiters to the AI generation endpoints:

```typescript
import rateLimit from 'express-rate-limit';

const aiGenerateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 10,                    // 10 requests per window per IP
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many generation requests. Please wait before retrying.' },
  keyGenerator: (req) => {
    // Use API key as identifier if present, fall back to IP
    return (req.headers['x-api-key'] as string) || req.ip || 'unknown';
  }
});

const videoGenerateLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 5,                     // 5 video generations per hour
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many video generation requests. Please wait before retrying.' },
  keyGenerator: (req) => (req.headers['x-api-key'] as string) || req.ip || 'unknown',
});
```

Apply these limiters to the specific routes:
- `router.post('/api/generate', aiGenerateLimiter, ...)` or equivalent
- `router.post('/api/video', videoGenerateLimiter, ...)` or equivalent

Also ensure Express has `app.set('trust proxy', 1)` set so `req.ip` resolves correctly behind Railway's proxy (otherwise all requests appear to come from the same IP and share the limit).

Add a test in `src/__tests__/routes/rateLimiting.test.ts`:
- Fire 11 requests to `/api/generate` → first 10 succeed (or 401 due to auth, not 429), 11th returns 429
- Use a mock or bypass auth in test environment

Run `npm test` to confirm all tests pass.

## Dependencies
None

## Estimated Effort
S

## Acceptance Criteria
- [ ] `/api/generate` has 10 req/15min limit per API key
- [ ] `/api/video` has 5 req/1hr limit per API key
- [ ] Rate limit key is API key (not just IP) when present
- [ ] `trust proxy` is set so Railway proxy doesn't collapse all IPs
- [ ] 429 response includes `Retry-After` header (via `standardHeaders: true`)
- [ ] Rate limiter test verifies 429 is returned after limit exceeded
- [ ] All existing tests pass
