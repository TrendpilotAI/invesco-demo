---
id: 638
status: pending
priority: P1
repo: signal-studio-templates
title: Rate limit by JWT sub claim (not IP)
effort: S (half day)
dependencies: []
---

# Fix Rate Limiting: Use JWT Sub Claim Instead of IP

## Problem
Current rate limiters in `api/templates.ts` use IP-based limiting (`keyGenerator` defaults to IP). Behind a load balancer or reverse proxy, all requests appear to come from the same IP, making rate limits ineffective. Financial API rate limits should be per authenticated user (JWT `sub` claim).

## Task
Update rate limiters to use the JWT `sub` claim as the key when a valid JWT is present, fall back to IP for unauthenticated requests.

## Coding Prompt
```
Edit /data/workspace/projects/signal-studio-templates/api/templates.ts

Update globalLimiter and executeLimiter to use JWT sub:

const jwtSubOrIp = (req: Request): string => {
  // req.auth is set by express-jwt middleware
  const sub = (req as any).auth?.sub;
  return sub ?? req.ip ?? 'anonymous';
};

const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: jwtSubOrIp,
  standardHeaders: 'draft-7',
  legacyHeaders: false,
  message: { error: 'Too many requests. Global limit: 100 req / 15 min.' },
});

const executeLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 20,
  keyGenerator: jwtSubOrIp,
  standardHeaders: 'draft-7',
  legacyHeaders: false,
  message: { error: 'Too many execute requests. Limit: 20 req / 60 sec.' },
});

Add test in __tests__/api.test.ts verifying that two requests with different JWT subs
are tracked independently, and same sub from different IPs share one limit.
```

## Acceptance Criteria
- [ ] Rate limits keyed by JWT `sub` when token present
- [ ] Falls back to IP for unauthenticated requests
- [ ] Unit test verifies per-sub limiting
- [ ] `pnpm test` passes
