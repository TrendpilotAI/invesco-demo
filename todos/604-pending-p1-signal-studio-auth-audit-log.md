# TODO-604: Audit Log Migration + Endpoint

**Repo:** signal-studio-auth  
**Priority:** P1 (MEDIUM)  
**Effort:** 4h  
**Status:** pending

## Problem
No audit trail for auth events (login, logout, signup, invite, password reset). Required for enterprise compliance and SOC2.

## Fix

### Step 1: Migration `migrations/004_audit_log.sql`
```sql
CREATE TABLE IF NOT EXISTS auth_audit_log (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL,  -- 'login', 'logout', 'signup', 'invite', 'password_reset', 'token_theft'
    ip_address INET,
    user_agent TEXT,
    org_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_log_user_id ON auth_audit_log(user_id);
CREATE INDEX idx_audit_log_event_type ON auth_audit_log(event_type);
CREATE INDEX idx_audit_log_created_at ON auth_audit_log(created_at DESC);

-- RLS: only admins can read audit log
ALTER TABLE auth_audit_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Service key full access" ON auth_audit_log
    USING (auth.jwt() ->> 'role' = 'service_role');
```

### Step 2: Audit logging helper in `routes/auth_routes.py`
```python
async def _log_audit_event(
    client: httpx.AsyncClient,
    event_type: str,
    request: Request,
    user_id: str = None,
    org_id: str = None,
    metadata: dict = None,
):
    try:
        await client.post(
            f"{SUPABASE_URL}/rest/v1/auth_audit_log",
            json={
                "user_id": user_id,
                "event_type": event_type,
                "ip_address": request.client.host,
                "user_agent": request.headers.get("user-agent"),
                "org_id": org_id,
                "metadata": metadata or {},
            },
            headers={"apikey": SUPABASE_SERVICE_KEY, "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"},
        )
    except Exception as e:
        logger.warning(f"Audit log failed: {e}")  # non-fatal
```

### Step 3: `GET /auth/audit-log` (admin-only)
```python
@router.get("/audit-log")
async def get_audit_log(
    request: Request,
    limit: int = 100,
    _: None = Depends(require_role("admin")),
):
    ...
```

## Files to Create/Modify
- `migrations/004_audit_log.sql` (new)
- `routes/auth_routes.py` — add `_log_audit_event()` calls in login/logout/signup/invite handlers
- `routes/auth_routes.py` — add `GET /auth/audit-log` endpoint

## Acceptance Criteria
- [ ] Migration creates `auth_audit_log` with RLS
- [ ] Login, logout, signup, invite events logged
- [ ] Token theft event logged (in TODO-603)
- [ ] `GET /auth/audit-log` requires admin role
- [ ] Audit logging failures are non-fatal (log + continue)

## Dependencies
- TODO-600 (httpx pooling — use shared client)
- TODO-603 (token theft logging)
