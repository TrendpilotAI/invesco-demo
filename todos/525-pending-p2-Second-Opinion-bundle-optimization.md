# TODO 525: Bundle Size Optimization
**Repo:** Second-Opinion  
**Priority:** P2 — Performance  
**Effort:** 4h  
**Status:** pending

## Description
43 components + framer-motion + recharts + firebase likely puts bundle >2MB. Code splitting and lazy loading will improve initial load time significantly.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/:

1. Install rollup-plugin-visualizer: `npm i -D rollup-plugin-visualizer`
2. Add to vite.config.ts to generate bundle analysis
3. Implement lazy loading in App.tsx:
   - React.lazy() for: ResearchPanel, AdminDashboard, ClinicalTrialMatcher, SpecialistDirectory
   - Wrap in Suspense with LoadingSpinner fallback
4. Review recharts: only import needed chart types, not full library
   - Replace `import { ... } from 'recharts'` with specific chart imports
5. Add route-level code splitting via vite manualChunks:
   - chunk: 'vendor-ui' → framer-motion, lucide-react
   - chunk: 'vendor-firebase' → firebase/*
   - chunk: 'vendor-charts' → recharts
6. Enable gzip/brotli compression in firebase.json hosting
```

## Acceptance Criteria
- [ ] Initial bundle under 500KB gzipped
- [ ] Lazy loaded routes load in <1s on 3G
- [ ] Lighthouse Performance score >80
- [ ] Bundle visualizer report saved to docs/bundle-analysis.html

## Dependencies
None
