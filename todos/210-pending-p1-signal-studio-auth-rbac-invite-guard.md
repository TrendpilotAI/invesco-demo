---
status: pending
priority: p1
issue_id: "210"
tags: [signal-studio-auth, security, rbac, fastapi]
dependencies: []
---

# 210 — signal-studio-auth: Add RBAC Role Guard on invite-to-org Endpoint

## Task
The `/auth/invite-to-org` endpoint only checks `is_authenticated` but NOT role. Any authenticated user can invite others to any org. Add a `require_role("admin")` FastAPI dependency that reads `request.state.user` app_metadata role claim.

## Coding Prompt
In `/data/workspace/projects/signal-studio-auth/routes/auth_routes.py`:

1. Add a new FastAPI dependency function `require_role(role: str)` that:
   - Reads `request.state.user` from the request
   - Checks if `user.is_authenticated` is True
   - Checks if `user` has a `role` attribute (or reads from `request.state.supabase_claims["app_metadata"]["role"]`)
   - Raises `HTTPException(403, "Insufficient permissions")` if role doesn't match
   - Returns the user if check passes

2. Update the `invite_to_org` route to use this dependency:
```python
@router.post("/invite-to-org")
async def invite_to_org(
    body: InviteRequest,
    request: Request,
    _: None = Depends(require_role("admin"))
):
```

3. Remove the existing manual `caller.is_authenticated` check from the route body (it's now handled by the dependency).

4. Add the `role` field to the `User` model in `/data/workspace/projects/signal-studio-auth/middleware/_compat.py`.

5. Update `supabase_claims_to_user_dict` in `/data/workspace/projects/signal-studio-auth/mapping/user_mapping.py` to include `role` from `app_metadata`.

6. Add tests in `/data/workspace/projects/signal-studio-auth/tests/test_auth.py` verifying:
   - Admin user can call invite-to-org successfully (mock Supabase response)
   - Non-admin user gets 403 Forbidden
   - Unauthenticated user gets 401 Unauthorized

## Files to Modify
- `/data/workspace/projects/signal-studio-auth/routes/auth_routes.py`
- `/data/workspace/projects/signal-studio-auth/middleware/_compat.py`
- `/data/workspace/projects/signal-studio-auth/mapping/user_mapping.py`
- `/data/workspace/projects/signal-studio-auth/tests/test_auth.py`

## Dependencies
None (foundational security fix)

## Effort
S (2 hours)

## Acceptance Criteria
- [ ] `require_role("admin")` dependency exists and is used on `/auth/invite-to-org`
- [ ] Non-admin authenticated user receives HTTP 403
- [ ] Unauthenticated request receives HTTP 401 (unchanged)
- [ ] Admin user successfully sends invite
- [ ] `User` model has `role: str` field populated from JWT claims
- [ ] Tests pass: `pytest tests/test_auth.py -v`
