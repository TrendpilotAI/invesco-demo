# 805 — Add Social OAuth Endpoints (Google, GitHub)

**Repo:** signal-studio-auth  
**Priority:** P1 (revenue impact — reduces signup friction)  
**Effort:** M (1-2 days)  
**Dependencies:** 801 (CORS)

## Acceptance Criteria

- [ ] `GET /auth/oauth/{provider}` — initiates OAuth flow, returns Supabase redirect URL
- [ ] `POST /auth/oauth/callback` — handles OAuth callback, wraps tokens with opaque refresh token
- [ ] Supports providers: `google`, `github`
- [ ] Refresh tokens wrapped in same opaque UUID pattern as password auth
- [ ] Tests cover the callback flow with mocked Supabase response

## Coding Prompt

```
Add OAuth endpoints to /data/workspace/projects/signal-studio-auth/routes/auth_routes.py:

@router.get("/oauth/{provider}")
async def oauth_init(provider: str, request: Request):
    """Return the Supabase OAuth URL for the given provider."""
    if provider not in ("google", "github", "linkedin"):
        raise HTTPException(400, f"Unsupported provider: {provider}")
    
    redirect_to = request.query_params.get("redirect_to", SUPABASE_URL)
    # Return the Supabase OAuth URL — frontend redirects the user there
    return {
        "url": f"{SUPABASE_URL}/auth/v1/authorize?provider={provider}&redirect_to={redirect_to}"
    }

@router.post("/oauth/callback")
async def oauth_callback(request: Request):
    """
    Exchange an OAuth code for tokens.
    Supabase handles the actual exchange; we just wrap the refresh token.
    The frontend should POST the code + code_verifier here.
    """
    body = await request.json()
    code = body.get("code")
    if not code:
        raise HTTPException(400, "Missing code")
    
    async with _http_client(request) as client:
        resp = await client.post(
            f"{SUPABASE_URL}/auth/v1/token?grant_type=pkce",
            headers=_supabase_headers(),
            json={"auth_code": code, "code_verifier": body.get("code_verifier", "")},
        )
    if resp.status_code >= 400:
        raise HTTPException(resp.status_code, resp.json())
    return _wrap_with_opaque_token(resp.json())

Add tests in tests/test_auth.py for the OAuth endpoints.
```
