# TODO 429: Implement Real DataProvider Adapters (Snowflake + Postgres)

**Repo:** signal-studio-templates  
**Priority:** P1 (High — templates are useless without real data connections)  
**Effort:** L (3–5 days)  
**Status:** pending

## Description

The `DataProvider` interface is defined but has no concrete implementations. Templates can't actually run against Invesco or ForwardLane data without these adapters. This is a P1 blocker for any real customer demo.

## Acceptance Criteria

- [ ] `adapters/snowflake-data-provider.ts` — Snowflake adapter using `snowflake-sdk`
- [ ] `adapters/postgres-data-provider.ts` — Postgres adapter using `pg`
- [ ] Both adapters implement `DataProvider` interface correctly
- [ ] Both use `buildQuery` parameterized queries (no interpolation)
- [ ] Connection string configurable via env vars
- [ ] Both adapters tested with mock connections
- [ ] README updated with adapter setup instructions

## Coding Prompt

```typescript
// adapters/postgres-data-provider.ts
import { Pool, PoolConfig } from 'pg';
import { DataProvider, DataSource } from '../engine/template-engine';

export class PostgresDataProvider implements DataProvider {
  private pool: Pool;
  
  constructor(config?: PoolConfig) {
    this.pool = new Pool(config || {
      connectionString: process.env.DATABASE_URL,
      max: 10,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
    });
  }
  
  async executeSQL(sql: string, params?: unknown[]): Promise<Record<string, any>[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(sql, params);
      return result.rows;
    } finally {
      client.release();
    }
  }
  
  async availableDataSources(): Promise<DataSource[]> {
    // Query information_schema to detect available tables
    const result = await this.executeSQL(`
      SELECT table_name FROM information_schema.tables 
      WHERE table_schema = 'public'
    `);
    return mapTableNamesToDataSources(result.map(r => r.table_name));
  }
  
  async close(): Promise<void> {
    await this.pool.end();
  }
}

// adapters/snowflake-data-provider.ts
import snowflake from 'snowflake-sdk';
import { DataProvider, DataSource } from '../engine/template-engine';

export class SnowflakeDataProvider implements DataProvider {
  private connection: any;
  
  constructor(private config: {
    account: string;
    username: string;
    password: string;
    database: string;
    schema: string;
    warehouse: string;
  }) {}
  
  async connect(): Promise<void> {
    this.connection = snowflake.createConnection({
      account: this.config.account,
      username: this.config.username,
      password: this.config.password,
      database: this.config.database,
      schema: this.config.schema,
      warehouse: this.config.warehouse,
    });
    await new Promise<void>((resolve, reject) => {
      this.connection.connect((err: Error) => err ? reject(err) : resolve());
    });
  }
  
  async executeSQL(sql: string, params?: unknown[]): Promise<Record<string, any>[]> {
    if (!this.connection) await this.connect();
    return new Promise((resolve, reject) => {
      this.connection.execute({
        sqlText: sql,
        binds: params as any[],
        complete: (err: Error, stmt: any, rows: any[]) => {
          err ? reject(err) : resolve(rows || []);
        },
      });
    });
  }
  
  async availableDataSources(): Promise<DataSource[]> {
    return ['crm', 'holdings', 'transactions', 'interactions', 'market-data', 
            'compliance', 'demographics', 'pipeline'];
  }
}

// Add to package.json dependencies:
// "pg": "^8.11.3"
// "snowflake-sdk": "^1.9.0"
// "@types/pg": "^8.11.2"
```

## Dependencies

- TODO 426 (auth) — auth context needed to determine which DB the user has access to
- TODO 427 (tests) — MockDataProvider created there can be used as reference

## Notes

ForwardLane already has working Snowflake/Oracle connections in `forwardlane-backend`. Reference those for connection pooling patterns. The Oracle adapter can be added as TODO 429b once Postgres/Snowflake are proven.
