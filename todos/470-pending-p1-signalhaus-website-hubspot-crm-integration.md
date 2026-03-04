# TODO-470: HubSpot CRM Integration — Contact Form → Pipeline

**Priority:** P1 (High)
**Effort:** M (4 hours)
**Repo:** signalhaus-website
**Status:** pending
**Depends on:** TODO-469 (env guard fix)

## Problem

Every contact form submission goes to email + Slack but is never added to a CRM. Nathan has no structured pipeline visibility — leads are tracked manually. This is the #1 revenue gap for the site.

## Solution

Integrate HubSpot Contacts API v3 on form submit:
1. Create/update HubSpot Contact with lead details
2. Create a HubSpot Deal in "New Lead" pipeline stage
3. Associate deal with contact
4. Fire-and-forget (don't block email send on HubSpot success)

## Agent Prompt

```
Add HubSpot CRM integration to /data/workspace/projects/signalhaus-website/src/app/api/contact/route.ts

1. Add env var: HUBSPOT_API_KEY (private app token from HubSpot)

2. Create /data/workspace/projects/signalhaus-website/src/lib/hubspot.ts:

```typescript
const HUBSPOT_BASE = "https://api.hubapi.com"

interface HubSpotContactProps {
  email: string
  firstname: string
  lastname?: string
  company?: string
  message?: string
  budget?: string
}

export async function upsertHubSpotContact(
  apiKey: string,
  props: HubSpotContactProps
): Promise<string | null> {
  try {
    const nameParts = props.firstname.split(" ")
    const firstname = nameParts[0]
    const lastname = nameParts.slice(1).join(" ") || ""
    
    const res = await fetch(`${HUBSPOT_BASE}/crm/v3/objects/contacts`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        properties: {
          email: props.email,
          firstname,
          lastname,
          company: props.company || "",
          message: props.message || "",
          hs_lead_status: "NEW",
        },
      }),
    })
    
    if (res.status === 409) {
      // Contact exists — get their ID
      const errBody = await res.json()
      return errBody?.message?.match(/ID: (\d+)/)?.[1] || null
    }
    
    if (!res.ok) return null
    const data = await res.json()
    return data.id || null
  } catch {
    return null
  }
}

export async function createHubSpotDeal(
  apiKey: string,
  contactId: string,
  dealName: string,
  budget?: string
): Promise<void> {
  try {
    const dealRes = await fetch(`${HUBSPOT_BASE}/crm/v3/objects/deals`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        properties: {
          dealname: dealName,
          pipeline: "default",
          dealstage: "appointmentscheduled",
          description: budget ? `Budget: ${budget}` : "",
        },
      }),
    })
    
    if (!dealRes.ok) return
    const deal = await dealRes.json()
    
    // Associate deal with contact
    await fetch(
      `${HUBSPOT_BASE}/crm/v4/objects/deals/${deal.id}/associations/contacts/${contactId}/deal_to_contact`,
      {
        method: "PUT",
        headers: { "Authorization": `Bearer ${apiKey}` },
      }
    )
  } catch {
    // fire-and-forget
  }
}
```

3. In route.ts, after Resend email success, add fire-and-forget HubSpot call:
```typescript
const HUBSPOT_API_KEY = process.env.HUBSPOT_API_KEY
if (HUBSPOT_API_KEY) {
  const { upsertHubSpotContact, createHubSpotDeal } = await import("@/lib/hubspot")
  upsertHubSpotContact(HUBSPOT_API_KEY, {
    email, firstname: name, company, message, budget
  }).then(contactId => {
    if (contactId) {
      createHubSpotDeal(HUBSPOT_API_KEY!, contactId, `SignalHaus Lead: ${name}`, budget)
    }
  }).catch(() => {})
}
```

4. Add HUBSPOT_API_KEY to .env.example

5. Run: cd /data/workspace/projects/signalhaus-website && npx tsc --noEmit
```

## Acceptance Criteria
- [ ] HubSpot contact created on form submit
- [ ] HubSpot deal created and associated with contact
- [ ] HubSpot failure does NOT block email send
- [ ] `HUBSPOT_API_KEY` in `.env.example`
- [ ] TypeScript compiles without errors
