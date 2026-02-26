---
module: Signal Studio
date: 2026-02-22
problem_type: api_development
component: signal_generation
symptoms:
  - "Needed natural language → SQL for creating financial signals"
  - "Original had simplified 15-column schema, needed full Invesco data"
root_cause: incomplete_schema_context
severity: high
tags: [nl-to-sql, openai, signals, invesco, api]
---

# NL→SQL Signal Generation Engine

## Problem

Build an API endpoint that converts natural language descriptions into executable SQL queries for financial signal creation.

## Investigation

1. Analyzed signal-builder-backend repo for SQLAlchemy models
2. Found 22 analytical tables with 200+ columns
3. Extracted complete Invesco schema: MF/ETF/SMA/UIT book data, rankings, ML scores

## Failed Attempts

- **Attempt 1:** Hardcoded 15 simplified columns → Generated SQL missed key fields
- **Attempt 2:** No schema context in prompt → LLM guessed wrong table/column names
- **Attempt 3:** Missing relationship joins → SQL couldn't execute

## Solution

### 1. Schema Extraction
Created comprehensive schema context:
```typescript
// lib/schema-context.ts
export const ANALYTICAL_SCHEMA = `
### t_clients (Core — every advisor/firm)
- id, external_id (CRD), full_name, city, state, segment

### invesco_mf_book_data (~52 columns)
- mswm_current_assets, invesco_current_assets, invesco_prior_year_assets
- equities_category, fixed_income_preferreds_category, multi_asset_category
- mutual_funds_vehicle, closed_end_funds_etfs_vehicle

### customers_invesco_datasciencerecommendation (ML scores)
- opportunity_score, risk_score (1-100)
- upsell_opportunity_score, cross_sell_opportunity_score
- defend_revenue_opportunity_score, defend_aum_m
- distressed_aum_score, ria_opportunity_score
`
```

### 2. API Endpoint
```typescript
// app/api/signals/generate/route.ts
const result = await generateObject({
  model: openai("gpt-4o"),
  schema: SignalSchema,
  system: `You are a financial signals engineer...
  ${ANALYTICAL_SCHEMA}`,
  prompt: `Create a signal for: ${prompt}`,
})
```

### 3. Tested Queries

**Query 1:** "Find advisors whose Invesco AUM declined >25% YoY"
```sql
SELECT c.id AS client_id, c.full_name AS client_name,
  mf.invesco_current_assets, mf.invesco_prior_year_assets,
  ((mf.invesco_current_assets - mf.invesco_prior_year_assets) / 
   NULLIF(mf.invesco_prior_year_assets, 0) * 100) AS aum_decline_percentage
FROM t_clients c
JOIN invesco_mf_book_data mf ON c.id = mf.client_id
WHERE ...
```

**Query 2:** "MF declining but ETF growing" → 3-table JOIN

**Query 3:** "High cross-sell + zero SMA" → ML scores LEFT JOIN SMA book

## Prevention

- Always include full schema context for LLM code generation
- Test generated SQL before deployment
- Use parameterized queries for safety

## Related Issues

- See also: railway-signal-studio-fullstack-deployment
- See also: signal-agent-framework
