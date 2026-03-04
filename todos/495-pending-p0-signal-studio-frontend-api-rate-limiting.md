# TODO-495: Add Rate Limiting to AI API Routes

**Repo:** signal-studio-frontend  
**Priority:** P0  
**Effort:** M (4-6 hours)  
**Status:** pending

## Description
AI API routes (`/api/ai/completion`, `/api/chat/openrouter`, `/api/agent/research`, `/api/agent/morning-brief`) have no rate limiting. A single user could exhaust API credits. Redis is already present (dump.rdb in root).

## Coding Prompt
Implement rate limiting middleware for all AI routes:

1. Create `lib/middleware/rate-limit.ts`:
```typescript
import { LRUCache } from 'lru-cache'
// Use lru-cache (already a dependency) for in-memory rate limiting
// Or use Redis via ioredis for production distributed limiting
export function rateLimit(opts: { interval: number; uniqueTokenPerInterval: number }) { ... }
```

2. Apply to all AI routes with appropriate limits:
   - `/api/ai/completion`: 20 requests/minute per IP
   - `/api/chat/openrouter`: 30 requests/minute per user token  
   - `/api/agent/*`: 10 requests/minute per user token

3. Return 429 with `Retry-After` header when limit exceeded

4. Add rate limit headers to responses: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Acceptance Criteria
- [ ] 21st request within 1 minute returns 429
- [ ] Rate limit headers present on all AI route responses
- [ ] Different limits for different route tiers
