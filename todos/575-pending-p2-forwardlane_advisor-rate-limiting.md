# TODO-575: Add Rate Limiting to Auth & API Routes — forwardlane_advisor

**Repo:** forwardlane_advisor  
**Priority:** P2  
**Status:** pending

## Description
No rate limiting on login or dialog API endpoints — brute force and abuse risk.

## Steps
1. `npm install express-rate-limit`
2. Add rate limiter to `routes.js`:
   - Auth routes: max 10 req/15min
   - Dialog/AI routes: max 30 req/min per user
   - General API: max 100 req/min
3. Return 429 with `Retry-After` header
4. Log rate limit violations via bunyan

## Acceptance Criteria
- Brute force attempts fail after configured limit
- Legitimate users not affected
- Rate limit headers returned in responses

## Dependencies
None
