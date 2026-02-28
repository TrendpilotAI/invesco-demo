# Add API Rate Limiting

**Repo:** signal-builder-backend  
**Priority:** high  
**Effort:** S (2-3 hours)  
**Phase:** 0

## Problem
No rate limiting on any endpoints. Auth endpoints vulnerable to brute force. Signal validation endpoint (computationally expensive) can be abused.

## Task
1. Add `slowapi` to Pipfile
2. Configure `Limiter` with Redis backend (already available)
3. Apply limits:
   - `/auth/` endpoints: 10 req/min per IP
   - `/signals/*/validate/`: 30 req/min per user
   - Default: 100 req/min per user
4. Return proper 429 responses with Retry-After header
5. Add rate limit headers to all responses

## Acceptance Criteria
- slowapi middleware installed and configured
- Auth endpoints protected from brute force
- 429 responses include Retry-After header
- Rate limits configurable via environment variables
