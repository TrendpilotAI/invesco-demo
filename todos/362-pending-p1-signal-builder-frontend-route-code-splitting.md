# TODO-338: Route-Level Code Splitting + ReactFlow Lazy Load

**Repo:** signal-builder-frontend  
**Priority:** P1 | **Effort:** S (2h)  
**Status:** pending

## Problem
All routes bundle into a single JS chunk. ReactFlow (~200KB gzipped) loads even on non-builder pages.

## Task
1. Wrap all page-level route components in `React.lazy()`
2. Add `<Suspense>` boundaries with loading fallback
3. Ensure ReactFlow ends up in its own async chunk
4. Verify with `npm run build` chunk sizes

## Coding Prompt
```
In /data/workspace/projects/signal-builder-frontend/src/app/router/router.tsx:
1. Convert all page imports to React.lazy dynamic imports
2. Wrap route tree in <Suspense fallback={<LoadingSpinner />}>
3. In vite.config.ts, add rollupOptions.output.manualChunks to split reactflow into 'vendor-reactflow' chunk
4. Run: npm run build && ls -lh build/assets/ to verify chunk sizes
```

## Acceptance Criteria
- [ ] Initial JS bundle < 300KB gzipped
- [ ] ReactFlow in separate chunk
- [ ] No flash/error on route navigation
