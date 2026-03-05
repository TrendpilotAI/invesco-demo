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

---

# Plan v4 — Judge Agent Update (2026-03-04)
**Demo deployed. Week 2 of retention window. Dry run not yet done.**

## Immediate Priority Order (This Week)

1. **Schedule dry run with Megan & Craig** — Nathan action, 0 engineering required (#219)
2. **Record backup MP4s** — Honey action, use demo-video skill, 2-4 hours (#220, #302)
3. **Print-to-PDF button** — Honey codes, ~2 hours, adds huge leave-behind value (new TODO)
4. **Demo tab pre-setup script** — XS, creates browser bookmarks, <30 min (#341)
5. **iPhone PWA test** — Nathan action, 15 minutes (#332)

## New TODOs to Create

### TODO: Print-to-PDF Leave-Behind Button
- File: `426-pending-p0-invesco-retention-print-to-pdf-button.md`
- Add "Save as PDF" / "Print Brief" button to /salesforce meeting brief
- Uses `window.print()` with `@media print` CSS or html2pdf.js
- Shows Invesco logo, advisor name, signal summary, recommended actions
- Effort: S (2-3h)

### TODO: Live AUM Input on ROI Calculator  
- File: `427-pending-p1-invesco-retention-live-aum-input.md`
- Input field on dashboard/ROI section: "Your AUM with this advisor"
- Pre-filled with synthetic $40M; user can type actual number
- ROI recalculates live
- Effort: S (1-2h)

### TODO: Pilot Timeline Widget
- File: `428-pending-p1-invesco-retention-pilot-timeline-widget.md`
- Visual day-by-day timeline: Day 0 → Day 14
- Add to /salesforce bottom section or as standalone modal
- Effort: XS (1h)

## Risk Assessment (Updated)
- **Highest risk:** Demo hasn't been dry-run. Megan/Craig may flag political issues.
- **Second risk:** Live demo failure. Mitigated by backup recordings.
- **Third risk:** Brian focuses on integration complexity. Mitigated by "Connect Your Data" wizard.
- **Fourth risk:** Ten Decoders bench concern. Mitigated by existing IT security one-pager (#335).


---

## Plan Update v4 — 2026-03-05

### New TODOs from Code Audit

| # | Task | Priority | Effort |
|---|------|----------|--------|
| #429 | Use Railway URL for IT security demo (headers not sent by GH Pages) | P0 | XS |
| #430 | Verify TypeScript clean build before demo | P0 | XS |

### Revised Demo Day Execution Order

```
IMMEDIATE (today/tomorrow before demo):
1. #430 — npm run build (XS, verify clean)
2. Bookmark /salesforce directly (XS, not a TODO file — just do it)
3. #332 — iPhone PWA test (XS)
4. #222 — Demo day checklist finalize (XS)
5. #219 — Dry run with Megan/Craig (S — schedule now)

PRE-DEMO PARALLEL:
6. #220 — Record backup MP4s (S)  
7. #426 — Print-to-PDF button (S, high win-rate impact)
8. #383 — Competitor displacement persona (S)
9. #424 — Signal confidence scores (XS)
10. #423 — Seismic content recommendations (S)

POST-DEMO:
11. #429 — Railway deploy + security header verification
12. #380 — E2E smoke tests
13. #381 — PostHog analytics
```

### Risk Flags
- 🔴 Dry run (#219) not yet done — HIGHEST RISK
- 🟠 No backup recordings yet (#220) — if live demo fails, nothing to fall back on
- 🟡 Security headers not on GH Pages — low risk for demo, medium risk if IT reviews
