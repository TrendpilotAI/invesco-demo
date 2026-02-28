# 233 · P1 · signal-builder-frontend · Route-Level Code Splitting + Lazy ReactFlow

## Status
pending

## Priority
P1 — ReactFlow is ~800KB; eager loading all pages in initial bundle causes slow first load

## Description
The router likely imports all pages synchronously, and ReactFlow (large library) is bundled into the initial chunk. This task adds React.lazy code splitting for all routes and lazy-loads ReactFlow, plus adds memoization to the most expensive components.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: Identify the router file
cat src/app/router/router.tsx  (or similar path)

Step 2: Add React.lazy + Suspense for all page imports
```typescript
// Before
import BuilderPage from 'src/pages/builder';
import CatalogPage from 'src/pages/catalog';
import CollectionsPage from 'src/pages/collections';

// After
import React, { lazy, Suspense } from 'react';
const BuilderPage = lazy(() => import('pages/builder'));
const CatalogPage = lazy(() => import('pages/catalog'));
const CollectionsPage = lazy(() => import('pages/collections'));
const OnboardingPage = lazy(() => import('pages/onboarding'));

// Wrap router outlet with Suspense:
<Suspense fallback={<div className="page-loader"><Loader /></div>}>
  <Routes>
    <Route path="/builder/:id" element={<BuilderPage />} />
    <Route path="/catalog" element={<CatalogPage />} />
    {/* etc */}
  </Routes>
</Suspense>
```

Step 3: Memoize FlowNode component
In `src/modules/builder/containers/FlowNode/FlowNode.tsx`:
```typescript
// Wrap export with React.memo:
export const FlowNode = React.memo<{ data: TNodeData }>(({ data }) => {
  // existing component body
});
FlowNode.displayName = 'FlowNode';
```

Step 4: Memoize BuilderRightBar
In `src/modules/builder/containers/RightBar/BuilderRightBar.tsx`:
```typescript
export const BuilderRightBar = React.memo<{ selectedNode: TNodeData }>(({ selectedNode }) => {
  // existing component body
});
BuilderRightBar.displayName = 'BuilderRightBar';
```

Step 5: Fix inline render functions in BuilderRightBar
Convert from:
```typescript
const renderTargetContent = () => <TargetContent data={selectedNode} />;
```
To using useCallback or a static component-type map:
```typescript
const CONTENT_MAP: Record<ESignalNodeTypes, React.ComponentType<{ data: TNodeData }>> = {
  [ESignalNodeTypes.TARGET]: TargetContent,
  [ESignalNodeTypes.DATASET]: DatasetContent,
  // etc
};
const ContentComponent = CONTENT_MAP[selectedNode.nodeType];
return <ContentComponent data={selectedNode} />;
```

Step 6: Add bundle analyzer script to package.json:
```json
"analyze": "craco build && npx source-map-explorer 'build/static/js/*.js'"
```
Run it and document current bundle sizes in a comment.

Step 7: Add RTK Query cache tags to prevent unnecessary refetches in `src/redux/builder/api.ts`:
```typescript
getSchema: build.query<TSchemaDTO, void>({
  providesTags: ['Schema'],
}),
getSignal: build.query<TSignal, string>({
  providesTags: (result, error, id) => [{ type: 'Signal' as const, id }],
}),
updateSignal: build.mutation({
  invalidatesTags: (result, error, { id }) => [{ type: 'Signal' as const, id }],
}),
```

Commit: "perf: add route code splitting, memoize FlowNode/RightBar, add RTK cache tags"
```

## Dependencies
- 229 (type fixes) helps with correctly typing memoized components

## Effort Estimate
S–M (1 day)

## Acceptance Criteria
- [ ] All page imports in router use `React.lazy()`
- [ ] `<Suspense>` wrapper exists in router with a loading fallback
- [ ] `FlowNode` exports `React.memo` wrapped component
- [ ] `BuilderRightBar` exports `React.memo` wrapped component
- [ ] Inline render functions replaced with stable references or component map
- [ ] RTK Query `providesTags` / `invalidatesTags` defined for Signal and Schema
- [ ] `yarn build` succeeds and bundle main chunk is measurably smaller
