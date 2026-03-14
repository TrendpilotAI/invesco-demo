# MASTER TODO — forwardlane_advisor

**Last judged:** 2026-03-14 | **Composite Score:** 5.8/10
**Category:** CORE (ForwardLane client-facing advisor app)

---

## 🔴 P0 — Critical

- [ ] **TODO-838** — Remove all Watson dead code artifacts
  - `app/hdialog/conversation_zeno.js`, `app/nlc/watson_service.js`, `app/nlc/routes_nlc.js`
  - `config/express.js:47` WATSON_DIALOG_PASSWORD reference
  - Watson Dialog actions in `app/hdialog/actions/`
  - Effort: 4-6 hours | Unblocks everything else

- [ ] **TODO-876** — Streaming LLM dialog (SSE/WebSocket)
  - Current gateway is request/response only; add SSE streaming via Anthropic SDK
  - Effort: 3-4 days | Critical UX improvement for demos

## 🟠 P1 — High Priority

- [ ] **TODO-836** — Sequelize v3 → v6 upgrade
  - 40+ model files using legacy callback API. EOL ORM with known CVEs.
  - Effort: 3-5 days | Depends on TODO-838

- [ ] **TODO-837** — AWS SDK v2 → v3 upgrade
  - v2 EOL since Dec 2023. Multiple CVE risks.
  - Effort: 2-3 days | Can parallel with TODO-838

- [ ] **TODO-840** — Redis session store (replace session-file-store)
  - File-based sessions block horizontal scaling
  - Effort: 4-6 hours | Self-contained

- [ ] **TODO-839** — Test coverage → 40%+
  - Current: ~5-10%. 14 test files for 165 app files.
  - LLM gateway tests exist (270 LOC) but need more scenarios.
  - Priority targets: alerts, portfolios, auth middleware, dialog flow
  - Effort: 1 week | Depends on TODO-836

- [ ] **TODO-454 / TODO-571** — CI/CD pipeline
  - No CI/CD exists. Need lint → test → docker build → deploy staging.
  - Effort: 2-3 days

- [ ] **TODO-455** — N+1 query audit
  - `app/portfolios/`, `app/clients/` likely have N+1 patterns
  - Effort: 1-2 days | After Sequelize upgrade

- [ ] **TODO-877** — AI portfolio narrative generation
  - Auto-generate portfolio summaries/risk assessments via Claude
  - Effort: 3-5 days | Strong demo/sales differentiator

## 🟡 P2 — Medium Priority

- [ ] **TODO-575** — Rate limiting on LLM API endpoints
  - `app/hdialog/` routes have no rate limiting → unlimited Anthropic API calls
  - Effort: 2 hours

- [ ] Merge duplicate Morningstar directories
  - `app/morning_star/` AND `app/morningstar_funds/` — ~500 lines duplicated
  - Effort: 1 day

- [ ] Health check endpoints (`/health`, `/ready`)
  - Required for load balancer / k8s readiness probes
  - Effort: 1-2 hours

- [ ] LLM response caching (Redis, 1hr TTL)
  - Could cut Anthropic API costs 30-50% for common queries
  - Effort: 4-6 hours

- [ ] Fix typos in file/directory names
  - `models/startegy_instrument.js` → `strategy_instrument.js`
  - `models/alert_notifiations.js` → `alert_notifications.js`
  - `app/recomendation/` → `app/recommendation/`
  - `app/scheduller/` → `app/scheduler/`

- [ ] CORS origin hardening — require `CORS_ALLOWED_ORIGINS` in production
  - Currently falls back to `localhost:4000`

## 🟢 P3 — Low Priority / Long-term

- [ ] Frontend modernization (Jade/jQuery → React or Hotwire)
- [ ] Salesforce/CRM integration
- [ ] Content Security Policy hardening
- [ ] OpenTelemetry observability (replace Bunyan file logging)
- [ ] RabbitMQ dead letter queue (prevent silent message loss)
- [ ] Upgrade `xmldom` to `@xmldom/xmldom ^0.8` (XXE risk)
- [ ] Replace `trim@0.0.1` (prototype pollution risk)

---

## 🚩 Critical Flags

1. **AWS SDK v2 EOL** — Active CVE risk in production dependency
2. **Sequelize v3 EOL** — 8-year-old ORM with known vulnerabilities
3. **~5% test coverage** — No safety net for refactoring
4. **Watson credentials in git history** — Need `git filter-repo` to purge
5. **No rate limiting on LLM endpoints** — Cost abuse vector
