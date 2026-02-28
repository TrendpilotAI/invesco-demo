# TODO-225: Wire Dark Mode to Tailwind

**Repo:** signal-studio-frontend  
**Priority:** P2  
**Effort:** S (1-2 hours)  
**Status:** pending

## Problem
Zustand store has `darkMode` state and `toggleDarkMode` action but Tailwind's `dark:` classes require `class="dark"` on the `<html>` element. Nothing wires these together.

## Acceptance Criteria
- Toggling darkMode in the store applies `dark` class to `document.documentElement`
- All `dark:` Tailwind variants activate correctly
- State persists across page refreshes (already handled by Zustand persist middleware)
- No flash of wrong theme on load

## Coding Prompt

```
In /src/components/providers.tsx, add a useEffect that syncs darkMode to the DOM:

import { useAppStore } from '@/lib/stores/app-store'
import { useEffect } from 'react'

function DarkModeSync() {
  const darkMode = useAppStore(s => s.darkMode)
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])
  return null
}

Add <DarkModeSync /> inside Providers component.

Also ensure tailwind.config.ts has: darkMode: 'class' (not 'media').

Then audit all components that should have dark variants:
- sidebar.tsx, topbar.tsx, app-shell.tsx, card, button, input
- Add dark: classes where missing (dark:bg-gray-900, dark:text-white, etc.)
```

## Dependencies
None
