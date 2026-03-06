---
id: 635
status: done
priority: P0
repo: signal-studio-templates
title: Create MockDataProvider with seed data for demo
completed: 2026-03-06
---

# Done ✅

## What was implemented

### `engine/seed-data.ts`
- `MOCK_ADVISORS` — 50 synthetic financial advisors with names, firms, territories (NE/SE/MW/SW/W), AUM ($1.5M–$180M+), tiers (platinum/gold/silver/bronze), YTD sales, risk profiles, preferred contact
- `MOCK_ACCOUNTS` — 500 accounts linked to advisors with balances, account types (IRA/Roth/Brokerage/401k etc.), concentration %, RMD eligibility, days since review
- `MOCK_INTERACTIONS` — 200 interaction records (calls/emails/meetings) — first 30 advisors have recent contact, last 20 are dormant (45–130 days silent)
- `MOCK_HOLDINGS` — 1000 holding records across accounts with product names, allocations, YTD returns, expense ratios

### `engine/mock-data-provider.ts`
- Implements `DataProvider` interface (`executeSQL` + `availableDataSources`)
- `availableDataSources()` returns all 11 data source types
- `executeSQL()` inspects SQL string keywords to route to 20 template-specific mock handlers:
  - dormant-relationships, meeting-brief, relationship-health, recent-activity-digest, competitive-landscape
  - best-shots-on-goal, product-fit-scorer, territory-pulse
  - risk-drift-alert, rmd-life-events, concentration-risk, suitability-check
  - product-adoption-tracker, competitive-displacement, cross-sell-recommender, campaign-target-list
  - wholesaler-scorecard, team-coverage-gaps, pipeline-health, regional-benchmark
- Constructor supports `{ latencyMs?: number }` for simulated network delay

### `index.ts`
- Exports `MockDataProvider`, `MockDataProviderOptions`
- Exports all seed data arrays for external use

### `__tests__/mock-data-provider.test.ts`
- 10 new tests covering seed data counts, field validation, executeSQL routing, latency simulation, and full template execution
- All 35 tests pass (25 original + 10 new)

## Commit
`31c900e` pushed to `TrendpilotAI/signal-studio-templates` main branch
