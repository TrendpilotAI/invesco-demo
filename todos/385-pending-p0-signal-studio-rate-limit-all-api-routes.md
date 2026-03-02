# TODO-385: Extend Rate Limiting to Oracle Query and Signal Run Routes

**Repo:** signal-studio
**Priority:** P0 (security hardening)
**Effort:** S (2-3 hours)
**Status:** pending
**Audit ref:** NEW-004

## Description
LLM proxy routes have per-IP rate limiting (20 req/min) but `/api/signals/run` and `/api/oracle/query` are unprotected from abuse. An attacker could spam Oracle queries or signal executions causing cost overruns and database exhaustion.

## Task
1. Locate existing rate limiting implementation (check `app/api/llm/` middleware)
2. Extract rate limiter into shared `lib/rate-limit.ts` utility
3. Apply to:
   - `app/api/signals/run/route.ts` — 10 req/min per IP
   - `app/api/oracle/query/route.ts` — 5 req/min per IP (Oracle queries are expensive)
   - `app/api/oracle/execute/route.ts` — 5 req/min per IP
4. Return 429 with `Retry-After` header on limit exceeded
5. Test with: `for i in {1..15}; do curl -X POST /api/signals/run; done`

## Coding Prompt (autonomous execution)
```
In /data/workspace/projects/signal-studio/:
1. Read app/api/llm/ or app/api/ai/ to find existing rate limiter pattern
2. Create lib/rate-limit.ts with reusable createRateLimiter(max, windowMs) factory
3. Import and apply in:
   - app/api/signals/run/route.ts (10/min)
   - app/api/oracle/query/route.ts (5/min)
4. Ensure 429 response includes Retry-After header
5. Add unit test in __tests__/rate-limit.test.ts
```

## Acceptance Criteria
- [ ] Rate limiter applied to signals/run and oracle/query routes
- [ ] 429 returned after limit exceeded
- [ ] Existing LLM rate limiting unchanged
- [ ] Unit test passes

## Dependencies
None.
