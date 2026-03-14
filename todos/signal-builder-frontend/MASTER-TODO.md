# Signal Builder Frontend — Master TODO

*Judge Agent Scoring Run: 2026-03-14 16:20 UTC*
*Composite Score: 5.8/10*

---

## 🔴 CRITICAL (Fix Immediately)

### TODO-878: Fix Pipeline REACT_APP_* → VITE_* Env Vars
- **File:** `bitbucket-pipelines.yml`
- **Impact:** Demo and QA deployments have NO API connectivity — all env vars silently ignored by Vite
- **Effort:** XS (30 min)
- **Fix:** Rename all `REACT_APP_*` → `VITE_*` in demo and qa pipeline steps
- **Status:** PENDING

### TODO-879: Fix Axios Interceptor — Use Promise.reject()
- **File:** `src/shared/lib/getAxiosInstance.ts`
- **Impact:** React Query never sees errors; users get zero error feedback on failed API calls
- **Effort:** XS (15 min)
- **Fix:** Replace `return { error: {...} }` with `return Promise.reject(error)` in response interceptor
- **Status:** PENDING

---

## 🔴 HIGH PRIORITY

### TODO-880: Remove localStorage Auth Token Fallback (XSS Risk)
- **File:** `src/shared/lib/getAxiosInstance.ts`
- **Impact:** XSS vulnerability — localStorage accessible to any injected script
- **Effort:** S
- **Fix:** Remove `localStorage.getItem(TOKEN_STORAGE_KEY)` fallback; use httpOnly cookie exclusively
- **Status:** PENDING

### TODO-881: Add Playwright E2E Tests
- **Impact:** No E2E tests — regressions reach production undetected
- **Effort:** M
- **Depends on:** TODO-878 (correct env vars), TODO-879 (error propagation)
- **Status:** PENDING

### TODO-882: Add lint + typecheck + test to CI Pipeline
- **File:** `bitbucket-pipelines.yml`
- **Effort:** S
- **Depends on:** TODO-878
- **Status:** PENDING

### TODO-883: Undo/Redo for Builder Canvas
- **Impact:** Critical UX gap — users accidentally delete nodes with no recovery
- **Effort:** M
- **Status:** PENDING

### TODO-884: Add nginx Security Headers
- **File:** `nginx.conf`
- **Impact:** Missing CSP, X-Frame-Options, HSTS, X-Content-Type-Options
- **Effort:** XS
- **Status:** PENDING

---

## 🟡 MEDIUM PRIORITY

### TODO-885: Migrate Storybook from Webpack to Vite
- **Impact:** Dead webpack deps in devDependencies; Storybook v6 is EOL
- **Effort:** S
- **Status:** PENDING

### TODO-886: Add Keyboard Shortcuts
- **Impact:** Power user productivity (Del, Ctrl+Z, +/-, Ctrl+S)
- **Effort:** S
- **Depends on:** TODO-883
- **Status:** PENDING

### TODO-887: React Query DevTools + staleTime Tuning
- **Impact:** Performance improvement; developer experience
- **Effort:** S
- **Status:** PENDING

### TODO-888: Consolidate Duplicate FilterContent Components
- **Files:** `src/shared/ui/FilterContent/` and `src/modules/builder/containers/RightBar/Filter/FilterContent.tsx`
- **Impact:** Bug fixes require double-application; code divergence risk
- **Effort:** S
- **Status:** PENDING

### TODO-889: Signal Templates Library
- **Impact:** Revenue — reduces time-to-value for new customers, premium differentiator
- **Effort:** L
- **Status:** PENDING

---

## 🟢 LOW / FUTURE

- Remove CRA dead code (`react-app-env.d.ts`, `reportWebVitals.ts`)
- Remove `@types/react-router` v5 (conflicts with router v6)
- Fix `@proccesses` alias typo in vite.config.ts
- Upgrade TypeScript 4 → 5
- Upgrade jotai v1 → v2
- Upgrade @sentry/tracing → @sentry/react v8
- Upgrade React Query v4 → v5
- Plan ReactFlow v11 → v12 migration
- Replace `compose-function` with native
- Expand shared/ui unit tests to 70%+ coverage
- Add React.memo to FlowNode/FlowEdge components
- Analytics integration (Mixpanel/Amplitude)
- Feature flags (LaunchDarkly/Statsig)
- AI-Assisted Filter Building (future)
- Real-time Collaboration (future)
- Signal Health Dashboard (future)

---

## Score Breakdown

| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 5/10 | CRA artifacts, DRY violations, dead code |
| Test Coverage | 3/10 | ~15% coverage, 7 test files, no E2E |
| Security | 4/10 | localStorage XSS, missing nginx headers, broken env vars |
| Documentation | 7/10 | Good README, BRAINSTORM, PLAN, AUDIT exist |
| Architecture | 7/10 | Solid FSD pattern, good module separation |
| Business Value | 9/10 | Core ForwardLane product with active client deployments |
| **Composite** | **5.8/10** | Two critical blockers drag score significantly |
