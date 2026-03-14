# TODO — invesco-retention
> Judge Swarm Tier 1 | Updated: 2026-03-14 | Composite: 9.3/10 (weighted)
> Business Priority: 🔴 CRITICAL — $300K Invesco account

## 📊 Score Card (2026-03-14)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 7.5/10 | Clean Next.js/React, demo-grade; minor console.error & DRY cleanup |
| Test Coverage | 3.0/10 | Zero automated tests — ROI/DemoTour/SignalPulse all untested |
| Security | 4.0/10 | 🔴 CRITICAL: real employee names in PUBLIC repo; no auth on demo URL |
| Documentation | 8.0/10 | AUDIT.md, PLAN.md, BRAINSTORM.md, SECURITY.md, deploy instructions |
| Architecture | 8.0/10 | Modern stack (Next.js 15.3, React 19, Tailwind 4, TypeScript) |
| Business Value | 9.5/10 | Direct $300K Invesco account retention at stake |
| **Composite** | **9.3/10** | Weighted by urgency + revenue potential (highest priority project) |

---

## ⚠️ CRITICAL FLAGS

### 🔴 SECURITY — Real Employee Names in Public Repo [STILL OPEN]
- **File:** `demo-app/src/lib/mock-data.ts:383` → "Megan Weber"
- **File:** `demo-app/src/lib/mock-data.ts:406` → "Craig Lieb"
- **File:** `demo-app/src/lib/posthog.ts:3` → "Nathan/Megan to monitor Brian's session"
- **Risk:** If Invesco legal/security discovers this, **deal is dead immediately**
- **Fix:** Make repo PRIVATE or rename to generic personas — 5 minute fix
- **Status:** TODO #321 — ❗ UNFIXED SINCE 2026-03-10

### 🟡 DEMO RISK — No Automated Tests
- ROICalculator.tsx (252 lines), DemoTour.tsx (420 lines), SignalPulse.tsx (155 lines) — all untested
- iPhone mobile PWA not validated on real device
- **Risk:** Live regression during demo with Brian Kiley / Vanessa

---

## P0 — Pre-Demo Blockers (DO NOW)

- [ ] **#321** 🔴 Make repo PRIVATE or rename real employee names (Megan Weber, Craig Lieb)
- [ ] **#380** E2E smoke tests (Playwright) — Home → SF Brief → Dashboard → Create → Mobile
- [ ] **#332** iPhone live test — verify mobile PWA on real device
- [ ] **#333** Executive leave-behind 2-pager (PDF export)
- [ ] **#334** Objection handling scripts (IT security, procurement, data governance)
- [ ] **#429** Security headers + hide Railway URL (custom domain or password-protect)
- [ ] **#430** TypeScript clean build — zero errors before demo day

## P1 — High Value Demo Improvements

- [ ] **#423** Seismic content recommendations in meeting brief
- [ ] **#424** Signal confidence scores — animated probability bars
- [ ] **#425** "Schedule Pilot Webhook" — simulate onboarding trigger
- [ ] **#426** Print-to-PDF button for exec brief
- [ ] **#427** Live AUM input field (editable, updates ROI live)
- [ ] **#428** Pilot timeline widget (Gantt-style visual)
- [ ] **#341** Demo tab setup script (one-click reset + browser tabs)
- [ ] **#632** "Your data here" tooltips on mock advisor data
- [ ] **#381** Demo analytics — PostHog funnel tracking per persona view
- [ ] **#382** "Connect Your Data" toggle (simulated onboarding flow)
- [ ] **#383** Competitor displacement persona — Michael Torres migration

## P2 — Polish

- [ ] **#630** Real fund names in demo data (Invesco-branded content)
- [ ] **#217** Leave-behind package polish (branded, professional)
- [ ] **#218** Support model polish (chat/escalation flows)
- [ ] Remove `console.error` calls in 4 error.tsx files
- [ ] Fix dead `#analytics` link in app launcher
- [ ] Consolidate 4 duplicate `error.tsx` into shared component
- [ ] Type safety pass on combined-data.ts (Zod validation)

## Recently Completed ✅

- [x] **#864** DemoTour.tsx — self-serve narrated demo mode (420 lines) — built 2026-03-11
- [x] **#865** ROICalculator.tsx — interactive ROI calculator (252 lines) — built 2026-03-11
- [x] **#866** SignalPulse.tsx — live signal pulse widget (155 lines) — built 2026-03-11
- [x] **#007** Deployed to Vercel + GitHub Pages ✅
- [x] **#211** Vercel deploy confirmed ✅
- [x] **#213** Salesforce push simulation ✅
- [x] **#214** Invesco branding applied ✅
- [x] **#215** Skeleton loaders ✅
- [x] **#216** Demo reset ✅
- [x] **#631** Global demo reset ✅
- [x] INV-001 through INV-007 complete ✅
- [x] PostHog analytics live ✅
- [x] CVE patched (express-rate-limit) ✅
- [x] Persona URLs working (?demo=megan, ?demo=craig) ✅

---
*Scored by Judge Subagent | 2026-03-14 16:01 UTC | Tier 1*
