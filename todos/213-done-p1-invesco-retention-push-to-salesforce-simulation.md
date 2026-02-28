# 213 — Invesco Retention: Push-to-Salesforce Simulation (P1)

**Priority:** 🟠 P1 — High demo impact  
**Project:** invesco-retention  
**Effort:** S (1-2 hrs)  
**Owner:** Honey  
**Dependencies:** 211 (deploy), but can develop before deploy

---

## Task Description

Add a working "Push to Salesforce" button to the signal creation page. When clicked, it simulates creating a Salesforce task with a realistic loading state and success toast. This is pure simulation — no actual Salesforce API call — but it must feel completely real.

Brian Kiley needs to see the Salesforce integration working. This is the moment that justifies "embedded in your existing Salesforce." Make it convincing.

---

## Coding Prompt (Agent-Executable)

```
You are adding a "Push to Salesforce" simulation to the invesco-retention demo app.

REPO: /data/workspace/projects/invesco-retention/demo-app

CONTEXT:
- The signal creation page is at src/app/signals/page.tsx (or similar)
- There is a results list showing ranked advisors after a signal query
- We need a "Push to Salesforce" button on each result (or on the selected advisor)

IMPLEMENTATION:

1. Find the signals/page.tsx (or signal-creation component) and locate where advisor results are displayed.

2. Add a "Push to Salesforce" button with these states:
   - DEFAULT: Blue button with Salesforce cloud icon: "Push to Salesforce"
   - LOADING: Spinner + "Creating task..." (1.5s fake delay)
   - SUCCESS: Green checkmark + "✅ Task created in Salesforce"
   - Button becomes disabled after success (prevents double-push)

3. On click, run this sequence:
   ```typescript
   const handlePushToSalesforce = async (advisorName: string) => {
     setPushState('loading');
     await new Promise(resolve => setTimeout(resolve, 1500));
     setPushState('success');
     // Show toast notification
     toast({
       title: "Task created in Salesforce",
       description: `✅ Follow-up task assigned to Marcus Thompson for ${advisorName}`,
       variant: "success",
     });
   };
   ```

4. Toast styling: Use the existing toast/sonner component if present. If not, add a simple fixed-position toast div that auto-dismisses after 4 seconds.

5. The success message should include:
   - Advisor name (dynamic from the signal result)
   - "Due: Tomorrow, 9:00 AM"
   - "Assigned to: Marcus Thompson"
   - Salesforce task ID (fake): "00T" + random 15 chars

6. Add the Salesforce logo/icon if you can (SVG inline or from public/):
   ```svg
   <!-- Simple Salesforce cloud icon placeholder -->
   <svg viewBox="0 0 24 24" className="w-4 h-4">...</svg>
   ```

7. Also add a "Push All to Salesforce" button at the top of the results list that runs the simulation for all results sequentially (200ms delay between each), showing a progress indicator.

8. After implementation, run: npm run build
   Ensure 0 TypeScript errors.

Report: Which files were modified, what the button looks like, and any issues found.
```

---

## Acceptance Criteria
- [ ] "Push to Salesforce" button visible on signal results
- [ ] Loading state shows for ~1.5 seconds
- [ ] Success toast appears with advisor name + task details
- [ ] Button disables after success (no double-push)
- [ ] "Push All" batch button works
- [ ] Build passes with 0 errors
- [ ] Mobile-responsive (button visible on small screens)
