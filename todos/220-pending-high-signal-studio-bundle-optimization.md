# TODO 220 — [HIGH] Bundle Optimization: Lazy Load Heavy Deps

**Repo:** signal-studio  
**Priority:** HIGH  
**Effort:** 2 hours  
**Dependencies:** None

---

## Description

Signal Studio ships `@xenova/transformers` (WASM, ~50MB) and has both `reactflow` AND `@xyflow/react` installed (duplicate). This severely bloats the initial bundle. Fix:
1. Remove duplicate reactflow package
2. Lazy load `@xenova/transformers` (server-side only, not needed client-side)
3. Dynamic import ReactFlow component in visual builder

## Acceptance Criteria
- [ ] Only one of `reactflow` / `@xyflow/react` is in package.json
- [ ] Visual builder loads with `dynamic(() => import(...), { ssr: false })`
- [ ] `@xenova/transformers` is imported only in server-side API routes, never in client bundle
- [ ] Next.js bundle analyzer shows reduction of >500KB

## Coding Prompt

```
1. In package.json, remove `reactflow` (keep `@xyflow/react` as it's newer):
   pnpm remove reactflow

2. Update visual builder page to use dynamic import:
   // app/visual-builder/builder/page.tsx
   const FlowEditor = dynamic(
     () => import('@/components/visual-editor/reactflow-editor'),
     { ssr: false, loading: () => <div>Loading builder...</div> }
   )

3. Check all files importing @xenova/transformers:
   grep -r "xenova" /data/workspace/projects/signal-studio/lib --include="*.ts"
   Ensure these are ONLY in /lib/ or /app/api/ (server-side), never in components/

4. Add to next.config.mjs:
   webpack: (config, { isServer }) => {
     if (!isServer) {
       config.resolve.fallback = { ...config.resolve.fallback, fs: false }
       config.externals = [...(config.externals || []), '@xenova/transformers']
     }
     return config
   }
```
