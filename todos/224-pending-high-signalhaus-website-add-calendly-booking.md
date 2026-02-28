# Add Calendly Booking Integration

**Priority:** HIGH  
**Effort:** 1 hour  
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Problem
CTAs say "Book a Free Consultation" but link to a contact form. Calendly inline booking dramatically reduces friction and increases conversion for consulting businesses.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/:

1. Create src/components/CalendlyEmbed.tsx (client component):
   - Load Calendly widget script via useEffect
   - Render inline Calendly widget: https://calendly.com/signalhaus/consultation
   - Style to match site (dark background, full width)
   - Show loading spinner while Calendly loads

2. Update src/app/contact/page.tsx (or ContactForm.tsx after #223):
   - Add tabs: "Send a Message" | "Book a Call"
   - "Book a Call" tab shows <CalendlyEmbed />
   - Default to "Book a Call" tab (higher conversion)

3. Optionally add floating "Book a Call" button in Header.tsx on desktop
   - Secondary button next to main CTA

Calendly embed code reference:
<div class="calendly-inline-widget" data-url="https://calendly.com/YOUR_LINK" />
<script src="https://assets.calendly.com/assets/external/widget.js" />
```

## Acceptance Criteria
- [ ] Calendly widget loads on contact page
- [ ] Works on mobile
- [ ] No layout shift during load
- [ ] Nathan's actual Calendly URL configured
