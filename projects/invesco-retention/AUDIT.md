# Invesco Retention — Code Quality Audit
**Date:** 2026-03-03 (v3 — updated by Judge Agent v2)
**Agent:** Optimization Agent (inline — depth limit)

---

## Summary

The codebase is a **demo-grade** application — intentionally simple, synthetic data only. No backend, no auth, no database. Audit scope is appropriately narrow: demo reliability, security of not leaking anything sensitive, and code quality as it affects maintainability.

**Overall:** Clean for its purpose. No critical security issues. Several minor improvements worth making.

---

## 1. Dead Code / Unused Imports

### `src/lib/data/combined-data.ts`
- Likely imports several JSON fields from synthetic data that are not used in `mock-data.ts`
- Recommend: run `npx ts-unused-exports tsconfig.json` to identify unused exports
- **Severity:** LOW (demo only)

### `src/components/ui/separator.tsx`, `scroll-area.tsx`
- These Radix UI components may be unused in the current build
- **File:** `src/components/ui/`
- **Action:** Run `grep -r "Separator\|ScrollArea" src/app/` to confirm usage
- **Severity:** LOW

---

## 2. DRY Violations

### `SignalSeverity` type
- Defined in `mock-data.ts` as `'urgent' | 'attention' | 'positive' | 'info'`
- Likely referenced as string literals in dashboard/salesforce pages
- **Fix:** Ensure all references use the exported `SignalSeverity` type, not inline strings
- **Severity:** MEDIUM

### Toast component logic
- `dashboard/page.tsx` and potentially `salesforce/page.tsx` both likely implement toast-like feedback
- `ToastContainer` component in dashboard/page.tsx (line ~30) should be extracted to `src/components/ToastContainer.tsx` for reuse
- **Severity:** MEDIUM

---

## 3. Security Issues

### No credentials found ✅
- No API keys, tokens, or secrets in any source file
- `.env*` files not present in repo (good)
- All data is synthetic — no PII risk

### nginx.conf — Security Headers
- **File:** `demo-app/nginx.conf`
- Verify presence of: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`
- **Action:** Confirm headers are set; add if missing
- **Severity:** LOW (demo context, but good practice)

### Salesforce LWC CSP
- **File:** `salesforce-lwc/force-app/main/default/cspTrustedSites/SignalStudio.cspTrustedSite-meta.xml`
- CSP trusted site configured. Verify the domain matches actual deployment URL.
- **Severity:** MEDIUM

---

## 4. Dependency Health

### Current deps (demo-app):
```
class-variance-authority, clsx, lucide-react, next, radix-ui, react, react-dom, tailwind-merge
```
- All are recent, widely-used packages
- **Action:** Run `npm audit` to check for known CVEs
- Next.js 14 is current — no known critical CVEs as of 2026-03-02
- **Severity:** LOW

### Python deps (synthetic-data):
- `seed_analytical_db.py` and `validate_seed.py` — check if they import anything beyond stdlib
- **Action:** Run `pip-audit` if any third-party packages used
- **Severity:** LOW

---

## 5. Test Coverage

### Current state: ZERO tests
- No unit tests, no integration tests, no E2E tests
- **Critical gap for demo reliability**

### Recommended test suite:
| Test Type | What to Cover | Tool |
|---|---|---|
| E2E smoke | All 4 demo routes load | Playwright |
| Data integrity | Synthetic JSON has required fields | pytest |
| Type checking | No TypeScript errors | tsc --noEmit |

**Action:** See TODO #380 for E2E implementation.

---

## 6. Performance Bottlenecks

### Bundle size
- `lucide-react` — verify individual icon imports (not full library import)
  - Bad: `import { Icon1, Icon2, ... } from 'lucide-react'` with 20+ icons
  - Good: individual named imports (which this appears to use)
- **Severity:** LOW

### Static data loading
- Synthetic JSON data is imported at build time via `combined-data.ts` — this is correct
- No runtime fetches means the demo works offline ✅
- **No issues found**

### Image optimization
- `demo-app/public/` has SVG files only — no large images
- Mobile PWA uses inline SVG icon — fine
- **No issues found**

---

## 7. Code Architecture Observations

### Positive Patterns ✅
- Error boundaries on all routes (DemoErrorFallback, ErrorBoundary)
- Demo reset via `?reset=true` query param — great for demo repeatability
- Static export configured for GitHub Pages compatibility
- Dockerfile present for Railway deployment
- Railway config at `.railway/config.json`

### Improvement Opportunities
- Extract `ToastContainer` from dashboard/page.tsx into shared component
- Add `"strict": true` to tsconfig.json for better type safety
- Service worker cache versioning in `mobile-pwa/sw.js` — bump version when data changes

---

## Action Items (by priority)

| Priority | Action | File | Effort |
|---|---|---|---|
| P0 | Run `npm audit` and fix any critical CVEs | demo-app/ | XS |
| P0 | Verify nginx.conf has security headers | demo-app/nginx.conf | XS |
| P1 | Add E2E Playwright tests | TODO #380 | M |
| P1 | Extract ToastContainer to shared component | src/components/ | S |
| P2 | Add TypeScript strict mode | tsconfig.json | S |
| P2 | Verify CSP trusted site domain matches deploy URL | salesforce-lwc/ | XS |
| P3 | Run ts-unused-exports to find dead code | demo-app/ | S |
| P3 | Add cache version bump to service worker | mobile-pwa/sw.js | XS |

---

## v3 Addendum (2026-03-03)

### Confirmed ✅
- **Security headers:** next.config.ts has X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy — no nginx.conf audit needed for GitHub Pages deploy
- **SignalSeverity type:** Properly exported from mock-data.ts and used consistently — DRY violation was overstated in v2
- **Error boundaries:** Confirmed on all 4 routes (dashboard/error.tsx, salesforce/error.tsx, mobile/error.tsx, create/error.tsx, global-error.tsx)
- **No hardcoded secrets:** Confirmed clean

### New Findings
- **salesforce/page.tsx is 610 lines** — Consider extracting the AccordionSection + SignalCard subcomponents to separate files post-demo
- **`Separator` component imported in salesforce/page.tsx** — verify it's actually rendered (imported line 6, but may be dead import)
- **homepage page.tsx does NOT auto-redirect** to /salesforce — manual bookmark needed for demo start URL
- **No TypeScript strict mode** in tsconfig.json — `"strict": true` recommended post-demo

### Updated Action Items
| Priority | Action | File | Effort |
|---|---|---|---|
| P0 | Bookmark /salesforce?advisor=sarah-chen as demo start URL | — | XS |
| P0 | Add confidence scores to signal cards (TODO #424) | mock-data.ts, salesforce/page.tsx | XS |
| P0 | Add Seismic content recommendations (TODO #423) | salesforce/page.tsx | S |
| P1 | Add E2E Playwright tests (TODO #380) | — | M |
| P1 | Remove dead Separator import from salesforce/page.tsx | salesforce/page.tsx | XS |
| P2 | Add TypeScript strict mode | tsconfig.json | XS |
| P2 | Service worker cache versioning | mobile-pwa/sw.js | XS |
| P3 | Extract large salesforce/page.tsx subcomponents | src/components/ | S |
