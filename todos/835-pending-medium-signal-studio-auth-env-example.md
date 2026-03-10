# TODO-835: Create .env.example File

**Repo:** signal-studio-auth
**Priority:** P2 (Medium)
**Effort:** 15 minutes
**Status:** pending
**Dependencies:** TODO-834 (startup validation — documents which vars are required)
**Created:** 2026-03-10

## Problem

No `.env.example` exists. New developers have no reference for required environment variables. They must read `config/supabase_config.py` and `config/redis_config.py` to discover what's needed.

## Files to Create

- `.env.example` at repo root

## Coding Prompt

```
Create /data/workspace/projects/signal-studio-auth/.env.example with:

# signal-studio-auth — Environment Variables
# Copy to .env and fill in values

# ── Required ────────────────────────────────────────────
# Supabase project settings (from Settings → API in Supabase dashboard)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=eyJ...your-service-role-key
SUPABASE_JWT_SECRET=your-jwt-secret-from-supabase-settings

# Legacy ForwardLane JWT secret (must be ≥32 chars, cryptographically random)
AUTH_SECRET_KEY=generate-a-random-string-at-least-32-chars

# ── Optional ────────────────────────────────────────────
# Redis URL for cross-replica rate limiting + refresh token storage
# Falls back to in-memory if not set (not safe for multi-replica)
REDIS_URL=redis://localhost:6379/0

# Auth mode: "supabase" | "forwardlane" | "dual" (default: dual)
AUTH_MODE=dual

# ForwardLane backend URL (only needed in forwardlane/dual mode)
FORWARDLANE_API_URL=http://localhost:8000

# CORS allowed origins (comma-separated, for TODO-826)
# ALLOWED_ORIGINS=http://localhost:3000,https://signal-studio.example.com

# Trusted proxy IPs for X-Forwarded-For validation (comma-separated, for TODO-838)
# TRUSTED_PROXY_IPS=10.0.0.0/8,172.16.0.0/12

Also add .env to .gitignore if not already present:
echo ".env" >> /data/workspace/projects/signal-studio-auth/.gitignore
```

## Acceptance Criteria

- [ ] `.env.example` exists with all env vars documented
- [ ] Required vs optional clearly marked
- [ ] `.env` is in `.gitignore`
- [ ] A new developer can configure the app from `.env.example` alone
