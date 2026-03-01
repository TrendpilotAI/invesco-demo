# TODO 356 — Add RBAC require_role() FastAPI Dependency
**Repo:** signal-studio-auth
**Priority:** HIGH
**Effort:** 3 hours
**Status:** pending

## Description
No reusable RBAC mechanism exists. Role checks are duplicated ad-hoc (or missing).
A `require_role()` FastAPI dependency enables clean declarative access control.

## Coding Prompt
Create `/data/workspace/projects/signal-studio-auth/middleware/rbac.py`:

```python
"""
Role-Based Access Control (RBAC) FastAPI dependencies.

Usage:
    from middleware.rbac import require_role

    @router.get("/admin-only")
    async def admin_route(user=Depends(require_role("admin"))):
        ...

    @router.get("/analysts")
    async def analyst_route(user=Depends(require_role("analyst", "admin", "owner"))):
        ...
"""
from __future__ import annotations
from typing import Callable
from fastapi import Depends, HTTPException, Request, status


def _get_user_role(request: Request) -> str:
    """Extract role from request state. Checks User model, then raw Supabase claims."""
    user = getattr(request.state, "user", None)
    if user is None:
        return "anonymous"
    
    # Check User model attribute
    role = getattr(user, "role", None)
    if role:
        return role
    
    # Fall back to raw Supabase claims
    claims = getattr(request.state, "supabase_claims", {})
    return claims.get("app_metadata", {}).get("role", "viewer")


def require_role(*allowed_roles: str) -> Callable:
    """
    FastAPI dependency factory. Returns a dependency that checks
    the current user's role against allowed_roles.
    """
    def dependency(request: Request) -> str:
        if not getattr(getattr(request.state, "user", None), "is_authenticated", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        
        role = _get_user_role(request)
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' not permitted. Required: {list(allowed_roles)}",
            )
        return role
    
    return dependency


# Convenience dependencies
require_admin = require_role("admin", "owner", "super_admin")
require_analyst = require_role("analyst", "admin", "owner", "super_admin")
```

Then update `routes/auth_routes.py` to use it:
```python
from middleware.rbac import require_admin

@router.post("/invite-to-org")
async def invite_to_org(
    body: InviteRequest,
    request: Request,
    _role: str = Depends(require_admin),
):
    ...
```

Add tests in `tests/test_rbac.py` covering admin access, non-admin rejection, unauthenticated rejection.

## Acceptance Criteria
- [ ] `require_role()` factory works as FastAPI Depends
- [ ] Returns 401 for unauthenticated requests
- [ ] Returns 403 for wrong role
- [ ] Works with both Supabase claims and User model role attribute
- [ ] invite-to-org updated to use `require_admin`
- [ ] Tests cover all cases
