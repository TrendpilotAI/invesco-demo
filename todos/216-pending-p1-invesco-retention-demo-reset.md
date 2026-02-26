# 216 — Invesco Retention: Demo Reset Button (P1)

**Priority:** 🟠 P1 — Demo resilience, prevents live failure  
**Project:** invesco-retention  
**Effort:** XS (20-30 min)  
**Owner:** Honey  
**Dependencies:** None

---

## Task Description

Add a demo reset mechanism so the app can be run multiple times without stale state. In live demos, "Push to Salesforce" buttons get clicked, signals get filtered, forms get filled — all leaving state that makes the second run look broken.

Two mechanisms:
1. URL param: `?reset=true` — clears all state on load
2. Hidden keyboard shortcut: `Cmd+Shift+R` or `Ctrl+Shift+R` (not the browser refresh) — triggers reset without page reload

---

## Coding Prompt (Agent-Executable)

```
You are adding a demo reset mechanism to the invesco-retention demo app.

REPO: /data/workspace/projects/invesco-retention/demo-app

TASK:

1. Create a DemoReset utility at src/lib/demo-reset.ts:

   ```typescript
   export const DEMO_RESET_KEYS = [
     'push-to-sf-state',        // Push to Salesforce button states
     'signal-query',            // Last search query
     'signal-results',          // Cached results
     'selected-advisor',        // Selected advisor state
     'territory-filter',        // Territory filter state
     'demo-interactions',       // Any interaction tracking
   ];
   
   export function resetDemo() {
     // Clear localStorage
     DEMO_RESET_KEYS.forEach(key => localStorage.removeItem(key));
     // Clear sessionStorage
     sessionStorage.clear();
     // Reload to home
     window.location.href = '/salesforce?demo=fresh';
   }
   ```

2. In the root layout (src/app/layout.tsx), add URL param detection:

   ```typescript
   'use client';
   import { useEffect } from 'react';
   import { useSearchParams } from 'next/navigation';
   import { resetDemo } from '@/lib/demo-reset';
   
   export default function RootLayout({ children }) {
     const searchParams = useSearchParams();
     
     useEffect(() => {
       if (searchParams.get('reset') === 'true') {
         resetDemo();
       }
     }, [searchParams]);
     
     // ... rest of layout
   }
   ```

3. Add keyboard shortcut listener (in a DemoKeyboardHandler client component):

   ```typescript
   useEffect(() => {
     const handler = (e: KeyboardEvent) => {
       // Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows) — but NOT browser default
       if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 'D') {
         e.preventDefault();
         resetDemo();
       }
     };
     window.addEventListener('keydown', handler);
     return () => window.removeEventListener('keydown', handler);
   }, []);
   ```
   Use Cmd+Shift+D (D for Demo) to avoid browser shortcut conflicts.

4. Add a hidden "Demo Controls" panel accessible via:
   - URL: `?demo-controls=true`
   - Shows buttons: [Reset Demo] [Go to Salesforce View] [Go to Mobile View]
   - Invisible to Brian, useful for Nathan during setup
   
   ```tsx
   {showControls && (
     <div className="fixed bottom-4 right-4 bg-black text-white p-3 rounded-lg z-50 text-sm">
       <div className="font-bold mb-2">Demo Controls</div>
       <button onClick={resetDemo}>🔄 Reset Demo</button>
       <a href="/salesforce">📊 Salesforce View</a>
       <a href="/signals">🔍 Signals View</a>
     </div>
   )}
   ```

5. Make sure Push-to-Salesforce button state (from TODO 213) is stored in localStorage
   and cleared by resetDemo().

6. Run: npm run build — confirm 0 errors.

Report: How to trigger the reset, what state gets cleared, and any edge cases.
```

---

## Acceptance Criteria
- [ ] `?reset=true` URL param resets all state and redirects to clean Salesforce view
- [ ] `Cmd+Shift+D` keyboard shortcut triggers reset
- [ ] Push-to-Salesforce button returns to default state after reset
- [ ] Signal query/results clear on reset
- [ ] Hidden demo controls panel accessible via `?demo-controls=true`
- [ ] Build passes 0 errors
