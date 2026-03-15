# Signal Builder Frontend — Master TODO

*Judge Agent Scoring Run: 2026-03-15 16:20 UTC*
*Composite Score: 5.6/10*
*Previous Score: 5.7/10 (2026-03-15 07:20 UTC)*
*Trend: ▼ -0.1 (critical blockers unresolved 15+ days; security score degrading with time)*

---

## 🔴 CRITICAL (Fix Immediately)

### TODO-878: Fix Pipeline REACT_APP_* → VITE_* Env Vars
- **File:** `bitbucket-pipelines.yml` (demo + qa steps)
- **Impact:** Demo and QA deployments have NO API connectivity — all env vars silently ignored by Vite. App code uses `import.meta.env.VITE_*` (confirmed in `src/shared/config/appConfig.ts`), but pipeline injects `REACT_APP_*`.
- **Effort:** XS (30 min)
- **Fix:** Rename all `REACT_APP_*` → `VITE_*` in both `demo` and `qa` pipeline steps:
  - `REACT_APP_IS_DEV_AUTH_METHOD` → `VITE_IS_DEV_AUTH_METHOD`
  - `REACT_APP_API_BASE_PATH` → `VITE_API_BASE_PATH`
  - `REACT_APP_API_BASE_URL` → `VITE_API_BASE_URL`
  - `REACT_APP_FORWARDLANE_URL` → `VITE_FORWARDLANE_URL`
  - `REACT_APP_AUTH_COOKIE_DOMAIN` → `VITE_AUTH_COOKIE_DOMAIN`
  - `REACT_APP_FL_API_URL` → `VITE_FL_API_URL`
- **Status:** PENDING ⚠️ VERIFIED — pipeline still uses `REACT_APP_*` as of 2026-03-15 16:20
- **Days Open:** 15+ (since Vite migration commit `b3c0724`)

### TODO-879: Fix Axios Interceptor — Use Promise.reject()
- **File:** `src/shared/lib/getAxiosInstance.ts` (response interceptor, line ~58-65)
- **Impact:** React Query never sees errors; users get zero error feedback on failed API calls. TypeScript generics bypassed. The interceptor returns `{ error: { status, data } }` — React Query treats this as success.
- **Effort:** XS (15 min)
- **Fix:** Replace:
  ```ts
  return {
    error: {
      status: error.response?.status,
      data: error.response?.data.detail || error.message,
    },
  };
  ```
  With:
  ```ts
  return Promise.reject(error);
  ```
- **Status:** PENDING ⚠️ VERIFIED — interceptor still returns object as of 2026-03-15 16:20

### TODO-890: Fix .env.schema to use VITE_* prefix
- **File:** `.env.schema`
- **Impact:** Schema documents `REACT_APP_*` vars that Vite ignores — developers set wrong vars locally, app has no API URL
- **Effort:** XS (10 min)
- **Fix:** Rename all `REACT_APP_*` → `VITE_*` in `.env.schema` to match `src/shared/config/appConfig.ts`
- **Related:** TODO-878
- **Status:** PENDING ⚠️ VERIFIED — .env.schema still uses `REACT_APP_*` as of 2026-03-15 16:20

---

## 🔴 HIGH PRIORITY

### TODO-880: Remove localStorage Auth Token Fallback (XSS Risk)
- **File:** `src/shared/lib/getAxiosInstance.ts` (line ~22)
- **Impact:** XSS vulnerability — `localStorage.getItem(TOKEN_STORAGE_KEY)` accessible to any injected script. Combined with no CSP headers (TODO-884), this is exploitable.
- **Effort:** S
- **Fix:** Remove localStorage fallback; use httpOnly cookie exclusively; redirect to login if cookie absent
- **Also:** Remove `VITE_DEV_AUTH_EMAIL` / `VITE_DEV_AUTH_PASSWORD` from `.env.schema`; replace with MSW auth mock
- **Status:** PENDING ⚠️ VERIFIED

### TODO-881: Add Playwright E2E Tests
- **Impact:** No E2E tests — regressions reach production undetected. 0% E2E coverage across 271 source files.
- **Effort:** M
- **Depends on:** TODO-878 (correct env vars), TODO-879 (error propagation)
- **Target flows:** Create signal → add nodes → connect → validate → publish; Auth flow; Collections CRUD
- **Status:** PENDING

### TODO-882: Add lint + typecheck + test to CI Pipeline
- **File:** `bitbucket-pipelines.yml`
- **Impact:** No automated quality gates — broken types/lint can ship to production
- **Effort:** S
- **Depends on:** TODO-878
- **Status:** PENDING

### TODO-883: Undo/Redo for Builder Canvas
- **Impact:** Critical UX gap — users accidentally delete nodes with no recovery
- **Effort:** M
- **Implementation:** ReactFlow `useReactFlow` + Redux command pattern, 50-state history stack
- **Status:** PENDING

### TODO-884: Add nginx Security Headers
- **File:** `nginx.conf`
- **Impact:** Missing CSP, X-Frame-Options, HSTS, X-Content-Type-Options — fails basic security audits. Zero security headers present.
- **Effort:** XS
- **Fix:** Add to server block:
  ```nginx
  add_header X-Frame-Options "SAMEORIGIN" always;
  add_header X-Content-Type-Options "nosniff" always;
  add_header X-XSS-Protection "1; mode=block" always;
  add_header Referrer-Policy "strict-origin-when-cross-origin" always;
  add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://*.forwardlane.com;" always;
  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
  ```
- **Status:** PENDING ⚠️ VERIFIED — nginx.conf has zero security headers

---

## 🟡 MEDIUM PRIORITY

### TODO-885: Migrate Storybook from Webpack to Vite
- **Impact:** Dead webpack deps (`@storybook/builder-webpack5`, `@storybook/manager-webpack5`, `@storybook/preset-create-react-app`) bloating install; Storybook v6 is EOL
- **Effort:** S
- **Status:** PENDING

### TODO-886: Add Keyboard Shortcuts
- **Impact:** Power user productivity (Del, Ctrl+Z, +/-, Ctrl+S, ? cheatsheet)
- **Effort:** S
- **Depends on:** TODO-883
- **Status:** PENDING

### TODO-887: React Query DevTools + staleTime Tuning
- **Impact:** DX improvement + performance (catalog staleTime: 5min, signal list: 30s, default staleTime: 0 causing excessive refetches)
- **Effort:** S
- **Status:** PENDING

### TODO-888: Consolidate Duplicate FilterContent Components
- **Files:** `src/shared/ui/FilterContent/` and `src/modules/builder/containers/RightBar/Filter/FilterContent.tsx`
- **Impact:** Bug fixes require double-application; code divergence risk
- **Effort:** S
- **Status:** PENDING

### TODO-889: Signal Templates Library
- **Impact:** Revenue — reduces time-to-value for new customers, premium differentiator in sales demos
- **Effort:** L
- **Status:** PENDING

---

## 🟢 LOW / FUTURE

- Remove CRA dead code (`src/react-app-env.d.ts`, `src/reportWebVitals.ts`)
- Remove duplicate Navigation export in `src/shared/widgets/index.ts`
- Remove `@types/react-router` v5 (conflicts with react-router-dom v6)
- Fix `@proccesses` alias typo in `vite.config.ts`
- Upgrade TypeScript 4 → 5
- Upgrade jotai v1 → v2
- Upgrade @sentry/tracing → @sentry/react v8
- Upgrade React Query v4 → v5
- Plan ReactFlow v11 → v12 migration
- Replace `compose-function` with native
- Expand shared/ui unit tests to 70%+ coverage (currently: Button, Checkbox, Icon, Popover, Radio = 7 test files out of 271 source files)
- Add React.memo to FlowNode/FlowEdge components (prevent unnecessary re-renders)
- Analytics integration (Mixpanel/Amplitude)
- Feature flags (LaunchDarkly/Statsig)
- AI-Assisted Filter Building (future)
- Real-time Collaboration via Yjs CRDT (future)
- Signal Health Dashboard (future)
- Export to PDF/Excel (future)
- Mobile-responsive canvas (future)

---

## Score Breakdown

| Dimension | Score | Δ | Weight | Notes |
|-----------|-------|---|--------|-------|
| Code Quality | 5/10 | = | 15% | CRA artifacts remain, DRY violations (FilterContent), dead code, `@proccesses` typo, duplicate export |
| Test Coverage | 3/10 | = | 15% | ~2.6% test file ratio (7/271), 0 E2E, 0 integration tests. Critical builder module untested. |
| Security | 3.5/10 | ▼ | 20% | CRITICAL: pipeline env vars broken 15+ days; localStorage XSS; no nginx sec headers; .env.schema wrong prefix. Degraded from 4 due to elapsed time. |
| Error Handling | 4/10 | = | 10% | CRITICAL: axios interceptor silently eating errors. Sentry exists but can't capture swallowed errors. |
| Dependencies | 5/10 | = | 10% | 6+ outdated major versions (TS4, jotai v1, RQ v4, Storybook v6, Sentry v7, ReactFlow v11) |
| Documentation | 7/10 | = | 5% | Good README, BRAINSTORM, PLAN, AUDIT. FSD architecture well-documented. |
| Architecture | 7/10 | = | 10% | Solid FSD pattern, good module separation, lazy-loaded routes. Dual state mgmt (Redux+RQ+Jotai) slightly complex. |
| Business Value | 9/10 | = | 15% | Core ForwardLane product, active client deployments (demo+qa), revenue_potential=8, strategic_value=9 |
| **Composite** | **5.6/10** | **▼ -0.1** | | Two critical blockers unresolved 15+ days. Security time-decay applied. |

### Scoring Notes
- **Security time-decay:** Critical issues open 15+ days without remediation warrant downgrade (4.0 → 3.5). Each additional week without fix will further degrade by 0.5.
- **Business value remains high:** This is a core revenue product for ForwardLane. The gap between business importance (9/10) and code quality (5/10) represents significant risk.
- **Quick wins available:** TODO-878 + TODO-879 + TODO-890 are all XS effort (< 1 hour combined) and would immediately raise composite score to ~6.5.

---

## Risk Register

| Risk | Likelihood | Impact | Status | Days Open |
|------|-----------|--------|--------|-----------|
| Demo/QA broken — REACT_APP_* env vars | **HIGH** | **CRITICAL** | ⚠️ UNMITIGATED | 15+ |
| Silent API error swallowing | **HIGH** | **HIGH** | ⚠️ UNMITIGATED | 15+ |
| Auth token XSS via localStorage | **MEDIUM** | **HIGH** | ⚠️ UNMITIGATED | 15+ |
| .env.schema misleads developers | **HIGH** | **MEDIUM** | ⚠️ UNMITIGATED | 15+ |
| No E2E tests → production regressions | **HIGH** | **MEDIUM** | ⚠️ UNMITIGATED | — |
| No CI quality gates → broken code ships | **HIGH** | **MEDIUM** | ⚠️ UNMITIGATED | — |
| No nginx security headers | **MEDIUM** | **MEDIUM** | ⚠️ UNMITIGATED | — |
| Storybook webpack deps → install failures | LOW | MEDIUM | Tracked (TODO-885) | — |
| Outdated deps (jotai v1, TS4, RQ v4) | MEDIUM | LOW | Tracked | — |

---

## Execution Priority (Recommended Order)

1. **Day 1 (URGENT):** TODO-878 + TODO-890 + TODO-879 — XS effort, maximum impact (~1 hour total)
2. **Day 2:** TODO-880 (auth security) + TODO-882 (CI gates) + TODO-884 (nginx headers)
3. **Week 1:** TODO-881 (E2E tests) + TODO-887 (DevTools/perf)
4. **Week 2:** TODO-885 (Storybook) + TODO-888 (DRY) + TODO-886 (shortcuts)
5. **Week 3:** TODO-883 (undo/redo)
6. **Month 2:** TODO-889 (templates)

---

## History

| Date | Score | Δ | Key Changes |
|------|-------|---|-------------|
| 2026-03-15 16:20 | 5.6 | ▼ -0.1 | Security time-decay; no remediation; all criticals verified still open |
| 2026-03-15 07:20 | 5.7 | ▼ -0.1 | Added TODO-890 (.env.schema); security downgrade |
| 2026-03-14 | 5.8 | — | Baseline with CRITICAL-1 (TODO-878) and CRITICAL-2 (TODO-879) |
