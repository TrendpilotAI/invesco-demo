# TODO-339: Implement Dark Mode CSS Toggle

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (1-2 hours)  
**Dependencies:** none

## Description
`darkMode` state exists in Zustand store and a toggle exists in topbar, but toggling it has no effect. Wire it to CSS class on `<html>` element.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. In src/app/layout.tsx, read darkMode from useAppStore on the server
   (or use a client wrapper component)

2. Create src/components/theme-provider.tsx — client component that:
   - Subscribes to useAppStore darkMode
   - Applies/removes "dark" class on document.documentElement

3. Add ThemeProvider to app layout

4. Ensure tailwind.config.ts has darkMode: "class"

5. Add dark: variants to globals.css CSS variables if not present

6. Test toggle in topbar switches theme visually
```

## Acceptance Criteria
- [ ] Toggle in topbar switches between light/dark immediately
- [ ] Dark mode persists across page refreshes (Zustand persist)
- [ ] All existing components look correct in dark mode
