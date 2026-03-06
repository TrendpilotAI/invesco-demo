---
id: 635
status: pending
priority: P0
repo: signal-studio-templates
title: Create MockDataProvider with seed data for demo
effort: S (1-2 days)
dependencies: []
---

# Create MockDataProvider + Realistic Seed Data

## Problem
There is no concrete `DataProvider` implementation, and no mock/seed data for demos. This means Signal Studio Templates cannot be demonstrated to Invesco without a live ForwardLane database connection. Demo-blocking.

## Task
Create `src/providers/mock-data-provider.ts` with 50 realistic financial advisors and 500 accounts, plus pre-canned results for all 20 templates.

## Coding Prompt
```
Create /data/workspace/projects/signal-studio-templates/src/providers/mock-data-provider.ts

Implement the DataProvider interface from engine/template-engine.ts:
  interface DataProvider {
    executeSQL(sql: string, params?: unknown[]): Promise<Record<string, any>[]>;
    availableDataSources(): Promise<DataSource[]>;
  }

Requirements:
1. availableDataSources() returns ALL data sources (all 11 types from schema)
2. executeSQL() inspects the sql string to determine which template is being run
   and returns realistic mock data:
   - 50 advisors with names, AUM ($1M-$500M range), firms, territories
   - 500 accounts with advisor_id, account_type, balance, last_contact_date
   - Realistic dates (last 90 days), dollar amounts, product names
3. Create separate seed data file: src/providers/seed-data.ts
   with typed arrays for advisors, accounts, interactions, holdings
4. Template-specific mock results:
   - dormant-relationships: 8-15 advisors not contacted in 45+ days
   - meeting-brief: comprehensive advisor profile data
   - best-shots-on-goal: 5-10 ranked opportunities
   - concentration-risk: 3-5 accounts with >25% single-holding concentration
   - (implement all 20 templates with realistic results)
5. Add optional delay simulation: constructor({ latencyMs?: number })

Create src/providers/seed-data.ts with:
- MOCK_ADVISORS: 50 entries with realistic names, territories, AUM
- MOCK_ACCOUNTS: 500 entries linked to advisors
- MOCK_INTERACTIONS: 200 entries (calls, emails, meetings)
- MOCK_HOLDINGS: 1000 entries (products, amounts, percentages)

Export MockDataProvider from index.ts
```

## Acceptance Criteria
- [ ] `src/providers/mock-data-provider.ts` implements DataProvider
- [ ] `src/providers/seed-data.ts` has realistic data (50 advisors, 500 accounts)
- [ ] All 20 templates return non-empty results from MockDataProvider
- [ ] `pnpm test` passes with new mock provider tests
- [ ] Demo can run without any external DB connection
