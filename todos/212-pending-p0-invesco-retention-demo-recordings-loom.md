# 212 — Invesco Retention: Record Demo Views (Loom) (P0)

**Priority:** 🔴 P0 — Safety net if live demo fails  
**Project:** invesco-retention  
**Effort:** S (2-3 hrs including setup)  
**Owner:** Nathan (screen recorder) + Honey (script prep)  
**Dependencies:** 211 (Vercel deploy must be live first)

---

## Task Description

Record all 4 demo views as Loom screen recordings using the deployed public URL. These serve as:
1. **Backup** — if live demo fails (WiFi, Vercel outage), play recordings
2. **Leave-behind** — share Loom links in the post-demo package
3. **Internal alignment** — let Megan & Craig preview before dry run

The 8-minute demo follows a tight narrative arc. Nathan should drive the recording with the demo script.

---

## Demo Script (for Recording)

### Scene 1 — Hook (30s)
Open Salesforce view. Say: "Here's what a Marcus Thompson — one of your top wholesalers — sees tomorrow morning before his 9am advisor meeting."

### Scene 2 — Salesforce Embed (2 min)
- Show the ForwardLane panel embedded in Salesforce
- Walk through: signals list, confidence scores, AI-generated talking points
- Highlight the Vanguard displacement signal for the target advisor

### Scene 3 — Signal Creation (2 min)
- Navigate to /signals
- Type a natural language query: "Show me advisors in the Southeast who haven't allocated to Invesco funds in 90+ days"
- Pause for skeleton loader / "AI analyzing..." animation
- Results appear: ranked advisor list
- Click "Push to Salesforce" → toast: "✅ Task created in Salesforce for Marcus Thompson"

### Scene 4 — Territory Dashboard (1 min)
- Navigate to /territory
- Quick filter by channel (Wirehouse), sort by AUM
- Show the geographic heat map or list view

### Scene 5 — Mobile (1 min)
- Switch to phone (or use browser DevTools mobile emulation)
- Open mobile PWA view
- Swipe through signal cards
- Say: "Same brief, optimized for mobile — Brian can review this before any meeting"

### Scene 6 — Close (1.5 min)
- Return to Salesforce view
- "We're proposing a 2-week pilot at no cost, running inside your existing Salesforce infrastructure. Megan and Craig can speak to the technical requirements."

---

## Recording Instructions

1. Deploy URL must be live (TODO 211)
2. Open Loom (loom.com) — use Nathan's account
3. Record each view as a SEPARATE Loom (easier to share individual pieces)
4. Also record ONE combined 8-minute run-through
5. Upload all recordings
6. Save all Loom URLs to `/data/workspace/projects/invesco-retention/RECORDING_URLS.md`

---

## Acceptance Criteria
- [ ] Salesforce view recorded (Loom link saved)
- [ ] Signal creation recorded (includes Push-to-SF moment)
- [ ] Territory dashboard recorded
- [ ] Mobile view recorded
- [ ] Full 8-min combined recording done
- [ ] All URLs saved to RECORDING_URLS.md
- [ ] Recordings are shareable (not private)
