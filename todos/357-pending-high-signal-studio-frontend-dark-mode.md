# TODO 357 — Signal Studio Frontend: Implement Dark Mode CSS Toggling

**Status:** pending  
**Priority:** high  
**Project:** signal-studio-frontend  
**Estimated Effort:** 3–5 hours  

---

## Description

The Zustand store already has a `darkMode` boolean and a `toggleDarkMode` action, but the CSS side is not implemented — toggling dark mode has no visual effect. This task wires the store state to the `<html>` element's `class` attribute and ensures all components use Tailwind's `dark:` variant correctly.

---

## Coding Prompt (Autonomous Agent)

```
Repo: /data/workspace/projects/signal-studio-frontend

Task: Make dark mode functional end-to-end.

Step 1 — Tailwind Config
  Open `tailwind.config.ts` (or `.js`). Ensure:
    darkMode: 'class'
  is set. If it's not present or set to 'media', change it to 'class'.

Step 2 — HTML Class Toggle
  In `src/app/layout.tsx` (or a client component wrapping the body), read `darkMode`
  from the Zustand store and apply/remove the `dark` class on `document.documentElement`.
  
  Create `src/components/DarkModeProvider.tsx`:
  ```tsx
  'use client';
  import { useEffect } from 'react';
  import { useAppStore } from '@/store'; // adjust import
  
  export function DarkModeProvider({ children }: { children: React.ReactNode }) {
    const darkMode = useAppStore((s) => s.darkMode);
    useEffect(() => {
      document.documentElement.classList.toggle('dark', darkMode);
    }, [darkMode]);
    return <>{children}</>;
  }
  ```
  Wrap the body children in layout.tsx with `<DarkModeProvider>`.

Step 3 — Persist Preference
  In the Zustand store, wrap the store with `persist` middleware from `zustand/middleware`
  (using localStorage key `'signal-studio-prefs'`) if not already persisted.
  This ensures dark mode preference survives page refreshes.

Step 4 — Dark Mode Toggle UI
  Locate the existing dark mode toggle button/switch in the navbar or settings.
  Confirm it calls `toggleDarkMode()`. If no toggle exists, add a sun/moon icon
  button to the top navigation bar that calls the action.

Step 5 — Audit dark: classes
  Do a quick grep for components that use hardcoded light-only Tailwind classes
  (e.g., `bg-white`, `text-gray-900`, `border-gray-200`) and add corresponding
  `dark:bg-gray-900 dark:text-gray-100 dark:border-gray-700` variants to the
  most visible ones: Navbar, Sidebar, main layout wrapper, Card, Button.

Step 6 — Verify
  Run `pnpm tsc --noEmit` and `pnpm build`. Confirm no errors.
  Visually verify toggle works in browser (if possible).
```

---

## Dependencies

- None (self-contained)

---

## Acceptance Criteria

- [ ] `tailwind.config` has `darkMode: 'class'`
- [ ] `DarkModeProvider` adds/removes `dark` class on `<html>` based on store state
- [ ] Dark mode preference persists across page refreshes (localStorage)
- [ ] A toggle button exists in the UI and calls `toggleDarkMode()`
- [ ] At minimum Navbar, Sidebar, Card, and main layout have `dark:` Tailwind variants
- [ ] `pnpm tsc --noEmit` passes
- [ ] `pnpm build` succeeds
