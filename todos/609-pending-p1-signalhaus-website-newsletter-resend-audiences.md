# TODO-609: Newsletter Signup with Resend Audiences

**Repo:** signalhaus-website  
**Priority:** P1  
**Effort:** S (3-4 hours)  
**Status:** pending

## Description
No email list capture exists beyond contact form submissions. Add newsletter signup in footer and blog sidebar to build an owned audience.

## Tasks
1. Create `/api/subscribe` endpoint using Resend Audiences API
2. Add `NewsletterSignup` component with email input + submit
3. Place in: footer, blog listing page sidebar, after each blog post
4. Create Resend Audience "SignalHaus Newsletter"
5. Optionally offer a lead magnet ("Download our AI ROI Checklist")

## Coding Prompt
Create `src/app/api/subscribe/route.ts`:
```ts
export async function POST(req: NextRequest) {
  const { email } = await req.json()
  // Validate email
  // POST to Resend Audiences API
  const resp = await fetch('https://api.resend.com/audiences/{AUDIENCE_ID}/contacts', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, unsubscribed: false })
  })
  return NextResponse.json({ success: resp.ok })
}
```

Create `src/components/NewsletterSignup.tsx` with the form UI.

## Acceptance Criteria
- [ ] Email submits to Resend Audience
- [ ] Success/error state shown to user
- [ ] Rate limited (5 req/IP/15min)
- [ ] Double opt-in confirmation email sent
- [ ] Placed in footer, blog, and after posts

## Dependencies
- RESEND_API_KEY env var (already set)
- Resend Audience created in dashboard
