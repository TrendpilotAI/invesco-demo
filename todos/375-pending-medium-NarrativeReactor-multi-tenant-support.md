# 375 — Add Multi-Tenant Support with Per-Tenant API Keys

## Task Description
NarrativeReactor currently uses a single global API key. For SaaS commercialization, add proper multi-tenant isolation: per-tenant API keys, `tenant_id` scoping on all DB tables, and middleware that resolves tenant context from the API key on every request.

## Coding Prompt
You are working on the NarrativeReactor repo at `/data/workspace/projects/NarrativeReactor/`.

This is a large feature. Implement it in stages:

### Stage 1: Tenants + API Keys Tables
Add to `src/lib/db.ts` migrations:
```sql
CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS api_keys (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL REFERENCES tenants(id),
  key_hash TEXT NOT NULL UNIQUE,  -- SHA-256 hash of the actual key
  name TEXT,                       -- human label e.g. "Production Key"
  scopes TEXT NOT NULL DEFAULT '["*"]',  -- JSON array
  last_used_at INTEGER,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  is_active INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX IF NOT EXISTS idx_api_keys_tenant_id ON api_keys(tenant_id);
```

### Stage 2: Tenant Context Middleware
Create `src/middleware/tenantContext.ts`:
- On each request, SHA-256 hash the `x-api-key` header
- Look up `api_keys` table by `key_hash`
- If found and active: attach `req.tenantId` and `req.tenantScopes` to the request
- If not found: fall back to legacy `API_KEY` env var (single-tenant mode for backward compatibility)
- Attach tenant context before route handlers

### Stage 3: Add tenant_id to Core Tables
Add `tenant_id TEXT` column to: `content_drafts`, `campaigns`, `workflows`, `scheduled_posts`
Use a DB migration with `ALTER TABLE ... ADD COLUMN tenant_id TEXT` (SQLite supports this).
For backward compatibility, allow NULL tenant_id (treated as "default tenant").

### Stage 4: Scope Queries by tenant_id
Update service layer queries to include `WHERE tenant_id = ?` when `req.tenantId` is set.
Create a helper: `src/lib/tenantScope.ts` → `scopeQuery(tenantId?: string)` returns SQL fragment.

### Stage 5: Admin API Endpoints
Add routes (admin-only, scoped to `admin:*` scope):
- `POST /api/admin/tenants` — create tenant
- `GET /api/admin/tenants` — list tenants
- `POST /api/admin/tenants/:id/keys` — generate API key (return plaintext once, store hash)
- `DELETE /api/admin/tenants/:id/keys/:keyId` — revoke key

### Stage 6: Backward Compatibility
- If `API_KEY` env var is set and no tenants exist, create a "default" tenant and migrate the env key to the DB on startup
- Existing integrations using the old API_KEY continue working
- All new keys are stored in DB

### Testing
Add `src/__tests__/middleware/tenantContext.test.ts` — mock DB, test key lookup, scope enforcement, fallback to env key.

Run `npm test` to confirm all tests pass.

## Dependencies
370 (DB indexes — migrate DB schema together)
369 (CI pipeline — validates this doesn't break builds)

## Estimated Effort
XL

## Acceptance Criteria
- [ ] `tenants` and `api_keys` tables created in migration
- [ ] `tenantContext` middleware resolves tenant from API key hash
- [ ] Core tables (`content_drafts`, `campaigns`, `workflows`) have `tenant_id` column
- [ ] Service queries scoped by `tenant_id` when present
- [ ] Admin API endpoints for tenant/key management work
- [ ] Backward compatible: existing `API_KEY` env var still works
- [ ] API key is only returned in plaintext once (stored as hash)
- [ ] Tenant middleware tests cover: valid key, invalid key, revoked key, legacy fallback
- [ ] All existing tests pass
