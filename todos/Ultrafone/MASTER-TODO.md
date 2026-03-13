# MASTER-TODO: Ultrafone
**Scored:** 2026-03-13 | **Composite:** 7.3/10 | **Tier:** 2

## Score Breakdown
| Dimension       | Score |
|----------------|-------|
| code_quality   | 8.0   |
| test_coverage  | 8.0   |
| security       | 5.0   |
| documentation  | 8.0   |
| architecture   | 8.0   |
| business_value | 7.0   |
| **COMPOSITE**  | **7.3** |

## 🚨 CRITICAL FLAGS — SECURITY BREACH
- **LEAKED API KEYS in git history** — `backend/.env.development` contains real Groq, Deepgram, Twilio auth tokens, Fish Audio keys, JWT secrets, and personal phone numbers
- **Immediate key rotation required** — all exposed credentials must be considered compromised
- **Git history purge required** — remove `.env.development` from all git history commits

---

## P0 — IMMEDIATE (Security Breach)
- [ ] **Rotate ALL leaked API keys NOW:** Groq, Deepgram, Twilio Auth Token, Fish Audio, JWT Secret
- [ ] **Purge git history** to remove `backend/.env.development` from all commits (`git filter-branch` or BFG)
- [ ] Add `.env.development`, `.env.*` (except `.env.example`) to `.gitignore`
- [ ] Set up pre-commit secret scanning hooks (git-secrets or gitleaks)
- [ ] Rotate any personal phone numbers exposed in config

## P1 — This Sprint
- [ ] Complete Railway deployment: PostgreSQL + Redis provision, Twilio webhook endpoint config
- [ ] Add integration tests to complement existing unit tests
- [ ] Connect iOS Flutter app to live backend streaming + push notifications
- [ ] Set up Sentry error tracking and UptimeRobot monitoring

## P2 — Next Sprint
- [ ] Implement feedback loop for caller reputation scoring
- [ ] Improve API documentation for external integrations
- [ ] Add health check endpoints for all backend services
- [ ] Build admin dashboard for call analytics / voicemail management

## P3 — Backlog
- [ ] Multi-tenant account management UI
- [ ] Enterprise features: team sharing, shared blocklist
- [ ] iOS App Store submission preparation
- [ ] Pricing page and Stripe billing integration
- [ ] Optimize STT/TTS latency for faster call response times
