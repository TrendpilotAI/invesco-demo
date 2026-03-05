# TODO 582: MockDataProvider with Demo Seed Data (Invesco Demo Readiness)

**Repo:** signal-studio-templates  
**Priority:** P1 (High — can't demo to Invesco without working end-to-end)  
**Effort:** M (1–2 days)  
**Status:** pending

## Description

There is no working demo environment. The DataProvider interface exists but no implementation. For the Invesco demo, we need a `MockDataProvider` with realistic advisor/account seed data so all 20 templates return meaningful results without needing a production database.

## Implementation

```typescript
// src/providers/mock-data-provider.ts
import { DataProvider, DataSource } from "../../schema/signal-template";

const SEED_ADVISORS = [
  { advisor_id: "adv-001", name: "Sarah Chen", aum: 45000000, territory: "Northeast", ... },
  // 50 advisors...
];

const SEED_ACCOUNTS = [
  { account_id: "acc-001", advisor_id: "adv-001", client_name: "Acme Corp", aum: 2500000, ... },
  // 500 accounts...
];

export class MockDataProvider implements DataProvider {
  async executeSQL(sql: string, params?: unknown[]): Promise<Record<string, any>[]> {
    // Pattern-match SQL to return appropriate seed data subset
    // Use simple keyword detection to route to right seed dataset
    if (sql.includes("dormant") || sql.includes("last_contact")) return this.getDormantAdvisors();
    if (sql.includes("concentration")) return this.getRiskConcentration();
    // etc. for all 20 template patterns
    return SEED_ADVISORS.slice(0, 10);
  }
  
  async availableDataSources(): Promise<DataSource[]> {
    return ["crm", "holdings", "transactions", "interactions", "market-data", 
            "compliance", "demographics", "pipeline", "activity-log", 
            "product-catalog", "benchmarks"];
  }
}
```

## Acceptance Criteria

- [ ] `src/providers/mock-data-provider.ts` with 50 realistic advisor records
- [ ] Seed data for all DataSource types (crm, holdings, transactions, etc.)
- [ ] Each of the 20 templates returns meaningful non-empty results with mock data
- [ ] `demo/` directory with runnable example: `ts-node demo/run-all-templates.ts`
- [ ] Demo script prints formatted results for all 20 templates
- [ ] MockDataProvider exported from package index

## Dependencies
- None (standalone)
