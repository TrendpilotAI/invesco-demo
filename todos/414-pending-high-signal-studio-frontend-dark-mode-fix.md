# TODO-414: Fix Dark Mode — Signal Studio Frontend

**Priority:** High  
**Repo:** signal-studio-frontend  
**Status:** pending  
**Effort:** S (half day)

## Description

Dark mode toggle exists in Zustand store and Topbar, but no component uses `dark:` Tailwind variants — dark mode is functionally invisible. The `<html>` class gets set correctly but has no effect.

## Fix

1. In `tailwind.config.ts`, ensure `darkMode: 'class'` is set
2. Add `dark:` variants to all layout and UI components:
   - `src/components/layout/app-shell.tsx` — `dark:bg-gray-950`
   - `src/components/layout/sidebar.tsx` — `dark:bg-gray-900 dark:border-gray-800`
   - `src/components/layout/topbar.tsx` — `dark:bg-gray-900 dark:border-gray-800`
   - `src/components/ui/*.tsx` — all Radix-based components
3. Ensure Providers.tsx properly sets the class on `<html>`:
   ```tsx
   useEffect(() => {
     document.documentElement.classList.toggle('dark', darkMode);
   }, [darkMode]);
   ```

## Acceptance Criteria

- [ ] Toggling dark mode visually changes the app to dark colors
- [ ] Dark mode preference persists across page refreshes
- [ ] All 8 pages look correct in dark mode
- [ ] No white flash on initial load (use SSR cookie or localStorage check)
