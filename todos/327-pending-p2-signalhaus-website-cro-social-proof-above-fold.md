# TODO-327: CRO — Social Proof Above the Fold

**Priority:** P2  
**Effort:** 30 min  
**Repo:** signalhaus-website  
**Status:** pending  

## Description
Move the results metrics strip (60-80% reduction, $50M+, 30 days, 100% retention) to appear immediately below the hero CTA buttons. Currently buried after the Services section — visitors leave before seeing it. Proof before pitch = better conversion.

## Coding Prompt (Agent-Executable)

```
In /data/workspace/projects/signalhaus-website/src/app/page.tsx:

1. Move the "results" metrics section (currently after services) to appear
   IMMEDIATELY AFTER the hero CTA buttons, before the badges/social proof section.
   
2. The metrics strip should be compact: 4 metrics in a single horizontal row on desktop,
   2x2 grid on mobile. Each metric: large number, small label underneath.
   Style: subtle, doesn't compete with the hero. Maybe add a thin top border.

3. Add a subtle count-up animation on scroll into view using Intersection Observer:
   - When the section enters viewport, animate the numbers from 0 to their values
   - Use CSS transition or simple JS counter
   - Duration: 1.5s ease-out
   - Only trigger once (mark as seen)

Current order: Hero → Badges → Services → Metrics → Pricing → Testimonials → CTA
Target order:  Hero → Metrics → Badges → Services → Pricing → Testimonials → CTA
```

## Acceptance Criteria
- [ ] Metrics appear before services section
- [ ] Count-up animation on scroll
- [ ] Mobile responsive (2x2 grid)
- [ ] Doesn't break existing layout on any breakpoint

## Dependencies
None
