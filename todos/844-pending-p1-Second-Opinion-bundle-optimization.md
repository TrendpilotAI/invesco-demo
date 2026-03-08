# TODO #844 — Second-Opinion: Bundle Size Optimization

**Priority:** P1  
**Effort:** S (4 hours)  
**Repo:** /data/workspace/projects/Second-Opinion/  
**Created:** 2026-03-08 by Judge Agent v2

## Task Description

Optimize bundle size via route-level code splitting. App.tsx likely imports all 45 components eagerly. Estimated 40-60% bundle reduction possible.

## Implementation

### Analyze Current Bundle
```bash
cd /data/workspace/projects/Second-Opinion
pnpm build 2>&1 | grep -E "dist/|kB|gzip"
# Or add rollup-plugin-visualizer to vite.config.ts
```

### Add React.lazy() for Heavy Components

```typescript
// In App.tsx, replace static imports:
// Before:
import { ClinicalTrialMatcher } from './components/ClinicalTrialMatcher';
import { SpecialistDirectory } from './components/SpecialistDirectory';
import { AnalysisDashboard } from './components/AnalysisDashboard';

// After:
const ClinicalTrialMatcher = React.lazy(() => import('./components/ClinicalTrialMatcher'));
const SpecialistDirectory = React.lazy(() => import('./components/SpecialistDirectory'));
const AnalysisDashboard = React.lazy(() => import('./components/AnalysisDashboard'));
```

### Wrap in Suspense
```tsx
<Suspense fallback={<LoadingSpinner />}>
  <ClinicalTrialMatcher />
</Suspense>
```

### Target Components for Lazy Loading
- ClinicalTrialMatcher — heavy, rarely used first visit
- SpecialistDirectory — directory data, lazy OK
- FamilySharingModal — modal, definitely lazy
- ResearchPanel — power users only
- InsurancePreAuth — conditional workflow
- ConsultationBooking — post-analysis step

### Vite Config Update
```typescript
// vite.config.ts — add chunk size warning
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ['react', 'react-dom'],
        firebase: ['firebase/app', 'firebase/auth', 'firebase/firestore'],
        charts: ['recharts'],
        animation: ['framer-motion'],
      }
    }
  },
  chunkSizeWarningLimit: 500,
}
```

### Acceptance Criteria
- [ ] `pnpm build` shows no chunk > 500KB
- [ ] Initial JS bundle reduced by ≥ 30%
- [ ] LCP (Largest Contentful Paint) improves by ≥ 20%
- [ ] All lazy components load correctly in production
- [ ] Loading spinner shown during lazy load

## Dependencies
- None — can do immediately
