# TODO — invesco-retention
> Judge Swarm | Updated: 2026-03-15 16:00 UTC | Composite: 6.5/10 (weighted)
> Business Priority: 🔴 CRITICAL — $300K Invesco account retention

## 📊 Score Card (2026-03-15)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 7.5/10 | Clean Next.js 16/React 19/Tailwind 4/TypeScript; minor console.error & DRY cleanup |
| Test Coverage | 1.0/10 | 🔴 ZERO automated tests — ROI/DemoTour/SignalPulse all untested |
| Security | 2.5/10 | 🔴 CRITICAL: real employee names in PUBLIC repo; no auth on demo URL |
| Documentation | 8.5/10 | Excellent: AUDIT.md, PLAN.md, BRAINSTORM.md, deploy instructions |
| Architecture | 8.0/10 | Modern stack, clean component structure, proper TypeScript |
| Business Value | 9.5/10 | Direct $300K Invesco account retention at stake |
| **Composite** | **6.5/10** | Weighted: 30% biz, 25% security, 15% code, 15% arch, 10% test, 5% docs |

---

## 🚨 CRITICAL FLAGS

### 🔴 SECURITY — Real Employee Names in Public Repo [UNFIXED SINCE 2026-03-10]
- **File:** `demo-app/src/lib/mock-data.ts:383` → "Megan Weber"
- **File:** `demo-app/src/lib/mock-data.ts:406` → "Craig Lieb"
- **File:** `demo-app/src/lib/posthog.ts:3` → mentions "Nathan/Megan to monitor Brian's session"
- **Risk:** If Invesco legal/security discovers this, **deal is dead immediately**
- **Fix:** Make repo PRIVATE or rename to generic personas — 5 minute fix
- **Status:** TODO #321 — ❗ UNFIXED FOR 5 DAYS

### 🔴 ZERO TEST COVERAGE
- No Playwright, Jest, or any test files in project src
- 880-line mock-data.ts untested; ROICalculator (252 lines), DemoTour (420 lines), SignalPulse (155 lines) — all untested
- **Risk:** Any deployment could silently break demo before client viewing

---

## P0 — Pre-Demo Blockers (DO NOW)

- [ ] **#321** 🔴 Make repo PRIVATE or rename real employee names (Megan Weber, Craig Lieb) — **5 min fix, 5 days overdue**
- [ ] **#380** E2E smoke tests (Playwright) — Home → SF Brief → Dashboard → Create → Mobile — **2-3 hours**
- [ ] **#332** iPhone live test — verify mobile PWA on real device — **30 min**
- [ ] **#333** Executive leave-behind 2-pager (PDF export) — **1-2 hours**
- [ ] **#334** Objection handling scripts (IT security, procurement, data governance) — **1-2 hours**
- [ ] **#429** Security headers + password-protect demo URL — **30 min**
- [ ] **#430** TypeScript clean build — zero errors before demo day — **30 min**

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

## P2 — Polish & Cleanup

- [ ] Remove `console.error` calls in 4 error.tsx files — **15 min**
- [ ] Fix dead `#analytics` link in app launcher — **15 min**
- [ ] Consolidate 4 duplicate `error.tsx` into shared component — **30 min**
- [ ] Type safety pass on combined-data.ts (Zod validation) — **1 hour**
- [ ] Split mock-data.ts (880 lines) into domain-specific modules — **1 hour**
- [ ] Bundle size audit (`ANALYZE=true pnpm build`) — **30 min**
- [ ] Lighthouse score audit (target 95+ perf, 100 a11y) — **30 min**
- [ ] **#630** Real fund names in demo data (Invesco-branded content)
- [ ] **#217** Leave-behind package polish (branded, professional)
- [ ] **#218** Support model polish (chat/escalation flows)

## Recently Completed ✅

- [x] **#864** DemoTour.tsx — self-serve narrated demo mode (420 lines)
- [x] **#865** ROICalculator.tsx — interactive ROI calculator (252 lines)
- [x] **#866** SignalPulse.tsx — live signal pulse widget (155 lines)
- [x] INV-001 through INV-007 all complete
- [x] PostHog analytics live
- [x] CVE patched (commit 036a20c)
- [x] Persona URLs (?demo=megan, ?demo=craig) working
- [x] Deployed to Vercel + GitHub Pages

---

## Quick Score Improvement Path
| Action | Time | Score Impact |
|--------|------|-------------|
| Make repo private | 5 min | Security 2.5 → 6.0, Composite +0.9 |
| Add Playwright smoke tests | 3 hours | Test 1.0 → 5.0, Composite +0.4 |
| Remove console.error + dead links | 30 min | Code Quality 7.5 → 8.0, Composite +0.1 |
| **Total** | **~3.5 hours** | **Composite 6.5 → 7.9** |

---
*Assessed by Judge Subagent | 2026-03-15 16:00 UTC*
