# AUDIT.md — Code Quality Audit
*Updated by Judge Agent v2 | 2026-03-09*

## Summary

Code quality is **good for a demo app** — clean architecture, modern stack (Next.js 16, React 19, Tailwind 4, TypeScript). Primary risks are demo fidelity and missing test coverage, not fundamental code issues.

**Audit Score: 7.5/10** — Well-structured, deployment-ready, with minor cleanup opportunities.

---

## 1. Dead Code

### 1a. Console.error in Error Boundaries
**Severity:** Low | **Impact:** Bad look if DevTools open during demo
- `src/app/salesforce/error.tsx:6` — `console.error('[Signal Studio] Salesforce view error:', ...)`
- `src/app/dashboard/error.tsx:6` — `console.error('[Signal Studio] Dashboard view error:', ...)`
- `src/app/mobile/error.tsx` — likely similar pattern (not verified)
- `src/app/create/error.tsx` — likely similar pattern (not verified)
- `src/app/global-error.tsx` — console.error
- `src/components/ErrorBoundary.tsx` — console.log/error calls
- **Fix:** Add optional `context` prop to `DemoErrorFallback`; remove bare console calls. Already using `DemoErrorFallback` correctly — just strip the console lines.
- **Effort:** 15 minutes

### 1b. Unused `#analytics` Route in App Launcher
**Severity:** Low
- App launcher has `href: '#'` for analytics — route never implemented
- Clicking it does nothing (dead link in demo)
- **Fix:** Remove from launcher OR add simple placeholder page at `/analytics`
- **Effort:** 15 minutes

---

## 2. DRY Violations

### 2a. Error Page Pattern Duplication
**Severity:** Medium | **Files:** 4 route-level `error.tsx` files
- All 4 error files: identical `ErrorProps` interface, identical `DemoErrorFallback` import, only differ in `console.error` context string and subtitle text
- Already improved by using `DemoErrorFallback` (good!) but boilerplate remains
- **Fix:** Move context string to `DemoErrorFallback` props; all error.tsx files become ~8 lines
- **Estimated savings:** ~60 lines of duplication removed

### 2b. SLDS Component Split
**Severity:** Low | **Files:** `slds-icons.tsx`, `slds-patterns.tsx`
- Two files serving Salesforce Lightning DS — may have overlapping utility patterns
- Could consolidate into `src/components/slds/index.ts` with named exports
- **Note:** Only refactor if these files are actively modified; otherwise stable dead code is fine

---

## 3. Security Issues

### 3a. Rate-Limit CVE in devDependency Chain
**Severity:** Medium (dev-only, no production risk)
- **CVE:** GHSA-46wh-pxpv-q5gq — IPv4-mapped IPv6 bypass in express-rate-limit
- **Path:** shadcn → @modelcontextprotocol/sdk → express-rate-limit >=8.2.0 <8.2.2
- **Git:** Fixed in commit `036a20c` — verify current version is clean
- **Command:** `cd demo-app && pnpm audit` to confirm resolved
- **Production impact:** NONE — static export, no server runtime

### 3b. Public GitHub Repo with Business Context
**Severity:** Medium | **Repo:** `TrendpilotAI/invesco-demo`
- Demo is public on GitHub under `TrendpilotAI` org
- Review for: Invesco employee names (Megan Weber, Craig Lieb, Brian Kiley) in code
- `?demo=megan` and `?demo=craig` URL params may be fine (just persona labels) but verify data doesn't include actual employee details
- Internal deal context (deal size, timeline) should NOT be in public code comments
- **Fix:** Audit all `.ts/.tsx` files for proper nouns + deal details; move sensitive docs to private repo
- **Command:** `grep -r "Megan\|Craig\|Brian\|Kiley\|Weber\|Lieb\|300K\|retention" src/ --include="*.ts" --include="*.tsx"`

### 3c. No Authentication on Demo URL
**Severity:** Low (intentional for demo)
- Demo is publicly accessible without auth
- URL obscurity is the only protection (acceptable for demo phase)
- **Mitigation:** PostHog analytics will show if unexpected visitors arrive
- **Post-win:** Add Basic Auth or Vercel password protection before any sensitive data is added

---

## 4. Dependency Health

### 4a. Verify Package Freshness
```bash
cd /data/workspace/projects/invesco-retention/demo-app
pnpm outdated
pnpm audit
```
- Next.js 16, React 19, Tailwind 4 — cutting edge, likely fine
- `@modelcontextprotocol/sdk` — track version as this changes rapidly
- shadcn components — check for breaking changes

### 4b. Node.js Version Lock
- Verify `.nvmrc` or `engines` in `package.json` specifies Node version
- Prevents deploy failures from Node version drift

---

## 5. Test Coverage

### 5a. Current Coverage: ~0%
- No test files found in `src/__tests__/` or adjacent to components
- No `playwright.config.ts` found
- **Risk:** Any code change could break demo undetected until it's live

### 5b. Priority Test Targets
| Test | Type | Risk if Missing |
|---|---|---|
| `?demo=megan` persona loads | E2E | Megan demo breaks silently |
| Salesforce page renders signals | E2E | Hero feature failure |
| Dashboard loads advisor data | E2E | Demo regression |
| mock-data all personas complete | Unit | undefined in demo |
| ROI calculator math | Unit | Wrong numbers shown |

### 5c. Recommendation
- Add Playwright: `pnpm create playwright` in demo-app
- 1 spec file covering the 5 scenarios above = 80% risk reduction
- Run in GitHub Actions before every deploy

---

## 6. Performance

### 6a. Bundle Size (Unverified)
- `src/lib/mock-data.ts` is 880 lines — all imported into client bundles
- Consider: lazy-load advisor data per-route vs. shipping everything upfront
- **Check:** `ANALYZE=true pnpm build` — if > 300kb initial JS, refactor

### 6b. Lighthouse Score
- Run Lighthouse on deployed URL: https://trendpilotai.github.io/invesco-demo/
- Target: 95+ Performance (static site should easily achieve this)
- Target: 100 Accessibility (important for enterprise demo)
- **Command:** `npx lighthouse https://trendpilotai.github.io/invesco-demo/ --view`

### 6c. GitHub Pages vs Vercel
- GitHub Pages has CDN but no edge functions
- If any server-side features are needed post-win, migrate to Vercel
- Static export is correct for current needs

---

## 7. Architecture Observations

### 7a. Well-Designed Areas ✅
- `combined-data.ts` properly aggregates synthetic data sources
- `DemoResetOverlay` is a clean state management approach
- `DemoErrorFallback` centralizes error UI (good!)
- `posthog.ts` isolation is clean — analytics don't pollute components
- TypeScript types in `src/lib/data/types.ts` are well-defined

### 7b. Areas to Watch ⚠️
- `mock-data.ts` at 880 lines will grow unwieldy — consider splitting by domain
- `salesforce/page.tsx` may become large as features are added — extract sub-components
- No `constants.ts` pattern for magic strings (signal severities, persona IDs)

---

## Quick Wins Checklist

- [ ] `pnpm audit` — verify no unresolved CVEs
- [ ] Remove console.error from 4 error.tsx files (~15min)
- [ ] Remove #analytics dead route (~15min)  
- [ ] `grep` for Invesco employee names in public code (~10min)
- [ ] Run Lighthouse on deployed URL (~5min)
- [ ] Add `engines` field to package.json for Node version lock (~5min)
