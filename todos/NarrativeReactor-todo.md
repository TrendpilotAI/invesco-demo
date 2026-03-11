# NarrativeReactor — Prioritized TODOs

> Generated: 2026-03-11 | Composite Score: 6.9/10

---

## 🔴 CRITICAL (Security — blocks production readiness)

### 1. Migrate SHA-256 API key hashing → scrypt
- **File:** `src/services/tenants.ts` line 131+
- **Risk:** SHA-256 is fast = brute-forceable; API keys at risk if DB leaks
- **Fix:** Complete scrypt migration (legacy fallback already scaffolded), remove SHA-256 path after migration window
- **Effort:** 2h | **Impact:** Security 5→7

### 2. Fix dual SQLite connection bug in tenants.ts
- **File:** `src/services/tenants.ts` line 6 — uses `better-sqlite3` directly
- **Risk:** Lock contention on every API auth call; bypasses WAL singleton from `db.ts`
- **Fix:** Migrate to `import { getDb } from '../lib/db'`, remove `better-sqlite3` dependency
- **Effort:** 2h | **Impact:** Architecture stability, removes native dep from Docker builds

### 3. Pin wildcard genkit dependencies
- **File:** `package.json` — 6 genkit packages at wildcard versions
- **Risk:** Any genkit release could break the app silently
- **Fix:** Pin to current working versions (e.g., `"^1.29.0"` instead of `"*"`)
- **Effort:** 30min | **Impact:** Supply chain security

---

## 🟡 HIGH PRIORITY (Quality & Reliability)

### 4. Add ESLint to project root
- **Status:** Only exists in `/dashboard`, not in main project
- **Fix:** Add `eslint.config.js` with TypeScript rules, add `lint` script to package.json, integrate into CI
- **Effort:** 1h | **Impact:** Code quality enforcement, catches bugs early

### 5. Replace console.log with pino structured logging
- **Status:** 18+ console.log/error calls across services
- **Fix:** Install pino, create logger singleton, replace all console calls, configure Railway log drain
- **Effort:** 3h | **Impact:** Production observability, debugging capability

### 6. Add SQLite indexes on hot query columns
- **Files:** `src/lib/db.ts` migration
- **Risk:** Performance degrades as data grows; every tenant auth lookup is unindexed
- **Fix:** Add indexes on `api_key_hash`, `tenant_id`, `campaign_id`, `created_at`
- **Effort:** 1h | **Impact:** Query performance at scale

### 7. Make video generation async (job queue)
- **File:** `src/flows/orchestration.ts`
- **Risk:** Synchronous Fal.ai calls block Express thread for 30-60s
- **Fix:** Implement video_jobs table + worker polling pattern (scaffolded in PLAN.md)
- **Effort:** 1d | **Impact:** Server stability under load

### 8. Add real HTTP E2E tests with supertest
- **Status:** E2E test exists but is fully mocked — no real HTTP layer testing
- **Fix:** Add supertest-based tests that boot the Express app and hit actual routes
- **Effort:** 1d | **Impact:** Confidence in deployment, catches integration bugs

---

## 🟢 MEDIUM PRIORITY (Polish & Features)

### 9. Remove dead code: trendpilotBridge.ts
- No route consumer found — either wire to a route or delete
- **Effort:** 15min

### 10. Move `@types/better-sqlite3` to devDependencies
- Currently in prod `dependencies` — types shouldn't ship to production
- **Effort:** 5min (once #2 is done, remove entirely)

### 11. Tree-shake lodash imports
- `contentPipeline.ts` imports full lodash (~70KB)
- **Fix:** `import merge from 'lodash/merge'`
- **Effort:** 15min

### 12. Build Content Repurposing Pipeline
- One-click: blog → Twitter thread → LinkedIn → newsletter
- Leverages existing AI flows + Blotato publisher
- **Effort:** 1.5d | **Impact:** Direct revenue upsell feature

### 13. API Key Rotation UI in dashboard
- Backend route `/api/tenants/:id/rotate-key` already exists
- Just needs React dashboard UI
- **Effort:** 1d | **Impact:** Self-service security for tenants

---

## Summary

| Priority | Count | Total Effort |
|----------|-------|-------------|
| 🔴 CRITICAL | 3 | ~5h |
| 🟡 HIGH | 5 | ~3d |
| 🟢 MEDIUM | 5 | ~3d |
