# 🔴 CRITICAL Issues — SignalHaus Website
*Flagged: 2026-03-15*

## 1. Rate Limiter May Be Broken in Production
**Severity:** CRITICAL | **Status:** NEEDS VERIFICATION
**File:** `src/app/api/contact/route.ts`

Upstash packages are installed, but `getRatelimit()` falls back to an in-memory `Map` when `UPSTASH_REDIS_REST_URL` or `UPSTASH_REDIS_REST_TOKEN` are missing. On Vercel serverless, Map state resets on every cold start = zero rate limiting.

**Action:** Verify these env vars are set in Vercel dashboard → Settings → Environment Variables for Production. If not, the rate limiter is effectively disabled.

## 2. No Bot Protection on Contact Form
**Severity:** CRITICAL | **Status:** NOT IMPLEMENTED
**Files:** `src/app/contact/ContactForm.tsx`, `src/app/api/contact/route.ts`

No CAPTCHA, Turnstile, or honeypot field. The manual `BLOCKED_PATTERNS` XSS check is trivially bypassed by automated form submission tools. Any bot can spam the contact form and flood the Resend email quota + Slack channel.

**Action:** Implement Cloudflare Turnstile (free, invisible mode). ~2h effort.

## 3. Near-Zero Test Coverage
**Severity:** HIGH | **Status:** MINIMAL PROGRESS
**Current:** 1 test file (`roi.test.ts`), 0 tests for critical paths

Contact form validation, API routes, MDX parsing, and all components are untested. Any refactor risks silent breakage. The CI pipeline runs tests but there's almost nothing to run.

**Action:** Write Vitest tests for `validateContact()`, API routes (with msw mocks), and MDX parsing. ~5h total effort.
