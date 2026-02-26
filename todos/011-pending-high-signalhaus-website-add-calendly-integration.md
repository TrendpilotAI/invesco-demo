---
status: pending
priority: p1
issue_id: "011"
tags: [nextjs, calendly, booking, conversion, signalhaus-website]
dependencies: ["010"]
---

# Add Calendly Booking Integration to Contact Page

## Problem Statement

Prospects visiting the contact page must fill out a form and wait for a callback, adding friction to the conversion funnel. High-intent prospects (those ready to book now) may bounce if they can't immediately self-schedule. Adding a Calendly embed provides a direct "book now" path alongside the contact form, reducing friction and capturing warmer leads.

## Findings

- Contact page (`src/app/contact/page.tsx`) has only a form — no booking option
- No Calendly URL or booking link anywhere on the site
- BRAINSTORM.md rates this P1 / HIGH impact / Small effort
- The auto-reply email in TODO 010 references a Calendly link — this TODO delivers the actual widget
- `react-calendly` is the standard npm package for embedding Calendly in React apps

## Proposed Solutions

### Option 1: Inline Calendly Embed (Recommended)

**Approach:** Use `react-calendly` `InlineWidget` below the contact form. User sees both options: "Send a message" OR "Book directly."

**Pros:**
- Best UX — user never leaves the page
- Calendly handles scheduling, reminders, Zoom links automatically
- High-intent leads can book immediately

**Cons:**
- Adds ~50KB JS weight from react-calendly
- Requires Nathan to have a Calendly account with a public booking URL

**Effort:** 2-3 hours

**Risk:** Low

---

### Option 2: Popup/Modal Calendly Widget

**Approach:** Use `react-calendly` `PopupButton` — "Book a Call" button opens Calendly in a modal overlay.

**Pros:**
- Less page weight (widget loads on demand)
- Cleaner layout

**Cons:**
- Popup blocker risk
- Extra click to initiate

**Effort:** 2 hours

**Risk:** Low

---

### Option 3: Simple Link to Calendly

**Approach:** Add a "Book directly on Calendly →" link/button that opens Calendly in a new tab.

**Pros:**
- Zero dependencies, zero JS weight
- Works immediately

**Cons:**
- User leaves the site
- Less integrated experience

**Effort:** 30 minutes

**Risk:** Very Low

---

## Recommended Action

Implement Option 1 (Inline Embed) with an "OR" divider between the form and the calendar widget. Structure the page as two distinct sections:
1. Send a Message (existing form, fixed in TODO 010)
2. Book a 30-Minute Discovery Call (Calendly inline widget)

## Technical Details

**Affected files:**
- `src/app/contact/page.tsx` — add Calendly section below form
- `package.json` — add `react-calendly` dependency
- `.env.example` — add `NEXT_PUBLIC_CALENDLY_URL`

**Install:**
```bash
npm install react-calendly
```

**Usage in contact page:**
```tsx
"use client";
import { InlineWidget } from "react-calendly";

// Add below the form section:
<div className="mt-16">
  <div className="flex items-center gap-4 mb-10">
    <div className="flex-1 h-px bg-gray-800" />
    <span className="text-gray-500 text-sm font-medium">OR BOOK DIRECTLY</span>
    <div className="flex-1 h-px bg-gray-800" />
  </div>

  <h2 className="text-2xl font-bold text-center mb-2">Book a 30-Min Discovery Call</h2>
  <p className="text-gray-400 text-center mb-6">
    Skip the back-and-forth. Pick a time that works for you.
  </p>

  <div className="rounded-2xl overflow-hidden border border-gray-800">
    <InlineWidget
      url={process.env.NEXT_PUBLIC_CALENDLY_URL || "https://calendly.com/signalhaus/discovery"}
      styles={{ height: '650px' }}
      pageSettings={{
        backgroundColor: '111827',
        hideEventTypeDetails: false,
        hideLandingPageDetails: false,
        primaryColor: '6366f1',
        textColor: 'ffffff',
      }}
    />
  </div>
</div>
```

**Environment variable:**
```
NEXT_PUBLIC_CALENDLY_URL=https://calendly.com/YOUR_CALENDLY_USERNAME/discovery
```

**Note on `"use client"` + metadata:** Contact page already uses `"use client"`. The metadata fix (TODO 017) should be done alongside or after this task. The Calendly `InlineWidget` requires client-side rendering, so the client directive is needed regardless.

## Resources

- react-calendly: https://www.npmjs.com/package/react-calendly
- Calendly embed docs: https://developer.calendly.com/api-docs/ZG9jOjI3ODgyNTI0-getting-started-with-calendly-s-embeddable-features
- Calendly dashboard: https://calendly.com/app/settings/integrations

## Acceptance Criteria

- [ ] `npm install react-calendly` added to dependencies
- [ ] `NEXT_PUBLIC_CALENDLY_URL` added to `.env.example`
- [ ] Calendly `InlineWidget` renders below the contact form on `/contact`
- [ ] "OR BOOK DIRECTLY" divider visually separates form from calendar
- [ ] Widget uses dark color scheme matching site design (`backgroundColor: '111827'`, `primaryColor: '6366f1'`)
- [ ] Widget height is sufficient (650px min) to show calendar without scrolling inside widget
- [ ] Page is responsive — widget fits on mobile screens
- [ ] Calendly URL is configurable via environment variable (not hardcoded)
- [ ] Auto-reply email from TODO 010 references the correct Calendly URL

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Reviewed contact page structure
- Identified react-calendly as standard integration approach
- Documented InlineWidget pattern with dark theme color codes matching site palette
- Noted dependency on TODO 010 (contact form must work before Calendly is added)

**Learnings:**
- Calendly color customization uses hex without `#` prefix
- InlineWidget requires `"use client"` — aligns with existing contact page directive
