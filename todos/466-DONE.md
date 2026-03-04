# TODO-466 — DONE ✅

**Task:** Add rate limiting and CORS to signal-studio-templates API  
**Commit:** `6d1e40c` — `feat: add rate limiting + CORS to Templates API (TODO-466)`  
**Pushed to:** `TrendpilotAI/signal-studio-templates` (main)  
**Date:** 2026-03-04

---

## What Was Changed

### `api/templates.ts`
- Added `cors` middleware with regex-based allowlist:
  - `https://*.forwardlane.com`
  - `https://*.invesco.com`
- Added global rate limiter: **100 req / 15 min** (per IP, RFC draft-7 headers)
- Added execute-specific rate limiter: **20 req / 60 sec** on `POST /templates/:id/execute`
- Pre-flight `OPTIONS` handling via `router.options("*", cors(...))`
- Exported `jsonBodyLimit` middleware (`express.json({ limit: "10kb" })`) for mounting in parent app
- Exported `corsOptions`, `globalLimiter`, `executeLimiter` for test/integration reuse

### `README.md`
- Added **Security Configuration** section documenting:
  - CORS allowlist table
  - Rate limit table (global + execute)
  - Body size limit (10kb)
  - Example mount snippet

### `package.json` + `pnpm-lock.yaml`
- Added `cors@2.8.6` + `express-rate-limit@8.2.1` as dependencies
- Added `@types/cors@2.8.19` as dev dependency

---

## Test Results
- All **25 tests** passed (`pnpm test`)
- TypeScript build clean (`pnpm build`)
