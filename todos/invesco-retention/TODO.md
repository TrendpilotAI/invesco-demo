# TODO — invesco-retention
> Judge Swarm Tier 1 | Updated: 2026-03-13 | Score: 8.9/10
> Business Priority: 🔴 CRITICAL — $300K Invesco account

## 📊 Score Card (2026-03-13)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 7.5/10 | Clean Next.js/React, demo-grade, minor console.error cleanup |
| Test Coverage | 3.0/10 | No automated tests — demo app, but E2E smoke tests needed |
| Security | 5.5/10 | CRITICAL: real employee names in public repo; rate-limit CVE in dev only |
| Documentation | 8.0/10 | AUDIT.md, PLAN.md, BRAINSTORM.md, deploy instructions all present |
| Architecture | 8.0/10 | Modern stack (Next.js 16, React 19, Tailwind 4, TypeScript) |
| Business Value | 9.5/10 | Direct $300K Invesco account retention at stake |
| **Composite** | **8.9/10** | Up from 7.2 — Vercel deployed, demo features complete |

---

## ⚠️ CRITICAL FLAGS

### 🔴 SECURITY — Real Employee Names in Public Repo
- **File:** `demo-app/src/lib/mock-data.ts:383,406`
- **Issue:** Real Invesco employees "Megan Weber" and "Craig Lieb" named in PUBLIC GitHub repo
- `posthog.ts` comment references "Nathan/Megan to monitor Brian's session" — business-sensitive
- **Risk:** If Invesco legal/security discovers this, it could derail the $300K deal immediately
- **Fix:** Make repo PRIVATE immediately OR rename personas to generic names
- **Status:** TODO #321 — **DO THIS TODAY**

### 🟡 DEMO RISK — No E2E Smoke Tests
- iPhone mobile demo not tested on real device
- TypeScript errors may still produce broken compiled output
- **Status:** TODO #380, #430

---

## P0 — Pre-Demo Blockers (DO NOW)

- [ ] **#321** 🔴 Make repo PRIVATE (GitHub → Settings → Danger Zone) OR rename real employee names
- [ ] **#864** Self-serve narrated demo mode — auto-advance slides with voiceover
- [ ] **#865** Interactive ROI calculator with AUM input → projected savings
- [ ] **#380** E2E smoke tests (Playwright) before each demo session
- [ ] **#332** iPhone live test — verify mobile PWA works on real device
- [ ] **#333** Executive leave-behind 2-pager (PDF)
- [ ] **#334** Objection handling scripts (IT security, procurement, data governance)
- [ ] **#429** Security headers + hide Railway URL (custom domain or password-protect)
- [ ] **#430** TypeScript clean build — zero errors before demo day

## P1 — High Value Demo Improvements

- [ ] **#423** Seismic content recommendations integration (real-time during demo)
- [ ] **#424** Signal confidence scores — animated probability bars
- [ ] **#425** "Schedule Pilot Webhook" — simulate onboarding trigger
- [ ] **#426** Print-to-PDF button for exec brief
- [ ] **#427** Live AUM input field (editable, updates ROI live)
- [ ] **#428** Pilot timeline widget (Gantt-style visual)
- [ ] **#341** Demo tab setup script (one-click reset + browser tabs)
- [ ] **#632** "Your data here" tooltips on mock advisor data
- [ ] **#631** Global demo reset button — one-click clean state ✅ Done — verify still works
- [ ] **#381** Demo analytics — PostHog funnel tracking per persona view
- [ ] **#382** "Connect Your Data" toggle (simulated, shows onboarding flow)
- [ ] **#383** Competitor displacement persona (migration from incumbent)
- [ ] **#341** Demo tab setup script

## P2 — Polish

- [ ] **#630** Real fund names in demo data (verify Invesco-branded content)
- [ ] **#217** Leave-behind package polish (branded, professional)
- [ ] **#218** Support model polish (chat/escalation flows)
- [ ] **#866** Live Signal Pulse widget (animated real-time metrics)
- [ ] Remove `console.error` calls in error.tsx files (visible in DevTools)
- [ ] Fix dead `#analytics` link in app launcher
- [ ] Consolidate 4 duplicate `error.tsx` files into shared component

## Done (Recent)

- [x] **#007** Deployed to Vercel ✅
- [x] **#211** Vercel deploy confirmed ✅
- [x] **#213** Salesforce push simulation ✅
- [x] **#214** Invesco branding applied ✅
- [x] **#215** Skeleton loaders ✅
- [x] **#216** Demo reset ✅
- [x] **#631** Global demo reset ✅

---
*Scored by Judge Swarm v2 | 2026-03-13 16:00 UTC | Tier 1*
