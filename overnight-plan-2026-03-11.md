# Overnight Agent Plan — March 11, 2026
> Nathan directive: MAX agents. Security + bugs first, then completion + monetization + GTM.
> Platform limit: 5 concurrent sub-agents (hard cap). Running in waves.
> All results logged to `/data/workspace/overnight-results-2026-03-11.json` for Convex import.

## Wave 1 (RUNNING — 5 active, 1 completed)
1. ✅ **signalhaus-prod-ready** — Completed 3 min — Vercel prep, contact form, OG tags, rate limiting, 404
2. 🔄 **flipmyera-billing** — Stripe checkout, remove client keys, upsell flow, tier pricing
3. 🔄 **invesco-demo-polish** — Interactive elements, demo tour, ROI calc, pulse animation
4. 🔄 **narrativereactor-billing** — Stripe integration, scrypt, helmet, JWT, DB singleton
5. 🔄 **gtm-materials** — GTM playbook, pitch deck, email sequences, case study
6. 🔄 **security-wave2a** — SQL injection, JWT secrets, CORS, EXPLAIN injection (signal-builder-backend)

## Wave 2 (QUEUED — spawn as slots open)
7. **security-wave2b** — signal-studio: SKIP_AUTH removal, prompt injection, rate limiting, dump.rdb
8. **security-wave2c** — signal-studio-auth: refresh token rotation, CORS middleware, admin RBAC, hardcoded secrets
9. **security-wave2d** — Snowflake SQL injection (data-provider), NarrativeReactor CORS, Ultrafone git purge

## Wave 3 (QUEUED — Bug Fixes)
10. **bugfix-backend** — Django REST auth, psycopg2 pooling, Django 4.2 compat, urllib→requests, env vars
11. **bugfix-frontend** — ReactFlow dedup, signal-studio build errors, templates ESM fix, CI pipelines

## Wave 4 (QUEUED — Completion + More Security)
12. **completion-1** — signal-builder-backend rate limiting, webhook HMAC, celery idempotency
13. **completion-2** — Second-Opinion HIPAA + Stripe, flip-my-era remaining, Ultrafone Twilio validation
14. **completion-3** — core-entityextraction test suite + connection leak, forwardlane_advisor Node upgrade
15. **completion-4** — signal-studio-frontend auth middleware, CI/CD, bundle optimization

## Target: 15 agents across 3-4 waves overnight
