# TODO-613: HubSpot CRM Integration for Contact Form

**Repo:** signalhaus-website  
**Priority:** P1  
**Effort:** M (3-4 hours)  
**Status:** pending

## Description
Contact form submissions go to email + Slack but not to a CRM. HubSpot free tier supports full pipeline management, deal tracking, and follow-up sequences.

## Tasks
1. Create HubSpot account (free tier)
2. Get HubSpot Forms API key or Private App token
3. In `/api/contact/route.ts`, add HubSpot contact creation after email send
4. Map form fields: name → firstname+lastname, email, company, message → notes, budget → custom property
5. Assign new contacts to a "Website Inbound" pipeline stage

## Coding Prompt
In `src/app/api/contact/route.ts`, after Resend success:
```ts
// HubSpot contact creation
if (process.env.HUBSPOT_API_KEY) {
  await fetch('https://api.hubapi.com/crm/v3/objects/contacts', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.HUBSPOT_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      properties: {
        firstname: name.split(' ')[0],
        lastname: name.split(' ').slice(1).join(' '),
        email,
        company,
        message,
        budget_range: budget,
        hs_lead_status: 'NEW',
        lifecyclestage: 'lead',
      }
    })
  }).catch(err => console.error('HubSpot error:', err))
}
```
Add `HUBSPOT_API_KEY` to Vercel env vars.

## Acceptance Criteria
- [ ] New contacts appear in HubSpot on form submit
- [ ] Budget field mapped to custom property
- [ ] HubSpot failure doesn't block form submission (fire-and-forget)
- [ ] CRM pipeline stage set to "New Lead"

## Dependencies
- HubSpot account creation
- HUBSPOT_API_KEY env var in Vercel
