# TODO: Fix IDOR on Signal Access (signal-builder-backend)

**Priority:** CRITICAL  
**Repo:** signal-builder-backend  
**Effort:** 2 hours  
**Status:** pending

## Description
Signal GET endpoints may return signals belonging to other tenants (Insecure Direct Object Reference). If signal lookups use only `signal_id` without tenant scoping, any authenticated user can access any signal.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend:

1. Audit all signal retrieval in apps/signals/storages/:
   grep -rn "get.*signal\|filter.*id\|where.*id" apps/signals/storages/

2. For every query that fetches by signal_id, verify it also filters by tenant/org:
   # WRONG (vulnerable):
   await session.get(Signal, signal_id)
   # CORRECT:
   await session.execute(select(Signal).where(Signal.id == signal_id, Signal.tenant_id == current_tenant))

3. Check all routers in apps/signals/routers/ — confirm current_user tenant is extracted and passed to storage layer

4. Add tenant scoping to every signal storage method that currently only takes signal_id

5. Add tests in tests/signals/ for cross-tenant access:
   - Create signal as tenant A
   - Authenticate as tenant B  
   - Assert GET /signals/{id} returns 403/404 for tenant B

6. Check schema_builder and analytical_db modules for same issue
```

## Dependencies
- None (security critical)

## Acceptance Criteria
- Every signal query includes tenant_id filter
- Cross-tenant access returns 403 or 404
- Tests verify isolation between tenants
