# TODO #864: Self-Serve Narrated Demo Mode

**Priority:** P0 (pre-demo — CRITICAL)
**Effort:** M (3-4 hours)
**Repo:** invesco-retention
**Source:** BRAINSTORM.md v2, Category 1.1

## Context

Brian Kiley and Vanessa (the actual decision-makers) may view the demo WITHOUT Nathan present. The demo currently requires a live guide to explain what they're seeing. Without a self-serve narration mode, solo viewing yields a polished but confusing demo.

## Description

Build a guided tour / narrated demo mode that auto-advances through key screens with animated callout tooltips, narrating ROI context at each step. User can click through manually or let it auto-advance. Perfect for leave-behind or trade show use.

## Acceptance Criteria
- [ ] Floating "▶ Start Demo" button (bottom-right, pulsing animation) on homepage
- [ ] Clicking launches narrated overlay mode
- [ ] Step 1: Homepage ROI panel — "Meet Sarah, a wholesaler who saves 47 minutes per meeting"
- [ ] Step 2: Salesforce view — "Signal Studio surfaces 6 data sources in one glance"
- [ ] Step 3: Meeting brief signals — "Urgent: $500K competitor displacement detected"
- [ ] Step 4: Dashboard — "Territory view: 4 advisors need attention this week"
- [ ] Step 5: Signal Studio — "Create a custom signal in natural language"
- [ ] Step 6: Mobile — "Works on iPhone — for Brian's mobile-first vision"
- [ ] Each step: highlighted element with tooltip callout, ROI stat, and "Next →" button
- [ ] Auto-advances every 8 seconds if no interaction
- [ ] Keyboard: Right arrow = next, Left = back, Escape = exit
- [ ] Works on mobile (responsive overlay)
- [ ] Demo-mode persists across page navigation (stores progress in sessionStorage)

## Implementation Prompt

```
Build a self-serve narrated demo mode for /data/workspace/projects/invesco-retention/demo-app/

### Step 1: Create demo script config
File: src/lib/demo-script.ts

export interface DemoStep {
  id: string;
  route: string;           // URL path to navigate to
  targetSelector: string;  // CSS selector for highlighted element
  title: string;           // Tooltip headline
  body: string;            // Explanation text
  roiStat: string;         // Bold ROI callout (e.g., "47 min saved per meeting")
  duration: number;        // Auto-advance time in ms (default 8000)
}

export const DEMO_STEPS: DemoStep[] = [
  {
    id: 'intro',
    route: '/',
    targetSelector: '.roi-impact-panel',  // The Before/After panel
    title: 'From Reports to Revenue',
    body: 'Invesco wholesalers currently spend 47 minutes manually prepping for each advisor meeting. Signal Studio reduces that to 3 minutes.',
    roiStat: '93% time reduction on meeting prep',
    duration: 8000,
  },
  {
    id: 'salesforce',
    route: '/salesforce?demo=megan',
    targetSelector: '.signal-list',
    title: 'Meeting Brief in Salesforce',
    body: 'Signal Studio surfaces insights from 6 data sources — CRM activities, Snowflake transactions, Seismic content, digital engagement, holdings, and market data — in one compact panel.',
    roiStat: '6 data sources → 1 actionable brief',
    duration: 10000,
  },
  {
    id: 'signals',
    route: '/salesforce?demo=megan',
    targetSelector: '.urgent-signal',
    title: 'Competitor Displacement Alert',
    body: 'Real-time signal: Jennifer Martinez is moving $500K to American Funds. Without Signal Studio, this would be discovered after the assets left.',
    roiStat: '$500K retention opportunity — caught in time',
    duration: 8000,
  },
  {
    id: 'dashboard',
    route: '/dashboard?demo=megan',
    targetSelector: '.advisor-risk-table',
    title: 'Territory Intelligence at a Glance',
    body: 'Territory dashboard shows which advisors need immediate attention this week, ranked by risk score and AUM at stake.',
    roiStat: '4 advisors flagged this week = $2.3M protected',
    duration: 8000,
  },
  {
    id: 'create',
    route: '/create?demo=megan',
    targetSelector: '.signal-input',
    title: 'Natural Language Signal Studio',
    body: 'Type what you want to know in plain English. Signal Studio writes the query, surfaces the data, and delivers results to 450 wholesalers in seconds.',
    roiStat: 'No SQL. No data team. Just results.',
    duration: 8000,
  },
  {
    id: 'mobile',
    route: '/mobile?demo=megan',
    targetSelector: '.mobile-brief-header',
    title: 'Mobile-First for Brian\'s Vision',
    body: 'Full meeting brief on iPhone — designed for wholesalers in the field. Check signals before walking into any advisor office.',
    roiStat: 'Works on any device, anywhere',
    duration: 8000,
  },
];
```

### Step 2: Create DemoNarrator component
File: src/components/DemoNarrator.tsx

```tsx
'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { DEMO_STEPS } from '@/lib/demo-script';

// Floating launch button (shown when not in demo mode)
// Overlay with spotlight highlight + tooltip callout
// Progress dots at bottom
// Keyboard navigation (←→ Escape)
// Auto-advance timer with pause on hover
// sessionStorage: persists demo step across route navigations
```

### Step 3: Integrate into layout
File: src/app/layout.tsx

Add <DemoNarrator /> before closing </body>. It renders the floating button globally and manages routing.

### Design guidelines:
- Button: fixed bottom-right, 56px circle, bg-blue-600, white play icon, subtle pulse ring
- Overlay: dark backdrop 40% opacity behind target element
- Spotlight: 4px blue ring around target element, drop shadow
- Tooltip: white card, positioned above/below target, max-w-sm
  - Headline in semibold, body in sm, ROI stat in bold blue
  - Previous / Next buttons + step counter "2 of 6"
  - "Exit Demo" link top-right of tooltip
- Progress: 6 dots at bottom center of screen, active dot = filled blue
```

## Dependencies
- None — can be built in parallel with any other work

## Estimated Effort
- 3-4 hours for a focused implementation
- Can be simplified to 2h if tooltip positioning is simplified (always bottom of screen vs. anchored to element)
