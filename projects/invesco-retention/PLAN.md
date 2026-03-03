# Invesco Retention — Execution Plan v3
**Date:** 2026-03-03
**Agent:** Judge Agent v2 (Planning inline)
**Based on:** BRAINSTORM.md v3

---

## Architecture Overview

The invesco-retention project is a **demo-only** Next.js application + supporting deliverables. No backend. All data is static/synthetic. Architecture is intentionally simple for maximum demo reliability.

```
invesco-retention/
├── demo-app/          # Next.js 14, static export, deployed Railway + GitHub Pages
├── mobile-pwa/        # Standalone PWA (no framework)
├── salesforce-lwc/    # LWC package for actual SF deployment
├── synthetic-data/    # Python data generation scripts + JSON/CSV outputs
└── materials/         # Executive brief, deck, pilot proposal
```

---

## Execution Order (by phase)

### Phase 1: Pre-Demo Critical Path (NOW → Demo Day)
These must be done before any demo to Brian Kiley.

| TODO | File | Effort | Owner |
|---|---|---|---|
| Dry run with Megan & Craig | #219 (existing) | S | Nathan |
| Demo screen recordings backup | #220 (existing) | S | Honey |
| iPhone live test | #332 (existing) | XS | Nathan |
| Demo day checklist | #222 (existing) | XS | Honey |

### Phase 2: Demo Polish (1-2 days)
Features that increase win probability.

| TODO | File | Effort |
|---|---|---|
| Competitor displacement persona | #383 | S (2h) |
| Connect Your Data modal | #382 | M (3-4h) |
| Demo default to /salesforce route | inline fix | XS |

### Phase 3: Infrastructure (post-demo or parallel)

| TODO | File | Effort |
|---|---|---|
| E2E smoke tests | #380 | M (2-3h) |
| Demo analytics (PostHog) | #381 | S (1-2h) |
| CI/CD GitHub Actions auto-deploy | new | S |

---

## Dependency Graph

```
Phase 1 (no deps) → Phase 2 (can run parallel) → Phase 3 (can run parallel)

#383 (competitor persona) → no deps
#382 (connect data modal) → no deps
#380 (E2E tests) → runs after Phase 2 polish
#381 (analytics) → no deps
```

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|---|---|---|
| Live demo tech failure | Medium | Backup recordings (TODO #220) |
| "Real data" question derails meeting | High | Scripted answer (in BRAINSTORM.md) |
| Demo route navigation confusion | Medium | Bookmark /salesforce as default open tab |
| Brian not engaged in first 30s | High | Open directly on Salesforce scene, advisor pre-selected |
| Competitor asks similar capability | Low | Competitive one-pager ready |

---

## Success Definition

Demo wins if Brian Kiley says: *"This is what I've been looking for."*

That requires:
1. ✅ Opens on Salesforce scene instantly
2. ✅ Dr. Sarah Chen's brief is loaded and impressive
3. ✅ Competitor Displacement signal is visible (Michael Torres)
4. ✅ Push to Salesforce toast fires smoothly
5. ✅ Mobile PWA shown on physical iPhone
6. ✅ "Connect Your Data" bridges to pilot proposal
7. ✅ Brian's question about real data gets a confident answer

---

## TODOs Added This Sprint

- `/data/workspace/todos/380-pending-p0-invesco-retention-e2e-smoke-tests.md`
- `/data/workspace/todos/381-pending-p1-invesco-retention-demo-analytics.md`
- `/data/workspace/todos/382-pending-p1-invesco-retention-connect-your-data-toggle.md`
- `/data/workspace/todos/383-pending-p1-invesco-retention-competitor-displacement-persona.md`
