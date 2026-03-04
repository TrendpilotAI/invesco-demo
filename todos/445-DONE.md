# TODO-445: Wire TanStack Query Hooks to all pages — DONE ✅

**Completed:** 2026-03-04

## Summary

Wired TanStack Query hooks throughout the signal-studio-frontend, replacing all hardcoded mock data with live API calls.

## Changes Made

### 1. `app/layout.tsx`
- Imported and wrapped app with `Providers` component (from `src/components/providers.tsx`)
- `Providers` wraps `QueryClientProvider` with a properly configured `QueryClient`

### 2. `@tanstack/react-query` installed
- Added via `pnpm add @tanstack/react-query` (was missing from package.json)

### 3. `app/signal-studio/page.tsx`
- **Removed:** hardcoded `recentSignals` (4 items) and `templates` (4 items) mock arrays
- **Added:** `useSignals(orgId)` → live signals list with search filter
- **Added:** `useTemplates()` → live templates grid
- **Added:** `useDeleteSignal()` → delete button on each signal card with toast feedback
- **Added:** `useRunSignal()` → run button on each signal card with toast feedback
- **Added:** Loading skeletons (`SignalsSkeleton`, `TemplatesSkeleton`)
- **Added:** Error state component with `AlertCircle` icon
- **Added:** Empty state with CTA link to create first signal
- **Added:** `useOrganizations()` to get `orgId` for org-scoped hooks

### 4. `app/analytics/page.tsx`
- **Removed:** hardcoded numbers (128 signals, 1842 clients, 42 risk signals, 56 opportunity signals)
- **Added:** `useDashboardStats(orgId)` → live stats (total_signals, active_signals, recent_runs, data_health)
- **Added:** Loading skeletons for all 4 stat cards
- **Added:** Live activity feed in Overview tab from `DashboardStats.activity`
- **Added:** Error state banner on API failure

## Pages NOT Changed (No Mock Data)
- `app/chat/page.tsx` — uses `useChat` from `ai/react` (streaming), not mock data
- `app/agent/page.tsx` — delegates to component, no mock arrays
- `app/signal-library/page.tsx` — delegates to `SignalLibrary` component
- `app/session-dashboard/page.tsx` — polls actual session files, no mock data
- Other pages — no hardcoded data arrays to replace

## Notes
- Pre-existing TypeScript errors in `__tests__/` files (jest-dom type declarations not configured) are unrelated to this PR
- `typescript.ignoreBuildErrors: true` is set in `next.config.mjs` so build is not blocked
- Commit pushed to `main` on `TrendpilotAI/signal-studio-platform`
