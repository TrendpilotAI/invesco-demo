# MASTER-TODO: signal-builder-frontend
**Scored:** 2026-03-13 | **Composite:** 5.8/10 | **Tier:** 2

## Score Breakdown
| Dimension       | Score |
|----------------|-------|
| code_quality   | 6.0   |
| test_coverage  | 3.0   |
| security       | 4.0   |
| documentation  | 5.0   |
| architecture   | 7.0   |
| business_value | 7.0   |
| **COMPOSITE**  | **5.8** |

## 🚨 CRITICAL FLAGS
- **Bitbucket pipeline uses `REACT_APP_*` env vars instead of `VITE_*`** — deployed builds break API connectivity
- **Axios interceptor returns error object instead of rejecting Promise** — React Query errors silently swallowed, no user feedback
- **localStorage auth token storage** — XSS vulnerability, should use httpOnly cookies
- Missing E2E tests, coverage ~15-20%
- Storybook uses webpack bundler alongside Vite — unnecessary bloat
- nginx config missing critical security headers

---

## P0 — Fix Now (Prod Broken)
- [ ] Fix Bitbucket pipeline: replace `REACT_APP_*` env var prefix with `VITE_*` across all pipeline steps
- [ ] Fix Axios response interceptor to `return Promise.reject(error)` instead of returning error object
- [ ] Verify deployed builds can connect to API endpoints after env fix

## P1 — This Sprint
- [ ] Remove localStorage auth token fallback — use httpOnly cookies only to close XSS vector
- [ ] Add Playwright E2E tests for critical flows: login → signal builder → save → publish
- [ ] Add nginx security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options

## P2 — Next Sprint
- [ ] Migrate Storybook to Vite-based builder, remove webpack dependencies
- [ ] Increase unit test coverage from ~15% to 50%+
- [ ] Remove dead code / duplicate utility functions
- [ ] Improve README with full setup and deployment guide

## P3 — Backlog
- [ ] Add loading states and skeleton screens for signal builder UX
- [ ] Implement signal preview live mode
- [ ] Add API request caching layer
- [ ] Accessibility audit and WCAG 2.1 compliance pass
