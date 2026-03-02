# TODO-411: Wire Real APIs — Signal Studio Frontend

**Priority:** Critical  
**Repo:** signal-studio-frontend  
**Status:** pending  
**Effort:** S (1-2 days)

## Description

All app pages in the Signal Studio frontend use hardcoded mock data instead of the real TanStack Query hooks that already exist in `src/lib/api/hooks.ts`. This single change unlocks the entire product.

## Files to Change

| Page | Mock Data Location | Hook to Use |
|------|--------------------|-------------|
| `src/app/(app)/dashboard/page.tsx` | `const stats = [...]` lines 11-14, `recentActivity` lines 16-25 | `useDashboardStats(orgId)` |
| `src/app/(app)/signals/page.tsx` | `const signals = [...]` | `useSignals(orgId)` |
| `src/app/(app)/signals/[id]/page.tsx` | Hardcoded signal object | `useSignal(id)` |
| `src/app/(app)/templates/page.tsx` | `const templates = [...]` | `useTemplates()` |
| `src/app/(app)/chat/page.tsx` | Mock messages array | `useChatConversations()` |
| `src/app/(app)/settings/page.tsx` | Hardcoded user/org | `useOrganizations()`, `useOrgMembers(orgId)` |

## Also Fix

1. Wire `useRunSignal` to "Run Now" dropdown item `onClick`
2. Wire `useDeleteSignal` to "Delete" dropdown item `onClick` (with confirmation dialog)
3. Add `formatRelativeTime` export to `src/lib/utils.ts` (currently missing, causes runtime crash)
4. Add loading skeleton states (use `data-loading` Radix pattern or simple `<Skeleton>` component)
5. Add error states with retry CTA

## Autonomous Coding Prompt

```
You are working on /data/workspace/projects/signal-studio-frontend/.

TASK: Replace all hardcoded mock data in app pages with real TanStack Query hooks.

1. First, add `formatRelativeTime` to src/lib/utils.ts:
   export function formatRelativeTime(dateStr: string): string {
     const diff = Date.now() - new Date(dateStr).getTime();
     if (diff < 60_000) return "just now";
     if (diff < 3_600_000) return `${Math.floor(diff / 60_000)}m ago`;
     if (diff < 86_400_000) return `${Math.floor(diff / 3_600_000)}h ago`;
     return `${Math.floor(diff / 86_400_000)}d ago`;
   }

2. In src/app/(app)/dashboard/page.tsx:
   - Remove hardcoded stats and recentActivity arrays
   - Import useDashboardStats from @/lib/api/hooks
   - Get orgId from useAppStore
   - Replace static data with hook data
   - Show loading skeleton when isLoading
   - Show error message when isError

3. In src/app/(app)/signals/page.tsx:
   - Import useSignals, useRunSignal, useDeleteSignal
   - Replace mock signals array with hook
   - Wire onClick on "Run Now" to useRunSignal mutation
   - Wire onClick on "Delete" to useDeleteSignal mutation with window.confirm

4. In src/app/(app)/templates/page.tsx:
   - Import useTemplates
   - Replace mock templates array with hook

5. In src/app/(app)/chat/page.tsx:
   - Import useChatConversations, useSendMessage
   - Wire send button to useSendMessage mutation

Run: cd /data/workspace/projects/signal-studio-frontend && npm run build
Verify: no TypeScript errors, build succeeds.
```

## Acceptance Criteria

- [ ] All pages use real hooks (no hardcoded arrays in page components)
- [ ] `npm run build` passes with no errors
- [ ] `npm run lint` passes
- [ ] Loading states shown while data fetches
- [ ] Error states shown on API failure
- [ ] Run and Delete actions functional in signals page

## Dependencies

- Backend must be running at `NEXT_PUBLIC_API_URL`
- Supabase auth configured in `.env.local`
