# MASTER-TODO: Ultrafone
**Scored:** 2026-03-15 | **Composite:** 5.8/10 | **Tier:** 2

## Score Breakdown
| Dimension       | Score | Δ vs 3/14 | Notes |
|----------------|-------|-----------|-------|
| code_quality   | 6.0   | —         | DRY violations (3 TTS services, duplicate dep), 8x hardcoded user_id |
| test_coverage  | 6.5   | —         | 24 test files, good unit coverage, zero E2E, no TTS/calendar tests |
| security       | 2.5   | ▼0.5      | Keys STILL in git history (day +4), validator built but NOT wired to routes, rate limiter built but NOT applied |
| documentation  | 8.0   | —         | Excellent: README, ARCHITECTURE, DEVELOPER, DEPLOYMENT, CHANGELOG, BRAINSTORM, PLAN, AUDIT |
| architecture   | 7.0   | —         | Solid Pipecat pipeline, good separation, Supabase+Redis, multi-tenant design exists on paper |
| business_value | 7.0   | —         | Clear SaaS model, defined pricing, strong product concept, zero live users |
| **COMPOSITE**  | **5.8** | ▼0.3    | Security drag pulls overall score down |

## 🚨 CRITICAL FLAGS

### 1. LEAKED API KEYS — STILL IN GIT HISTORY (Day +4)
`backend/.env.development` was removed from tracking (commit `2b29d25`, Mar 11) but **git history still contains plaintext credentials**: Groq, Deepgram, Twilio auth token, Fish Audio, JWT secret, personal phone number. No evidence of `git-filter-repo` or BFG having run.

### 2. SECURITY MIDDLEWARE NOT APPLIED
- `twilio_validator.py` exists with `RequestValidator` logic — **NOT imported or used in any API route**
- `RateLimiter` class exists in `redis_service.py` — **NOT called from any API endpoint**
- Both were built but never wired up. The webhook endpoints remain unprotected.

---

## P0 — IMMEDIATE (Security Breach + Deployment Blockers)
- [ ] **Rotate ALL leaked API keys** — Groq, Deepgram, Twilio Auth Token, Fish Audio, JWT Secret. Check billing dashboards for unauthorized usage.
- [ ] **Purge git history** — `git filter-repo --path backend/.env.development --invert-paths` + force push. Current `.gitignore` covers future commits but history is exposed.
- [ ] **Wire `twilio_validator` into API routes** — Middleware exists in `backend/utils/twilio_validator.py` but is not applied to `/twilio/voice` or any webhook endpoint.
- [ ] **Wire `RateLimiter` into webhook routes** — `RateLimiter` class exists in `backend/services/redis_service.py` but is never called. Target: 10 req/min per IP, 5 req/min per phone.
- [ ] **Install pre-commit secret scanning** — No `.pre-commit-config.yaml` exists. Add gitleaks hook.

## P1 — This Sprint (Deployment + Foundation)
- [ ] **Deploy to Railway** — `railway.toml` + `nixpacks.toml` present. Provision Postgres + Redis, set env vars, wire Twilio webhook URL.
- [ ] **Fix 8x hardcoded `user_id="nathan"`** — 5 in `receptionist.py` (lines 171, 276, 374, 424, 512) + 3 in `agent_functions.py` (lines 206, 254, 301). Route Twilio `To` → `UserProfile` lookup. Blocks all SaaS/multi-tenant work.
- [ ] **Consolidate 3 TTS services** — `fish_tts.py`, `elevenlabs_tts.py`, `voice_service.py` overlap. Create unified `TTSProvider` ABC. Remove duplicate `elevenlabs>=1.0.0` from `requirements.txt`.
- [ ] **Complete security analyzer DB lookup** — `backend/processors/security_analyzer.py` lines 224-226 are TODO stubs.
- [ ] **Set up health monitoring** — `/health/ready` exists. Wire UptimeRobot or Railway health checks. Confirm Sentry DSN is configured.

## P2 — Next Sprint (Features & Growth)
- [ ] **Google Calendar integration** — OAuth2 flow, feed schedule to LLM context
- [ ] **Complete HubSpot integration** — `hubspot_contacts.py` exists but incomplete
- [ ] **SMS call summary** — Twilio SMS to Nathan after each call
- [ ] **Zapier webhook bridge** — Fire signed events for integration ecosystem
- [ ] **Android app** — Flutter is cross-platform, rename `ios-app/` → `mobile-app/`, add FCM
- [ ] **Audit `icloud_contacts.py`** — iCloud has no public API; likely stub

## P3 — Backlog (Quality & Scale)
- [ ] **E2E test suite** — No test covers full Twilio→Backend→Groq→Response chain
- [ ] **Connection pooling** — Groq client per-call, WebSocket per-call in agent_service.py
- [ ] **CI/CD pipeline** — GitHub Actions: lint → test → deploy on merge
- [ ] **Pydantic settings consolidation** — Scattered config across `config/` and `.env`
- [ ] **Wire Sentry + PostHog** — In requirements.txt, not confirmed active
- [ ] **iOS TestFlight beta** — App built, needs backend integration testing
- [ ] **Stripe billing** — Plans defined ($29/$79/$199), not implemented
