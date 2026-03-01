# TODO-338: Toast Notification System

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (1-2 hours)  
**Dependencies:** none

## Description
No user feedback on mutations (create signal, run signal, save settings). Add a toast notification system.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. Install: npm install sonner

2. Add <Toaster /> to src/app/layout.tsx

3. Create src/lib/toast.ts with typed helpers:
   - toast.success(message)
   - toast.error(message)
   - toast.loading(message) → returns id
   - toast.dismiss(id)

4. Add onSuccess/onError callbacks to existing mutations in hooks:
   - useCreateSignal → toast.success("Signal created")
   - useDeleteSignal → toast.success("Signal deleted")
   - useRunSignal → toast.loading("Running...") → success/error on completion

5. Style toaster to match app theme (dark/light aware)
```

## Acceptance Criteria
- [ ] Success toast on signal creation
- [ ] Error toast on API failures
- [ ] Loading toast on long operations
- [ ] Toasts auto-dismiss after 4 seconds
