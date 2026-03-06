# 809 — Add Admin User Management Endpoints

**Repo:** signal-studio-auth  
**Priority:** P2  
**Effort:** M (1 day)  
**Dependencies:** 808 (org CRUD), 801 (CORS)

## Acceptance Criteria

- [ ] `GET /auth/admin/users` — list users in caller's org (admin only)
- [ ] `PATCH /auth/admin/users/{user_id}` — update user role (admin only)
- [ ] `DELETE /auth/admin/users/{user_id}` — deactivate user (admin only)
- [ ] All endpoints require `admin` role
- [ ] Pagination on list endpoint (`limit`, `offset`)

## Coding Prompt

```
Add admin user management routes to auth_routes.py or a new admin_routes.py:

@router.get("/admin/users", dependencies=[Depends(require_role("admin"))])
async def list_users(request: Request, limit: int = 50, offset: int = 0):
    """List users in the caller's organization."""
    org_id = _get_caller_org_id(request)
    async with _http_client(request) as client:
        resp = await client.get(
            f"{SUPABASE_URL}/auth/v1/admin/users",
            headers=_supabase_headers(service=True),
            params={"page": offset // limit + 1, "per_page": limit},
        )
    # Filter by org_id from app_metadata
    ...

@router.patch("/admin/users/{user_id}", dependencies=[Depends(require_role("admin"))])
async def update_user_role(user_id: str, body: dict, request: Request):
    new_role = body.get("role")
    if new_role not in ("viewer", "editor", "admin"):
        raise HTTPException(422, "Invalid role")
    # PATCH to Supabase admin API
    ...

@router.delete("/admin/users/{user_id}", dependencies=[Depends(require_role("admin"))])
async def deactivate_user(user_id: str, request: Request):
    # Set banned=true on the user via Supabase admin API
    ...
```
