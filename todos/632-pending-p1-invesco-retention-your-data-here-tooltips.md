# TODO #632 — "Your Data Here" Integration Path Tooltips

**Priority:** P1 (Win-the-Deal)
**Effort:** XS (1h)
**Repo:** invesco-retention
**Status:** pending

## Description
Add subtle "Replace with your Snowflake data in Week 1" tooltips to key data cards in the demo. This proactively addresses the "how would this work with our actual data?" question that Brian/Vanessa will definitely ask, and signals that we've thought through the integration path.

## Coding Prompt
```
In /data/workspace/projects/invesco-retention/demo-app/src/app/salesforce/page.tsx:

Add a small info icon (ℹ️ or Lucide `Info` icon) next to data source labels.
On hover, show a tooltip: "Connects to your Snowflake data warehouse in Week 1"
or "Pulls from your Salesforce CRM — no manual data entry"

Target locations:
1. AUM/transaction data card → "Syncs from Snowflake daily"  
2. CRM activity feed → "Live from your Salesforce org"
3. Content recommendations → "Personalized from your Seismic library"
4. Competitor intelligence → "From your existing market data feeds"

Use a simple CSS tooltip (no library needed):
- Small grey "ℹ️" icon inline
- Tooltip appears on hover, positioned above the icon
- Text: 10px, muted color
- Does NOT distract from demo — subtle only
```

## Acceptance Criteria
- [ ] 4 data source tooltips visible in /salesforce view
- [ ] Tooltips are subtle (don't compete with main content)
- [ ] Each tooltip explains the integration source
- [ ] Works on mobile breakpoint
