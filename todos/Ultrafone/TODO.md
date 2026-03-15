# Ultrafone — TODO
*Judge scored: 2026-03-15 | Composite: 5.8/10*

## 🚨 CRITICAL (Do Before Anything Else)

- [ ] **Rotate ALL exposed API keys** — Groq, Deepgram, Twilio, Fish Audio, JWT Secret committed in `backend/.env.development` git history. Check billing for unauthorized usage. **Day +4 unresolved.**
- [ ] **Purge git history** — Run `git filter-repo --path backend/.env.development --invert-paths` + force push. File removed from tracking (commit `2b29d25`) but history still contains plaintext keys.
- [ ] **Wire Twilio webhook validator to routes** — `backend/utils/twilio_validator.py` has full `RequestValidator` implementation but it is **not imported or called** in any `backend/api/routes/` file. Fake call injection is possible.
- [ ] **Wire rate limiter to webhook routes** — `RateLimiter` class exists in `backend/services/redis_service.py` with sliding window algo but is **never called** from API endpoints. Cost amplification attack vector remains open.
- [ ] **Install pre-commit secret scanning** — No `.pre-commit-config.yaml` exists anywhere in the repo.

## 🔴 P0 — Security & Deployment

- [ ] **Deploy to Railway** — `railway.toml` + `nixpacks.toml` exist. Need: provision Postgres + Redis add-ons, set env vars from rotated keys, wire Twilio webhook URL.
- [ ] **Set up health monitoring** — `/health/ready` endpoint exists. Wire UptimeRobot or Railway health checks + Sentry DSN.

## 🟡 P1 — SaaS Foundation

- [ ] **Fix 8x hardcoded `user_id="nathan"`** — 5 in `receptionist.py` (lines 171, 276, 374, 424, 512) + 3 in `agent_functions.py` (lines 206, 254, 301). Route Twilio `To` number → `UserProfile` DB lookup. Blocks ALL multi-tenant/SaaS work.
- [ ] **Consolidate 3 TTS services** — `fish_tts.py`, `elevenlabs_tts.py`, `voice_service.py` overlap. Create unified `TTSProvider` ABC. Remove duplicate `elevenlabs>=1.0.0` from `requirements.txt` (still present).
- [ ] **Complete security analyzer DB lookup** — `backend/processors/security_analyzer.py` lines 224-226 have TODO stubs. Caller history not actually queried.
- [ ] **Audit `icloud_contacts.py`** — iCloud has no public API. Likely a stub/placeholder. Mark as unsupported or remove.

## 🟢 P2 — Features & Growth

- [ ] **Google Calendar integration** — OAuth2 flow (pattern exists in `google_contacts.py`). Feed schedule to LLM context.
- [ ] **Complete HubSpot integration** — `hubspot_contacts.py` exists but incomplete. Auto-create leads, push call summaries.
- [ ] **SMS summary after calls** — Twilio SMS to Nathan with caller name, category, summary, action taken.
- [ ] **Zapier webhook bridge** — Fire signed events (`call.completed`, `lead.created`) for 5,000+ integration ecosystem.
- [ ] **Android app** — Flutter is cross-platform already. Rename `ios-app/` → `mobile-app/`, add FCM push, submit to Google Play.
- [ ] **Live call dashboard widget** — React component partially exists in `frontend/`.

## 🔵 P3 — Code Quality & Testing

- [ ] **Add E2E test suite** — No test exercises full Twilio→Backend→Groq→Response chain. Mock Twilio webhooks for CI.
- [ ] **Connection pooling** — Groq client created per call in `receptionist.py`. `agent_service.py` creates new WebSocket per call (~100-200ms cold start).
- [ ] **CI/CD pipeline** — GitHub Actions: lint → test → deploy on merge to main. Add Dependabot.
- [ ] **Pydantic settings consolidation** — Config scattered across `config/` and `.env`. Move to `pydantic-settings` `BaseSettings`.
- [ ] **Wire Sentry + PostHog** — Both in `requirements.txt` but not confirmed wired up.
- [ ] **iOS TestFlight + App Store submission pipeline**
- [ ] **Stripe billing integration** — Plans defined on paper ($29/$79/$199), zero implementation.

## 📊 Scoring Breakdown

| Dimension | Score | Notes |
|-----------|-------|-------|
| Security | 2.5/10 | Keys in git history (day +4), validator+limiter built but NOT wired, no pre-commit hooks |
| Code Quality | 6/10 | Good structure, DRY violations (3 TTS, 8x hardcoded ID, dup dep) |
| Test Coverage | 6.5/10 | 24 test files, good unit tests, 3 integration tests, zero E2E |
| Documentation | 8/10 | Excellent: README, ARCHITECTURE, DEVELOPER, DEPLOYMENT, CHANGELOG |
| Architecture | 7/10 | Solid pipeline design, good separation, multi-tenant planned |
| Business Value | 7/10 | Clear SaaS model, strong product concept, zero live users |
| **Composite** | **5.8/10** | Security is the dominant drag factor |

## Delta from Last Score (3/14 → 3/15)
- **Security:** 3.0 → 2.5 (▼) — Another day with keys exposed; validator/limiter built but not connected is worse than not existing (false sense of security)
- **Composite:** 6.1 → 5.8 (▼) — Security deterioration over time

## Notes
- 16K+ lines Python backend, well-organized into api/models/services/processors/utils
- React+TypeScript frontend with 7 pages, 10 components, WebSocket hooks
- Flutter iOS app with all screens built
- Supabase migrations present
- Last commit: Mar 11 — Twilio webhook validation + consent announcement
- No commits in 4 days — project appears paused
