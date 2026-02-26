# Railway Cost Optimization Report

**Generated:** 2026-02-24
**Total Services:** 39 across 5 projects
**Total Projects:** 5

---

## Executive Summary

We're running **39 services** but realistically need ~20. The biggest offender is **Ultrafone with 12 services** (5 Redis + 6 Postgres for ONE app). Estimated **40-50% cost reduction** possible through consolidation and cleanup.

### Quick Wins (Immediate Savings)

| Action | Services Affected | Est. Monthly Savings |
|--------|------------------|---------------------|
| Delete Hypebase-ai duplicate project | 1 | ~$5 |
| Consolidate Ultrafone Redis (5→1) | 4 removed | ~$20-40 |
| Consolidate Ultrafone Postgres (6→1-2) | 4 removed | ~$20-40 |
| Stop crashed/failed services | 6 | ~$10-20 |
| Delete unused "." service (Hypebase AI) | 1 | ~$5 |
| **Total Quick Wins** | **16 services** | **~$60-110/mo** |

---

## Project-by-Project Analysis

### 1. Hypebase AI (8 services)

| Service | Status | Last Deploy | Action |
|---------|--------|-------------|--------|
| `.` | ⛔ CRASHED | Feb 24 | **DELETE** — unnamed service, crashed |
| LibreChat | ✅ SUCCESS | Feb 20 | Keep |
| VectorDB | ✅ SUCCESS | Jan 13 | Review — 6 weeks stale |
| hypebase-ai | ✅ SUCCESS | Feb 6 | Keep (main app) |
| Meilisearch | ✅ SUCCESS | Jan 13 | Review — 6 weeks stale |
| RAG API 📚 | ✅ SUCCESS | Jan 30 | Keep |
| MongoDB | ✅ SUCCESS | Jan 13 | Keep (LibreChat dependency) |
| FalkorDB | 💤 SLEEPING | Jan 2 | **DELETE** — sleeping since Jan 2, likely unused |

**Recommendation:** Delete `.` and FalkorDB. Review if VectorDB and Meilisearch are actively used.

### 2. Ultrafone (12 services) — 🚨 CRITICAL WASTE

| Service | Status | Last Deploy | Action |
|---------|--------|-------------|--------|
| ultrafone-app | ✅ SUCCESS | Feb 20 | Keep (main app) |
| Ultrafone | ⛔ FAILED | Feb 20 | **DELETE** — duplicate of ultrafone-app, FAILED |
| Postgres | ✅ SUCCESS | Jan 8 | Keep as primary DB |
| Postgres-ATOx | ✅ SUCCESS | Jan 14 | **CONSOLIDATE** |
| Postgres-09RY | ✅ SUCCESS | Jan 14 | **CONSOLIDATE** |
| Postgres-Wq5P | ✅ SUCCESS | Jan 14 | **CONSOLIDATE** |
| Postgres-dW-g | ✅ SUCCESS | Jan 12 | **CONSOLIDATE** |
| Redis | ❌ NO DEPLOYS | — | **DELETE** — never deployed |
| Redis-jbi5 | ✅ SUCCESS | Jan 14 | Keep as primary cache |
| Redis-I90J | ✅ SUCCESS | Jan 14 | **CONSOLIDATE** |
| Redis-rfwD | ✅ SUCCESS | Jan 14 | **CONSOLIDATE** |
| Redis-MqUf | ✅ SUCCESS | Jan 12 | **CONSOLIDATE** |

**The Ultrafone Problem:**
- **6 Postgres instances** for one app — likely created during development experimentation. All deployed Jan 8-14 and never touched. Consolidate to 1-2 (primary + analytical if needed).
- **5 Redis instances** — same pattern. One app needs ONE Redis (or two: cache + queue). Consolidate to 1.
- **Two app services** ("Ultrafone" FAILED + "ultrafone-app" SUCCESS) — delete the failed duplicate.

**Action Plan:**
1. Verify which Postgres has actual data: `SELECT count(*) FROM information_schema.tables` on each
2. Migrate any needed data to primary Postgres
3. Delete 4 Postgres + 4 Redis + 1 failed app = **9 services removed**

### 3. Hypebase-ai (1 service) — 🗑️ DELETE PROJECT

| Service | Status | Last Deploy | Action |
|---------|--------|-------------|--------|
| Hypebase-ai | ⛔ FAILED | Jan 7 | **DELETE** — duplicate of Hypebase AI project, failed since Jan 7 |

**This is a duplicate project.** The main "Hypebase AI" project has the working `hypebase-ai` service. This entire project should be deleted.

### 4. OpenClaw AI + n8n + Tailscale (8 services)

| Service | Status | Last Deploy | Action |
|---------|--------|-------------|--------|
| openclaw-railway-template | ✅ SUCCESS | Feb 24 | Keep (main gateway) |
| Postgres | ✅ SUCCESS | Feb 19 | Keep |
| Redis | ✅ SUCCESS | Feb 19 | Keep |
| Temporal | ✅ SUCCESS | Feb 20 | Keep |
| Primary | ✅ SUCCESS | Feb 20 | Keep |
| Worker | ✅ SUCCESS | Feb 20 | Keep |
| Postiz | ✅ SUCCESS | Feb 20 | Review — social media tool, is it used? |
| Agent Ops Center | ⛔ FAILED | Feb 24 | **FIX or DELETE** — recently failed |

**This project is healthy.** Agent Ops Center needs investigation (just failed today). Postiz should be reviewed for actual usage.

### 5. ForwardLane Signal Studio (10 services)

| Service | Status | Last Deploy | Action |
|---------|--------|-------------|--------|
| Django Backend | ✅ SUCCESS | Feb 23 | Keep |
| Postgres Default | ✅ SUCCESS | Feb 22 | Keep |
| Postgres Analytical | ✅ SUCCESS | Feb 22 | Keep (legitimate — separate analytical DB) |
| Redis | ✅ SUCCESS | Feb 22 | Keep |
| Signal Studio | ✅ SUCCESS | Feb 23 | Keep |
| Signal Builder API | ✅ SUCCESS | Feb 23 | Keep |
| Celery Worker | ⛔ FAILED | Feb 23 | **FIX** — needed for async tasks |
| Celery Beat | ⛔ FAILED | Feb 23 | **FIX** — needed for scheduled tasks |
| Entity Extraction | ⛔ FAILED | Feb 24 | **Known failure** — review if still needed |
| New Design | ⛔ FAILED | Feb 22 | **DELETE or FIX** — what is this? |

**Note:** 2 Postgres here is **justified** (Default for app data, Analytical for signal SQL). 4 services are failing — Celery Worker/Beat are critical and need fixing. Entity Extraction is a known issue.

---

## Failed/Crashed Services Summary

| Service | Project | Status | Last Deploy | Priority |
|---------|---------|--------|-------------|----------|
| `.` | Hypebase AI | CRASHED | Feb 24 | Delete |
| Hypebase-ai | Hypebase-ai | FAILED | Jan 7 | Delete project |
| Ultrafone | Ultrafone | FAILED | Feb 20 | Delete (duplicate) |
| Agent Ops Center | OpenClaw | FAILED | Feb 24 | Fix (recent) |
| Celery Worker | ForwardLane | FAILED | Feb 23 | **Fix (critical)** |
| Celery Beat | ForwardLane | FAILED | Feb 23 | **Fix (critical)** |
| Entity Extraction | ForwardLane | FAILED | Feb 24 | Review |
| New Design | ForwardLane | FAILED | Feb 22 | Delete or Fix |

---

## Stale Services (No deploy >30 days)

| Service | Project | Last Deploy | Days Stale |
|---------|---------|-------------|------------|
| FalkorDB | Hypebase AI | Jan 2 | 53 days |
| VectorDB | Hypebase AI | Jan 13 | 42 days |
| Meilisearch | Hypebase AI | Jan 13 | 42 days |
| MongoDB | Hypebase AI | Jan 13 | 42 days |
| Hypebase-ai | Hypebase-ai | Jan 7 | 48 days |
| All Ultrafone DBs | Ultrafone | Jan 8-14 | 41-47 days |

---

## Consolidation Recommendations

### Priority 1: Ultrafone Database Consolidation
- **Current:** 6 Postgres + 5 Redis = 11 database services
- **Target:** 1 Postgres + 1 Redis = 2 database services
- **Savings:** 9 services removed (~$45-90/mo)
- **Risk:** Low — most are likely empty/unused development artifacts
- **Steps:**
  1. Connect to each Postgres, check for actual data
  2. If data exists, pg_dump and restore to primary
  3. Update ultrafone-app environment variables
  4. Delete redundant services

### Priority 2: Delete Dead Projects/Services
- Delete entire Hypebase-ai project (duplicate)
- Delete `.` service in Hypebase AI (crashed, unnamed)
- Delete `Ultrafone` service (failed duplicate of ultrafone-app)
- Delete `Redis` in Ultrafone (never deployed)
- **Savings:** 4 services removed (~$10-20/mo)

### Priority 3: Fix Critical Failures
- Fix Celery Worker + Celery Beat in ForwardLane (critical for async processing)
- Investigate Agent Ops Center failure
- Decide on Entity Extraction fate

### Priority 4: Review Sleeping/Stale Services
- FalkorDB sleeping since Jan 2 — likely safe to delete
- Postiz in OpenClaw — is it actively used?

---

## Estimated Monthly Impact

| Category | Current Services | Target Services | Est. Savings |
|----------|-----------------|-----------------|-------------|
| Ultrafone consolidation | 12 | 3 | $45-90 |
| Dead project/service cleanup | 4 | 0 | $10-20 |
| Sleeping/stale services | 2-3 | 0 | $10-15 |
| **Total** | **39** | **~22** | **$65-125/mo** |

**Note:** Exact savings depend on Railway's per-service pricing and actual resource consumption. Services with higher CPU/memory limits cost more. Database services (Postgres, Redis) typically run 24/7 and are the biggest cost drivers.

---

## Temporal Automation

The following Temporal workflows have been created to automate ongoing management:

1. **ResourceOptimizationWorkflow** — Weekly audit that identifies waste and alerts
2. **ServiceScalerWorkflow** — Scale services up/down based on demand
3. **DeploymentPipelineWorkflow** — Managed deployments with auto-rollback

Schedule: Weekly resource audit via Temporal Schedule (`railway-resource-audit-weekly`)

---

*Report generated by Honey AI Railway Resource Management System*
