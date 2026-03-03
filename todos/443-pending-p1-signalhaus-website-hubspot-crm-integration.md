# TODO-443: HubSpot CRM Integration

**Repo:** signalhaus-website  
**Priority:** P1 (High)  
**Effort:** M (~4 hours)  
**Status:** pending

## Description
Contact form submissions go to email + Slack but there is no CRM. Every lead requires manual tracking. Integrate HubSpot Contacts API v3 to automatically create contacts and deals on form submission.

## Acceptance Criteria
- [ ] HubSpot contact created/upserted on contact form submit (server-side)
- [ ] HubSpot deal created in "New Lead" pipeline stage with budget context
- [ ] Contact properties: firstName, lastName, email, company, phone, message, source="signalhaus-website"
- [ ] Deal properties: dealname (company name), amount (from budget field), pipeline, dealstage="newlead"
- [ ] `HUBSPOT_API_KEY` env var checked at startup (500 if missing)
- [ ] HubSpot failure does NOT block email send (non-blocking, fire-and-forget with error log)
- [ ] `.env.example` updated with `HUBSPOT_API_KEY=`

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/src/app/api/contact/route.ts:

1. Add HubSpot integration after Resend email send succeeds.
2. Use HubSpot Contacts API v3: POST https://api.hubapi.com/crm/v3/objects/contacts
   Headers: Authorization: Bearer {HUBSPOT_API_KEY}, Content-Type: application/json
   Body: { properties: { firstname, lastname, email, company, phone, message, hs_lead_source: "Website" }}
3. Use upsert: POST /crm/v3/objects/contacts/upsert to avoid duplicates on email.
4. Create HubSpot deal: POST https://api.hubapi.com/crm/v3/objects/deals
   Body: { properties: { dealname: `${company} - Website Lead`, amount: budgetToNumber(budget), pipeline: "default", dealstage: "appointmentscheduled" }}
5. Associate contact to deal: POST /crm/v3/associations/contact/{contactId}/deal/{dealId}/associate/default
6. Wrap all HubSpot calls in try/catch — log errors but don't fail the response.
7. Add HUBSPOT_API_KEY to env check block alongside RESEND_API_KEY.
8. Update .env.example with HUBSPOT_API_KEY=

Budget to amount mapping:
- "under-10k" → 10000
- "10k-50k" → 30000
- "50k-100k" → 75000
- "100k-plus" → 150000
```

## Dependencies
- HUBSPOT_API_KEY env var (Nathan needs to create HubSpot account + API key)
- No code dependencies
