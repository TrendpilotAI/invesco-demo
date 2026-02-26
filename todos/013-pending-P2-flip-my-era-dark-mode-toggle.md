---
status: pending
priority: P2
issue_id: "013"
tags: [flip-my-era, dark-mode, tailwind, ux, frontend]
dependencies: []
---

# 013 — Implement Dark Mode Toggle

## Overview

FlipMyEra's Tailwind config already has `darkMode: ["class"]` configured and many components already have `dark:` variants (observed in `StoryGallery.tsx` and other components). However, there is no theme toggle anywhere in the UI — users cannot switch to dark mode. For a late-night story-reading app targeting Taylor Swift fans (who associate Midnights era with dark aesthetics), dark mode is a meaningful feature and a quick win.

**Why P2:** High-impact UX improvement with relatively low implementation effort given the Tailwind groundwork already exists.

## Coding Prompt

You are working on FlipMyEra, a React 18 + TypeScript + Vite + Tailwind SaaS app at `/data/workspace/projects/flip-my-era/`.

**Task:** Implement a working dark mode toggle that persists user preference.

### Step 1 — Create the theme hook

Create `src/core/hooks/useTheme.ts`:

```typescript
import { useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => {
    if (typeof window === 'undefined') return 'system';
    return (localStorage.getItem('flipmyera-theme') as Theme) || 'system';
  });

  useEffect(() => {
    const root = window.document.documentElement;
    const isDark = 
      theme === 'dark' || 
      (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    
    root.classList.toggle('dark', isDark);
    localStorage.setItem('flipmyera-theme', theme);
  }, [theme]);

  // Listen for system theme changes when in 'system' mode
  useEffect(() => {
    if (theme !== 'system') return;
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = () => {
      const root = window.document.documentElement;
      root.classList.toggle('dark', mediaQuery.matches);
    };
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [theme]);

  return { theme, setTheme };
}
```

### Step 2 — Create the ThemeToggle component

Create `src/modules/shared/components/ThemeToggle.tsx`:

```typescript
import { Moon, Sun, Monitor } from 'lucide-react';
import { Button } from './ui/button';
import { useTheme } from '@/core/hooks/useTheme';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const toggle = () => {
    setTheme(theme === 'light' ? 'dark' : theme === 'dark' ? 'system' : 'light');
  };

  return (
    <Button variant="ghost" size="icon" onClick={toggle} aria-label="Toggle theme">
      {theme === 'light' && <Sun className="h-4 w-4" />}
      {theme === 'dark' && <Moon className="h-4 w-4" />}
      {theme === 'system' && <Monitor className="h-4 w-4" />}
    </Button>
  );
}
```

### Step 3 — Add toggle to Layout/Header

Read `src/modules/shared/components/Layout.tsx` and locate the header/nav bar.

Add `<ThemeToggle />` to the header, near existing action buttons (typically next to the user avatar or sign-in button). Import from the shared components.

Export `ThemeToggle` from `src/modules/shared/components/index.ts`.

### Step 4 — Prevent flash of wrong theme (FODT)

In `index.html`, add an inline script in `<head>` BEFORE any other scripts to apply the saved theme class immediately:

```html
<script>
  (function() {
    var theme = localStorage.getItem('flipmyera-theme') || 'system';
    var isDark = theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    if (isDark) document.documentElement.classList.add('dark');
  })();
</script>
```

### Step 5 — Audit key pages for missing dark: variants

Check these pages and add missing `dark:` Tailwind classes where backgrounds/text are hardcoded:
- `src/app/pages/Gallery.tsx` — card backgrounds
- `src/modules/ebook/components/BookReader.tsx` — reading surface (most important — dark mode for reading)
- `src/modules/user/components/UserDashboard.tsx` — dashboard cards
- `src/app/pages/Index.tsx` (landing) — hero section

For each, ensure `bg-white` → `bg-white dark:bg-gray-900`, `text-gray-900` → `text-gray-900 dark:text-gray-100`, etc.

### Step 6 — Add to Settings page

In `src/modules/user/components/Settings.tsx` or `SettingsDashboard.tsx`, add a "Appearance" section with three radio buttons: Light / Dark / System. Wire to `useTheme()`.

## Dependencies

None.

## Effort

M (1-2 days)

## Acceptance Criteria

- [ ] `useTheme` hook created at `src/core/hooks/useTheme.ts`
- [ ] `ThemeToggle` component in header (visible on every page)
- [ ] Theme persists in `localStorage` across page refreshes
- [ ] System preference respected when set to 'system'
- [ ] No flash of wrong theme on page load
- [ ] BookReader (ebook reading surface) looks good in dark mode
- [ ] Settings page has appearance section
- [ ] `npm run typecheck` passes
- [ ] `npm run test:ci` passes
