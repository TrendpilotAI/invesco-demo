# TODO 356 — Signal Studio Frontend: Loading/Error States + Toast Notification System

**Status:** pending  
**Priority:** high  
**Project:** signal-studio-frontend  
**Estimated Effort:** 6–8 hours  

---

## Description

The app currently has no user feedback on async operations — no loading spinners, no error boundaries, and no toast notifications when mutations succeed or fail. This makes the app feel unfinished and leaves users confused after actions like creating a signal or triggering a run. This task implements a global toast system and adds loading/error states to all major data-fetching pages.

---

## Coding Prompt (Autonomous Agent)

```
Repo: /data/workspace/projects/signal-studio-frontend

Task: Add a toast notification system and loading/error states throughout the app.

Step 1 — Toast System
  Install: pnpm add sonner
  
  In `src/app/layout.tsx`, add `<Toaster />` from `sonner` inside the body.
  
  Create `src/lib/toast.ts` that re-exports `toast` from sonner with typed helpers:
    - toast.success(message)
    - toast.error(message)
    - toast.loading(message) → returns id for dismiss
  
  Wire toasts to all React Query mutations:
  - Signal create/update/delete → success/error toasts
  - Signal run trigger → success/error toasts
  - Any other mutations found in `src/hooks/`
  
  Pattern:
    onSuccess: () => toast.success('Signal created'),
    onError: (err) => toast.error(err.message ?? 'Something went wrong'),

Step 2 — Skeleton Loaders
  Create `src/components/ui/Skeleton.tsx` if it doesn't exist:
    A simple animated gray bar component using Tailwind's `animate-pulse`.
  
  Create skeleton variants:
    - `TableSkeleton` (5 rows × N cols)
    - `CardSkeleton` (stat card shape)
    - `ListSkeleton` (activity feed shape)
  
  Apply appropriate skeletons in:
    - Dashboard page (while useDashboardStats loads)
    - Signals list page
    - Templates page
    - Any other list/table pages

Step 3 — Error Boundaries
  Create `src/components/ErrorBoundary.tsx` as a React class component
  that catches render errors and displays a friendly "Something went wrong" card
  with a retry button (calls window.location.reload()).
  
  Wrap the main app content in layout.tsx with <ErrorBoundary>.
  Optionally wrap individual route segments that are high-risk.

Step 4 — Verify
  Run `pnpm tsc --noEmit` and fix type errors.
  Run `pnpm build` and verify success.
```

---

## Dependencies

- TODO 354 (dashboard real data) — skeleton loaders are most impactful there

---

## Acceptance Criteria

- [ ] `<Toaster />` mounted in root layout; `sonner` installed
- [ ] All mutations show success or error toasts
- [ ] Skeleton loaders shown on dashboard, signals list, and templates pages while fetching
- [ ] Global error boundary catches render errors with a retry option
- [ ] `pnpm tsc --noEmit` passes
- [ ] `pnpm build` succeeds
