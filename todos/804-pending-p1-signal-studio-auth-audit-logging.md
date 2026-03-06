# 804 — Add Audit Logging Middleware

**Repo:** signal-studio-auth  
**Priority:** P1 (compliance/enterprise requirement)  
**Effort:** M (3-4 hours)  
**Dependencies:** 801 (CORS)

## Problem

No audit trail of auth events. Enterprise customers and SOC2 compliance require logging of all auth events (login, logout, failed attempts, password changes, org invites).

## Acceptance Criteria

- [ ] Middleware logs all auth events to a structured JSON log
- [ ] Events include: timestamp, event_type, user_id (if known), IP, user_agent, success/failure
- [ ] Optionally writes to `auth_audit_log` table in Supabase DB (via service key)
- [ ] Structured JSON format compatible with Datadog/CloudWatch ingestion
- [ ] No PII in logs (no passwords, no full tokens — only first 8 chars of token)

## Coding Prompt

```
Create /data/workspace/projects/signal-studio-auth/middleware/audit_logger.py:

A FastAPI middleware that:
1. Intercepts all POST requests to /auth/* endpoints
2. After the response is generated, logs a structured JSON event:
   {
     "timestamp": "ISO8601",
     "event": "auth.login" | "auth.signup" | "auth.logout" | ...,
     "success": bool,
     "status_code": int,
     "user_id": str | null,  # from request.state.user if available
     "ip": str,
     "user_agent": str,
     "request_id": str  # X-Request-ID header
   }
3. Uses Python's structured logging (json format)
4. Optional: if SUPABASE_AUDIT_LOG=true env var, also inserts to auth_audit_log table

Add the middleware to main.py.
Add tests in tests/test_audit_logger.py.
```
