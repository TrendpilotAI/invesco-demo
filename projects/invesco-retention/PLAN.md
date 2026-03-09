# PLAN.md — Invesco Retention Execution Plan
*Updated by Judge Agent v2 | 2026-03-09*

## Architecture Overview

The Invesco retention demo is a **static Next.js 16 app** deployed on GitHub Pages at `trendpilotai.github.io/invesco-demo`.

```
/demo-app (Next.js 16, React 19, Tailwind 4, TypeScript)
  /src/app
    /salesforce    → Meeting Brief (HERO — Salesforce embedded view)
    /dashboard     → Territory Dashboard
    /create        → Signal Studio creation
    /mobile        → Mobile meeting brief
  /src/lib
    mock-data.ts       → Advisor personas, signals, metrics (880 lines)
    constants.ts       → Config values
    demo-reset.ts      → Demo state management
    posthog.ts         → Analytics
    /data
      combined-data.ts → Aggregates all synthetic data sources
      types.ts         → Shared TypeScript types
  /src/components
    DemoResetOverlay.tsx  → Demo reset with keyboard shortcut
    DemoErrorFallback.tsx → Shared error UI (used by all error.tsx)
    ErrorBoundary.tsx     → Global error boundary
    slds-icons.tsx        → Salesforce Lightning DS icons
    slds-patterns.tsx     → SLDS layout patterns
    /ui                   → shadcn component library

/mobile-pwa        → Standalone PWA (separate codebase)
/salesforce-lwc    → Salesforce LWC package for real SF deploy
/synthetic-data    → Python scripts + JSON seed data
/materials         → Sales collateral (exec brief, competitive landscape, demo script)
```

**Deployment:** `next build` → static export → GitHub Pages auto-deploy
**Demo URL:** https://trendpilotai.github.io/invesco-demo/
**Persona URLs:** ?demo=megan | ?demo=craig

---

## Phase 1: Demo Win (Days 1-3) 🔴 CRITICAL

### Task 1.1: Self-Serve Narrated Demo Mode
**Goal:** Demo runs without Nathan present — Brian/Vanessa can explore solo
- New component: `src/components/DemoNarrator.tsx`
  - Floating "▶ Start Demo" button (bottom-right, pulsing)
  - Overlay with tooltip callouts on key UI elements
  - Auto-advance every 6 seconds OR manual click-through
  - Step-by-step script in `src/lib/demo-script.ts`
- Script covers: Home → Salesforce Brief → Key Signals → Dashboard → Mobile
- Each step has: `targetSelector`, `calloutText`, `roiHighlight`
- **Dependencies:** None
- **Effort:** 4 hours
- **Acceptance:** Demo auto-runs full flow; user can pause/resume; works on mobile

### Task 1.2: Invesco ROI Calculator
**Goal:** Quantified ROI for finance stakeholders
- Expand existing before/after panel in `src/app/page.tsx`
- Add interactive sliders: # wholesalers, meetings/day, current prep time
- Outputs: hours saved/week, $ value at $150/hr blended rate, annual AUM impact
- Preset: "Invesco Scale" — 450 wholesalers, 3 meetings/day, 47 min saved
- **Dependencies:** None
- **Effort:** 2 hours
- **Acceptance:** Calculator shows ≥$1M value for Invesco at default settings

### Task 1.3: Dry Run with Megan & Craig
**Goal:** Internal champions validate demo before Brian/Vanessa viewing
- Schedule 30-min Zoom with Megan and Craig
- Walk through ?demo=megan and ?demo=craig scenarios
- Get feedback: what's missing, what lands, what to skip
- **Dependencies:** Task 1.1 complete
- **Effort:** 2 hours (prep + call)
- **Acceptance:** Megan/Craig sign off; feedback incorporated

### Task 1.4: Leave-Behind Screen Recordings
**Goal:** Demo insurance + async leave-behind
- Record Loom walkthroughs: Salesforce view (3min), Dashboard (2min), Signal Studio (2min)
- Host as unlisted Loom; embed links in leave-behind one-pager
- **Dependencies:** None
- **Effort:** 1 hour
- **Acceptance:** 3 recordings available; links in materials/leave-behind.md

### Task 1.5: Ten Decoders Support One-Pager
**Goal:** Address bench depth concern Craig raised
- Create `materials/ten-decoders-support.md`
- Content: team bios, relevant certifications, SLA: < 4hr response, dedicated Slack channel
- Export to PDF; include in leave-behind package
- **Dependencies:** None
- **Effort:** 2 hours
- **Acceptance:** PDF sent to Craig before demo with Brian

---

## Phase 2: Demo Hardening (Days 4-7) 🟡 IMPORTANT

### Task 2.1: PostHog Analytics Events
**Goal:** Know when Brian/Vanessa view the demo
- Add custom events to existing PostHog setup (`src/lib/posthog.ts`):
  - `demo_view` with route + persona props
  - `demo_roi_expanded`
  - `demo_narration_started` / `demo_narration_completed`
- Configure PostHog webhook → Slack notification for `?demo=megan` views
- **Dependencies:** None
- **Effort:** 1 hour
- **Acceptance:** Nathan gets Slack ping when demo URL is visited

### Task 2.2: Playwright E2E Tests
**Goal:** Regression protection before every deploy
- `demo-app/playwright.config.ts` + `tests/demo-happy-path.spec.ts`
- Test: Home loads → ?demo=megan Salesforce view → check signals render → Dashboard → Create → Mobile
- Assert: no console errors, key elements visible, ROI panel expandable
- Add to GitHub Actions: `pnpm test` before deploy
- **Dependencies:** None
- **Effort:** 3 hours
- **Acceptance:** Tests pass on CI; fail if any route 404s or shows error

### Task 2.3: Live Signal Pulse
**Goal:** Dashboard feels alive, not static
- Add `useEffect` with setInterval in `src/app/dashboard/page.tsx`
- Every 8 seconds: new "incoming signal" banner slides in from top
- 5-10 pre-written signal templates cycling through
- Subtle animation — not distracting, but shows data is flowing
- **Dependencies:** None
- **Effort:** 3 hours
- **Acceptance:** Signal appears every ~8s; doesn't break demo flow; dismissable

---

## Phase 3: Polish & Cleanup (Days 8-14) 🟢 NICE TO HAVE

### Task 3.1: Error Page DRY Cleanup
- Add `context` prop to DemoErrorFallback
- Update all 4 error.tsx files to pass context string instead of console.error
- **Effort:** 30 minutes

### Task 3.2: Remove #analytics Dead Route
- Remove from app launcher or add simple placeholder analytics page
- **Effort:** 15 minutes

### Task 3.3: Bundle Size Audit
- Run `ANALYZE=true next build`; check vendor chunks
- Target: < 200kb initial JS, > 95 Lighthouse performance
- **Effort:** 30 minutes + fixes

### Task 3.4: Public Repo Audit
- Review `TrendpilotAI/invesco-demo` for sensitive content
- Ensure Invesco employee names used only in ?demo= context (not hardcoded public paths)
- **Effort:** 30 minutes

---

## Dependency Graph

```
1.1 (Narrated Demo) ──→ 1.3 (Dry Run with Megan/Craig)
1.2 (ROI Calc)      ──→ 1.3
1.4 (Recordings)    ──→ 1.5 (Ten Decoders One-Pager) ──→ Leave-Behind Package
2.1 (Analytics)     ──→ (independent, deploy anytime)
2.2 (Playwright)    ──→ 2.x (all subsequent deploys protected)
2.3 (Live Signals)  ──→ (independent)
```

## Recommended Execution Order

1. **Today:** Task 1.2 (ROI Calc) + Task 1.4 (Recordings) — fast wins, high impact
2. **Tomorrow:** Task 1.1 (Narrated Demo) — biggest differentiator
3. **Day 3:** Task 1.5 (Ten Decoders) + Schedule Megan/Craig dry run
4. **Day 4-5:** Task 2.1 (Analytics) + Task 2.3 (Live Signals)
5. **Day 6:** Task 2.2 (Playwright CI)
6. **Days 8-14:** Phase 3 polish as time allows

## Risk Assessment

| Risk | Likelihood | Mitigation |
|---|---|---|
| Brian views demo without Nathan | High | Task 1.1 (self-serve narration) |
| Live demo tech failure | Medium | Task 1.4 (recordings as backup) |
| Demo regression after update | Medium | Task 2.2 (Playwright CI) |
| Internal champion loses influence | Low | Task 1.5 + dry run with Craig |
| Decision delay beyond 2 weeks | Medium | Analytics to know when to follow up |
