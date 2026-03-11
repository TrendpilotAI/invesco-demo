# Signal Builder Frontend — Prioritized TODOs

*Generated: 2026-03-11*

## 🔴 CRITICAL (Fix Immediately)

### 1. [CRITICAL] Fix Bitbucket Pipeline Env Vars (TODO-878)
- **File:** `bitbucket-pipelines.yml`
- **Issue:** Pipeline injects `REACT_APP_*` env vars but Vite only reads `VITE_*`. Deployed demo/qa environments have undefined API URLs — app cannot connect to backend.
- **Fix:** Rename all `REACT_APP_*` → `VITE_*` in all pipeline steps.
- **Effort:** XS (30 min)

### 2. [CRITICAL] Fix Axios Error Interceptor (TODO-879)
- **File:** `src/shared/lib/getAxiosInstance.ts`
- **Issue:** Response interceptor returns `{ error: { status, data } }` instead of `Promise.reject(error)`. React Query sees errors as successful responses — `isError` never triggers, `onError` never fires. Users get no error feedback.
- **Fix:** Replace `return { error: {...} }` with `return Promise.reject(error)`.
- **Effort:** XS (30 min)

---

## 🟠 HIGH PRIORITY

### 3. Remove localStorage Auth Token Fallback (TODO-880)
- **Files:** `src/shared/lib/getAxiosInstance.ts`, `src/shared/lib/auth.ts`
- **Issue:** Auth token stored in localStorage as fallback — vulnerable to XSS. Cookie-only auth should be the only path.
- **Fix:** Remove `localStorage.getItem(TOKEN_STORAGE_KEY)` fallback, rely solely on httpOnly cookie.
- **Effort:** S

### 4. Add E2E Tests with Playwright (TODO-881)
- **Issue:** Only 7 unit tests for 271 source files (~2.6% coverage). No E2E tests. Zero confidence in deployments.
- **Fix:** Set up Playwright, write critical path tests (login flow, builder CRUD, signal creation).
- **Effort:** M

### 5. Add CI Quality Gates (TODO-882)
- **Issue:** No test/lint/typecheck enforcement in CI pipeline. Broken code can be deployed.
- **Fix:** Add `yarn lint`, `yarn typecheck`, `yarn test` steps to Bitbucket pipeline before build.
- **Effort:** S

---

## 🟡 MEDIUM PRIORITY

### 6. Add Undo/Redo for Builder Canvas (TODO-883)
- **Issue:** Users accidentally delete nodes with no recovery — critical UX gap for enterprise.
- **Fix:** ReactFlow history + Redux command pattern, toolbar buttons + Ctrl+Z/Ctrl+Shift+Z.
- **Effort:** M

### 7. Add Nginx Security Headers (TODO-884)
- **File:** `nginx.conf`
- **Issue:** Missing CSP, X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security headers.
- **Fix:** Add security headers to nginx config.
- **Effort:** XS

### 8. Migrate Storybook to Vite Builder (TODO-885)
- **Issue:** Storybook v6 uses webpack but app uses Vite. Dead webpack deps in devDependencies. Confusing build setup.
- **Fix:** Upgrade to Storybook v7+ with `@storybook/builder-vite`. Remove webpack devDependencies.
- **Effort:** S

### 9. Consolidate Duplicate FilterContent (TODO-888)
- **Files:** `src/shared/ui/FilterContent/` and `src/modules/builder/containers/RightBar/Filter/FilterContent.tsx`
- **Issue:** Two diverged FilterContent implementations. Bug fixes must be applied in two places.
- **Fix:** Merge into shared component with variant props.
- **Effort:** S

### 10. Clean Up Dead CRA Artifacts
- **Files:** `src/react-app-env.d.ts`, `src/reportWebVitals.ts`, `.env.schema` (still uses `REACT_APP_*`)
- **Issue:** Leftover Create React App files cause confusion post-Vite migration.
- **Fix:** Delete dead files, update `.env.schema` to use `VITE_*` prefix.
- **Effort:** XS

---

## 🔵 LOWER PRIORITY

### 11. Upgrade TypeScript 4 → 5
### 12. Upgrade Jotai v1 → v2
### 13. Fix `@proccesses` typo in aliases (vite.config.ts, tsconfig.json, jest config)
### 14. Add JSDoc to shared utilities and hooks
### 15. Signal Templates Library (TODO-889) — revenue feature
### 16. Keyboard Shortcuts for Builder (TODO-886)
### 17. Wire up reportWebVitals to Sentry or delete
### 18. Remove duplicate Navigation export in `src/shared/widgets/index.ts`
### 19. Remove `@types/react-router` v5 (conflicts with react-router-dom v6 types)
### 20. Re-enable disabled ESLint rules (`no-console`, `import/no-unresolved`, etc.)
