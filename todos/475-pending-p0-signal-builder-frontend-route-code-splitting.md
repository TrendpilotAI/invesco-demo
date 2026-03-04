# TODO-475: Route-Level Code Splitting + ReactFlow Lazy Load

**Project:** signal-builder-frontend
**Priority:** P0 (HIGH impact, S effort)
**Estimated Effort:** 2-3 hours
**Dependencies:** None

## Description

All routes are bundled into a single chunk. ReactFlow alone is ~200KB. Use React.lazy + Suspense for route-level splitting. Separate ReactFlow into its own chunk since only the builder page needs it.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Add route-level code splitting with React.lazy.

STEPS:
1. Read src/app/router/ to understand current routing structure
2. Read src/pages/ to identify all page components

3. Convert all page imports to lazy:
   import { lazy, Suspense } from 'react';
   const BuilderPage = lazy(() => import('@pages/builder'));
   const CatalogPage = lazy(() => import('@pages/catalog'));
   const CollectionsPage = lazy(() => import('@pages/collections'));
   const PreviewPage = lazy(() => import('@pages/preview'));
   const SettingsPage = lazy(() => import('@pages/settings'));
   // etc.

4. Wrap routes in <Suspense fallback={<Loader />}>

5. Configure Vite manual chunks in vite.config.ts:
   build: {
     rollupOptions: {
       output: {
         manualChunks: {
           'react-flow': ['reactflow', '@reactflow/core', '@reactflow/background', '@reactflow/controls', '@reactflow/minimap'],
           'redux': ['@reduxjs/toolkit', 'react-redux'],
           'vendor': ['axios', 'react-router-dom'],
         }
       }
     }
   }

6. Add rollup-plugin-visualizer as devDependency for bundle analysis:
   pnpm add -D rollup-plugin-visualizer
   Add to vite.config.ts (behind ANALYZE env flag)

7. Run: pnpm build — verify output shows multiple chunks
8. Run: pnpm typecheck && pnpm test

CONSTRAINTS:
- Use existing Loader component from shared/ui if available, or create a simple spinner
- Ensure no flash of unstyled content on route transitions
- ReactFlow chunk must be separate from main bundle
```

## Acceptance Criteria
- [ ] Each page route is a separate chunk
- [ ] ReactFlow is in its own chunk (~200KB saved from initial load)
- [ ] `pnpm build` produces multiple JS chunks
- [ ] Bundle visualizer available via `ANALYZE=true pnpm build`
- [ ] No regression in navigation behavior
- [ ] `pnpm typecheck` passes
