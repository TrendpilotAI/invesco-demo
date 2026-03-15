# MASTER TODO — forwardlane_advisor

**Last judged:** 2026-03-15 | **Composite Score:** 5.6/10
**Category:** CORE (ForwardLane client-facing advisor app)

---

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Code Quality** | 4/10 | 31 models still use Sequelize v3 `classMethods` pattern despite v6 in package.json. Watson dead code in 10 files. Typos in production paths. `var` throughout. |
| **Test Coverage** | 3/10 | ~1,085 LOC across 14 test files for 165 app files + 40 models. Estimated <10% coverage. No coverage tooling (nyc). No CI gate. |
| **Security** | 5/10 | Helmet + CORS configured. Session secret validated. BUT: `aws-sdk@2.x` EOL with CVEs, `trim@0.0.1` prototype pollution, `xmldom@0.6.0` XXE risk, no rate limiting on LLM endpoints, Watson creds in config, file-based sessions. |
| **Documentation** | 7/10 | Good README (7.9KB). BRAINSTORM.md, PLAN.md, AUDIT.md all present. CONTRIBUTING.md exists. Missing: JSDoc on most modules, no API docs. |
| **Architecture** | 5/10 | LLM gateway with primary/fallback is solid. RabbitMQ for async is good. BUT: monolithic routes.js, no API versioning, file-based sessions, no health endpoints, Jade templates (deprecated 2016), models use v3 API on v6 runtime (fragile). |
| **Business Value** | 8/10 | Core client-facing product for ForwardLane. LLM gateway modernization done. Revenue-critical for demos and client engagement. Streaming dialog and portfolio narratives would be strong differentiators. |

**Composite: 5.6/10** (weighted: business 2x, security 1.5x, rest 1x)

---

## 🚩 CRITICAL Issues

1. **⚠️ Sequelize v3 API on v6 runtime** — 31 model files use `classMethods` in `define()` options, which was removed in Sequelize v4+. This means associations may be silently broken or the app relies on a shim. Every model needs migration to the static `associate()` pattern. **Risk: silent data bugs in production.**

2. **⚠️ AWS SDK v2 EOL** — `aws-sdk@^2.1692.0` has been end-of-life since Dec 2023. Active CVE exposure on S3/DynamoDB operations.

3. **⚠️ No rate limiting on LLM endpoints** — `app/hdialog/` routes can trigger unlimited Anthropic API calls. Cost abuse vector with no mitigation.

4. **⚠️ `trim@0.0.1` prototype pollution** — Known CVE (CVE-2020-7753). Trivially exploitable.

5. **⚠️ `xmldom@0.6.0` XXE vulnerability** — Should be `@xmldom/xmldom@^0.8`. Used for conversation scenario parsing.

---

## 🔴 P0 — Critical

- [ ] **TODO-838** — Remove all Watson dead code (10 files still reference Watson/NLC)
  - Files: `app/hdialog/conversation_zeno.js`, `app/nlc/watson_service.js`, `app/nlc/routes_nlc.js`, `app/hdialog/user_input_decorators.js`, `app/hdialog/actions/atomic_company_action.js`, `app/hdialog/actions/company_action.js`, `app/hdialog/user_input.js`, `app/relationship/routes_relationship.js`, `config/express.js:47`
  - Effort: 4-6 hours | Unblocks TODO-836

- [ ] **TODO-568/836** — Fix Sequelize v3→v6 model migration
  - Package is v6 but 31 models still use `classMethods` pattern (removed in v4)
  - Must convert all `classMethods.associate` to static class method pattern
  - Effort: 3-5 days | **CRITICAL — possible silent association failures**

- [ ] **TODO-876** — Streaming LLM dialog (SSE)
  - LLM gateway is request/response only; Anthropic SDK supports streaming natively
  - Effort: 3-4 days | Critical UX improvement for demos

- [ ] **[NEW] Fix trim@0.0.1 + xmldom@0.6.0 CVEs**
  - `trim`: Replace with native `.trim()` or upgrade
  - `xmldom`: Migrate to `@xmldom/xmldom@^0.8`
  - Effort: 1-2 hours | **Active CVE exposure**

## 🟠 P1 — High Priority

- [ ] **TODO-837** — AWS SDK v2 → v3
  - EOL since Dec 2023. Migrate `app/uploader/`, DynamoDB usage.
  - Effort: 2-3 days | Can parallel with TODO-838

- [ ] **TODO-840** — Redis session store (replace session-file-store)
  - File-based sessions prevent horizontal scaling
  - Effort: 4-6 hours | Self-contained

- [ ] **TODO-839** — Test coverage → 40%+
  - Current: ~10% (1,085 LOC tests / 165 app files). 14 test files exist.
  - LLM gateway (270 LOC), adviser unit tests (443 LOC) are a start.
  - Add: alerts, portfolios, auth middleware, dialog flow, API route integration tests
  - Effort: 1 week | Should happen after Sequelize model fix

- [ ] **TODO-454/571** — CI/CD pipeline
  - No CI/CD exists. Need: lint → test → docker build → deploy staging
  - Effort: 2-3 days

- [ ] **TODO-455** — N+1 query audit (`app/portfolios/`, `app/clients/`)
  - Effort: 1-2 days | After Sequelize model fix

- [ ] **TODO-877** — AI portfolio narrative generation
  - Auto-generate portfolio summaries/risk assessments via Claude
  - Effort: 3-5 days | Strong demo differentiator

- [ ] **TODO-575** — Rate limiting on LLM API endpoints
  - `express-rate-limit` on `app/hdialog/` routes
  - Effort: 2 hours | **Prevents cost abuse**

## 🟡 P2 — Medium Priority

- [ ] Merge duplicate Morningstar directories
  - `app/morning_star/` AND `app/morningstar_funds/` — ~500 lines duplicated
  - Effort: 1 day

- [ ] Health check endpoints (`/health`, `/ready`)
  - Required for load balancer / k8s readiness probes
  - Effort: 1-2 hours

- [ ] LLM response caching (Redis, 1hr TTL)
  - Could cut Anthropic API costs 30-50% for common queries
  - Effort: 4-6 hours

- [ ] Fix typos in production file/directory names
  - `models/startegy_instrument.js` → `strategy_instrument.js`
  - `models/alert_notifiations.js` → `alert_notifications.js`
  - `app/recomendation/` → `app/recommendation/`
  - `app/scheduller/` → `app/scheduler/`

- [ ] CORS origin hardening — require `CORS_ALLOWED_ORIGINS` in production

- [ ] ESLint + Prettier setup (TODO-576)

- [ ] Move test_rig config files from `config/db/` to `test/fixtures/`

## 🟢 P3 — Low Priority / Long-term

- [ ] Frontend modernization (Jade/jQuery → React or Hotwire)
- [ ] Salesforce/CRM integration
- [ ] Content Security Policy hardening
- [ ] OpenTelemetry observability (replace Bunyan file logging)
- [ ] RabbitMQ dead letter queue (prevent silent message loss)
- [ ] API versioning (`/api/v1/`)

---

## Dependency Graph

```
TODO-838 (Watson dead code) ──────┐
                                   ↓
TODO-568/836 (Sequelize v3→v6) ──→ TODO-839 (tests) ──→ TODO-454 (CI/CD)
TODO-837 (AWS SDK v3)  ──parallel─┘
TODO-840 (Redis)       ──parallel─┘
CVE fixes (trim/xmldom) ──independent──→ immediate
TODO-575 (rate limit)  ──independent──→ immediate
```

## Change Log

- **2026-03-15:** Fresh judge scoring. Discovered Sequelize v6 in package.json but 31 models still use v3 `classMethods` — elevated to CRITICAL. Added `trim` + `xmldom` CVE fix as new P0. Bumped rate limiting to P1. Composite score adjusted from 5.8 to 5.6 due to Sequelize model/runtime mismatch risk.
- **2026-03-14:** Previous scoring at 5.8/10.
- **2026-03-10:** BRAINSTORM.md, PLAN.md, AUDIT.md refreshed by Judge Agent v2.
