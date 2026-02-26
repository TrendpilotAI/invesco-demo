---
status: pending
priority: p1
issue_id: "205"
tags: [performance, code-splitting, react, webpack, signal-builder-frontend]
dependencies: []
---

# 205 — Route-Level Code Splitting + Lazy ReactFlow

## Problem Statement

The initial JavaScript bundle includes all pages eagerly despite `React.lazy()` already being used in `router.tsx`. However, `reactflow` (~800KB minified) is bundled in the main chunk even for users who never visit the builder page (e.g., catalog/collections-only users). This significantly increases time-to-interactive for the most common entry points.

## Findings

Looking at `src/app/router/router.tsx`:
```typescript
// ALREADY has React.lazy for pages ✅
const BuilderPage = lazy(() => import('../../pages/builder'));
const CatalogPage = lazy(() => import('../../pages/catalog'));
// ... all pages use lazy()
```

However, the issue is likely that `reactflow` is imported at the module level in builder components, which causes it to be pulled into a shared chunk. The `Suspense` wrapper exists at the router level.

The bigger concern: `reactflow` is statically imported by `src/modules/builder/containers/Main/Flow.tsx`, which means even with lazy routing, webpack may still bundle it eagerly if it's in a shared module graph.

Key files to audit:
- `src/modules/builder/containers/Main/Flow.tsx`
- `src/modules/builder/containers/Builder.container.tsx`

## Proposed Solutions

### Option A: Verify lazy loading is working + fix bundle analysis (Recommended)
Run bundle analysis, confirm ReactFlow is only in the builder chunk, fix any static imports that break this.
- **Effort:** S (~2-3h)
- **Risk:** Low

### Option B: Dynamic import of ReactFlow component
Wrap the entire `<ReactFlow>` component in a dynamic import within the builder page.
- **Effort:** M
- **Risk:** Low

## Recommended Action

Option A first (audit + verify), then apply dynamic import fixes as needed.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

Task: Verify and improve route-level code splitting + lazy load ReactFlow

1. Install bundle analyzer:
   yarn add --dev webpack-bundle-analyzer source-map-explorer

2. Build with source maps and analyze:
   cd /data/workspace/projects/signal-builder-frontend
   yarn build 2>&1 | tail -30

3. Verify the router in src/app/router/router.tsx already uses React.lazy 
   for all page imports. If any page is NOT using lazy(), convert it:
   const BuilderPage = lazy(() => import('../../pages/builder'));
   // Ensure ALL pages use lazy()

4. Check src/modules/builder/containers/Main/Flow.tsx for direct reactflow imports.
   If ReactFlow is statically imported at the module level but the page is lazy-loaded,
   webpack SHOULD put reactflow in a separate chunk. Verify this works.

5. Add a loading fallback in the router's Suspense wrapper in src/app/router/router.tsx:
   import { Loader } from '@shared/ui';
   <Suspense fallback={<div style={{display:'flex',justifyContent:'center',
     alignItems:'center',height:'100vh'}}><Loader /></div>}>

6. Add webpack bundle size limits in package.json jest config or craco.config.js:
   // In craco.config.js, add webpack performance hints:
   module.exports = {
     webpack: {
       configure: (config) => {
         config.performance = {
           hints: 'warning',
           maxEntrypointSize: 512000,
           maxAssetSize: 512000,
         };
         return config;
       },
     },
   };

7. In the ReactFlow component file (likely src/modules/builder/containers/Main/Flow.tsx),
   ensure no top-level side effects that would force eager evaluation.

8. Verify build output shows separate chunks:
   yarn build 2>&1 | grep -E "chunk|reactflow|builder"

9. Document the chunk structure in a comment in craco.config.js.

10. Run typecheck to ensure no type regressions:
    yarn typecheck
```

## Dependencies

None — this is a standalone performance improvement.

## Estimated Effort

**Small** — 2-3 hours (mostly investigation + verification)

## Acceptance Criteria

- [ ] All route pages in `router.tsx` use `React.lazy()`
- [ ] `Suspense` has a meaningful fallback (not empty `<Suspense>`)
- [ ] `yarn build` output shows reactflow is NOT in the main chunk (it's in a separate async chunk)
- [ ] `yarn typecheck` passes with no new errors
- [ ] Bundle analysis shows initial JS payload ≤ 200KB (excluding reactflow)
- [ ] Webpack performance hints are configured in `craco.config.js`

## Work Log

### 2026-02-26 — Todo created

**By:** Planning Agent

**Actions:**
- Confirmed router.tsx already uses React.lazy for all pages
- Identified that the primary risk is reactflow ending up in shared chunk
- Noted Suspense wrapper exists but may lack meaningful fallback
