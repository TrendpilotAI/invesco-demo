---
id: 700
status: pending
repo: signal-studio-templates
priority: P0
effort: L
created: 2026-03-10
---

# TODO 700 — Implement PostgreSQL DataProvider (BLOCKS PRODUCTION)

**Repo:** signal-studio-templates  
**Priority:** P0 — Required for any production deployment  
**Effort:** L (2-3 days)

## Problem

Only `MockDataProvider` exists. Cannot run the template library against real data. This blocks Invesco deployment and all revenue from this product.

## Solution

Implement `PostgresDataProvider` using `postgres.js` (lightweight, native parameterization).

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates:

1. Install postgres.js:
   pnpm add postgres

2. Create engine/postgres-data-provider.ts implementing DataProvider interface:
   - constructor accepts: connectionString (string) and optional schemaMap (Record<DataSource, string> — maps DataSource enum values to actual table/view names)
   - executeSQL(sql, params): delegates to postgres.js tagged template executor. IMPORTANT: params are already $1/$2 positional from parameterizeLegacyTemplate — use postgres.js raw query mode: postgres.unsafe(sql, params)
   - availableDataSources(): introspect pg_tables + pg_views in the configured schema (default: 'public') and map table names back to DataSource enum values using the schemaMap

3. Add configuration via environment variables:
   - POSTGRES_CONNECTION_STRING: full connection URL (postgres://user:pass@host:5432/db)
   - POSTGRES_SCHEMA: schema name (default: public)
   - POSTGRES_CONNECTION_POOL_MAX: max pool size (default: 10)
   - POSTGRES_QUERY_TIMEOUT_MS: query timeout ms (default: 30000)

4. Wrap executeSQL in Promise.race with POSTGRES_QUERY_TIMEOUT_MS timeout (also addresses the query timeout AUDIT finding).

5. Add __tests__/engine/postgres-data-provider.test.ts:
   - Skip tests if POSTGRES_CONNECTION_STRING not set (for CI without real DB)
   - Integration test: connect, execute simple SELECT 1, verify result
   - Test all DataSource enum values map correctly via schemaMap

6. Add docker-compose.test.yml for local integration testing:
   - postgres:15-alpine
   - Seed with the same schema structure as MockDataProvider (advisors, accounts, interactions, opportunities, market_data, products)
   - Map MockDataProvider seed-data.ts structure to real SQL CREATE TABLE + INSERT statements

7. Update README.md with PostgresDataProvider usage example:
   import { TemplateEngine } from '@forwardlane/signal-studio-templates/engine';
   import { PostgresDataProvider } from '@forwardlane/signal-studio-templates/engine/postgres';
   const engine = new TemplateEngine(new PostgresDataProvider(process.env.POSTGRES_CONNECTION_STRING));
```

## Files

- `engine/postgres-data-provider.ts` (new)
- `__tests__/engine/postgres-data-provider.test.ts` (new)
- `docker-compose.test.yml` (new)
- `README.md` (update)
- `package.json` (add postgres.js dependency)

## Acceptance Criteria

- All 20 templates execute successfully against a real Postgres schema
- PostgresDataProvider passes `DataProvider` interface type check
- Tests skip gracefully when `POSTGRES_CONNECTION_STRING` is not set
- docker-compose.test.yml brings up a working test DB with seed data

## Dependencies

- Unblocks: TODO-429 (data provider implementations)
- Unblocks: integration tests
- Unblocks: Invesco Snowflake DataProvider (Task 3.1 in PLAN.md)
