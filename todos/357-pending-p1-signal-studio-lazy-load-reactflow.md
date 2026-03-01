# TODO-357: Lazy Load ReactFlow Visual Builder Components

**Priority:** P1
**Effort:** S
**Repo:** signal-studio
**Status:** pending

## Description
ReactFlow and visual builder components load eagerly on page load, adding to initial bundle. Users who never use the visual builder pay the cost.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Find visual builder components:
   ls components/visual-editor/

2. In the page that renders the visual builder (likely app/(app)/signals/canvas/page.tsx or similar):
   Replace static imports with dynamic:
   
   // Before:
   import { ReactFlowEditor } from '@/components/visual-editor/reactflow-editor'
   
   // After:
   import dynamic from 'next/dynamic'
   const ReactFlowEditor = dynamic(
     () => import('@/components/visual-editor/reactflow-editor').then(m => m.ReactFlowEditor),
     { 
       ssr: false,
       loading: () => <div className="flex items-center justify-center h-full">Loading visual builder...</div>
     }
   )

3. Do the same for any other heavy visual editor components:
   - flow-editor.tsx
   - rete-editor.tsx  
   - custom-nodes.tsx (if imported directly)

4. Also lazy load the gamma-mcp-server or any heavy chart library imports

5. Run: pnpm build and check bundle analysis output

6. Commit: "perf(bundle): lazy load ReactFlow visual builder with next/dynamic (ssr: false)"
```

## Dependencies
- TODO-352 (migrate to @xyflow/react first)

## Acceptance Criteria
- Visual builder components use `next/dynamic` with `ssr: false`
- Loading state shows while component loads
- Initial page bundle size reduced
- Visual builder still functions correctly
