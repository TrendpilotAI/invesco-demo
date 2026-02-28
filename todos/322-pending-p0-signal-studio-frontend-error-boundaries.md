# TODO-322: Error Boundaries + Loading States — Signal Studio Frontend

**Priority:** P0  
**Repo:** signal-studio-frontend  
**Effort:** S (2h)  
**Status:** pending  

## Description
No error boundaries exist. API failures crash pages silently or show blank screens. Add Next.js error.tsx, loading.tsx, and a reusable React error boundary.

## Coding Prompt (Autonomous Agent)
```
In /data/workspace/projects/signal-studio-frontend:

1. Create src/app/(app)/error.tsx:
"use client";
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
      <h2 className="text-xl font-semibold">Something went wrong</h2>
      <p className="text-muted-foreground text-sm">{error.message}</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  );
}

2. Create src/app/(app)/loading.tsx:
- Skeleton layout matching dashboard grid (4 stat cards + 2 content cards)
- Use animate-pulse bg-muted rounded-lg blocks

3. Create src/components/ui/skeleton.tsx (if not exists):
- Simple div with animate-pulse className

4. Add loading.tsx for key routes:
- src/app/(app)/signals/loading.tsx — table skeleton
- src/app/(app)/dashboard/loading.tsx — dashboard skeleton
```

## Dependencies
- None

## Acceptance Criteria
- [ ] API error shows friendly error page with retry button
- [ ] Route navigation shows skeleton while loading
- [ ] No white flash/blank screen on page transitions
