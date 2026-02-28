# TODO-223: Password Reset Routes (signal-studio-auth)

**Priority:** HIGH  
**Repo:** signal-studio-auth  
**Status:** pending  

## Description
No password reset flow exists. The auth module is incomplete without forgot-password / reset-password routes.

## Task
Add two routes:
- `POST /auth/forgot-password` — sends reset email via Supabase
- `POST /auth/reset-password` — sets new password with recovery token

## Coding Prompt
```
In /data/workspace/projects/signal-studio-auth/routes/auth_routes.py:

1. Add Pydantic schemas:
   class ForgotPasswordRequest(BaseModel):
       email: EmailStr
   
   class ResetPasswordRequest(BaseModel):
       access_token: str  # from the reset email link
       new_password: str

2. Add route POST /auth/forgot-password:
   - Proxy to POST {SUPABASE_URL}/auth/v1/recover
   - Body: {"email": body.email}
   - Return 200 regardless (don't reveal if email exists)

3. Add route POST /auth/reset-password:
   - Proxy to PUT {SUPABASE_URL}/auth/v1/user
   - Headers: Authorization: Bearer {body.access_token}
   - Body: {"password": body.new_password}
   - Validate password length >= 8 chars

4. Add tests for both routes in tests/test_auth.py
   (mock httpx responses)

5. Document in MIGRATION_GUIDE.md
```

## Estimated Effort
S (2 hours)

## Acceptance Criteria
- Forgot password triggers Supabase reset email
- Reset password updates user password
- Tests pass
