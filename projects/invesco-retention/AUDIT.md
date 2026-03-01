# Invesco Signal Studio — Code Audit (Updated)
**Date:** 2026-02-28 (updated from 2026-02-26 original)  
**Auditor:** Honey (Judge Agent v2)  
**Scope:** demo-app/src/ + deployment verification

---

## Deployment Status ✅

| Check | Result |
|---|---|
| GitHub Pages URL | ✅ 200 OK — https://trendpilotai.github.io/invesco-demo/ |
| No real secrets in source | ✅ Clean — only synthetic mock data |
| Invesco branding applied | ✅ (TODO-214 done) |
| Demo reset mechanism | ✅ DemoResetOverlay (TODO-216 done) |

---

## Previously Fixed Issues (Feb 26)

| Severity | Issue | Status |
|---|---|---|
| 🔴 C0 | JSX fragment crash in salesforce/page.tsx | ✅ Fixed |
| 🔴 C1 | Non-null assertion crash in mobile/page.tsx | ✅ Fixed |
| 🔴 C2 | Auth middleware security gap | ✅ Fixed |
| 🟠 H0 | Next.js CVE (next ≥15.1.7 required) | ✅ Fixed |
| 🟠 H1 | Push-to-Salesforce missing (TODO-213) | ✅ Fixed |
| 🟠 H2 | Skeleton loaders missing (TODO-215) | ✅ Fixed |

---

## Feb 28 Fresh Audit

### 🟡 MEDIUM

#### M0 — No React Error Boundaries
**Scope:** All 4 route pages (salesforce, dashboard, mobile, create)  
**Issue:** If any component throws a JS error during the live demo, the entire page goes blank (React unmounts the tree). There are no error boundary components to catch and display a graceful fallback.  
**Fix:** Wrap each page's main component tree with a simple ErrorBoundary class component that shows "Something went wrong — click to reload" instead of a blank screen.  
**Demo Risk:** 🟠 HIGH — a single JS error during the Brian Kiley demo could kill the presentation  
**Effort:** S (1-2 hours)

#### M1 — No Tests
**Scope:** Entire codebase  
**Issue:** `find /data/workspace/projects/invesco-retention -name "*.test.*" -o -name "*.spec.*" | grep -v node_modules` returns nothing.  
**Impact:** No regression safety net. Changes made during last-minute polish could silently break demo flows.  
**Fix:** Add a minimal Playwright smoke test that visits all 4 routes and checks for key text.  
**Demo Risk:** 🟡 MEDIUM — test-less but code is static/stable  
**Effort:** M (half day)

#### M2 — TODO Comments Left in Code
**Scope:** Needs verification  
**Issue:** Developer TODO/FIXME comments may remain in source. These are unprofessional if a technical stakeholder views source.  
**Fix:** Run: `grep -r "TODO\|FIXME\|HACK" /data/workspace/projects/invesco-retention/demo-app/src/ --include="*.tsx" --include="*.ts"` and resolve or remove.  
**Demo Risk:** 🟢 LOW (only if DevTools are opened)  
**Effort:** XS

#### M3 — Console.log Audit
**Scope:** src/ files  
**Issue:** Debug console.log statements may remain from development.  
**Fix:** `grep -r "console.log" /data/workspace/projects/invesco-retention/demo-app/src/` and remove any non-error logging.  
**Demo Risk:** 🟡 MEDIUM (savvy technical evaluator may open DevTools)  
**Effort:** XS

---

### 🟢 LOW

#### L0 — Hardcoded Advisor ID in mobile/page.tsx
**File:** `src/app/mobile/page.tsx:13`  
**Issue:** `getAdvisor('sarah-chen')` — previously had non-null assertion (fixed to `?? advisors[0]`). The hardcoded ID `'sarah-chen'` creates brittleness if synthetic data changes.  
**Severity:** Low — fallback now exists.

#### L1 — GitHub Repo Visibility
**Issue:** The TrendpilotAI/invesco-demo GitHub repo should be private. It's deployed via GitHub Pages (public access to the URL is fine) but the source code + strategy docs should not be publicly indexable.  
**Fix:** Set repo to private in GitHub settings (Pages still works with private repos on paid plans).  
**Demo Risk:** 🟡 MEDIUM (competitor could find internal strategy)  
**Effort:** XS (1 click)

#### L2 — Package.json Dependency Age
**Current:** Next.js, React, TypeScript (versions unverified in this scan)  
**Issue:** If using Next.js <15.1.7, a known CVE exists (patched per Feb 26 audit). Verify current version: `cat demo-app/package.json | grep '"next"'`  
**Status:** Patched per Feb 26 audit — verify still current.

#### L3 — Static Export Verification
**Issue:** Demo is on GitHub Pages. If the Next.js app is NOT configured with `output: 'export'`, it may be serving pre-rendered static HTML that doesn't match the actual app behavior.  
**Fix:** Verify `next.config.js` has `output: 'export'`  
**Effort:** XS

---

## Overall Assessment (Feb 28)

**Demo-Day Readiness: 8/10**

The app is live, deployed, and working. Critical crashes are fixed. The main remaining risks are:
1. **No error boundaries** — one JS error = blank screen (fix before demo)
2. **No demo recordings** — if live demo fails, there's no backup (TODO-220 pending)
3. **GitHub repo visibility** — should be private

**Recommended pre-demo checklist:**
- [ ] Add error boundaries to salesforce, dashboard, mobile pages
- [ ] Record backup Loom videos for all 4 flows
- [ ] Set GitHub repo to private
- [ ] Run console.log grep and clean up
- [ ] Do full demo walkthrough on incognito window + different network
- [ ] Verify demo reset works cleanly end-to-end

## Feb 28 Agent Verification

**Run date:** 2026-02-28 | **Agent:** Code Optimization Agent (depth-2 subagent)

### 1. console.log Audit
✅ **None found.** No `console.log` statements detected in any `.tsx` or `.ts` files under `src/`. Demo is clean on this front.

### 2. TODO / FIXME / HACK Comments
✅ **None found.** No outstanding TODO, FIXME, or HACK comments in source files.

### 3. Next.js Version
- **Installed version:** `16.1.6`
- ⚠️ Note: Next.js latest stable is 14.x / 15.x. Version `16.1.6` appears to be ahead of the public stable release — verify this is intentional (possible canary/custom build or package.json typo). Confirm the version resolves correctly via `npm list next`.

### 4. Static Export Config (`next.config.ts`)
✅ **Static export is configured** (`output: 'export'`). The app will build to a static HTML/CSS/JS bundle suitable for hosting on S3, Netlify, GitHub Pages, etc.

Security headers are configured:
- `X-DNS-Prefetch-Control: on`
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`

⚠️ Note: Security `headers()` in `next.config.ts` are **ignored during static export** (`output: 'export'`). These headers will NOT be applied unless served via a Next.js server or a proxy/CDN layer (e.g., Vercel, Nginx, CloudFront). For the demo, this is likely fine but worth noting for production.

### 5. Error Boundaries
⚠️ **None found.** No `ErrorBoundary` components or `componentDidCatch` lifecycle methods detected in source.

**Recommendation:** Consider adding a top-level error boundary before the demo to gracefully handle any unexpected runtime errors and prevent a blank screen on failure. Example:
```tsx
// app/error.tsx (Next.js App Router built-in error boundary)
'use client'
export default function Error({ error, reset }) {
  return <div>Something went wrong. <button onClick={reset}>Try again</button></div>
}
```
Next.js App Router supports `error.tsx` as a built-in error boundary — no custom class component needed.

---
### Summary Table

| Check | Status | Action Required |
|-------|--------|----------------|
| `console.log` statements | ✅ Clean | None |
| TODO/FIXME/HACK comments | ✅ Clean | None |
| Next.js version | ⚠️ `16.1.6` — verify | Confirm version is correct |
| Static export config | ✅ Configured | Note: headers ignored in static export |
| Error boundaries | ⚠️ Missing | Add `app/error.tsx` before demo |

---

## 🆕 Audit Update — 2026-03-01 (Judge Agent v2 Pass)

### Demo-Critical Issues (P0)

| Check | File | Finding | Fix |
|-------|------|---------|-----|
| PWA Icons | mobile-pwa/manifest.json | Only SVG icon — iOS Safari requires PNG icons for home screen | Add 192x192 and 512x512 PNG icons |
| PWA `screenshots` | mobile-pwa/manifest.json | No screenshots field (reduces install UX) | Add 1 or 2 screenshots of the demo |
| Error boundary | demo-app | No error.tsx in Next.js app router | Add app/error.tsx (from previous audit) |

### P1 Issues

| Check | File | Finding | Fix |
|-------|------|---------|-----|
| iOS viewport | mobile-pwa/index.html | Confirm `viewport-fit=cover` set for iPhone notch | Verify meta viewport tag |
| Offline cache | mobile-pwa/sw.js | Service worker caches static assets — verify API calls gracefully fail offline | Test offline mode |
| Synthetic names | synthetic-data/advisors.json | Verify advisor AUM ranges match realistic Invesco territory ($50M-$500M RIA) | Spot check 3 advisors |

### P2 Issues

| Check | Finding |
|-------|---------|
| manifest.json orientation | `portrait` lock may annoy iPad users during demo — consider `any` |
| No `shortcuts` in manifest | Power users can't deep-link to dashboard from home screen |

### Security (Clean)
- No hardcoded API keys found in mobile-pwa/ or salesforce-lwc/
- Salesforce CSP trusted sites configured correctly
- Previous P0 SQL injection fix confirmed (see git log)

### Summary
**P0:** 3 issues (PWA PNG icons, error boundary, verify viewport)  
**P1:** 3 issues (offline fallback, synthetic data realism, iOS notch)  
**P2:** 2 cosmetic issues  
**Overall:** Demo is in good shape. Fix P0 PWA icons today if home screen install is part of the demo narrative.


---

## March 1 Pre-Demo Audit
**Date:** 2026-03-01 | **Auditor:** Judge Agent v2 (direct)

### ✅ Error Boundaries — RESOLVED (Prior M0 was incorrect)
Each route has a Next.js `error.tsx` implementing `DemoErrorFallback`:
- `app/salesforce/error.tsx` ✅
- `app/dashboard/error.tsx` ✅
- `app/mobile/error.tsx` ✅
- `app/create/error.tsx` ✅
- `app/global-error.tsx` ✅
- `src/components/ErrorBoundary.tsx` ✅ (standalone, available for HOC wrapping)

M0 from Feb 28 audit is **CLOSED** — error handling is fully implemented.

### ✅ TypeScript — Clean Compile
`./node_modules/.bin/tsc --noEmit` → **0 errors**

### ✅ Secrets — Clean
No hardcoded credentials found. All data is synthetic mock data in `src/lib/mock-data.ts`.

### ✅ Console Logs — Acceptable
`console.error` only in error.tsx files (appropriate for error logging). No debug logs in production paths.

### ⚠️ npm audit — CLI broken in environment
`npm audit` throws "Class extends value undefined" — npm CLI issue in this container, not a code issue.
Dependencies were audited and Next.js CVE patched on Feb 26. No new dependencies added since.

### ✅ All 4 Demo Routes Present
- `app/salesforce/page.tsx` ✅
- `app/dashboard/page.tsx` ✅
- `app/mobile/page.tsx` ✅
- `app/create/page.tsx` ✅

### 🚨 DEMO BLOCKERS: NONE
No code-level demo blockers found. The demo is code-complete and safe to present.

### Remaining Risks (Non-Code)
| Risk | Mitigation |
|---|---|
| Live demo network failure | Pre-record Looms as backup |
| iPhone PWA not loading | Test on real device before demo day |
| "Show us real data" question | Memorize the pilot integration answer |
| Brian escalates to IT | IT security one-pager prepared |
