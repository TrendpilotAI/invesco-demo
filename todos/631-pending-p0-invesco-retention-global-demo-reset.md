# TODO #631 — Global Demo Reset Mechanism

**Priority:** P0 (Demo Reliability)
**Effort:** S (1-2h)
**Repo:** invesco-retention
**Status:** pending

## Description
Each route (/salesforce, /dashboard, /mobile) has its own reset button, but there's no global cross-page demo reset. During a live demo, if Nathan navigates around and leaves dirty state, there's no fast recovery.

## Coding Prompt
```
In /data/workspace/projects/invesco-retention/demo-app:

1. Add a global keyboard shortcut: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
   that calls a window.__DEMO_RESET__() function which:
   - Clears all localStorage keys with prefix "demo-" or "invesco-"
   - Reloads the current page

2. Add window.__DEMO_RESET__ to src/app/layout.tsx as a useEffect:
   ```
   useEffect(() => {
     window.__DEMO_RESET__ = () => {
       Object.keys(localStorage).filter(k => k.startsWith('demo') || k.startsWith('invesco')).forEach(k => localStorage.removeItem(k));
       window.location.reload();
     };
     const handler = (e: KeyboardEvent) => {
       if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'R') {
         e.preventDefault();
         window.__DEMO_RESET__();
       }
     };
     window.addEventListener('keydown', handler);
     return () => window.removeEventListener('keydown', handler);
   }, []);
   ```

3. Add a small floating "Reset Demo" button visible only in demo mode
   (check URL param ?demo=true or NODE_ENV !== 'production')
   Position: bottom-right, low opacity until hover
```

## Acceptance Criteria
- [ ] Ctrl+Shift+R resets all demo state from any page
- [ ] window.__DEMO_RESET__() callable from browser console
- [ ] Demo reset button visible in demo mode
- [ ] Does not affect non-demo state
