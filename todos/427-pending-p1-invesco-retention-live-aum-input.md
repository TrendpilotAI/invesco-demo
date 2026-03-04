# TODO #427: Live AUM Input on ROI Calculator
**Priority:** P1 | **Effort:** S (1-2h) | **Status:** Pending
**Repo:** invesco-retention | **Date:** 2026-03-04

## Description
Add an interactive AUM input field to the dashboard ROI section. Pre-filled with synthetic $40M figure, but Brian can type HIS actual AUM with Invesco. The ROI at-risk calculation then becomes personal and visceral — not a demo number, but his actual number.

## Coding Prompt (Agent-Executable)
```
In /data/workspace/projects/invesco-retention/demo-app/src/app/dashboard/page.tsx:

1. Find the AUM / ROI at-risk section (likely shows "$40M" or similar synthetic figure)

2. Replace the static AUM display with an editable input:
   <div className="flex items-center gap-2">
     <span className="text-sm text-gray-500">Your AUM with this advisor:</span>
     <input 
       type="text" 
       value={aumInput}
       onChange={(e) => setAumInput(e.target.value)}
       className="border-b border-blue-500 bg-transparent text-2xl font-bold w-32 text-right"
       placeholder="$40M"
     />
   </div>

3. Parse the input value (handle "$40M", "40M", "40000000", "40,000,000" formats)
   Use a simple parser: strip $, commas, convert M/B suffix to number.

4. Recalculate ROI at-risk live:
   - If AUM is parsed → show: "Based on your $X AUM, signals at risk: $Y"
   - Use same % calculation as synthetic data (e.g., 8% at-risk = $X * 0.08)

5. Add subtle "Enter your actual AUM" hint text below the input on first render.
   Fade it out after user types.

6. Rebuild and deploy.
```

## Acceptance Criteria
- [ ] AUM input field is editable in dashboard view
- [ ] Parses common number formats ($40M, 40000000, etc.)
- [ ] ROI calculation updates live as user types
- [ ] Pre-filled with synthetic $40M
- [ ] Deployed to GitHub Pages

## Dependencies
None

## Impact
Medium-High — Makes ROI personal. Brian typing his own AUM is a powerful commitment device.
