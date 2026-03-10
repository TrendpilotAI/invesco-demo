# TODO-880: Fix tenants.ts — Migrate from better-sqlite3 to db.ts Singleton

**Repo**: NarrativeReactor  
**Priority**: P0 — Stability (potential SQLite lock contention)  
**Effort**: 2 hours  
**Status**: Pending  

## Problem

`src/services/tenants.ts` imports `better-sqlite3` directly:
```typescript
import Database from 'better-sqlite3';  // line 6
```

This creates a SECOND independent SQLite connection, separate from the WAL singleton in `src/lib/db.ts`. Two concurrent writers to the same SQLite WAL database can cause lock contention. Since `tenants.ts` is called on EVERY API request (auth check), this is a critical performance and stability issue.

Additionally:
- `better-sqlite3` is a native C++ addon — unnecessary build complexity
- `@types/better-sqlite3` is in prod `dependencies` (should be `devDependencies`)

## Solution

1. Migrate `tenants.ts` to use `getDb()` from `src/lib/db.ts` (which uses `node:sqlite`, built-in Node 22+)
2. Add tenant table schema to the `db.ts` migration system
3. Remove `better-sqlite3` and `@types/better-sqlite3` from `package.json`

### Key Changes

```typescript
// src/services/tenants.ts — BEFORE
import Database from 'better-sqlite3';
const db = new Database('data/narrative.db');

// AFTER
import { getDb } from '../lib/db';
// Use getDb() wherever db was used
// Note: better-sqlite3 uses synchronous .prepare().run() API same as node:sqlite
// Migration should be straightforward
```

### db.ts Migration Addition

Add tenant tables to `MIGRATIONS` array in `src/lib/db.ts`:
```typescript
{
  version: N,  // next version number
  up: `
    CREATE TABLE IF NOT EXISTS tenants (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      email TEXT,
      plan TEXT NOT NULL DEFAULT 'free',
      api_key_hash TEXT NOT NULL,
      active INTEGER NOT NULL DEFAULT 1,
      stripe_customer_id TEXT,
      stripe_subscription_id TEXT,
      quota_tokens INTEGER NOT NULL DEFAULT 10000,
      used_tokens INTEGER NOT NULL DEFAULT 0,
      reset_at TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
    CREATE UNIQUE INDEX IF NOT EXISTS idx_tenants_api_key_hash ON tenants(api_key_hash);
    CREATE INDEX IF NOT EXISTS idx_tenants_stripe_customer ON tenants(stripe_customer_id);
  `
}
```

## Dependencies

- Blocks TODO-878 (scrypt migration — should happen together)
- Should run full test suite after this change

## Files to Change

- `src/services/tenants.ts` — remove better-sqlite3, use getDb()
- `src/lib/db.ts` — add tenant table to migrations
- `package.json` — remove `better-sqlite3` and `@types/better-sqlite3`

## Acceptance Criteria

- [ ] tenants.ts uses `getDb()` from db.ts exclusively
- [ ] `better-sqlite3` removed from package.json dependencies
- [ ] `@types/better-sqlite3` removed from package.json dependencies
- [ ] All 287 tests still passing
- [ ] No two SQLite connections open simultaneously
- [ ] Index on `api_key_hash` exists for O(log n) auth lookup
