# forwardlane_advisor — Prioritized TODO List

Generated: 2026-03-11

## CRITICAL Issues 🔴

1. **AWS SDK v2 EOL** — `aws-sdk@^2.1692.0` reached EOL Dec 2023, multiple known CVEs. Migrate to `@aws-sdk/client-s3`, `@aws-sdk/client-dynamodb`, `@aws-sdk/lib-dynamodb`. Remove `dynamodb` + `dynamodb-doc` wrappers.
2. **Watson credentials in git history** — Hardcoded secrets were removed from source but remain in git history. Run `git filter-repo` or BFG Repo-Cleaner to purge `d6c3d747...` username and `BntGMB1nxSHs` password.
3. **`trim@0.0.1` prototype pollution** — Known CVE. Replace with native `String.prototype.trim()` or upgrade.

## HIGH Priority

4. **Add rate limiting on LLM endpoints** — `app/hdialog/` routes have no rate limiting; users can trigger unlimited Anthropic/OpenAI API calls. Add `express-rate-limit` with per-user token bucket. (Effort: 2-4h)
5. **Replace file-based sessions with Redis** — `session-file-store` doesn't scale horizontally, does disk I/O on every request. Switch to `connect-redis`. (Effort: 4-6h)
6. **Sequelize v3 → v6 upgrade** — v3 is EOL (2015), callback-based, known security issues. 40+ model files need migration. (Effort: 3-5 days)
7. **Test coverage from ~5% to 40%+** — Add `nyc` for coverage reporting. Priority test targets: `app/llm/gateway.js` (fallback logic), `app/alerts/rules/`, auth middleware, `app/portfolios/`. (Effort: 1 week)

## MEDIUM Priority

8. **Remove Watson dead code** — `app/nlc/watson_service.js`, Watson references in `app/hdialog/`, `config/express.js` Watson Dialog config. Verify `USE_LLM_GATEWAY=true` fully bypasses all Watson paths. (Effort: 4-6h)
9. **Merge duplicate Morningstar integrations** — `app/morning_star/` and `app/morningstar_funds/` share ~500 lines of duplicated HTTP client code. Merge into single `app/morningstar/` module. (Effort: 1 day)
10. **Fix typos in production paths** — `models/startegy_instrument.js` → `strategy_instrument.js`, `models/alert_notifiations.js` → `alert_notifications.js`, `app/recomendation/` → `app/recommendation/`. (Effort: 2-4h, but requires careful migration of all references)
11. **Upgrade `xmldom` to `@xmldom/xmldom`** — Current `xmldom ^0.6.0` has XXE vulnerabilities. (Effort: 1h)
12. **Add health check endpoint** — No `/health` or `/ready` endpoint exists. Required for container orchestration and monitoring. (Effort: 30min)
13. **CORS: require explicit origins in production** — Currently falls back to `http://localhost:4000`. Add startup validation that `CORS_ALLOWED_ORIGINS` is set when `NODE_ENV=production`. (Effort: 30min)

## LOW Priority

14. **Jade → Pug migration** — `jade ~1.11.0` deprecated since 2016. Rename to `pug` or plan frontend modernization. (Effort: long-term)
15. **Move test rig configs out of production** — `config/db/test_rig_*.js` files should live in `test/fixtures/`. (Effort: 2h)
16. **Add API versioning** — No `/api/v1/` prefix on routes. Makes future breaking changes risky. (Effort: 1 day)
17. **Add RabbitMQ dead letter queue** — Current setup has no DLQ, so failed messages are silently lost. (Effort: 4h)
18. **README quality** — Current README is auto-generated and lists jQuery minified functions as "key functions". Rewrite with actual architecture overview, setup guide, and API documentation. (Effort: 2-4h)
19. **Add CI/CD pipeline** — No `.github/workflows/` or equivalent. Add lint → test → build → deploy pipeline. (Effort: 1 day)
20. **LLM response caching** — Add Redis cache with TTL for repeated dialog queries to reduce API costs. (Effort: 4-6h)
