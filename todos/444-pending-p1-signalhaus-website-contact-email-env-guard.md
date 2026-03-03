# TODO-444: Fix CONTACT_EMAIL Silent Fallback Bug

**Repo:** signalhaus-website  
**Priority:** P1 (Security/Ops)  
**Effort:** S (~30 min)  
**Status:** pending

## Description
`src/app/api/contact/route.ts` line 3:
```ts
const CONTACT_EMAIL = process.env.CONTACT_EMAIL || "nathan@forwardlane.com"
```
If `CONTACT_EMAIL` env var is missing in production, emails silently route to Nathan's personal `@forwardlane.com` address instead of the intended SignalHaus address. This is a data leak and operational bug.

## Acceptance Criteria
- [ ] If `CONTACT_EMAIL` env var is not set, API returns 500 (same pattern as `RESEND_API_KEY`)
- [ ] Error message: "Server configuration error" (no internal detail)
- [ ] `.env.example` documents `CONTACT_EMAIL` as required
- [ ] Personal email address removed from source code

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/src/app/api/contact/route.ts:

Change line 3 from:
  const CONTACT_EMAIL = process.env.CONTACT_EMAIL || "nathan@forwardlane.com"

To:
  const CONTACT_EMAIL = process.env.CONTACT_EMAIL

Then in the POST handler, add CONTACT_EMAIL to the startup check alongside RESEND_API_KEY:
  if (!RESEND_API_KEY || !CONTACT_EMAIL) {
    return NextResponse.json({ error: "Server configuration error" }, { status: 500 })
  }

Update .env.example to mark CONTACT_EMAIL as required with a comment.
```
