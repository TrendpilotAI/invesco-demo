# Add Analytics to SignalHaus Website

**Priority:** MEDIUM  
**Effort:** 1 hour  
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Task
Add Google Analytics 4 for SEO data and conversion tracking.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/:

1. Create src/components/Analytics.tsx:
   - Google Analytics 4 via next/script with Strategy="afterInteractive"
   - Measurement ID from env: NEXT_PUBLIC_GA_ID

2. Add to src/app/layout.tsx:
   - Import and render <Analytics /> in <body>

3. Track key events:
   - Contact form submission (gtag event: 'generate_lead')
   - Calendly booking opened (gtag event: 'begin_checkout')  
   - CTA clicks (gtag event: 'click', label: button text)

4. Add to .env.example: NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX

5. Set up GA4 property at analytics.google.com
   - Property: SignalHaus AI
   - Domain: signalhaus.ai
   - Configure conversion: form_submit, calendly_booking
```

## Acceptance Criteria
- [ ] GA4 tracking code loads on all pages
- [ ] Real-time view shows page views
- [ ] Form submission triggers lead conversion event
- [ ] No performance impact (afterInteractive strategy)
