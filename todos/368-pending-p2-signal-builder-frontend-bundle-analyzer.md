# TODO-344: Add Bundle Analyzer + Optimize Chunk Sizes

**Repo:** signal-builder-frontend  
**Priority:** P2 | **Effort:** S (1 day)  
**Status:** pending

## Problem
No visibility into bundle composition. ReactFlow, lodash, and other heavy deps may be inflating the initial load. No baseline measurement exists.

## Task
1. Add `rollup-plugin-visualizer` to vite.config.ts
2. Run `npm run build` to generate treemap
3. Identify largest chunks and optimize:
   - Replace `lodash` with `lodash-es` or native equivalents
   - Ensure ReactFlow is in separate async chunk
   - Audit for any accidentally bundled test/mock code

## Coding Prompt
```
cd /data/workspace/projects/signal-builder-frontend
1. npm install --save-dev rollup-plugin-visualizer
2. In vite.config.ts, import { visualizer } and add to plugins array
3. npm run build — open stats.html in browser to see treemap
4. Find lodash imports: grep -r "from 'lodash'" src/ — replace with lodash-es or native
5. Add manualChunks in rollupOptions to split reactflow, redux, react-query into vendor chunks
6. Measure before/after: build size, initial load time
```

## Acceptance Criteria
- [ ] Bundle visualizer report generated
- [ ] Initial bundle < 300KB gzipped (excluding lazy chunks)
- [ ] lodash replaced with tree-shakeable alternative
- [ ] ReactFlow in separate chunk
