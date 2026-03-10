# TODO-887: Add React Query DevTools + Performance Tuning

**Repo:** signal-builder-frontend  
**Priority:** P2 (Medium)  
**Effort:** S (2-3 hours)  
**Status:** pending

## Tasks

### 1. Add React Query DevTools in Dev Mode

```
In src/app/App.tsx, add ReactQueryDevtools:

import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

// Inside QueryClientProvider:
{import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
```

### 2. Tune staleTime for Static Data

```
In src/redux/api.ts or wherever QueryClient is initialized in App.tsx:

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30 * 1000,      // 30s default (vs 0)
      retry: 1,                   // vs 3 (faster failure UX)
      refetchOnWindowFocus: false, // prevent refetch on tab switch
    },
  },
});

Then for catalog/dataset queries (rarely change), set per-query:
  staleTime: 5 * 60 * 1000  // 5 minutes

For signal list (changes more often):
  staleTime: 30 * 1000       // 30 seconds
```

### 3. Add React.memo to FlowNode Components

```
Find all ReactFlow node components in src/modules/builder/containers/:
  FlowNode, FlowEdge, custom node types

Wrap each with React.memo():
  export const MyFlowNode = React.memo(({ data, selected }: NodeProps) => {
    // component body
  });

Add useCallback() for event handlers passed as props:
  const handleClick = useCallback(() => dispatch(selectNode(id)), [dispatch, id]);
  const handleDelete = useCallback(() => dispatch(deleteNode(id)), [dispatch, id]);
```

### 4. Add vite-bundle-visualizer

```
yarn add -D rollup-plugin-visualizer

In vite.config.ts:
import { visualizer } from 'rollup-plugin-visualizer';

plugins: [
  react(),
  ...(process.env.ANALYZE ? [visualizer({ open: true, gzipSize: true })] : []),
],

Add package.json script:
"analyze": "ANALYZE=true yarn build"

Run yarn analyze, document bundle sizes in AUDIT.md.
```

## Acceptance Criteria
- [ ] React Query DevTools visible in dev mode (bottom right panel)
- [ ] ReactQueryDevtools not included in production bundle
- [ ] Catalog queries use 5-minute staleTime (verify via DevTools)
- [ ] React.memo applied to at least 3 FlowNode components
- [ ] Bundle visualizer generates treemap on `yarn analyze`
- [ ] Bundle report documented in AUDIT.md
