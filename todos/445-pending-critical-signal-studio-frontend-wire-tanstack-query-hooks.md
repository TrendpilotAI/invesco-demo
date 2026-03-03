# TODO-445: Wire TanStack Query Hooks — Replace All Mock Data

**Repo:** signal-studio-frontend  
**Priority:** Critical  
**Effort:** S (1-2 days)  
**Status:** pending

## Description

Every page in the app renders hardcoded mock arrays. The TanStack Query hooks layer in `src/lib/api/hooks.ts` is complete and correct — `useSignals`, `useCreateSignal`, `useDashboardStats`, `useChatConversations`, `useSendMessage`, `useDeleteSignal`, `useRunSignal` — but zero pages import or call them.

This is the single most impactful task: replacing mocks with real API calls transforms the app from a prototype to a working product.

## Files to Update

1. **Dashboard page** — replace mock stats with `useDashboardStats()`
2. **Signals page** — replace mock signal array with `useSignals()`, wire Delete/Run onClick handlers to `useDeleteSignal` and `useRunSignal`
3. **Templates page** — replace mock templates with `useTemplates()`
4. **Chat page** — replace mock messages with `useChatConversations()` + `useSendMessage()`
5. **Signal detail page** — replace mock with `useSignal(id)`

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/:

1. Open src/lib/api/hooks.ts — read each hook's interface
2. For each page in app/(app)/:
   a. Remove the hardcoded mock const arrays at the top
   b. Import the appropriate hook(s) from src/lib/api/hooks
   c. Replace mock data with hook data: const { data: signals, isLoading, error } = useSignals()
   d. Add loading state: if (isLoading) return <SignalsSkeleton />
   e. Add error state: if (error) return <ErrorState message={error.message} />
3. For the Signals page Delete/Run dropdowns:
   const { mutate: deleteSignal } = useDeleteSignal()
   const { mutate: runSignal } = useRunSignal()
   Wire onClick: <DropdownMenuItem onClick={() => deleteSignal(signal.id)}>Delete</DropdownMenuItem>
4. Verify QueryClientProvider is at the root in app/layout.tsx (it should be)
```

## Dependencies
- TODO-444 (auth middleware — users must be authenticated for API calls to succeed)

## Acceptance Criteria
- [ ] Dashboard shows real stats from API (not hardcoded numbers)
- [ ] Signals page shows real signals or empty state
- [ ] Delete signal action removes it from the list
- [ ] Run signal action triggers execution
- [ ] Loading skeletons shown during data fetch
- [ ] Error states shown on API failure
