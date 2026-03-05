# TODO-586: Extend Rate Limiting to All API Routes

**Repo:** signal-studio
**Priority:** P0
**Effort:** S (1-2 hours)
**Status:** pending

## Problem
`/api/oracle/query`, `/api/oracle/schema`, and `/api/signals/run` lack per-IP rate limiting.
LLM proxy routes already have it via `lib/rate-limit.ts`. Oracle queries and signal runs can be 
expensive (CPU, DB connections) and are attack vectors for scraping or DoS.

## Task
1. Audit all routes in `app/api/` without rate limiting
2. Apply existing `lib/rate-limit.ts` to: oracle query, oracle schema, signals/run, data-pipeline routes
3. Set appropriate limits (oracle: 30/min, signals: 20/min)
4. Return 429 with Retry-After header on limit exceeded
5. Add integration test

## Coding Prompt
```
In /data/workspace/projects/signal-studio:
1. Read lib/rate-limit.ts to understand existing implementation
2. Read app/api/oracle/query/route.ts and app/api/signals/run/route.ts
3. Apply rate limiting middleware to these routes (same pattern as LLM proxy)
4. Oracle query: 30 req/min per IP, Signal run: 20 req/min per IP
5. Test with: curl -X POST http://localhost:3000/api/oracle/query -H "Content-Type: application/json" -d '{}' --repeat 35
```

## Acceptance Criteria
- [ ] Oracle query route returns 429 after 30 req/min
- [ ] Signal run route returns 429 after 20 req/min
- [ ] 429 includes `Retry-After` header
- [ ] Existing unit tests still pass

## Dependencies
None
