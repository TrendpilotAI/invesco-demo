# TODO-382: "Connect Your Data" Demo Mode Toggle

**Repo:** invesco-retention
**Priority:** P1
**Effort:** M (3-4 hours)
**Status:** pending

## Description
Add a "Connect Your Data" button in the Salesforce demo view that opens a modal showing a 3-step integration wizard (Seismic → CRM → Snowflake). Doesn't actually connect — shows the product vision credibly.

## Acceptance Criteria
- [ ] Button visible in salesforce route: "Connect Your Data →"
- [ ] Modal opens with 3-step wizard UI
- [ ] Step 1: Seismic (OAuth-style connect button, shows "Connected ✓" after click)
- [ ] Step 2: Salesforce CRM (same pattern)
- [ ] Step 3: Snowflake (same pattern)
- [ ] "Launch Pilot" CTA at the end
- [ ] Mobile-responsive

## Coding Prompt
```
Add a "Connect Your Data" feature to /data/workspace/projects/invesco-retention/demo-app/src/app/salesforce/page.tsx

1. Add a "Connect Your Data →" button in the header area of the Signal Studio panel
2. Create a ConnectDataModal component:
   - 3-step wizard UI using existing UI components (Card, Button, Badge)
   - Step 1: Seismic — logo, "Authenticate with Seismic" button, success state "Content library synced ✓"
   - Step 2: Salesforce CRM — "Connect CRM" button, success "10,847 activities synced ✓"
   - Step 3: Snowflake — "Connect Data Warehouse" button, success "3.2M transactions indexed ✓"
   - Final screen: "Your Signal Studio is ready" + "Schedule Pilot Kickoff" CTA button
3. Each step has a 1.5s simulated loading state before showing success
4. Modal is dismissible with X button
5. Use Tailwind for styling consistent with existing design
```

## Dependencies
- None (all mock/simulation)
