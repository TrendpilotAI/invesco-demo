# FL-034: API Audit Logging Middleware

**Repo:** forwardlane-backend  
**Priority:** P0  
**Effort:** M (2-3 days)  
**Status:** pending

## Task Description
Implement append-only API audit logging for SOC2 and financial regulatory compliance. Every API request must be logged with user, tenant, endpoint, method, timestamp, status code, and IP address. Required for Invesco enterprise contract compliance.

## Problem
No audit trail exists for data access. Enterprise financial clients (Invesco) require audit logs for compliance (SOC2 Type II, financial regulations). Currently we have zero visibility into who accessed what data and when.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Create core/middleware/audit_middleware.py:
   - Django middleware class: AuditLogMiddleware
   - Hook: process_response(request, response)
   - Capture: user_id (null if anonymous), tenant_id (from request.user.tenant if available),
     endpoint (request.path), method (request.method), status_code (response.status_code),
     ip_address (X-Forwarded-For or REMOTE_ADDR), user_agent (request.META.get('HTTP_USER_AGENT')),
     timestamp (timezone.now())
   - Write to AuditLog model (see step 2)
   - Skip: /health/, /metrics/, /favicon.ico, static files

2. Create core/models/audit_log.py:
   - class AuditLog(models.Model):
       user_id = models.IntegerField(null=True, blank=True, db_index=True)
       tenant_id = models.IntegerField(null=True, blank=True, db_index=True)
       endpoint = models.CharField(max_length=500)
       method = models.CharField(max_length=10)
       status_code = models.IntegerField()
       ip_address = models.GenericIPAddressField(null=True)
       user_agent = models.TextField(blank=True)
       timestamp = models.DateTimeField(default=timezone.now, db_index=True)
       class Meta:
           db_table = 'core_audit_log'
           # No delete permissions — append only
   - Create migration

3. Add AuditLogMiddleware to MIDDLEWARE in forwardlane/settings/base.py
   (after SecurityMiddleware, before SessionMiddleware)

4. Create admin view in core/admin.py:
   - AuditLogAdmin with list_display, list_filter (tenant_id, method, status_code, timestamp), search_fields
   - Read-only admin (no delete/edit allowed)

5. Create API endpoint GET /api/v1/audit-logs/ (admin only):
   - Filter by tenant_id, user_id, date range
   - Paginated response
   - Used for compliance exports

6. Write tests in core/tests/test_audit_middleware.py:
   - Test log is created on API request
   - Test anonymous request captures null user_id
   - Test static file requests are skipped
   - Test admin-only endpoint enforces permissions

File structure:
- core/middleware/audit_middleware.py (new)
- core/models/audit_log.py (new)
- core/migrations/XXXX_add_audit_log.py (new)
- core/admin.py (update)
- core/tests/test_audit_middleware.py (new)
- forwardlane/settings/base.py (update MIDDLEWARE)
```

## Acceptance Criteria
- [ ] Every authenticated API request creates an AuditLog row
- [ ] AuditLog table is append-only (no UPDATE/DELETE in admin or code)
- [ ] Admin view allows filtering by tenant/user/date
- [ ] Compliance export API endpoint works (admin only)
- [ ] Tests pass with 80%+ coverage for the middleware
- [ ] Health/metrics endpoints are excluded from audit log

## Dependencies
None — can run independently.
