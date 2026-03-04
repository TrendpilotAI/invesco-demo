# TODO-503: Auth Audit Log to Postgres

**Priority:** P2  
**Effort:** M (~4h)  
**Repo:** signal-studio-auth  
**Status:** pending

## Description
For SOC2 compliance and enterprise customers, write auth events to an `auth_audit_log` table.

## Migration (004_auth_audit_log.sql)
```sql
CREATE TABLE IF NOT EXISTS auth_audit_log (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL, -- login, logout, signup, invite, password_reset
    user_id TEXT,             -- Supabase UUID
    organization_id INT,
    ip_address TEXT,
    user_agent TEXT,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_audit_log_user_id ON auth_audit_log(user_id, created_at DESC);
CREATE INDEX idx_audit_log_org_id ON auth_audit_log(organization_id, created_at DESC);
```

## Acceptance Criteria
- [ ] All auth events (login/logout/signup/invite/refresh) logged
- [ ] Failed attempts logged with error_message
- [ ] Migration script created
- [ ] Async fire-and-forget (don't block auth response on DB write)
