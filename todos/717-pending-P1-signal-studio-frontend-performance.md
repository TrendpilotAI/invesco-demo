# TODO-717: Performance Optimizations (Virtualization + Lazy Loading)

**Repo**: signal-studio-frontend  
**Priority**: P1  
**Effort**: M (1-2 days)  
**Status**: pending

## Description
Signal list can grow to 100+ items. Visual builder (ReactFlow) is heavy. Both need optimization.

## Coding Prompt
```
Optimize signal-studio-frontend performance:

1. Virtualize Signal Library List:
   npm install @tanstack/react-virtual
   
   Find the signal list component (likely app/signal-library/ or components/signal-library/).
   Replace map() rendering with useVirtualizer from @tanstack/react-virtual.
   Maintain existing filter/sort functionality.
   Add skeleton loading states for virtualized items.

2. Lazy Load Visual Builder:
   In any page that imports the visual builder (flow-editor, reactflow-editor):
   Replace:
     import FlowEditor from '@/components/visual-editor/flow-editor'
   With:
     const FlowEditor = dynamic(() => import('@/components/visual-editor/flow-editor'), {
       ssr: false,
       loading: () => <div className="animate-pulse ...">Loading builder...</div>
     })

3. Add loading.tsx files for slow routes:
   Create app/signal-library/loading.tsx — skeleton grid of signal cards
   Create app/oracle-connect/loading.tsx — skeleton form
   Create app/visual-builder/loading.tsx — skeleton canvas

4. Add bundle size check:
   npm install --save-dev @next/bundle-analyzer
   Add to next.config.js:
   const withBundleAnalyzer = require('@next/bundle-analyzer')({
     enabled: process.env.ANALYZE === 'true'
   })
   module.exports = withBundleAnalyzer(nextConfig)
```

## Acceptance Criteria
- [ ] Signal list renders 500 items without lag (test with mock data)
- [ ] Visual builder page initial load is < 3s (not blocked by ReactFlow bundle)
- [ ] `ANALYZE=true npm run build` works and shows bundle breakdown
- [ ] All major route segments have loading.tsx
