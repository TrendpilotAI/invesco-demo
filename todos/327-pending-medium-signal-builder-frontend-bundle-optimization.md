# TODO-327: Bundle Optimization — Signal Builder Frontend

**Priority:** P1 (Medium)
**Status:** Pending
**Project:** signal-builder-frontend
**Effort:** M (2 days)
**Depends On:** TODO-326 (Vite migration) must be done first
**Source:** PLAN.md → P1-002

---

## Task Description

Reduce the initial JavaScript bundle by 30%+ through: bundle analysis, replacing lodash with tree-shakeable lodash-es imports, adding route-level lazy loading for all pages, and deferring the onboarding bundle for returning users.

---

## Coding Prompt

```
You are working in the Signal Builder Frontend repo at /data/workspace/projects/signal-builder-frontend.

Optimize the JS bundle. Target: 30%+ reduction in initial bundle size.
Prerequisite: Vite migration (TODO-326) must be complete.

Steps:

1. Baseline measurement:
   ```
   yarn build
   # Note total bundle sizes from Vite build output
   ```

2. Install bundle visualizer:
   ```
   yarn add -D rollup-plugin-visualizer
   ```
   Add to `vite.config.ts`:
   ```ts
   import { visualizer } from 'rollup-plugin-visualizer';
   
   plugins: [
     react(),
     tsconfigPaths(),
     visualizer({ open: true, filename: 'bundle-report.html' }),
   ]
   ```
   Run `yarn build` and review `bundle-report.html` to identify the largest chunks.

3. Replace lodash with lodash-es:
   - Check if lodash is a dependency: `grep -r "from 'lodash'" src/ --include="*.ts" --include="*.tsx"`
   - Install: `yarn add lodash-es && yarn add -D @types/lodash-es`
   - Replace barrel imports: 
     ```ts
     // Before (pulls entire lodash)
     import { debounce, cloneDeep } from 'lodash';
     
     // After (tree-shakeable)
     import debounce from 'lodash-es/debounce';
     import cloneDeep from 'lodash-es/cloneDeep';
     ```
   - Or add Vite alias to auto-redirect lodash → lodash-es:
     ```ts
     resolve: {
       alias: { 'lodash': 'lodash-es' }
     }
     ```
   - Remove `lodash` package after migration: `yarn remove lodash`

4. Add route-level lazy loading:
   Find the router file (likely `src/App.tsx` or `src/router.tsx`).
   Convert all page imports to lazy:
   ```ts
   import { lazy, Suspense } from 'react';
   
   // Before
   import BuilderPage from './pages/BuilderPage';
   import CatalogPage from './pages/CatalogPage';
   
   // After
   const BuilderPage = lazy(() => import('./pages/BuilderPage'));
   const CatalogPage = lazy(() => import('./pages/CatalogPage'));
   
   // Wrap routes
   <Suspense fallback={<PageLoader />}>
     <Routes>
       <Route path="/builder" element={<BuilderPage />} />
       <Route path="/catalog" element={<CatalogPage />} />
     </Routes>
   </Suspense>
   ```
   Create a simple `<PageLoader />` component if one doesn't exist.

5. Defer onboarding bundle:
   - Find the onboarding flow (likely in `src/modules/onboarding/` or `src/pages/Onboarding*`)
   - Make it lazy-loaded AND only imported when the user is in onboarding state:
     ```ts
     const OnboardingFlow = lazy(() => import('./modules/onboarding'));
     ```
   - Ensure it's not included in the main chunk

6. Verify Vite manual chunk splitting in `vite.config.ts`:
   ```ts
   build: {
     rollupOptions: {
       output: {
         manualChunks: {
           'react-vendor': ['react', 'react-dom', 'react-router-dom'],
           'redux-vendor': ['@reduxjs/toolkit', 'react-redux'],
           'reactflow': ['reactflow'],
         }
       }
     }
   }
   ```

7. After-optimization measurement:
   ```
   yarn build
   # Compare new bundle sizes to baseline
   ```
   Document the before/after in a comment in `vite.config.ts` or in PLAN.md.
```

---

## Acceptance Criteria

- [ ] Bundle visualizer installed and `bundle-report.html` generated
- [ ] `lodash` replaced with `lodash-es` (or aliased) — no whole-lodash imports
- [ ] All route-level pages use `React.lazy()` + `Suspense`
- [ ] Onboarding bundle is deferred and not in initial chunk
- [ ] Vite `manualChunks` configured for major vendor libs
- [ ] Initial JS bundle reduced by ≥ 30% compared to pre-optimization baseline
- [ ] `yarn build` succeeds with no errors
- [ ] Application loads and all routes work correctly after optimization
