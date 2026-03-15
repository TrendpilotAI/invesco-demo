# MASTER TODO — forwardlane_advisor

**Last judged:** 2026-03-15 | **Composite Score: 5.5/10**
**Category:** CORE (ForwardLane client-facing advisor app)
**Growth Tier:** 2 | **Priority:** 7.6

---

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Code Quality** | 4/10 | 31 models use Sequelize v3 `classMethods` despite v6 runtime. 12 files still reference Watson/NLC. Typos in production paths (`startegy`, `notifiations`, `recomendation`, `scheduller`). Legacy `var` usage. |
| **Test Coverage** | 3/10 | 14 test files for 205 source files (~7% file coverage). No coverage tooling (nyc/c8). No CI gate. Recent 63 unit tests for adviser core is a good start. |
| **Security** | 5/10 | Helmet + CORS configured. Session secret validated at startup. SSH exfil removed from Dockerfile. BUT: `trim@0.0.1` (CVE-2020-7753 prototype pollution), `xmldom@0.6.0` (XXE), `aws-sdk@2.x` EOL with CVEs, no rate limiting on LLM endpoints, Watson creds still in config, file-based sessions. |
| **Documentation** | 7/10 | README, BRAINSTORM.md, PLAN.md, AUDIT.md, CONTRIBUTING.md all present. Missing: JSDoc coverage, API endpoint docs. |
| **Architecture** | 5/10 | LLM gateway with primary/fallback is solid design. RabbitMQ for async good. BUT: monolithic `routes.js`, no API versioning, file-based sessions block scaling, Jade templates (deprecated 2016), Sequelize v3 API on v6 runtime = fragile. No health endpoints. No CI/CD. |
| **Business Value** | 8/10 | Core client-facing product. LLM gateway modernization done. Revenue-critical for demos and client engagement. Streaming dialog and portfolio AI narratives would be strong differentiators. |

**Composite: 5.5/10** (weighted: business 2×, security 1.5×, rest 1×)

Formula: `(4 + 3 + 5×1.5 + 7 + 5 + 8×2) / (1+1+1.5+1+1+2) = 41.5/7.5 = 5.53`

---

## 🚩 CRITICAL Issues (5)

1. **⚠️ Sequelize v3 API on v6 runtime** — 31 model files use `classMethods` in `define()` options, removed in Sequelize v4+. Associations may be silently broken or relying on an undocumented shim. **Risk: silent data bugs in production.**

2. **⚠️ `trim@0.0.1` prototype pollution** — CVE-2020-7753. Trivially exploitable. Direct dependency in package.json.

3. **⚠️ `xmldom@0.6.0` XXE vulnerability** — Should be `@xmldom/xmldom@^0.8`. Used for conversation scenario XML parsing.

4. **⚠️ AWS SDK v2 EOL** — `aws-sdk@^2.1692.0` end-of-life since Dec 2023. Active CVE exposure on S3/DynamoDB operations.

5. **⚠️ No rate limiting on LLM endpoints** — `app/hdialog/` routes trigger unlimited Anthropic/OpenAI API calls. Unmitigated cost abuse vector.

---

## 🔴 P0 — Critical

- [ ] **TODO-CVE-01** — Fix `trim@0.0.1` + `xmldom@0.6.0` CVEs
  - `trim`: Replace with native `.trim()` or remove dependency
  - `xmldom`: Migrate to `@xmldom/xmldom@^0.8`
  - Effort: 1-2 hours | **Active CVE exposure — do immediately**

- [ ] **TODO-838** — Remove all Watson dead code (12 files still reference Watson/NLC)
  - Files: `app/hdialog/conversation_zeno.js`, `app/nlc/watson_service.js`, `app/nlc/routes_nlc.js`, `app/hdialog/user_input_decorators.js`, `app/hdialog/actions/atomic_company_action.js`, `app/hdialog/actions/company_action.js`, `app/hdialog/user_input.js`, `app/hdialog/conversation_scenario_parser.js`, `app/relationship/routes_relationship.js`, `app/superadmin/routes_superadmin.js`, `app/utils/constants.js`, `config/express.js:47`
  - Note: `app/llm/gateway.js` references Watson for documentation purposes — keep
  - Effort: 4-6 hours | Unblocks TODO-836

- [ ] **TODO-568/836** — Fix Sequelize v3→v6 model migration
  - Package is v6 but 31 models use `classMethods` pattern (removed in v4)
  - Must convert all `classMethods.associate` to static class method pattern
  - Effort: 3-5 days | **CRITICAL — possible silent association failures**

- [ ] **TODO-575** — Rate limiting on LLM API endpoints
  - `express-rate-limit` on `app/hdialog/` routes with per-user token bucket
  - Effort: 2 hours | **Prevents cost abuse**

- [ ] **TODO-876** — Streaming LLM dialog (SSE)
  - LLM gateway is request/response only; Anthropic SDK supports streaming natively
  - Effort: 3-4 days | Critical UX improvement for demos

## 🟠 P1 — High Priority

- [ ] **TODO-837** — AWS SDK v2 → v3
  - EOL since Dec 2023. Migrate `app/uploader/`, DynamoDB usage.
  - Effort: 2-3 days | Can parallel with TODO-838

- [ ] **TODO-840** — Redis session store (replace session-file-store)
  - File-based sessions prevent horizontal scaling
  - Effort: 4-6 hours | Self-contained

- [ ] **TODO-839** — Test coverage → 40%+
  - Current: ~7% file coverage (14/205). 63 adviser unit tests exist.
  - Add: LLM gateway mocks, alerts, portfolios, auth middleware, dialog flow, API routes
  - Install `nyc` or `c8` for coverage reporting
  - Effort: 1 week | Should happen after Sequelize model fix

- [ ] **TODO-454/571** — CI/CD pipeline
  - No CI/CD exists. Need: lint → test → docker build → deploy staging
  - Effort: 2-3 days

- [ ] **TODO-455** — N+1 query audit (`app/portfolios/`, `app/clients/`)
  - Effort: 1-2 days | After Sequelize model fix

- [ ] **TODO-877** — AI portfolio narrative generation
  - Auto-generate portfolio summaries/risk assessments via Claude
  - Effort: 3-5 days | Strong demo differentiator

## 🟡 P2 — Medium Priority

- [ ] Merge duplicate Morningstar directories (`app/morning_star/` + `app/morningstar_funds/`)
  - ~500 lines duplicated code | Effort: 1 day

- [ ] Health check endpoints (`/health`, `/ready`)
  - Required for load balancer / k8s readiness probes | Effort: 1-2 hours

- [ ] LLM response caching (Redis, 1hr TTL)
  - Could cut Anthropic API costs 30-50% for common queries | Effort: 4-6 hours

- [ ] Fix typos in production file/directory names
  - `models/startegy_instrument.js` → `strategy_instrument.js`
  - `models/alert_notifiations.js` → `alert_notifications.js`
  - `app/recomendation/` → `app/recommendation/`
  - `app/scheduller/` → `app/scheduler/`
  - Effort: 2-3 hours (must update all imports/requires)

- [ ] CORS origin hardening — require `CORS_ALLOWED_ORIGINS` in production

- [ ] ESLint + Prettier setup (TODO-576) | Effort: 2-3 hours

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
TODO-CVE-01 (trim/xmldom) ──→ immediate (no deps)
TODO-575 (rate limiting)  ──→ immediate (no deps)

TODO-838 (Watson dead code) ──────┐
                                   ↓
TODO-568/836 (Sequelize v3→v6) ──→ TODO-839 (tests) ──→ TODO-454 (CI/CD)
TODO-837 (AWS SDK v3)  ──parallel─┘
TODO-840 (Redis)       ──parallel─┘
```

---

## Progress Since Last Audit

### ✅ Completed
- Node.js 0.10 → v20 LTS upgrade
- Dockerfile SSH key exfiltration removed
- `app/retrieve_and_rank/` directory deleted
- Watson NLC → LLM Gateway (Claude + GPT-4o-mini) implemented
- SESSION_SECRET validated at startup
- 63 unit tests added for adviser core logic
- Comprehensive docs (README, BRAINSTORM, PLAN, AUDIT, CONTRIBUTING)

### 🔄 Still Pending
- Watson references in 12 files (down from original but not zero)
- All 31 models still on v3 `classMethods` pattern
- CVE-vulnerable direct deps (`trim`, `xmldom`)
- AWS SDK v2 still in use
- No CI/CD, no rate limiting, no health endpoints
- File-based sessions

---

## Change Log

- **2026-03-15 (16:20 UTC):** Fresh judge scoring by judge-swarm. Validated 31 models still use classMethods, 12 Watson references remain, both CVE deps still present. Composite adjusted to 5.5/10 (down from 5.6 — trim/xmldom CVEs still unfixed after 5 days). Promoted CVE fixes + rate limiting to P0. Reorganized priority order.
- **2026-03-15 (prev):** Previous scoring at 5.6/10.
- **2026-03-14:** Scoring at 5.8/10.
- **2026-03-10:** BRAINSTORM.md, PLAN.md, AUDIT.md refreshed by Judge Agent v2.
