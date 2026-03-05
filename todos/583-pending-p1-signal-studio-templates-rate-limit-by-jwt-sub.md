# TODO 583: Fix Rate Limiting — Use JWT Sub, Not IP

**Repo:** signal-studio-templates  
**Priority:** P1 (Security — current rate limiting is bypassable)  
**Effort:** S (1–2 hours)  
**Status:** pending

## Description

Current rate limiting uses IP address as the key. This fails in two ways:
1. Behind a load balancer/reverse proxy, all requests appear to come from the same IP (proxy IP), making rate limiting useless
2. Users behind shared NAT/office networks all share one IP limit

For an authenticated API (JWT), rate limiting should be keyed by `req.auth.sub` (user identity from JWT).

## Fix

```typescript
// In api/templates.ts — configure trust proxy + custom key generator

// 1. In the Express app setup (before routes):
app.set("trust proxy", 1); // Trust first proxy (nginx/ALB)

// 2. Custom key generator for authenticated routes:
const authenticatedLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 20,
  keyGenerator: (req) => {
    // Use JWT sub if authenticated, fall back to IP
    return (req as any).auth?.sub ?? req.ip ?? "anonymous";
  },
  standardHeaders: "draft-7",
  legacyHeaders: false,
});

// 3. Apply authMiddleware BEFORE rate limiter on execute route
router.post("/:id/execute", 
  cors(corsOptions),
  authMiddleware,      // ← authenticate first
  executeLimiter,      // ← then rate limit by identity
  async (req, res) => { ... }
);
```

## Acceptance Criteria

- [ ] `app.set("trust proxy", 1)` configured
- [ ] Rate limiters use `req.auth?.sub` as key when JWT present
- [ ] Auth middleware applied before rate limiting on protected routes
- [ ] Test: two different JWT users have independent rate limits
- [ ] Test: same user hitting limit gets 429 (not different user)
