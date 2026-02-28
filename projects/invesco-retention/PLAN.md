# Invesco Retention — Execution Plan
**Date Updated:** 2026-02-28 (originally 2026-02-26)  
**Deadline:** Early March 2026 (~3-5 days remaining)  
**Stakes:** 🚨 $300K/yr account retention  
**Status (Feb 28):** ✅ DEPLOYED at https://trendpilotai.github.io/invesco-demo/ — critical bugs fixed — awaiting dry run + demo day

## ✅ COMPLETED (as of Feb 28)
- [x] P1.1 — Deployed (GitHub Pages, URL live, returns 200)
- [x] P1.2 — Mobile PWA built and accessible
- [x] P1.3 — Invesco branding applied (TODO-214 done)
- [x] P1.4 — Demo reset mechanism (DemoResetOverlay — TODO-216 done)
- [x] P2.1 — Push-to-Salesforce simulation with toast (TODO-213 done)
- [x] P2.2 — Skeleton loaders + AI animation (TODO-215 done)
- [x] C0 — JSX fragment crash in salesforce/page.tsx fixed
- [x] C1 — Non-null assertion crash in mobile/page.tsx fixed
- [x] Auth middleware security fix
- [x] Next.js CVE patched
- [x] All sales materials written (exec brief, demo script, pilot proposal, ROI, competitive positioning, leave-behind)

## 🔴 CRITICAL PATH (Remaining)

---

## TL;DR — The Critical Path

```
Vercel Deploy → Email Megan+Craig → Dry Run → Demo to Brian Kiley → Pilot Signed
```

Everything else serves this path. Do not let polish block deploy.

---

## Phase 1: Deploy NOW (Today — Day 1)
*Goal: Get a public URL in Megan & Craig's inbox before end of business today.*

### P1.1 — Vercel Deploy [Owner: Honey | 15 min]
```bash
cd /data/workspace/projects/invesco-retention/demo-app
npx vercel --prod
```
- No env vars needed (all static mock data)
- Expected URL: `signal-studio-invesco.vercel.app`
- **Risk:** 🔴 BLOCKS EVERYTHING. Nothing ships until this is done.

### P1.2 — Mobile PWA Verification [Owner: Honey | 10 min]
- Verify mobile-pwa is accessible from the deployed URL
- Test on iOS Safari (Brian Kiley's most likely platform)
- Note any HTTPS/service worker issues

### P1.3 — Invesco Branding Touchpoint [Owner: Honey | 20 min]
- Change org name from "Sales Cloud" → "Invesco Financial Services | Sales Cloud"
- Update in Salesforce chrome component
- Redeploy before sending URL
- **Risk:** 🟠 Without this, demo feels generic. Kelly or Brian will notice.

### P1.4 — Demo Reset Button [Owner: Honey | 20 min]
- Add `?reset=true` URL param handler that clears localStorage/sessionStorage
- Confirm each view returns to pristine state
- **Risk:** 🟠 Live demo with stale state = embarrassing failure

### P1.5 — Email Megan & Craig [Owner: Nathan | 5 min]
Template:
> "Team — we've built everything we discussed. Here's the live demo: [URL]. Can we jump on a 30-min Zoom this week before we show Brian? We want your coaching on which scenarios land best."
- **Risk:** 🔴 Dry run is essential. They know Brian's preferences.

**Phase 1 Definition of Done:**
- [ ] Public HTTPS URL live on Vercel
- [ ] Invesco branding visible in Salesforce view
- [ ] Demo reset working
- [ ] Email sent to Megan & Craig with URL + dry run request

---

## Phase 2: Polish (Days 2-4)
*Goal: Make the demo indistinguishable from a real product.*

### P2.1 — Push-to-Salesforce Simulation [Owner: Honey | 1-2 hrs]
- Add working "Push to Salesforce" button in signal creation flow
- Shows toast: "✅ Task created in Salesforce for Marcus Thompson"
- Button state: disabled → loading → success (with Salesforce checkmark)
- **Risk:** 🟠 High demo impact. Brian expects to see the Salesforce integration work.

### P2.2 — Skeleton Loaders / AI Animation [Owner: Honey | 2-3 hrs]
- Add "AI analyzing signals..." skeleton loader before signal results appear
- 1.5s fake delay → skeleton → content reveal
- Makes the AI intelligence feel real and dynamic
- Priority on mobile view (Brian is mobile-first)
- **Risk:** 🟠 Static data that "just appears" reduces perceived sophistication

### P2.3 — Support Model Polish [Owner: Nathan + Honey | 1 hr]
- Review `/materials/support-model.md`
- Add "dedicated Invesco support engineer" framing
- Answer Kelly's concern about support burden directly
- Add "Ten Decoders" SLA tier with named contacts
- **Risk:** 🟠 Kelly is in the room. Unanswered support questions can derail the deal.

### P2.4 — Demo Recording (Loom) [Owner: Nathan | 2-3 hrs]
- Record all 4 views: Salesforce embed, Signal creation, Territory dashboard, Mobile PWA
- Use demo script from BRAINSTORM.md Section 1.2
- Upload to Loom, get shareable links
- **Risk:** 🔴 If live demo fails (WiFi, Vercel down), recordings are the safety net

### P2.5 — Competitive Displacement Scene [Owner: Honey | 1 hr]
- Ensure "Competitive Intelligence Summary" in demo shows clear Vanguard → Invesco displacement
- Verify Marcus Thompson's scenario shows actionable talking points
- This is the most directly monetizable moment in the demo

**Phase 2 Definition of Done:**
- [ ] Push-to-Salesforce button works convincingly
- [ ] Skeleton loaders on signal results
- [ ] Support model doc polished and ready
- [ ] All 4 views recorded in Loom
- [ ] Competitive displacement scenario validated

---

## Phase 3: Demo Day Prep (Days 5-7)
*Goal: Dry run complete, leave-behind package ready, Brian demo scheduled.*

### P3.1 — Dry Run with Megan & Craig [Owner: Nathan | 30 min Zoom]
- Walk through full 8-minute demo
- Ask: "What's Brian going to push back on?"
- Ask: "Which of these 4 features matters most to him?"
- Incorporate feedback immediately after call

### P3.2 — Leave-Behind Package [Owner: Honey + Nathan | 2 hrs]
Bundle into single email or Notion page:
- Executive brief (PDF — already exists in `/materials/`)
- Loom screen recordings (linked)
- Pilot proposal (PDF — 2 weeks, zero cost, Invesco infra)
- ROI analysis (PDF)
- Live demo URL
- Support model doc (PDF export)
- **Risk:** 🟠 Brian will share this internally. One clean package beats 6 separate emails.

### P3.3 — ElevenLabs Narration (Optional Polish) [Owner: Honey | 2-3 hrs]
- Create narrated version of demo recording using ElevenLabs
- Professional voice, 8-minute runtime
- Attach to leave-behind package as "executive version"
- P2 priority — nice-to-have if time permits

### P3.4 — Custom Domain Setup [Owner: Nathan | 15 min]
- Set up `demo.forwardlane.com` or `signal-studio-demo.forwardlane.com` via DNS
- Configure in Vercel
- Update all materials with clean URL
- P2 priority — worth doing if DNS access is quick

### P3.5 — Demo Day Protocol [Owner: Nathan]
- Open demo on iPad/phone before Brian enters room
- Lead with mobile view first ("Here, take my phone")
- Salesforce view second
- Use `?reset=true` between any repeated runs
- Have Loom recordings queued in browser tab as backup

**Phase 3 Definition of Done:**
- [ ] Dry run with Megan & Craig completed
- [ ] Feedback incorporated
- [ ] Leave-behind package assembled
- [ ] Demo day protocol rehearsed

---

## Dependency Graph

```
[Vercel Deploy]
      │
      ├──► [Email Megan+Craig] ──► [Dry Run] ──► [Brian Demo]
      │
      ├──► [Invesco Branding]
      ├──► [Demo Reset]
      ├──► [Push-to-Salesforce Sim] ──► [Demo Recording]
      ├──► [Skeleton Loaders] ──► [Demo Recording]
      └──► [Support Model Polish] ──► [Leave-Behind Package]

[Demo Recording] ──► [Leave-Behind Package] ──► [Brian Demo]
[ElevenLabs Narration] ──► [Leave-Behind Package]
[Custom Domain] ──► [All Materials URLs]
```

---

## Day-by-Day Schedule

### Day 1 (Today — 2026-02-26) 🔴 CRITICAL
| Time | Task | Owner |
|------|------|-------|
| Morning | Vercel deploy | Honey |
| Morning | Invesco branding patch | Honey |
| Morning | Demo reset button | Honey |
| Midday | Email Megan & Craig | Nathan |
| Afternoon | Push-to-Salesforce simulation | Honey |

### Day 2
| Task | Owner |
|------|-------|
| Skeleton loaders implementation | Honey |
| Support model doc polish | Nathan + Honey |
| Demo script dry run (solo) | Nathan |

### Day 3
| Task | Owner |
|------|-------|
| Demo recording (all 4 views) | Nathan |
| Competitive displacement scene verify | Honey |
| Leave-behind package draft | Honey |

### Day 4
| Task | Owner |
|------|-------|
| Dry run with Megan & Craig | Nathan + Megan + Craig |
| Incorporate feedback | Nathan + Honey |
| Custom domain setup (if time) | Nathan |

### Day 5-6 (Buffer)
| Task | Owner |
|------|-------|
| ElevenLabs narration (optional) | Honey |
| Final leave-behind package | Honey |
| Demo day rehearsal | Nathan |

### Day 7-10 (Target)
| Task | Owner |
|------|-------|
| **DEMO TO BRIAN KILEY** | Nathan |
| Follow up with pilot proposal same day | Nathan + Honey |

---

## Risk Assessment

### 🔴 Deal-Breaking Risks (Must Fix)
| Risk | Mitigation |
|------|-----------|
| Demo app not deployed | P1.1 — Deploy TODAY before anything else |
| Live demo fails (WiFi, Vercel outage) | P2.4 — Loom recordings as backup, always have tab ready |
| Brian can't access demo on his phone | Test on iOS Safari before meeting |
| Kelly raises support burden objection | P2.3 — Polish support model doc, have answer ready |
| No dry run → Nathan goes in blind | P3.1 — Non-negotiable. Don't skip this. |

### 🟠 Deal-Damaging Risks (Should Fix)
| Risk | Mitigation |
|------|-----------|
| Generic "Sales Cloud" branding | P1.3 — Invesco branding (20 min fix) |
| Static data feels fake | P2.2 — Skeleton loaders |
| "Push to Salesforce" doesn't work | P2.1 — Simulation button |
| Post-demo confusion (6 separate docs) | P3.2 — One leave-behind package |

### 🟡 Nice-to-Have (Don't Let Block)
| Risk | Mitigation |
|------|-----------|
| Vercel subdomain looks unprofessional | P3.4 — Custom domain (15 min) |
| No narrated video version | P3.3 — ElevenLabs (if time allows) |

---

## Owner Summary

| Owner | Responsibilities |
|-------|----------------|
| **Honey** 🤖 | Vercel deploy, all code changes (branding, reset, push-to-SF, skeleton loaders), leave-behind package assembly, ElevenLabs narration |
| **Nathan** 👤 | Email Megan+Craig, demo recordings (Loom), dry run Zoom, all human relationship touches, demo day itself |
| **Megan + Craig** 🤝 | Dry run feedback, Brian Kiley personalization intel, internal Invesco relationship management |

---

## Final Sprint — Week of Feb 27

**Status:** Demo live at https://trendpilotai.github.io/invesco-demo/
**Remaining:** Recordings → Dry Run → Demo → Pilot Signed

### Critical Path

```
Email Megan+Craig (TODAY) → Dry Run Zoom (Day 2-3) → Record Loom (Day 2-3) → Demo to Brian (Day 4-7) → Pilot Proposal Signed
```

### Task List

| # | Task | Owner | Effort | Status |
|---|---|---|---|---|
| TODO-219 | Email Megan + Craig with live URL | Nathan | XS | 🔴 URGENT |
| TODO-219 | Schedule dry run Zoom | Nathan | XS | 🔴 URGENT |
| TODO-220 | Record Loom of all 4 views | Honey | M | 🟠 HIGH |
| TODO-221 | Polish leave-behind package | Honey | S | 🟡 MEDIUM |
| TODO-222 | Create demo day checklist | Honey | XS | 🟡 MEDIUM |

### What's DONE ✅
- Synthetic data (10 advisors, 6 data sources)
- Next.js demo app (Salesforce embed, dashboard, signal creation)
- Mobile PWA (iOS Safari compatible)
- Salesforce LWC package
- Leave-behind materials (draft)
- Push-to-Salesforce simulation (toast notification)
- Invesco branding in Salesforce chrome
- Skeleton loaders + AI analysis animation
- Demo reset (?reset=true URL param)
- Deployed to GitHub Pages
- Critical bugs fixed (JSX parse error, non-null crash)

### Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Live demo connection drops | Medium | High | Pre-recorded Loom backups (TODO-220) |
| Stale state confuses demo | Medium | Medium | Reset button + checklist (TODO-222) |
| Brian schedules short meeting | Low | High | Lead with Salesforce view (most compelling) |
| Internal politics shift | Low | High | Megan + Craig dry run (TODO-219) |
| Mobile rendering bug | Low | High | Test on real iPhone, have desktop fallback |
