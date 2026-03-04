# TODO #428: Pilot Timeline Widget
**Priority:** P1 | **Effort:** XS (1h) | **Status:** Pending
**Repo:** invesco-retention | **Date:** 2026-03-04

## Description
Add a visual "2-week pilot timeline" widget to the demo showing Day 0 → Day 14 milestones. Makes the pilot feel structured, real, and easy to say yes to. Pure UI, no backend.

## Coding Prompt (Agent-Executable)
```
In /data/workspace/projects/invesco-retention/demo-app/src/app/salesforce/page.tsx
(or create a new modal triggered by a "View Pilot Plan" button):

Create a PilotTimeline component:

const milestones = [
  { day: 0, label: "Kickoff Call", detail: "30-min setup with IT + sales ops" },
  { day: 1, label: "Data Access", detail: "Read-only Snowflake + Seismic webhook" },
  { day: 3, label: "Advisor Load", detail: "Your 50 advisors imported + validated" },
  { day: 5, label: "First Signals", detail: "Live signal outputs for top territory" },
  { day: 7, label: "Mid-Check", detail: "Review signal quality with Megan's team" },
  { day: 14, label: "Pilot Review", detail: "Full evaluation with leadership" },
];

Render as a horizontal timeline with dots and connecting lines.
Use Invesco brand colors (#0176D3 blue).
Show day number, milestone label, and brief detail below each dot.

Add a "View Pilot Plan" button to the bottom of the salesforce meeting brief.
On click, show the timeline in an inline section or modal.

Keep it simple: no animations required. Static, clean, professional.

Rebuild and deploy.
```

## Acceptance Criteria
- [ ] Pilot timeline widget renders in salesforce view
- [ ] Shows 6 milestones from Day 0 to Day 14
- [ ] Uses Invesco brand colors
- [ ] Triggered by "View Pilot Plan" button
- [ ] Deployed to GitHub Pages

## Dependencies
None

## Impact
Medium — Makes the path from "yes" to "value" feel short and structured. Reduces friction.
