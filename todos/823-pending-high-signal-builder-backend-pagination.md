# TODO-823: Add Pagination to All List Endpoints

**Repo**: signal-builder-backend  
**Priority**: HIGH  
**Effort**: Medium (4-8 hours)

## Problem
List endpoints likely return full result sets — risk of OOM for large organizations.

## Task
1. Identify all GET list endpoints in `apps/*/routers/*.py`
2. For each: add query params `limit: int = Query(50, le=1000)` and `offset: int = Query(0, ge=0)`
3. Update corresponding storage methods to accept `limit` and `offset`
4. Return paginated response: `{"items": [...], "total": N, "limit": N, "offset": N}`
5. Priority endpoints: GET /signals/, GET /signal-results/, GET /audit-logs/

## Acceptance Criteria
- All list endpoints accept limit/offset params
- Total count returned in response
- Default limit=50 to prevent large fetches
- Existing client behavior preserved (test with existing tests)
