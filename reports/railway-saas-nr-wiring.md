# Railway SaaS Template + NarrativeReactor Wiring — Summary

**Date:** 2026-02-18
**Commits:**
- `railway-saas-template`: `7ddee04` → pushed to TrendpilotAI/railway-saas-template
- `NarrativeReactor`: `ebb5464` → pushed to TrendpilotAI/NarrativeReactor

---

## Part 1: Railway SaaS Template

### Security Fixes
- **Next.js upgraded** from 14.2.35 → 15.5.12
- **npm audit**: 0 vulnerabilities (was 2 high + 1 moderate)
- Middleware rewritten for Next.js 15 compatibility
- Added proper 404 and 500 error pages

### OpenClaw Integration
- **`/api/ai/chat`** — POST endpoint that proxies to OpenClaw (OpenAI-compatible API)
  - Rate limited: 20 req/min per user
  - Auth required (session-based)
  - Env vars: `OPENCLAW_API_KEY`, `OPENCLAW_API_URL`, `OPENCLAW_MODEL`
- **`ChatWidget`** — Floating chat bubble component in bottom-right corner
  - Conversation UI with user/assistant messages
  - Auto-renders on all pages via layout
- **README** updated with OpenClaw section and env var docs

### Production Improvements
- **Email templates** (`src/lib/email-templates.ts`):
  - Welcome email with onboarding checklist
  - Invoice/payment receipt with plan details
  - Password reset with expiring link
  - Usage limit alert with upgrade CTA
- **Usage analytics** (`src/lib/analytics.ts`):
  - `trackUsage()` — daily per-endpoint counters via Prisma upsert
  - `getUserUsage()` — user usage summary with daily breakdown
  - `getAdminAnalytics()` — platform-wide metrics (total users, new users, daily API calls)
- **Rate limiting middleware** (`src/lib/rate-limit.ts`):
  - Reusable `checkRateLimit()` helper for API routes
  - IP-based, configurable limit/window, proper 429 response headers

### README
- Railway deploy button with referral link ✅ (was already present)
- OpenClaw integration docs added
- Env var table updated with OpenClaw vars

---

## Part 2: NarrativeReactor Dashboard Wiring

### Dashboard (Vite + React + React Router)
Built a full single-page dashboard wired to the existing Express API on port 3401.

**Pages:**
1. **Generate** (`/`) — Content pipeline UI: enter topic + context, generate multi-format drafts (X thread, LinkedIn post, blog article). Toggle Claude vs Gemini.
2. **Drafts** (`/drafts`) — List all drafts with status filtering (all/draft/approved/rejected/published). Click to view detail.
3. **Draft Detail** (`/drafts/:id`) — View/edit content per format, approve/reject with feedback, publish to selected platforms via Blotato.
4. **Quick Publish** (`/publish`) — Direct cross-platform publishing (no draft needed). Select platforms, paste content, publish.
5. **Queue** (`/queue`) — View Blotato publishing queue, cancel scheduled posts.

**API Client** (`src/api.ts`):
Wired to all pipeline endpoints:
- `POST /api/pipeline/generate` — full pipeline
- `POST /api/pipeline/research` — research only
- `GET /api/pipeline/drafts` — list drafts
- `GET/POST /api/pipeline/drafts/:id/*` — CRUD + approve/reject
- `POST /api/pipeline/publish` — publish draft via Blotato
- `POST /api/pipeline/publish/direct` — direct publish
- `GET/DELETE /api/pipeline/queue` — queue management
- `GET /api/pipeline/accounts` — connected Blotato accounts

**Dev Setup:**
- Dashboard runs on port 3403 (`npx vite`)
- Vite proxy forwards `/api/*` to NR API on port 3401
- Environment: `VITE_API_URL` and `VITE_API_KEY` for production

**Build:** Clean TypeScript compilation, Vite production build passes (241KB gzipped).

---

## Flow: Pipeline → Dashboard → Publish

```
1. User enters topic in Dashboard Generate page
2. Dashboard POSTs to /api/pipeline/generate
3. NR runs: research → 3 AI-generated formats (parallel)
4. Draft appears in Drafts list
5. User reviews/edits content in Draft Detail
6. User approves draft
7. User selects platforms + clicks Publish
8. Dashboard POSTs to /api/pipeline/publish
9. Blotato API publishes to X, LinkedIn, etc.
10. Draft status → published, appears in Queue
```
