# TODO 354 — Add Password Reset / Forgot Password Routes
**Repo:** signal-studio-auth
**Priority:** HIGH
**Effort:** 2 hours
**Status:** pending

## Description
No password reset flow exists. This blocks production launch — users have no recovery path.

## Coding Prompt
In `/data/workspace/projects/signal-studio-auth/routes/auth_routes.py`:

1. Add schemas:
```python
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    redirect_to: str = ""

class UpdatePasswordRequest(BaseModel):
    password: str
    access_token: str  # from recovery email link
```

2. Add routes:
```python
@router.post("/forgot-password")
async def forgot_password(body: ForgotPasswordRequest):
    """Send password reset email via Supabase."""
    async with httpx.AsyncClient() as client:
        payload = {"email": body.email}
        if body.redirect_to:
            payload["redirect_to"] = body.redirect_to
        resp = await client.post(
            f"{SUPABASE_URL}/auth/v1/recover",
            headers=_supabase_headers(),
            json=payload,
        )
    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.json())
    return {"detail": "Password reset email sent"}


@router.post("/reset-password")
async def reset_password(body: UpdatePasswordRequest):
    """Update password using recovery token."""
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"{SUPABASE_URL}/auth/v1/user",
            headers=_supabase_headers(access_token=body.access_token),
            json={"password": body.password},
        )
    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.json())
    return {"detail": "Password updated successfully"}
```

3. Add tests in `tests/test_auth.py` for both routes (mock httpx).

## Acceptance Criteria
- [ ] POST /auth/forgot-password sends reset email via Supabase
- [ ] POST /auth/reset-password updates password with recovery token
- [ ] Both routes return meaningful error messages on failure
- [ ] Tests with mocked Supabase API responses pass
