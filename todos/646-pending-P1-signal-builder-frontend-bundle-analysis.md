# TODO-646: Add Bundle Analysis to Signal Builder Frontend

**Repo:** signal-builder-frontend  
**Priority:** P1  
**Effort:** XS (1 hour)  
**Category:** Performance

## Description
No bundle analysis tooling. Team can't see what's making the bundle large. ReactFlow and lodash are suspected heavy hitters.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-frontend/:
1. yarn add -D rollup-plugin-visualizer
2. Update vite.config.ts to add:
   import { visualizer } from 'rollup-plugin-visualizer'
   plugins: [..., visualizer({ open: true, gzipSize: true })]
3. Add script: "analyze": "vite build --mode analyze"
4. Run yarn analyze and document findings
5. Check if lodash is being fully imported — fix to named imports
6. Check ReactFlow bundle size contribution
```

## Acceptance Criteria
- [ ] `yarn analyze` generates bundle visualization
- [ ] Lodash uses named imports only
- [ ] Bundle size documented in findings
- [ ] No single dependency > 200KB gzipped without justification

## Dependencies
None
