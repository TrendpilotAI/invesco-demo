# TODO 354 — Signal Studio Frontend: Wire Real Data to Dashboard

**Status:** pending  
**Priority:** high  
**Project:** signal-studio-frontend  
**Estimated Effort:** 4–6 hours  

---

## Description

The dashboard at `dashboard/page.tsx` currently renders hardcoded mock statistics and activity feed. The app already has a `useDashboardStats()` React Query hook and typed API client. This task wires the dashboard to real data from the API, replacing all hardcoded values.

---

## Coding Prompt (Autonomous Agent)

```
Repo: /data/workspace/projects/signal-studio-frontend

Task: Replace all hardcoded mock data in the dashboard with real API data.

Steps:
1. Open `src/app/dashboard/page.tsx` (or equivalent path). Identify all hardcoded stats
   arrays, activity items, and metric values.

2. Import and use the `useDashboardStats()` hook (check `src/hooks/` or `src/lib/hooks/`)
   to fetch live stats. If the hook doesn't exist yet, create it in `src/hooks/useDashboardStats.ts`
   that calls GET /api/dashboard/stats via the existing `apiClient`.

3. Replace the hardcoded stat cards with data from the hook response. Map over the
   returned array rather than a static one.

4. Wire the activity feed to a `useActivityFeed()` hook (create if missing) hitting
   GET /api/dashboard/activity.

5. Wrap async sections in React Suspense boundaries with skeleton loaders.
   Use the existing Skeleton/Spinner components if present, otherwise create a simple
   `DashboardSkeleton` component.

6. Add an error boundary or inline error state for when the API call fails.

7. Ensure TypeScript compiles cleanly: `pnpm tsc --noEmit`.

8. Run `pnpm build` and verify no build errors.

Constraints:
- Do not remove existing component structure; replace data sources only.
- Keep the StatCard / icon pattern; just feed it real data.
- Use React Query's `isLoading`, `isError`, `data` from the hook.
```

---

## Dependencies

- None (foundational data-wiring task)

---

## Acceptance Criteria

- [ ] Dashboard renders live stats returned by the API (not hardcoded values)
- [ ] Skeleton loader shown while data is fetching
- [ ] Error state shown when API returns error or network fails
- [ ] `pnpm tsc --noEmit` passes
- [ ] `pnpm build` succeeds
- [ ] No hardcoded numbers/strings remain in the dashboard page component
