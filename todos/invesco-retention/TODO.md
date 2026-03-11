# TODO — invesco-retention
> Judge Swarm Tier 1 | Updated: 2026-03-11 | Score: 7.2/10
> Business Priority: 🔴 CRITICAL — $300K Invesco account

## ⚠️ CRITICAL FLAGS

### 🔴 SECURITY — Real Employee Names in Public Repo
- **File:** `demo-app/src/lib/mock-data.ts:383,406`
- **Issue:** Real Invesco employees "Megan Weber" and "Craig Lieb" named in PUBLIC GitHub repo
- `posthog.ts` comment references "Nathan/Megan to monitor Brian's session" — business-sensitive
- **Risk:** If Invesco discovers this, it could derail the $300K deal
- **Fix:** Make repo PRIVATE immediately OR rename personas to "Alex Johnson"/"Taylor Smith"
- **Status:** TODO #321

---

## P0 — Pre-Demo Blockers

- [ ] **#321** Make `TrendpilotAI/invesco-demo` repo PRIVATE (or rename real employee names) — SECURITY
- [ ] **#864** Self-serve narrated demo mode — auto-advance slides with voiceover
- [ ] **#865** Interactive ROI calculator with AUM input → projected savings
- [ ] **#380** E2E smoke tests before each demo session
- [ ] **#332** iPhone live test — verify mobile PWA works on real device
- [ ] **#333** Executive leave-behind 2-pager (PDF)
- [ ] **#334** Objection handling scripts for IT security, procurement, data governance
- [ ] **#429** Security headers + hide Railway URL (set custom domain or password)
- [ ] **#430** TypeScript clean build — zero errors before demo

## P1 — High Value Improvements

- [ ] **#423** Seismic content recommendations integration (real-time during demo)
- [ ] **#424** Signal confidence scores — animated probability bars
- [ ] **#425** "Schedule Pilot Webhook" — simulate onboarding trigger
- [ ] **#426** Print-to-PDF button for exec brief
- [ ] **#427** Live AUM input field (editable, updates ROI calculations live)
- [ ] **#428** Pilot timeline widget (Gantt-style visual)
- [ ] **#341** Demo tab setup script (one-click reset + browser tabs)
- [ ] **#632** "Your data here" tooltips on mock advisor data
- [ ] **#631** Global demo reset button — one-click clean state
- [ ] **#381** Demo analytics — PostHog funnel tracking per persona view
- [ ] **#382** "Connect Your Data" toggle (simulated, shows onboarding flow)
- [ ] **#383** Competitor displacement persona (migration from incumbent)

## P2 — Polish

- [ ] **#630** Real fund names in demo data (verify Invesco-branded content)
- [ ] **#217** Leave-behind package polish (branded, professional)
- [ ] **#218** Support model polish (chat/escalation flows)
- [ ] **#866** Live Signal Pulse widget (animated real-time metrics)
- [ ] Remove `console.error` calls in error.tsx files (visible in DevTools)
- [ ] Fix dead `#analytics` link in app launcher

## Done (Recent)

- [x] **#007** Deployed to Vercel ✅
- [x] **#211** Vercel deploy confirmed ✅  
- [x] **#213** Salesforce push simulation ✅
- [x] **#214** Invesco branding applied ✅
- [x] **#215** Skeleton loaders ✅
- [x] **#216** Demo reset ✅
- [x] **#631** Global demo reset ✅
