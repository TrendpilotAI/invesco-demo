# TODO-605: Password Reset / Change Routes

**Repo:** signal-studio-auth  
**Priority:** P1 (HIGH)  
**Effort:** 2h  
**Status:** pending

## Problem
No password reset or change endpoints. Users cannot self-service password recovery. Blocks production deployment for new signups.

Note: TODO-354 (older) covered this but may not have been implemented. Check and complete.

## Fix

### `POST /auth/reset-password` (unauthenticated)
```python
class PasswordResetRequest(BaseModel):
    email: EmailStr

@router.post("/reset-password")
async def reset_password(body: PasswordResetRequest, request: Request):
    """Trigger Supabase password reset email."""
    client = request.app.state.http_client
    resp = await client.post(
        f"{SUPABASE_URL}/auth/v1/recover",
        json={"email": body.email},
        headers={"apikey": SUPABASE_SERVICE_KEY},
    )
    # Always return 200 to avoid email enumeration
    return {"message": "If an account exists, a reset email has been sent."}
```

### `POST /auth/update-password` (authenticated)
```python
class PasswordUpdateRequest(BaseModel):
    new_password: str

@router.post("/update-password")
async def update_password(body: PasswordUpdateRequest, request: Request):
    """Authenticated user changes their password."""
    user = getattr(request.state, "user", None)
    if not user or not user.is_authenticated:
        raise HTTPException(401, "Authentication required")
    
    client = request.app.state.http_client
    resp = await client.put(
        f"{SUPABASE_URL}/auth/v1/user",
        json={"password": body.new_password},
        headers={
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {user.access_token}",
        },
    )
    if resp.status_code != 200:
        raise HTTPException(400, "Password update failed")
    return {"message": "Password updated successfully"}
```

## Files to Modify
- `routes/auth_routes.py` — add both endpoints

## Acceptance Criteria
- [ ] `POST /auth/reset-password` triggers Supabase recovery email
- [ ] `POST /auth/reset-password` never reveals if email exists (always 200)
- [ ] `POST /auth/update-password` requires valid auth token
- [ ] Password update validated (min length 8, etc.)
- [ ] Audit event logged for password change (TODO-604)
- [ ] Tests for both endpoints

## Dependencies
- TODO-600 (httpx pooling)
- TODO-604 (audit logging)
