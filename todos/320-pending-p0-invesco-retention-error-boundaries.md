# TODO-320 — Error Boundary Components (Invesco Retention)

**Priority:** P0  
**Project:** invesco-retention  
**Status:** pending  
**Estimated Effort:** S (2-3 hrs)  
**Created:** 2026-02-28  

---

## Task Description

The Invesco demo app (`/data/workspace/projects/invesco-retention/demo-app`) currently has no React error boundaries. A runtime crash during the live demo with Brian Kiley would be catastrophic for a $300K retention deal. This task adds error boundary components to all critical demo views so that any unexpected JS error shows a graceful fallback UI instead of a blank white screen or cryptic error.

**Views to protect:**
- Salesforce embed view (`/app/salesforce/page.tsx`)
- Signal creation flow (`/app/signals/page.tsx`)
- Territory dashboard (`/app/dashboard/page.tsx`)
- Mobile PWA view (`/app/mobile/page.tsx`)

---

## Coding Prompt (Agent-Executable)

```
cd /data/workspace/projects/invesco-retention/demo-app

TASK: Add React error boundary components to all 4 demo views.

1. Create /components/ErrorBoundary.tsx — a class component that:
   - Catches any render/lifecycle errors via componentDidCatch
   - Shows a friendly fallback: Invesco-branded card with message
     "Signal Studio encountered an issue. Please refresh or contact support."
   - Includes a "Reload" button that calls window.location.reload()
   - Logs error to console.error for debugging

2. Create /components/DemoErrorFallback.tsx — a styled fallback UI that:
   - Uses Invesco blue (#003087) and gold accent
   - Shows the ForwardLane logo (or text)
   - Provides a professional, non-alarming message
   - Has a "Reset Demo" button that navigates to /?reset=true

3. Wrap each page-level component in ErrorBoundary:
   - app/salesforce/page.tsx
   - app/signals/page.tsx (or equivalent signal creation route)
   - app/dashboard/page.tsx
   - app/mobile/page.tsx

4. Add a withErrorBoundary HOC helper for easy wrapping.

5. Test by temporarily throwing in one component, confirm fallback renders.

6. Remove test throw, commit, push, redeploy to GitHub Pages.

Tech stack: Next.js 14, TypeScript, Tailwind CSS
Repo: /data/workspace/projects/invesco-retention/demo-app
Deploy: git push origin main (GitHub Pages auto-deploys)
```

---

## Acceptance Criteria

- [ ] `ErrorBoundary` class component exists at `/components/ErrorBoundary.tsx`
- [ ] Fallback UI is Invesco-branded (correct colors, professional copy)
- [ ] All 4 demo views wrapped in error boundaries
- [ ] Throwing a test error in any view renders fallback, not white screen
- [ ] "Reload" / "Reset Demo" buttons functional
- [ ] No TypeScript errors (`npx tsc --noEmit` passes)
- [ ] Deployed and verified live at https://trendpilotai.github.io/invesco-demo/

---

## Why This Matters

Demo is live and $300K is on the line. A single unhandled JS error during the Brian Kiley demo = deal lost. Error boundaries are the last line of defense. Effort is small; risk reduction is enormous.
