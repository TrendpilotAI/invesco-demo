# Signal Studio Frontend — Prioritized TODOs

> Generated: 2026-03-11 | Composite Score: 5.8/10

---

## 🔴 CRITICAL

### 1. Fix 32 Unprotected API Routes (Security — P0)
- **Impact:** All 32/44 API routes bypass auth via middleware whitelist
- **Risk:** Unauthenticated DB queries, AI cost DoS, data exfiltration
- **Fix:** Create `lib/auth/require-auth.ts`, apply to all routes
- **Effort:** M (2-4 hours)
- **Blocks:** Production deployment, any client demo

### 2. Add Rate Limiting on AI Chat Routes (Security — P0)
- **Impact:** Any user can spam `/api/chat/*` burning OpenAI/Anthropic credits
- **Fix:** Add `@upstash/ratelimit` (10 req/min/user on chat, 30 on oracle)
- **Effort:** S (1 hour)

---

## 🟠 HIGH

### 3. Add Tests to CI Pipeline (Quality — P0)
- **Impact:** Tests exist (26 files) but never run in CI — regressions go undetected
- **Fix:** Add `pnpm test:ci` + `pnpm audit` steps to `bitbucket-pipelines.yml`
- **Effort:** S (30 min)

### 4. Production Deployment (Business — P0)
- **Impact:** Platform is feature-complete but unreachable — zero revenue
- **Fix:** Deploy to Vercel/GCP, configure domain (signalstudio.signalhaus.ai), SSL, health check
- **Effort:** M (2-3 hours)

### 5. Add Zod Validation to All POST/PUT API Routes (Quality — P1)
- **Impact:** No runtime input validation — malformed requests can cause crashes
- **Fix:** Add Zod schemas to all data-mutating routes
- **Effort:** M (3-4 hours)

---

## 🟡 MEDIUM

### 6. Archive 37 Stale Root Markdown Files (Maintenance)
- `mkdir -p docs/archive && mv AI-CHAT-*.md IMPLEMENTATION-*.md MVP-*.md PHASE3-*.md docs/archive/`
- Move debug scripts (`test-*.js`, `check-*.js`) to `scripts/debug/`
- **Effort:** S (10 min)

### 7. Resolve Duplicate Middleware (Architecture)
- Root `middleware.ts` (active) vs `src/middleware.ts` (ignored by Next.js)
- Compare, merge unique logic, delete `src/middleware.ts`
- **Effort:** S (15 min)

### 8. Centralize Oracle Connection & AI Client Init (Code Quality)
- Three services independently init Oracle connections — consolidate to single factory
- AI clients initialized inline across routes — create `lib/ai/clients.ts` singletons
- **Effort:** M (2 hours)

### 9. Fix `any` Types in Oracle Service (Code Quality)
- 8+ `any` usages in `lib/oracle-service.ts`
- Replace with proper `oracledb` types
- **Effort:** S (1 hour)

### 10. Add Component Tests for Core UI (Testing)
- Signal Library, AI Chat Panel, Visual Builder have zero component tests
- Add React Testing Library tests for critical user flows
- **Effort:** M (4-6 hours)

---

## 🟢 LOW

### 11. Configure CORS headers in `next.config.mjs`
### 12. Add Sentry error tracking post-deployment
### 13. Add PostHog product analytics
### 14. Remove redundant `@anthropic-ai/sdk` (keep `@ai-sdk/anthropic`)
### 15. Add Renovate/Dependabot for automated dependency updates
