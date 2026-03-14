# TODO: Add React.lazy() Loading for All 43 Components

- **Project:** Second-Opinion
- **Priority:** HIGH
- **Status:** pending
- **Category:** Performance
- **Effort:** M (1 day)
- **Created:** 2026-03-14

## Description
43 components exist. Vite does code splitting at build time, but React-level lazy loading with `React.lazy()` + `<Suspense>` would improve initial load time significantly.

## Action Items
1. Verify current lazy loading state in `App.tsx`
2. Wrap all route-level components with `React.lazy()`
3. Add `<Suspense fallback={<LoadingSpinner />}>` wrappers
4. Keep critical-path components (Auth, LandingPage) eager-loaded
5. Test with Lighthouse for performance improvement
