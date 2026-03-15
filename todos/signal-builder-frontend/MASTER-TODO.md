# Signal Builder Frontend — Master TODO

*Judge Agent Scoring Run: 2026-03-15 07:20 UTC*
*Composite Score: 5.7/10*
*Previous Score: 5.8/10 (2026-03-14)*
*Trend: ▼ -0.1 (no remediation since last run; .env.schema REACT_APP_* also flagged)*

---

## 🔴 CRITICAL (Fix Immediately)

### TODO-878: Fix Pipeline REACT_APP_* → VITE_* Env Vars
- **File:** `bitbucket-pipelines.yml` (demo + qa steps), `.env.schema`
- **Impact:** Demo and QA deployments have NO API connectivity — all env vars silently ignored by Vite
- **Effort:** XS (30 min)
- **Fix:** Rename all `REACT_APP_*` → `VITE_*` in all pipeline steps (demo, qa) AND in `.env.schema`
- **Status:** PENDING ⚠️ VERIFIED — pipeline still uses `REACT_APP_*` as of 2026-03-15
- **Days Open:** 14+ (since Vite migration commit `b3c0724`)

### TODO-879: Fix Axios Interceptor — Use Promise.reject()
- **File:** `src/shared/lib/getAxiosInstance.ts` (response interceptor, line ~58-65)
- **Impact:** React Query never sees errors; users get zero error feedback on failed API calls. TypeScript generics bypassed.
- **Effort:** XS (15 min)
- **Fix:** Replace `return { error: {...} }` with `return Promise.reject(error)` in response interceptor
- **Status:** PENDING ⚠️ VERIFIED — interceptor still returns object as of 2026-03-15

---

## 🔴 HIGH PRIORITY

### TODO-880: Remove localStorage Auth Token Fallback (XSS Risk)
- **File:** `src/shared/lib/getAxiosInstance.ts` (line ~22)
- **Impact:** XSS vulnerability — `localStorage.getItem(TOKEN_STORAGE_KEY)` accessible to any injected script
- **Effort:** S
- **Fix:** Remove localStorage fallback; use httpOnly cookie exclusively; redirect to login if cookie absent
- **Also:** Remove `VITE_DEV_AUTH_EMAIL` / `VITE_DEV_AUTH_PASSWORD` from `.env.schema`; replace with MSW auth mock
- **Status:** PENDING ⚠️ VERIFIED

### TODO-881: Add Playwright E2E Tests
- **Impact:** No E2E tests — regressions reach production undetected. 0% E2E coverage.
- **Effort:** M
- **Depends on:** TODO-878 (correct env vars), TODO-879 (error propagation)
- **Target flows:** Create signal → add nodes → connect → validate → publish; Auth flow; Collections CRUD
- **Status:** PENDING

### TODO-882: Add lint + typecheck + test to CI Pipeline
- **File:** `bitbucket-pipelines.yml`
- **Impact:** No automated quality gates — broken types/lint can ship
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
- **Impact:** Missing CSP, X-Frame-Options, HSTS, X-Content-Type-Options — fails basic security audits
- **Effort:** XS
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
- **Impact:** DX improvement + performance (catalog staleTime: 5min, signal list: 30s)
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

### TODO-890: Fix .env.schema to use VITE_* prefix
- **File:** `.env.schema`
- **Impact:** Schema still documents `REACT_APP_*` vars that Vite ignores — developer confusion
- **Effort:** XS
- **Related:** TODO-878
- **Status:** PENDING (NEW — flagged 2026-03-15)

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
- Expand shared/ui unit tests to 70%+ coverage (currently: Button, Checkbox, Icon, Popover, Radio only)
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

| Dimension | Score | Δ | Notes |
|-----------|-------|---|-------|
| Code Quality | 5/10 | = | CRA artifacts remain, DRY violations (FilterContent), dead code, `@proccesses` typo |
| Test Coverage | 3/10 | = | ~15% coverage, 7 test files, 0 E2E, 0 integration tests. 271 TS/TSX files. |
| Security | 4/10 | ▼ | CRITICAL: pipeline env vars broken 14+ days; localStorage XSS; no nginx sec headers; .env.schema wrong prefix |
| Documentation | 7/10 | = | Good README, BRAINSTORM, PLAN, AUDIT. FSD architecture well-documented. |
| Architecture | 7/10 | = | Solid FSD pattern, good module separation, lazy-loaded routes. Dual state mgmt (Redux+RQ+Jotai) slightly complex. |
| Business Value | 9/10 | = | Core ForwardLane product, active client deployments (demo+qa), revenue_potential=8, strategic_value=9 |
| **Composite** | **5.7/10** | **▼** | Two critical blockers unresolved 14+ days. Security score downgraded due to .env.schema finding. |

---

## Risk Register

| Risk | Likelihood | Impact | Status |
|------|-----------|--------|--------|
| Demo/QA broken — REACT_APP_* env vars | **HIGH** | **CRITICAL** | ⚠️ UNMITIGATED 14+ days |
| Silent API error swallowing | **HIGH** | **HIGH** | ⚠️ UNMITIGATED |
| Auth token XSS via localStorage | **MEDIUM** | **HIGH** | ⚠️ UNMITIGATED |
| No E2E tests → production regressions | **HIGH** | **MEDIUM** | ⚠️ UNMITIGATED |
| Storybook webpack deps → install failures | LOW | MEDIUM | Tracked (TODO-885) |
| Outdated deps (jotai v1, TS4, RQ v4) | MEDIUM | LOW | Tracked |

---

## Execution Priority (Recommended Order)

1. **Day 1 (URGENT):** TODO-878 + TODO-890 (pipeline + .env.schema env vars) + TODO-879 (axios)
2. **Day 2:** TODO-880 (auth security) + TODO-882 (CI gates) + TODO-884 (nginx headers)
3. **Week 1:** TODO-881 (E2E tests) + TODO-887 (DevTools/perf)
4. **Week 2:** TODO-885 (Storybook) + TODO-888 (DRY) + TODO-886 (shortcuts)
5. **Week 3:** TODO-883 (undo/redo)
6. **Month 2:** TODO-889 (templates)
