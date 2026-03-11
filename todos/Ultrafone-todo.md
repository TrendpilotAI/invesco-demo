# Ultrafone — Prioritized TODO List
*Generated: 2026-03-11 | Composite Score: 6.1/10*

---

## 🚨 CRITICAL — Do Before Anything Else

### 1. Rotate ALL Exposed API Keys (P0, 1h)
**Status:** UNRESOLVED — keys still compromised  
- Groq, Deepgram, Twilio (SID + Auth Token), Fish Audio keys are live in `backend/.env.development`
- Nathan's personal phone (+13107798590) exposed
- **Action:** Rotate every key listed in SECRETS_ROTATION.md immediately
- Set new keys in Railway env vars only

### 2. Purge Git History (P0, 30min)
- `git filter-repo --path backend/.env.development --invert-paths`
- Force push all branches
- Verify: `git log --all --full-diff -p | grep "GROQ_API_KEY"` returns nothing

### 3. Add Twilio Webhook Signature Validation (P0, 2h)
- No `RequestValidator` on webhook endpoints — anyone can POST fake calls
- Cost amplification attack vector (each POST triggers Groq + Deepgram API calls)

### 4. Add Rate Limiting on Webhook Endpoints (P0, 2h)
- Install `slowapi`: 10 req/min per IP, 5 req/min per caller phone
- Prevents flood/cost amplification attacks

---

## 🔥 HIGH Priority

### 5. Deploy to Railway (P1, 4h)
- `railway.toml` and `nixpacks.toml` exist but not deployed
- Provision PostgreSQL + Redis add-ons
- Wire Twilio webhook to Railway URL
- Add `/health` endpoint monitoring

### 6. Fix Hardcoded `user_id="nathan"` — 5 Locations (P1, 1 day)
- `backend/services/receptionist.py` lines 171, 276, 374, 424, 512
- Blocks all multi-tenant/SaaS ambitions
- Route Twilio `To` number → UserProfile DB lookup

### 7. Consolidate 3 TTS Services into Unified Provider (P1, 4h)
- `fish_tts.py`, `elevenlabs_tts.py`, `voice_service.py` overlap
- Create `TTSProvider` ABC with config-driven provider selection
- Remove duplicate `elevenlabs>=1.0.0` from requirements.txt

### 8. Add Pre-commit Secret Scanning (P1, 1h)
- Install `gitleaks` pre-commit hook
- Prevent future credential leaks

---

## 📋 MEDIUM Priority

### 9. Add E2E Test Suite (P2, 1 week)
- No end-to-end test of full call flow
- Mock Twilio webhooks for CI
- Test call classification accuracy with fixtures

### 10. Add Coverage Config (P2, 1h)
- No `pytest-cov` or `.coveragerc` — can't measure actual coverage
- Add to CI pipeline

### 11. Complete Security Analyzer DB Lookup (P2, 4h)
- `backend/processors/security_analyzer.py` lines 224-226 are TODO stubs
- Caller history not actually queried

### 12. Audit `icloud_contacts.py` (P2, 1h)
- iCloud has no public API — likely a stub
- Mark as unsupported or remove from CONTACT_PLATFORMS

### 13. Connection Pooling for Groq + Redis (P2, 3h)
- New Groq client per call — should share with pool
- Verify Redis uses ConnectionPool

### 14. Google Calendar Integration (P2, 1 week)
- AI should know Nathan's schedule for context-aware responses
- Auto-schedule appointments for healthcare calls

### 15. CI/CD Pipeline (P2, 4h)
- GitHub Actions: lint → test → deploy on merge to main
- Secret scanning in CI

---

## 🔮 FUTURE / Nice to Have

### 16. SaaS Multi-Tenant Architecture (P3, 3-4 weeks)
- User onboarding, Stripe billing, per-user Twilio numbers

### 17. Android App via Flutter (P3, 1 week)
- Rename `ios-app/` → `mobile-app/`, add FCM push

### 18. Zapier Webhook Bridge (P3, 1 day)
- Fire `call.completed`, `lead.created` events for 5000+ integrations

### 19. Voice Latency Benchmarking (P3, 1 day)
- No baseline measurement exists — measure before optimizing

### 20. Frontend Tests (P3, 3 days)
- Zero frontend test files — add Vitest + React Testing Library
