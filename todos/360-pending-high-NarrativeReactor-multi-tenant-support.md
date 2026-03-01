# 360 · NarrativeReactor — Multi-Tenant Support (Per-Tenant API Keys & Brand Isolation)

**Priority:** high  
**Effort:** L (3–7 days)  
**Repo:** /data/workspace/projects/NarrativeReactor/

---

## Task Description

Currently NarrativeReactor uses a single global `API_KEY`. Multi-tenant support means each customer (workspace/tenant) gets their own API key, isolated data, and brand configuration. This is the core revenue enablement feature.

---

## Coding Prompt (agent-executable)

```
In /data/workspace/projects/NarrativeReactor/:

## Phase 1: Data Model

1. In src/db/schema.ts (or wherever SQLite schema is defined), add:

CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  api_key TEXT UNIQUE NOT NULL,
  plan TEXT DEFAULT 'starter',
  created_at TEXT DEFAULT (datetime('now')),
  is_active INTEGER DEFAULT 1
);

-- Add tenant_id to all resource tables:
ALTER TABLE content ADD COLUMN tenant_id TEXT REFERENCES tenants(id);
ALTER TABLE campaigns ADD COLUMN tenant_id TEXT REFERENCES tenants(id);
ALTER TABLE brands ADD COLUMN tenant_id TEXT REFERENCES tenants(id);
-- Repeat for all resource tables

2. Create src/services/tenantService.ts:

interface Tenant { id: string; name: string; apiKey: string; plan: string; }

export const tenantService = {
  create(name: string): Tenant,
  getByApiKey(apiKey: string): Tenant | null,
  list(): Tenant[],
  deactivate(id: string): void,
  generateApiKey(): string  // crypto.randomBytes(32).toString('hex')
};

## Phase 2: Auth Middleware Update

3. Update src/middleware/auth.ts:
   - Look up API key in tenants table instead of comparing to env var
   - Attach tenant to request: req.tenant = tenant
   - Fall back to env API_KEY for backwards compat (dev mode)

4. Create src/middleware/tenantContext.ts:
   - Ensure req.tenant is always set after auth
   - Provides req.tenantId shortcut

## Phase 3: Data Scoping

5. Update all service queries to filter by tenant_id:
   contentPipeline.list(tenantId): Content[]
   campaigns.list(tenantId): Campaign[]
   brands.list(tenantId): Brand[]

   Add a query wrapper utility:
   const scopeToTenant = (tenantId: string) => ({ where: { tenant_id: tenantId } });

## Phase 4: Admin API

6. Create src/routes/adminRoutes.ts (protected by ADMIN_KEY env var):
   POST   /admin/tenants          — create tenant, returns API key
   GET    /admin/tenants          — list all tenants
   DELETE /admin/tenants/:id      — deactivate tenant
   GET    /admin/tenants/:id/usage — cost/request stats

## Phase 5: Migration

7. Create scripts/migrate-to-multitenant.ts:
   - Create a "default" tenant with existing API_KEY
   - Assign all existing rows to default tenant_id
   - Run with: npx ts-node scripts/migrate-to-multitenant.ts

## Tests

8. Add tests/unit/tenantService.test.ts:
   - Create tenant, retrieve by API key
   - Deactivated tenant returns 401
   - Data isolation: tenant A cannot see tenant B's content
```

---

## Dependencies

- SQLite already in project (per completed items)
- #354 CI pipeline (for running migration tests safely)

## Acceptance Criteria

- [ ] `tenants` table exists in SQLite schema
- [ ] Auth middleware resolves tenant from API key
- [ ] All resource queries scoped by `tenant_id`
- [ ] Admin API can create/list/deactivate tenants
- [ ] Migration script assigns existing data to default tenant
- [ ] Tenant isolation tested: cross-tenant data access returns empty
- [ ] Backwards compatible with single env API_KEY in dev mode
