# JUDGE SUMMARY — signal-builder-backend
*Judge Swarm Assessment | 2026-03-15 16:00 UTC*

## 📊 Scores (1-10 scale)

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|-------------|
| **Business Value** | 8.5/10 | 30% | 2.55 |
| **Security** | 7.5/10 | 25% | 1.875 |
| **Code Quality** | 8.0/10 | 15% | 1.2 |
| **Architecture** | 8.5/10 | 15% | 1.275 |
| **Test Coverage** | 7.0/10 | 10% | 0.7 |
| **Documentation** | 7.0/10 | 5% | 0.35 |
| **COMPOSITE** | **8.1/10** | | **7.95 (rounded 8.1)** |

## Delta Since Last Run
- **No new commits detected** since last assessment (2026-03-15 07:01 UTC)
- Scores unchanged — no code changes to reassess
- Category corrected: UNKNOWN → CORE in project registry

## 🎯 Assessment Overview

**signal-builder-backend** is a **production-ready FastAPI backend** powering ForwardLane's core Signal Builder product. It translates visual signal node graphs into SQL queries for financial analytics. 591 Python files, 177 test files, clean architecture with DI, multi-tenant scoping, Celery async tasks.

**Strengths:**
- ✅ Robust security hardening (SQLglot SQL validation, HMAC webhook signing, JWT revocation)
- ✅ Clean architecture: FastAPI + Celery + Redis + PostgreSQL with proper async/sync separation
- ✅ Comprehensive testing (170+ test files) including multi-tenant isolation tests
- ✅ Active development with recent Invesco integrations
- ✅ Good documentation (BRAINSTORM.md, PLAN.md, AUDIT.md are thorough)

**Weaknesses:**
- ❌ Webhook secrets stored in plaintext (CRITICAL)
- ❌ Optional storage params mask DI wiring failures
- ❌ No JWT key rotation mechanism
- ❌ Test coverage estimated at 55-65% (target: 80%)
- ❌ Several outdated dependencies with potential CVEs

## 🔴 Critical Issues (2)

1. **🚨 Webhook secrets stored in plaintext** (`apps/webhooks/models/webhook.py:16`)
   - DB breach → all webhook consumer secrets exposed
   - **Fix:** AES-256-GCM encryption + migration script (TODO #832)

2. **⚠️ Optional storage parameters mask DI failures** (`apps/signals/cases/signal.py`)
   - `signal_version_storage=None`, `signal_run_storage=None` defaults → silent runtime errors
   - **Fix:** Remove `=None` defaults (TODO #826)

## 🟡 High Priority Issues (4)

3. **🔐 JWT key rotation** — Single `SECRET_KEY`, no rotation (TODO #833)
4. **📅 Signal scheduling** — No cron execution, critical for Invesco (TODO #827)
5. **🐳 Prod Dockerfile audit** — Dev deps (ipython CVEs) may leak into prod image (TODO #834)
6. **📊 CI security gates** — pip-audit, bandit, mypy not enforced as blocking (TODO #354)

## 📈 Trend
Stable at 8.1 — recent security hardening sprint (HMAC, JWT revocation, sqlglot, multi-tenant tests) lifted score from 7.7 → 8.1. Next improvement requires addressing webhook encryption and testing gaps.

---
*Scored by Judge Subagent | 2026-03-15 16:00 UTC | Tier 1 — CORE*
