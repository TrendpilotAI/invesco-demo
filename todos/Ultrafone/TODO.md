# Ultrafone — TODO
*Judge scored: 2026-03-14 | Composite: 6.1/10*

## 🚨 CRITICAL (Do Before Anything Else)

- [ ] **Rotate ALL exposed API keys** — Groq, Deepgram, Twilio, Fish Audio keys committed in `backend/.env.development` git history. Check billing for unauthorized usage.
- [ ] **Purge git history** — Run `git filter-repo --path backend/.env.development --invert-paths` + force push. The file was removed from tracking (commit `2b29d25`) but history still contains plaintext keys.
- [ ] **Add rate limiting to webhook endpoints** — No `slowapi` or similar. Each POST to `/twilio/voice` triggers Groq+Deepgram API calls = cost amplification attack vector. Target: 10 req/min per IP, 5 req/min per phone.

## 🔴 P0 — Security & Deployment

- [ ] **Verify Twilio webhook signature validation works in prod** — Added in commit `22d914c`, confirm it's active on all routes, not bypassed.
- [ ] **Deploy to Railway** — `railway.toml` + `nixpacks.toml` exist. Need: provision Postgres + Redis add-ons, set env vars, wire Twilio webhook URL.
- [ ] **Set up health monitoring** — `/health/ready` endpoint exists. Wire UptimeRobot or Railway health checks.
- [ ] **Install pre-commit secret scanning** — `gitleaks` or `git-secrets` hook to prevent future leaks.

## 🟡 P1 — SaaS Foundation

- [ ] **Fix 5x hardcoded `user_id="nathan"`** in `backend/services/receptionist.py` (lines ~171, 276, 374, 424, 512). Route Twilio `To` number → `UserProfile` DB lookup. This blocks ALL multi-tenant/SaaS work.
- [ ] **Consolidate 3 TTS services** — `fish_tts.py`, `elevenlabs_tts.py`, `voice_service.py` overlap. Create unified `TTSProvider` ABC. Remove duplicate `elevenlabs>=1.0.0` from `requirements.txt`.
- [ ] **Complete security analyzer DB lookup** — `backend/processors/security_analyzer.py` lines 224-226 have TODO stubs. Caller history not actually queried.
- [ ] **Audit `icloud_contacts.py`** — iCloud has no public API. Likely a stub/placeholder. Mark as unsupported or implement CardDAV.

## 🟢 P2 — Features & Growth

- [ ] **Google Calendar integration** — OAuth2 flow (pattern exists in `google_contacts.py`). Feed schedule to LLM context for aware responses.
- [ ] **Complete HubSpot integration** — `hubspot_contacts.py` exists but incomplete. Auto-create leads, push call summaries.
- [ ] **SMS summary after calls** — Twilio SMS to Nathan with caller name, category, summary, action taken.
- [ ] **Zapier webhook bridge** — Fire signed events (`call.completed`, `lead.created`) for 5,000+ integration ecosystem.
- [ ] **Android app** — Flutter is cross-platform already. Rename `ios-app/` → `mobile-app/`, add FCM push, submit to Google Play.

## 🔵 P3 — Code Quality & Testing

- [ ] **Add E2E test suite** — No test exercises full Twilio→Backend→Groq→Response chain. Mock Twilio webhooks for CI.
- [ ] **Connection pooling** — Groq client created per call in `receptionist.py`. Redis client may not use `ConnectionPool`. Agent service creates new WebSocket per call.
- [ ] **CI/CD pipeline** — GitHub Actions: lint → test → deploy on merge to main. Add Dependabot.
- [ ] **Pydantic settings consolidation** — Config scattered across `config/` and `.env`. Move to `pydantic-settings` `BaseSettings` with startup validation.
- [ ] **Wire Sentry + PostHog** — Both in `requirements.txt` but not confirmed wired up properly.

## 📊 Scoring Breakdown

| Dimension | Score | Notes |
|-----------|-------|-------|
| Security | 3/10 | Keys partially remediated, history unpurged, no rate limiting |
| Code Quality | 6/10 | Good structure, DRY violations (TTS, hardcoded IDs) |
| Test Coverage | 6.5/10 | 20+ unit tests, 3 integration tests, no E2E |
| Documentation | 8/10 | Excellent: README, ARCHITECTURE, DEVELOPER, DEPLOYMENT, CHANGELOG |
| Architecture | 7/10 | Solid pipeline design, good separation of concerns |
| Deployment | 4/10 | Config ready but not live, zero users |
| Business Value | 7/10 | Clear SaaS model, defined pricing, strong product concept |
| **Composite** | **6.1/10** | |

## Notes
- 16K+ lines Python backend, well-organized into api/models/services/processors/utils
- React+TypeScript frontend with 7 pages, 10 components, WebSocket hooks
- Flutter iOS app with all screens built
- Supabase migrations present
- Last commit: Twilio webhook validation + consent announcement (Mar 11)
