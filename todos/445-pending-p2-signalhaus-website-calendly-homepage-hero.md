# TODO-445: Calendly Inline Embed on Homepage Hero

**Repo:** signalhaus-website  
**Priority:** P2 (CRO)  
**Effort:** S (~1 hour)  
**Status:** pending

## Description
Calendly is currently only on the /contact page. Enterprise buyers who land on the homepage and want to book a call must navigate away. Add a "Book a 15-min call" section directly on the homepage to reduce friction from homepage → meeting.

## Acceptance Criteria
- [ ] Homepage has a Calendly inline embed section (below services or in CTA section)
- [ ] OR a sticky floating "Book a Call" button in the bottom-right corner (opens Calendly popup)
- [ ] Uses existing `NEXT_PUBLIC_CALENDLY_URL` env var
- [ ] Calendly popup/embed loads lazily (no performance impact on initial page load)
- [ ] Mobile-responsive

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/src/app/page.tsx:

Option A (Sticky Button — recommended for UX):
1. Add a sticky "Book a Free Call" button fixed at bottom-right (z-50)
   Clicking opens the Calendly popup (use the existing Calendly component or 
   window.Calendly.initPopupWidget pattern)
2. Style: bg-indigo-600 text-white rounded-full px-6 py-3 shadow-lg hover:bg-indigo-500
3. Load Calendly popup script lazily via next/script with strategy="lazyOnload"

Option B (Inline section — more prominent):
1. Add a new section between Testimonials and Footer:
   <section> "Ready to see AI in action? Book a 30-minute strategy call — free."
   Embed Calendly inline widget using Calendly's inline embed code.

Use NEXT_PUBLIC_CALENDLY_URL env var. Add to .env.example if not already there.
```
