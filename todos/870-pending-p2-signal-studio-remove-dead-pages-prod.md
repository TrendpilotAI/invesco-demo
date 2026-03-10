# 870 — Remove Dead Pages from Production Bundle

**Repo:** signal-studio  
**Priority:** P2 — Medium  
**Effort:** 1 day  
**Status:** pending

## Problem
These pages ship in the production bundle but serve no production purpose:
- `app/test-dashboard/page.tsx` — Development test harness for Phase 1-3 testing
- `app/oracle-ml/page.tsx` — Oracle ML connection tester (internal setup tool)
- `app/demo/` — Demo content (confirm with Nathan if still needed)

## Task
Gate these behind NODE_ENV check or move to admin section.

## Coding Prompt (for autonomous agent)
```typescript
// Option A: Gate with environment check (softer approach)
// Add to top of each dead page component:

export default function TestDashboardPage() {
  if (process.env.NODE_ENV === 'production') {
    notFound()  // import from 'next/navigation'
  }
  // ... rest of component
}

// Option B: Move to admin-only section (better)
// Move test-dashboard and oracle-ml under app/admin/
// app/admin/test-dashboard/page.tsx
// app/admin/oracle-ml/page.tsx
// Add admin route protection in middleware.ts (require admin role claim in JWT)

// Option C: Delete if truly not needed
// rm -rf app/test-dashboard app/oracle-ml
// Check git history to confirm no one depends on these URLs
```

## Acceptance Criteria
- [ ] `app/test-dashboard` not accessible at `/test-dashboard` in production
- [ ] `app/oracle-ml` not accessible at `/oracle-ml` in production
- [ ] Admin users can still access these pages in development
- [ ] Bundle size decreases (run next build --analyze before/after)

## Dependencies
- None (independent)

## Note
Confirm with Nathan whether demo pages should be deleted or kept for client demos.
