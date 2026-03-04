# TODO-489: Bundle Analysis + Optimization Target <300KB Gzipped

**Project:** signal-builder-frontend
**Priority:** P2 (MEDIUM impact, S effort)
**Estimated Effort:** 2-3 hours
**Dependencies:** TODO-475 (code splitting), TODO-481 (lodash-es)

## Description

Add rollup-plugin-visualizer to vite.config.ts. Generate treemap on build. Target: initial bundle <300KB gzipped.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Add bundle analysis and optimize to <300KB initial load.

STEPS:
1. pnpm add -D rollup-plugin-visualizer
2. Add to vite.config.ts (behind ANALYZE flag):
   import { visualizer } from 'rollup-plugin-visualizer';
   plugins: [
     react(),
     process.env.ANALYZE && visualizer({ open: true, gzipSize: true, template: 'treemap' })
   ].filter(Boolean)

3. Run: ANALYZE=true pnpm build — examine treemap
4. Identify top offenders and optimize:
   - Large vendor chunks → manual chunks in rollup config
   - Unused exports → verify tree-shaking working
   - Duplicate dependencies → pnpm dedupe
5. Document current vs target sizes in docs/BUNDLE_ANALYSIS.md
6. Add size-limit check (optional): pnpm add -D size-limit @size-limit/preset-app

CONSTRAINTS:
- Don't remove features to hit size target
- Focus on dead code elimination and chunking
- Document any packages that are unexpectedly large
```

## Acceptance Criteria
- [ ] `ANALYZE=true pnpm build` generates treemap
- [ ] Initial bundle <300KB gzipped (or documented path to get there)
- [ ] docs/BUNDLE_ANALYSIS.md documents current sizes and top offenders
- [ ] No functionality regressions
