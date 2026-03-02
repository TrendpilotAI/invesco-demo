# TODO-397: NarrativeReactor — Multi-Tenant SaaS Foundation

**Priority:** critical
**Repo:** NarrativeReactor
**Effort:** M (3-4 days)

## Description
Add `tenant_id` to all SQLite tables and scope all service queries by tenant. Required to monetize as SaaS.

## Coding Prompt
```
Add multi-tenancy to NarrativeReactor at /data/workspace/projects/NarrativeReactor/

1. Add tenant_id column to all SQLite tables in src/lib/db.ts
2. Update all 32 services (src/services/*.ts) to accept tenantId param and scope queries
3. Extract tenant from API key in middleware/auth.ts — map API key → tenant_id
4. Add tenant management endpoints: POST /api/tenants, GET /api/tenants/:id
5. Per-tenant API key issuance: POST /api/tenants/:id/keys
6. Update all tests to pass tenant context
```

## Acceptance Criteria
- [ ] All DB queries scoped by tenant_id
- [ ] API key → tenant mapping works
- [ ] Tenant A cannot see Tenant B's content
- [ ] Tests pass with multi-tenant isolation

## Dependencies
- TODO-396 (deploy) can happen in parallel
