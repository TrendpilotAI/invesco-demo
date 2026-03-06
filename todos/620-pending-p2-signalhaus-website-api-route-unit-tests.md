# TODO 620 — API Route Unit Tests with Vitest

**Repo:** signalhaus-website
**Priority:** P2
**Effort:** S (1-2 days)
**Status:** pending

## Problem
`/api/contact` has complex logic (rate limiting, input validation, XSS prevention, HTML escaping, Resend + Slack integration). Zero tests exist. Regressions go undetected.

## Task
Add Vitest unit tests for the `/api/contact` API route.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/:

1. Install: npm install -D vitest @vitest/coverage-v8

2. Add to package.json scripts:
   "test": "vitest run",
   "test:watch": "vitest",
   "test:coverage": "vitest run --coverage"

3. Create vitest.config.ts:
   import { defineConfig } from "vitest/config"
   export default defineConfig({ test: { environment: "node" } })

4. Create src/app/api/contact/__tests__/route.test.ts with tests for:
   
   a. Rate limiting:
   - 5 requests from same IP → 6th returns 429
   - Different IPs are independent
   - Rate limit window resets after 15 minutes
   
   b. Input validation:
   - Missing required fields (name, email, message) → 400
   - Invalid email format → 400  
   - Message too short → 400
   - XSS in inputs → sanitized or rejected
   
   c. Successful submission:
   - Valid input → calls Resend (mocked)
   - Valid input → calls Slack webhook (mocked)
   - Returns 200 with success message
   
   d. Service failures:
   - Resend API error → returns 500
   - Slack webhook failure → still returns 200 (non-critical)

5. Mock external services:
   vi.mock("resend", () => ({ Resend: vi.fn(() => ({ emails: { send: vi.fn() } })) }))
   Use vi.stubGlobal for fetch (Slack webhook)

6. Add "test" to GitHub Actions CI workflow (once TODO 611 is done)
```

## Acceptance Criteria
- [ ] `npm test` runs without errors
- [ ] Rate limiting logic tested (happy + edge cases)
- [ ] Input validation tested (all required fields)
- [ ] XSS prevention tested
- [ ] External services mocked (no real API calls in tests)
- [ ] Coverage >80% for `/api/contact/route.ts`
