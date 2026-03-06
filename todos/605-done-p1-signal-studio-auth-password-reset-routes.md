# TODO-605: Password Reset / Change Routes — DONE ✅

**Completed:** 2026-03-06  
**Commit:** a17b702  
**Branch:** master → TrendpilotAI/signal-studio-auth

## What Was Done

### New Endpoints
- **`POST /auth/reset-password`** (unauthenticated)
  - Accepts `{ "email": "..." }` (validated as EmailStr)
  - Calls Supabase `/auth/v1/recover`
  - Always returns HTTP 200 — prevents email enumeration
  - Swallows Supabase errors silently (logs warnings)

- **`POST /auth/update-password`** (requires auth)
  - Accepts `{ "new_password": "..." }`
  - Returns 401 if unauthenticated
  - Returns 422 if password < 8 characters
  - Calls Supabase `PUT /auth/v1/user` with Bearer token
  - Returns 400 on Supabase failure
  - Logs password change with user sub

### New Schemas
- `PasswordResetRequest` — EmailStr field
- `PasswordUpdateRequest` — new_password str field

### Tests
- `tests/test_password_reset.py` — 13 tests covering:
  - Both endpoints happy paths
  - Email validation / missing fields
  - Enumeration protection (always 200)
  - Network error resilience
  - Auth enforcement
  - Password length validation (min 8)
  - Supabase failure → 400
  - Correct Supabase URLs and payloads verified

### Test Results
- **90/90 tests pass** (0 failures, 1 pre-existing warning)

## Notes
- No audit infrastructure found (TODO-604 not yet implemented) — logged via `logger.info` instead
- Follows existing patterns: `_http_client`, `_supabase_headers`, `_extract_token`
