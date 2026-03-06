# TODO 619 — PostHog Funnel Analytics

**Repo:** signalhaus-website
**Priority:** P2
**Effort:** S (1 day)
**Status:** pending

## Problem
GA4 and Clarity provide page-level analytics but no funnel tracking. We can't see: how many people start the contact form vs complete it, how many use the ROI calculator, or which CTAs drive the most conversions.

## Task
1. Add PostHog to the site (free tier is generous)
2. Track key conversion events
3. Set up conversion funnel in PostHog dashboard

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/:

1. Install posthog-js: npm install posthog-js

2. Create src/components/PostHog.tsx:
   "use client"
   import posthog from "posthog-js"
   import { useEffect } from "react"
   import Script from "next/script"
   
   export function PostHogProvider({ children }) {
     useEffect(() => {
       posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
         api_host: "https://us.i.posthog.com",
         capture_pageview: true,
       })
     }, [])
     return children
   }

3. Track these events across the codebase:
   - posthog.capture("hero_cta_clicked", { cta: "Book a Call" }) — Header/Hero
   - posthog.capture("contact_form_started") — ContactForm first field focus
   - posthog.capture("contact_form_submitted", { budget }) — ContactForm submit
   - posthog.capture("roi_calculator_engaged") — ROICalculator interaction
   - posthog.capture("roi_calculator_completed", { roi_value }) — ROI result shown
   - posthog.capture("pricing_tier_cta_clicked", { tier }) — Pricing page
   - posthog.capture("blog_post_read", { slug, reading_time }) — Blog completion

4. Add NEXT_PUBLIC_POSTHOG_KEY to .env.example and Vercel env vars
5. Add posthog.com to CSP in next.config.ts

6. Add PostHogProvider to src/app/layout.tsx (alongside other analytics)
```

## Acceptance Criteria
- [ ] PostHog initializes in production
- [ ] All 7 events fire correctly
- [ ] PostHog domain added to CSP allowlist
- [ ] NEXT_PUBLIC_POSTHOG_KEY documented in README/DEPLOY.md
- [ ] Conversion funnel visible in PostHog dashboard
