# TODO #866: Live Signal Pulse — Real-Time Signals on Dashboard

**Priority:** P1
**Effort:** M (2-3 hours)
**Repo:** invesco-retention
**Source:** BRAINSTORM.md v2, Category 1.3

## Description

Add timer-driven signals appearing in real-time on the dashboard to create the feeling of a live, breathing system rather than a static HTML mockup. Signals cycle through a queue and appear with subtle animation, simulating a live data feed.

## Acceptance Criteria
- [ ] Dashboard page shows a "Live Feed" ticker or sidebar section
- [ ] New signal appears every 12-20 seconds (randomized interval)
- [ ] Signals cycle from a curated queue of 10-15 synthetic signals
- [ ] Each signal has: advisor name, signal type, colored badge, timestamp ("just now" / "2m ago")
- [ ] New signals appear at top with slide-in animation; old ones fade down
- [ ] Max 5 signals visible; 6th pushes oldest off
- [ ] Can be paused by hovering (natural UX)
- [ ] "Live" dot indicator (pulsing green) in section header

## Example Signals
```
🔴 Jennifer Martinez increased ETF allocation 23% this quarter
🟡 Robert Chen hasn't had a meeting in 47 days — $3.2M relationship
🟢 Sarah Williams opened 3 thought leadership pieces this week
🔴 Michael Torres: $500K position moving to American Funds
🟡 David Kim's practice AUM grew 18% — no corresponding Invesco increase
```

## Implementation Prompt

```
Add live signal pulse to /data/workspace/projects/invesco-retention/demo-app/src/app/dashboard/page.tsx

1. Create a LIVE_SIGNALS array in mock-data.ts (or inline):
   type LiveSignal = {
     id: string;
     advisorName: string;
     text: string;
     severity: 'urgent' | 'attention' | 'positive';
     timestamp: Date; // set dynamically
   }

2. Create useLiveSignals hook in src/lib/use-live-signals.ts:
   - Initializes with 3 signals visible
   - useInterval: every 12-20 seconds (random), prepend a new signal from queue
   - Cycles through LIVE_SIGNALS pool in random order (no repeats until all shown)
   - Pauses when document is hidden (visibility API)
   - Returns: { signals: LiveSignal[], isPaused, togglePause }

3. Add "Signal Feed" panel to dashboard:
   - Header: "● Live Signal Feed" (pulsing green dot using CSS animation)
   - List of max 5 signals, newest first
   - Each signal: colored left border (red/yellow/green), advisor name bold, signal text sm, "just now" / "Xm ago"
   - Slide-in animation: translate-y-[-8px] → translate-y-0 with opacity 0→1 over 400ms
   - Hover: pauses signal advancement

4. Position: right sidebar on desktop, full-width section on mobile
```

## Dependencies
- None

## Estimated Effort
- 2-3 hours
