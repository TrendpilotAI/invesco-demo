# TODO-589: Add compliance audit_log table

**Repo:** signal-studio
**Priority:** P1
**Effort:** S (2-3 hours)
**Status:** pending

## Problem
No immutable audit trail of user actions. Required for SOC2 compliance and enterprise sales.
Every state-changing action (signal run, delete, Oracle query, auth events) must be logged.

## Task
1. Create `audit_log` table in Postgres
2. Create `lib/audit.ts` helper
3. Wire into key API routes

## Coding Prompt
```
In /data/workspace/projects/signal-studio:
1. Add to migration SQL:
   CREATE TABLE IF NOT EXISTS audit_log (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     actor_id TEXT NOT NULL,
     action TEXT NOT NULL,
     resource_type TEXT,
     resource_id TEXT,
     metadata JSONB,
     ip_addr TEXT,
     created_at TIMESTAMPTZ DEFAULT now()
   );
   CREATE INDEX idx_audit_log_actor ON audit_log(actor_id);
   CREATE INDEX idx_audit_log_created ON audit_log(created_at DESC);

2. Create lib/audit.ts:
   export async function auditLog(event: {
     actorId: string; action: string;
     resourceType?: string; resourceId?: string;
     metadata?: Record<string, unknown>; ipAddr?: string;
   }) { /* INSERT INTO audit_log */ }

3. Wire into:
   - app/api/signals/run/route.ts → auditLog({ action: 'signal.run', ... })
   - app/api/oracle/query/route.ts → auditLog({ action: 'oracle.query', ... })
   - app/api/auth/login → auditLog({ action: 'auth.login', ... })
   - app/api/signals DELETE → auditLog({ action: 'signal.delete', ... })
```

## Acceptance Criteria
- [ ] audit_log table exists in Postgres
- [ ] Signal runs, Oracle queries, auth events create rows
- [ ] IP address captured from request headers
- [ ] Table is append-only (no UPDATE/DELETE permissions for app user)

## Dependencies
- TODO-588 (same migration file, add together)
