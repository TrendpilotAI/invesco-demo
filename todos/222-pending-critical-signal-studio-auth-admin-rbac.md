# TODO-222: Fix Admin Role Check + Add RBAC Dependency (signal-studio-auth)

**Priority:** CRITICAL  
**Repo:** signal-studio-auth  
**Status:** pending  

## Description
`/auth/invite-to-org` checks `is_authenticated` but NOT `role == admin`.
Any authenticated user can invite anyone to any organization — a serious privilege escalation bug.
Additionally, there's no reusable RBAC dependency for other routes.

## Task
1. Fix the immediate privilege escalation in `invite_to_org`
2. Add a reusable `require_role()` FastAPI dependency

## Coding Prompt
```
In /data/workspace/projects/signal-studio-auth/:

1. Create routes/dependencies.py:
   from fastapi import Depends, HTTPException, Request
   
   def require_role(*roles: str):
       def dependency(request: Request):
           user = getattr(request.state, 'user', None)
           if not user or not user.is_authenticated:
               raise HTTPException(status_code=401, detail="Not authenticated")
           user_role = getattr(user, 'role', None)
           if user_role not in roles:
               raise HTTPException(status_code=403, detail=f"Required role: {roles}")
           return user
       return Depends(dependency)

2. Update routes/auth_routes.py invite_to_org:
   from routes.dependencies import require_role
   
   @router.post("/invite-to-org")
   async def invite_to_org(body: InviteRequest, request: Request, _=require_role("admin")):
       ...
       # Remove the manual caller check (now handled by dependency)

3. Update mapping/user_mapping.py:
   - Include 'role' in the returned dict from supabase_claims_to_user_dict
   - Map from app_metadata.role

4. Update middleware/_compat.py:
   - Add 'role' field to User compat class

5. Add tests for require_role dependency:
   - Test 403 when viewer tries to invite
   - Test 200 when admin invites
```

## Estimated Effort
S (2-3 hours)

## Acceptance Criteria
- Non-admin users receive 403 on /auth/invite-to-org
- require_role dependency is reusable across routes
- Tests cover both 403 and 200 paths
