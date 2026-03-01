# TODO 353 — Fix Admin Role Check on invite-to-org
**Repo:** signal-studio-auth
**Priority:** HIGH
**Effort:** 1 hour
**Status:** pending

## Description
`/auth/invite-to-org` only checks `is_authenticated` but not role. Any authenticated user
(even a viewer) can invite anyone to any organization.

## Coding Prompt
In `/data/workspace/projects/signal-studio-auth/routes/auth_routes.py`:

1. Add RBAC check to `invite_to_org`:
```python
@router.post("/invite-to-org")
async def invite_to_org(body: InviteRequest, request: Request):
    caller = getattr(request.state, "user", None)
    if not caller or not caller.is_authenticated:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # NEW: Check admin role
    caller_role = getattr(caller, "role", None)
    # Also check supabase_claims if available
    if caller_role is None:
        claims = getattr(request.state, "supabase_claims", {})
        caller_role = claims.get("app_metadata", {}).get("role")
    
    if caller_role not in ("admin", "owner", "super_admin"):
        raise HTTPException(status_code=403, detail="Admin role required to invite users")
    ...
```

2. Also ensure org isolation: caller can only invite to their own org:
```python
    caller_org_id = getattr(caller.organization, "id", None)
    if caller_org_id and body.organization_id != caller_org_id:
        raise HTTPException(status_code=403, detail="Cannot invite to a different organization")
```

3. Add `role` field to `User` model in `middleware/_compat.py`:
```python
class User(BaseModel):
    ...
    role: str = "viewer"
```

4. Expose `role` from `supabase_claims_to_user_dict` in `mapping/user_mapping.py`.

5. Add test cases for non-admin invite attempt (should return 403).

## Acceptance Criteria
- [ ] Non-admin users get 403 when calling invite-to-org
- [ ] Admin users can successfully invite
- [ ] Cross-org invite attempts are blocked
- [ ] Tests cover all three cases
