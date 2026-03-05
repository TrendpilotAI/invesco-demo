# TODO-608: Add Calendly/Cal.com Booking to Contact Page

**Repo:** signalhaus-website  
**Priority:** P0  
**Effort:** S (2-3 hours)  
**Status:** pending

## Description
"Book a Free Consultation" CTA exists on homepage but routes to a form. Embedding a calendar widget dramatically reduces friction and increases conversions.

## Tasks
1. Choose between Calendly (hosted) or Cal.com (open source)
2. Add inline embed widget to `/contact` page below the form
3. Add booking widget link to homepage hero CTA as an alternative
4. Track booking events in GA4

## Coding Prompt
For Calendly embed in `src/app/contact/page.tsx`:
```tsx
'use client'
import { useEffect } from 'react'

export function CalendlyEmbed() {
  useEffect(() => {
    const script = document.createElement('script')
    script.src = 'https://assets.calendly.com/assets/external/widget.js'
    script.async = true
    document.body.appendChild(script)
    return () => document.body.removeChild(script)
  }, [])
  
  return (
    <div 
      className="calendly-inline-widget" 
      data-url="https://calendly.com/YOUR_USERNAME/consultation"
      style={{ minWidth: '320px', height: '700px' }}
    />
  )
}
```

## Acceptance Criteria
- [ ] Calendar widget loads on contact page
- [ ] Booking confirmation sends email to both parties
- [ ] Mobile responsive
- [ ] No layout shift on load

## Dependencies
- Calendly account setup (or Cal.com)
