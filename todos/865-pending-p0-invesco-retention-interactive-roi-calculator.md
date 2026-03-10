# TODO #865: Interactive Invesco ROI Calculator

**Priority:** P0 (pre-demo)
**Effort:** S (2 hours)
**Repo:** invesco-retention
**Source:** BRAINSTORM.md v2, Category 1.2

## Context

The existing homepage has a before/after panel with static ROI stats. Finance stakeholders (Brian's manager, procurement) need to see hard math with their own numbers. An interactive calculator lets them plug in Invesco's actual scale and see the dollar impact.

## Description

Expand the existing before/after ROI panel into an interactive calculator with sliders/inputs for key variables. Pre-populated with Invesco scale defaults (450 wholesalers, 3 meetings/day, 47 min saved). Should make the value undeniable in < 30 seconds.

## Acceptance Criteria
- [ ] Existing before/after panel expands to reveal calculator on "Calculate for your team →" click
- [ ] Three input controls:
  - Wholesalers: slider 50–1000, default 450
  - Meetings per day: slider 1–6, default 3
  - Minutes saved per meeting: slider 15–90, default 47
- [ ] Three output metrics (large, bold, animated count-up):
  - Hours saved per week: (wholesalers × meetings × minutes_saved) / 60
  - Annual value: hours/week × 52 × $150 blended rate
  - AUM protected: estimated based on at-risk advisors surfaced
- [ ] "Invesco Scale" preset button resets to 450 / 3 / 47
- [ ] Mobile responsive
- [ ] At Invesco defaults: shows "1,048 hrs/week" + "$8.2M annual value"

## Implementation Prompt

```
Expand the ROI panel in /data/workspace/projects/invesco-retention/demo-app/src/app/page.tsx

1. Add state for calculator: { wholesalers: 450, meetingsPerDay: 3, minutesSaved: 47, expanded: false }

2. Add "Calculate for your team →" button below existing before/after content
   - On click: setExpanded(true) with smooth height animation (max-h transition)

3. Calculator section (shown when expanded):

   Three slider inputs with labels and live value display:
   - "Number of wholesalers" — range 50-1000, step 10
   - "Meetings per day" — range 1-6, step 1  
   - "Minutes saved per meeting prep" — range 15-90, step 5

   Calculated outputs (update instantly as sliders move):
   const hoursPerWeek = (wholesalers * meetingsPerDay * minutesSaved * 5) / 60
   const annualValue = hoursPerWeek * 52 * 150  // $150/hr blended rate
   const aumProtected = wholesalers * 0.08 * 2200000  // 8% of advisors at-risk, avg $2.2M

   Display in 3-column grid:
   - "Hours reclaimed per week" — show formatted number with count-up animation
   - "Annual efficiency value" — show as $X.XM with count-up
   - "AUM protected annually" — show as $XXM with count-up

   "Invesco Scale" preset button (small, below sliders) — resets to 450/3/47

4. Styling:
   - Use existing Tailwind classes and color palette
   - Slider track: blue-600, thumb: white with blue border
   - Output numbers: text-3xl font-bold text-blue-600
   - Labels: text-sm text-gray-500

5. Count-up animation: use a simple useEffect with requestAnimationFrame or 
   a CSS transition on a numeric display — keep it < 20 lines
```

## Dependencies
- None

## Estimated Effort
- 1.5-2 hours
