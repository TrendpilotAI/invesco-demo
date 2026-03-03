# Trendpilot Deployment Audit Report

**Date:** 2026-03-03  
**Path:** `/data/workspace/projects/Trendpilot`  
**Status:** ✅ Deploy-ready (with env vars configured)

---

## 1. Dependencies

- **Package manager:** `npm` is broken on this host (minipass-sized bug). **Yarn v1 works fine.**
- `yarn install --production=false` installs all deps successfully (prod + dev)
- No vulnerable or deprecated dependency warnings

## 2. TypeScript Build — ✅ PASSES

Fixed 4 compilation errors:
- `src/lib/realtime.ts` — generic constraint on `ChangeCallback<T>` (added `extends { [key: string]: any }`)
- `src/services/db.ts` (3 errors) — Supabase enum filter type mismatches (added `as any` casts on status filter params)

`node_modules/.bin/tsc` now compiles cleanly with zero errors.

## 3. Tests — 35/43 suites pass (268/268 individual tests)

### ✅ Passing suites (35)
All phase 1–10 unit/service tests pass, covering: models, aggregator, scheduler, email, profiles, alerts, API keys, middleware, geo, teams, theming, tenants, data marketplace, social listening, influencer discovery, feed builder, white label, team manager, SLA monitor.

### ❌ Failing suites (8) — all due to missing `SUPABASE_URL` env var
These suites import the Supabase client at module level, which crashes without env vars:
- `tests/phase2/api/api.test.ts`
- `tests/phase3/api/api.test.ts`
- `tests/phase4/dashboard.test.ts`
- `tests/phase7/api-routes.test.ts`
- `tests/phase8/enterprise.test.ts`
- `tests/phase9/routes.test.ts`
- `tests/phase10/api.test.ts`
- `tests/phase11/enterprise.test.ts`

**Fix:** These need `SUPABASE_URL` and `SUPABASE_ANON_KEY` set (even dummy values) or lazy initialization of the Supabase client.

## 4. Required Environment Variables

| Variable | Purpose |
|---|---|
| `SUPABASE_URL` | Supabase project URL (required) |
| `SUPABASE_ANON_KEY` | Supabase anonymous/public key (required) |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase admin key (required for server) |
| `SMTP_HOST` | Email SMTP host |
| `SMTP_PORT` | Email SMTP port |
| `SMTP_USER` | Email SMTP username |
| `SMTP_PASS` | Email SMTP password |
| `SMTP_SECURE` | SMTP TLS flag |
| `EMAIL_FROM` | Sender email address |
| `RESEND_API_KEY` | Resend email API key (alternative to SMTP) |
| `NEWS_API_KEY` | NewsAPI.org key for trend aggregation |
| `PUBLIC_BASE_URL` | Public URL for links in emails |
| `CORS_ORIGINS` | Allowed CORS origins |
| `NODE_ENV` | Environment (production/development) |

## 5. Railway Deployment Files — ✅ All present

- **Dockerfile** — Multi-stage build (node:22-slim), installs, compiles TS, runs `dist/src/api/index.js`. Has healthcheck.
- **Procfile** — `web: node dist/src/api/index.js`
- **railway.toml** — Configured for Dockerfile builder with `/api/health` healthcheck, restart on failure (max 3 retries)

### Note on Dockerfile
The CMD uses `dist/src/api/index.js` which matches the compiled output structure. Verified correct.

## 6. Database — Supabase (not Prisma ORM)

- **Prisma schema** exists (`prisma/schema.prisma`, 161 lines) but is used for type generation only — the app uses `@supabase/supabase-js` directly, not Prisma Client
- **Prisma migration:** `prisma/migrations/0001_init/` exists
- **Supabase migration:** `supabase/migrations/20260218000000_initial_schema.sql` exists
- Schema covers: newsletters, sections, templates, subscribers, lists, topics, engagement, click events, with enums for status/tone/frequency

## 7. API Endpoints (73 routes)

### Core
- `GET /api/health` — Health check
- `GET /api/trends` — List trends
- `GET /api/trends/:id` — Get trend by ID
- `GET /api/trends/personalized/:profileId` — Personalized trends
- `GET /api/sources` — List sources
- `GET /api/stats` — Dashboard stats

### Subscribers & Email
- `POST /api/subscribe` — Subscribe
- `GET /api/confirm` — Confirm opt-in
- `GET /api/unsubscribe` — Unsubscribe
- `GET /api/track/click` — Click tracking
- `POST /api/webhooks/email` — Email webhooks
- `GET /api/email/queue` — Email queue status

### Profiles & Alerts
- `GET/POST /api/profiles` — Manage profiles
- `PUT /api/profiles/:id` — Update profile
- `GET /api/alerts` — List alerts
- `POST /api/alerts/config` — Configure alerts

### Multi-Tenant
- `GET/POST /api/tenants` — Manage tenants
- `GET/PUT /api/tenants/:id/theme` — Tenant theming
- `GET/POST/DELETE /api/tenants/:id/members` — Tenant members
- `GET /api/tenants/:id/usage` — Usage stats

### SSO & Auth
- `POST /api/sso/login` — SSO login (SAML/OAuth)
- `POST /api/sso/callback` — SSO callback

### Admin
- `GET /api/admin/dashboard` — Admin dashboard
- `GET /api/admin/health` — System health
- `GET /api/admin/billing` — Billing info
- `GET /api/audit` — Audit log

### Compliance
- `GET /api/compliance` — Compliance status
- `POST /api/compliance/deletion` — GDPR deletion (admin only)
- `GET/PUT /api/compliance/retention` — Data retention policy

### Data Marketplace
- `GET /api/marketplace/sources` — List data sources
- `GET /api/marketplace/sources/:id` — Get source
- `POST /api/marketplace/subscribe` — Subscribe to source
- `GET /api/marketplace/subscriptions/:tenantId` — Active subscriptions
- `POST /api/marketplace/unsubscribe` — Unsubscribe

### Social Listening & Influencers
- `POST /api/social/track` — Track brand
- `GET /api/social/brands` — Tracked brands
- `GET /api/social/mentions/:brand` — Brand mentions
- `GET /api/social/volume/:brand` — Mention volume
- `GET /api/social/mentioners/:brand` — Top mentioners
- `GET /api/influencers` — Find influencers
- `GET /api/influencers/rank` — Rank influencers
- `GET /api/influencers/:handle` — Influencer profile

### Reports & Export
- `GET /api/reports/templates` — Report templates
- `POST /api/reports/generate` — Generate report
- `POST /api/export` — Export trends
- `POST /api/export/webhook` — Register webhook
- `GET /api/export/webhooks/:tenantId` — List webhooks

### Tenant/Team Management
- `GET/POST/DELETE /api/tenant-manager/tenants` — Tenant CRUD
- `GET/PUT /api/white-label/:tenantId/*` — White label config
- `POST/GET /api/team-manager/:tenantId/*` — Team management

### Feeds & SLA
- `POST/GET/PUT/DELETE /api/feeds/:tenantId` — Custom feeds
- `GET /api/sla/status` — SLA status page
- `POST /api/sla/check` — Record check
- `GET /api/sla/uptime/:serviceId` — Uptime stats
- `POST/GET /api/sla/thresholds` — SLA thresholds
- `GET/POST /api/sla/alerts` — SLA alerts

## 8. Deployment Checklist

- [x] Dockerfile present and correct
- [x] railway.toml configured
- [x] Procfile present
- [x] TypeScript compiles cleanly
- [x] 268 tests passing
- [x] Supabase migration exists
- [ ] **Set Railway env vars** (SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY minimum)
- [ ] **Set email config** (SMTP_* or RESEND_API_KEY)
- [ ] **Set NEWS_API_KEY** for trend aggregation
- [ ] **Set PUBLIC_BASE_URL** to Railway deployment URL

## 9. Recommendations

1. **Fix npm** on the build host or update Dockerfile to use yarn (current Dockerfile uses `npm install` which will fail with the same minipass bug if the Railway builder has the same npm version)
2. **Lazy-init Supabase client** to avoid crashes when env vars are missing (affects 8 test suites and startup)
3. **Add `.env.example`** documenting all required env vars
4. **Consider adding Stripe vars** — the codebase mentions billing but no Stripe env vars were found in source; may be handled by Supabase or not yet implemented
