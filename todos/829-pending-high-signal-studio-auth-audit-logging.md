# TODO-829: Add Structured Audit Logging to signal-studio-auth

**Repo:** signal-studio-auth  
**Priority:** P1 (High)  
**Effort:** 3 hours  
**Status:** pending

## Task
- Create `migrations/004_audit_logs.sql` with `audit_logs` table
- Create `middleware/audit_log.py` with async fire-and-forget logging
- Log events: login (success/fail), signup, logout, password change, invitation, role change
- Schema: `(id UUID, event_type TEXT, user_id TEXT, org_id INT, ip_address TEXT, user_agent TEXT, metadata JSONB, created_at TIMESTAMPTZ)`

## Acceptance Criteria
- [ ] Migration runs cleanly on Supabase
- [ ] Every auth endpoint writes an audit log entry
- [ ] Logging is async (non-blocking)
- [ ] Failed auth attempts logged with reason
