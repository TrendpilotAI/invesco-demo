# 874 — Signal Performance Analytics Dashboard

**Repo:** signal-studio  
**Priority:** P1 — Revenue Feature  
**Effort:** 2 weeks  
**Status:** pending

## Problem
The `app/analytics/page.tsx` is a stub with no real data. Customers can't see which signals actually generated pipeline or closed deals. Without ROI proof, it's hard to justify the subscription price.

## Opportunity
- ROI proof → justifies enterprise pricing
- Signal attribution → which signals → which meetings → which closed deals
- Usage analytics → most popular signals, highest accuracy signals

## Architecture

```
Signal Events (PostgreSQL)
  → Signal created, triggered, viewed
  → Meeting prep used
  → Easy Button opened

CRM Sync
  → Salesforce opportunity stage changes attributed to signals
  → Win/loss analysis

Analytics API
  → app/api/analytics/signals/route.ts
  → app/api/analytics/performance/route.ts

Dashboard Components
  → components/analytics/signal-performance-chart.tsx
  → components/analytics/top-signals-table.tsx
  → components/analytics/roi-summary.tsx
  → components/analytics/meeting-prep-usage.tsx
```

## Key Metrics to Track
1. **Signal Fire Rate** — How often each signal triggers per week
2. **Meeting Prep Usage** — Easy Button opens per signal
3. **Signal Accuracy** — User thumbs up/down feedback
4. **Pipeline Attribution** — Signals used before deals closed (Salesforce)
5. **ROI Score** — Estimated revenue influenced per signal

## Acceptance Criteria
- [ ] Analytics page shows real signal usage data (not stub)
- [ ] Top signals by usage visible
- [ ] Signal fire rate over time chart
- [ ] Meeting prep usage count per signal
- [ ] Basic ROI summary (meetings + estimated pipeline)
- [ ] Filterable by date range

## Revenue Impact
- Makes the "why pay for this?" question easy to answer
- Enables customer success conversations with data
- Unlocks premium analytics tier pricing
