# TODO-383: Competitor Displacement Persona

**Repo:** invesco-retention
**Priority:** P1
**Effort:** S (2 hours)
**Status:** pending

## Description
Add a second advisor persona prominently featuring the Competitor Displacement signal type — showing a $500K position moving to American Funds. Resonates strongly with wholesalers.

## Acceptance Criteria
- [ ] New advisor persona added to synthetic data (advisors.json)
- [ ] Persona has prominent "Competitor Displacement Alert" signal as first signal
- [ ] Signal shows: American Funds attracting $500K of INVESCO client assets
- [ ] Visible in dashboard advisor list
- [ ] Full meeting brief available in salesforce view

## Coding Prompt
```
Add competitor displacement advisor persona to invesco-retention demo:

1. Add new advisor to /data/workspace/projects/invesco-retention/synthetic-data/advisors.json:
   - Name: "Michael Torres, CFP"
   - AUM: $18.2M with Invesco, $45M total
   - Location: Dallas, TX
   - At-risk: $500K moving to American Funds Growth Fund of America

2. Add corresponding signal to signal_outputs.json:
   - Type: "competitor_displacement"
   - Severity: "urgent"
   - Text: "⚠️ Competitor Alert: $500K reallocation detected toward American Funds"
   - Detail: "Michael Torres reduced INVPX allocation by 12% Q/Q. American Funds GOF showing in 3 recent client holdings."

3. Update mock-data.ts to include Torres in advisor list
4. Ensure he appears as #1 or #2 in dashboard sorted by urgency
5. Update salesforce page to include Torres as selectable advisor
```

## Dependencies
- None
