# NR-006 Done — LinkedIn OAuth2 PKCE Flow

**Completed:** 2026-03-13  
**Priority:** P1/S  
**Commit:** `22fe94d` on `main` (TrendpilotAI/NarrativeReactor)

## What Was Implemented

### New Service: `src/services/linkedin.ts`

**PKCE Helpers:**
- `generateCodeVerifier()` — cryptographically random 48-byte base64url string (64 chars)
- `generateCodeChallenge(verifier)` — SHA-256 of verifier, base64url-encoded (S256 method)

**OAuth2 Flow:**
- `generateAuthorizationUrl(tenantId)` — builds LinkedIn OAuth2 URL with PKCE, stores `code_verifier` + `state` in `linkedin_pkce_state` table (10-min TTL). Returns `{ authorizationUrl, state }`.
- `handleLinkedInCallback(code, state)` — validates state, consumes PKCE record (one-time use), exchanges authorization code for tokens, fetches userinfo from `/v2/userinfo`, stores encrypted credentials.

**Token Storage:**
- `persistTokens()` — encrypts `access_token` and `refresh_token` using AES-256-GCM with IV + auth tag prepended. Key derived from `TOKEN_ENCRYPTION_KEY` env var (64-hex) or falls back to `API_KEY` (development only).
- `getLinkedInCredentials(tenantId)` — decrypts and returns tokens.
- `hasValidLinkedInCredentials(tenantId)` — expiry check.
- `revokeLinkedInCredentials(tenantId)` — removes from DB.

**Schema:**
- `linkedin_credentials` table: `tenant_id` (PK), `access_token_enc`, `refresh_token_enc`, `expires_at`, `linkedin_member_id`, `linkedin_name`, `linkedin_email`.
- `linkedin_pkce_state` table: ephemeral PKCE state with 10-min expiry, auto-purged on each auth call.

### New Routes: `src/routes/linkedin.ts`

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /api/linkedin/auth` | Tenant API key | Returns `{ authorization_url, state }` |
| `GET /api/linkedin/callback` | None (public redirect) | Exchanges code, stores tokens, redirects to `/settings/integrations` or returns JSON |
| `GET /api/linkedin/status` | Tenant API key | Returns connection status, validity, expiry, member info |
| `DELETE /api/linkedin/disconnect` | Tenant API key | Revokes credentials |

### Wired in `src/index.ts`
- `app.use('/api/linkedin', linkedInRouter)` — mounted after billing routes.

### `.env.example`
```env
# LinkedIn OAuth2 — required for NR-006 native publishing authorization
# Create an app at https://www.linkedin.com/developers/apps
# LINKEDIN_CLIENT_ID=
# LINKEDIN_CLIENT_SECRET=
```

### Tests: `src/__tests__/services/linkedin.test.ts`
- 22 tests covering:
  - `generateCodeVerifier`: length, uniqueness, URL-safe chars
  - `generateCodeChallenge`: deterministic, unique, S256 correctness (known-value test)
  - `generateAuthorizationUrl`: valid URL, scopes, PKCE state storage, expiry
  - `handleLinkedInCallback`: invalid state, successful exchange + encrypted storage, token endpoint failure, state reuse prevention
  - `getLinkedInCredentials`: null for missing, encryption (raw DB ≠ plaintext, decrypted = plaintext)
  - `hasValidLinkedInCredentials`: missing / valid / expired
  - `revokeLinkedInCredentials`: removes from DB, no-op on missing
- All 22 tests pass ✅

## Security Notes
- `code_verifier` is server-side only — never sent to client
- State is single-use (deleted on callback)
- Tokens stored encrypted with AES-256-GCM (authenticated encryption)
- `TOKEN_ENCRYPTION_KEY` must be set in production (64-hex char env var)
- LinkedIn scopes: `openid profile email w_member_social`
