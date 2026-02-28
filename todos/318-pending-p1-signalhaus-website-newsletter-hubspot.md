# TODO 318: SignalHaus Website — Newsletter Signup + HubSpot CRM Integration

**Priority:** P1 (Lead Capture)
**Effort:** M (4-8 hours)
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Description
No email capture mechanism exists beyond the contact form. Adding newsletter signup + HubSpot contact creation on form submit will build an owned audience and feed the sales pipeline.

## Acceptance Criteria
- [ ] Newsletter signup component (email input + subscribe button)
- [ ] Newsletter signup in footer and after each blog post
- [ ] Contact form submission creates/updates contact in HubSpot via API
- [ ] HubSpot contact source tagged as "Website - Contact Form"
- [ ] Newsletter signup creates HubSpot contact tagged as "Newsletter Subscriber"
- [ ] API keys in environment variables (not hardcoded)

## Coding Prompt

```
In /data/workspace/projects/signalhaus-website/src/:

1. Create src/components/NewsletterSignup.tsx:
   - Client component with email input and submit button
   - POST to /api/newsletter
   - Show success/error state
   - Style matches dark theme (indigo accent button)

2. Create src/app/api/newsletter/route.ts:
   - Validate email with Zod
   - POST to HubSpot Contacts API: https://api.hubapi.com/crm/v3/objects/contacts
   - Body: { properties: { email, hs_lead_status: "NEW", lifecyclestage: "subscriber" } }
   - Auth: Bearer ${HUBSPOT_API_KEY}
   - Add to .env.example: HUBSPOT_API_KEY=

3. Update src/app/api/contact/route.ts:
   - After successful Resend email, also create/update HubSpot contact
   - Properties: email, firstname, message (as note), hs_lead_status: "NEW"

4. Add <NewsletterSignup /> to:
   - src/components/Footer.tsx (below links)
   - src/app/blog/page.tsx (bottom of page)
   - After blog post content

5. Add HUBSPOT_API_KEY to .env.example
```

## Dependencies
- TODO 315 (contact API security) should be done first
