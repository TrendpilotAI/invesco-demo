# TODO-388: Append-Only Compliance Audit Log

**Repo:** signal-studio
**Priority:** P2 (financial compliance)
**Effort:** M (1-2 days)
**Status:** pending
**Audit ref:** NEW-003

## Description
Financial platforms handling client data (especially regulated advisors using ForwardLane) need audit trails of all significant actions. Currently zero logging of who did what. This is a gap for SOC2, SEC, FINRA readiness.

## Schema
```sql
CREATE TABLE audit_log (
  id BIGSERIAL PRIMARY KEY,
  user_id TEXT,
  action TEXT NOT NULL,       -- e.g. 'signal.run', 'oracle.query', 'signal.create'
  resource_type TEXT,          -- 'signal', 'oracle_table', 'chat_session'
  resource_id TEXT,
  metadata JSONB,              -- action-specific context
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
-- Immutable: no UPDATE, no DELETE (use RLS policy)
CREATE INDEX ON audit_log (user_id, created_at DESC);
CREATE INDEX ON audit_log (action, created_at DESC);
```

## Task
1. Create migration `003-audit-log.sql`
2. Create `lib/audit.ts` — `logAuditEvent(action, resourceType, resourceId, metadata)` helper
3. Add to middleware or individual route handlers:
   - Signal run → `signal.run`
   - Oracle query → `oracle.query`
   - Login → `auth.login`
   - Signal create/update/delete → `signal.create`, etc.
4. Create admin UI page showing audit log with filters (user, action, date range)

## Acceptance Criteria
- [ ] Audit log table created with immutability policy
- [ ] All mutating API routes log to audit_log
- [ ] Admin page shows filterable audit log
- [ ] logAuditEvent helper tested

## Dependencies
TODO-384 (fix build errors), TODO-386 (signals run table for cross-reference)
