# TODO-469: Fix CONTACT_EMAIL Silent Fallback Bug

**Priority:** P0 (Critical)
**Effort:** S (30 min)
**Repo:** signalhaus-website
**Status:** pending

## Problem

`src/app/api/contact/route.ts` line 3:
```ts
const CONTACT_EMAIL = process.env.CONTACT_EMAIL || "nathan@forwardlane.com"
```

If `CONTACT_EMAIL` env var is not set in production, all contact form submissions silently route to Nathan's personal email without any warning. This is both a privacy concern and ops issue — leads could be missed or miscategorized.

## Fix

Apply the same guard pattern used for `RESEND_API_KEY`:

```ts
const CONTACT_EMAIL = process.env.CONTACT_EMAIL
const RESEND_API_KEY = process.env.RESEND_API_KEY

// In handler:
if (!RESEND_API_KEY || !CONTACT_EMAIL) {
  return NextResponse.json({ error: "Mailer not configured" }, { status: 500 })
}
```

## Agent Prompt

```
Edit /data/workspace/projects/signalhaus-website/src/app/api/contact/route.ts:

1. Change line 3 from:
   const CONTACT_EMAIL = process.env.CONTACT_EMAIL || "nathan@forwardlane.com"
   to:
   const CONTACT_EMAIL = process.env.CONTACT_EMAIL

2. In the POST handler, update the existing RESEND_API_KEY guard check to also check CONTACT_EMAIL:
   if (!RESEND_API_KEY || !CONTACT_EMAIL) {
     return NextResponse.json({ error: "Mailer not configured" }, { status: 500 })
   }

3. Verify the .env.example file includes CONTACT_EMAIL=your@email.com

4. Run: cd /data/workspace/projects/signalhaus-website && npx tsc --noEmit
```

## Acceptance Criteria
- [ ] `CONTACT_EMAIL` has no fallback value
- [ ] Missing `CONTACT_EMAIL` returns HTTP 500 just like missing `RESEND_API_KEY`
- [ ] `.env.example` documents the variable
- [ ] TypeScript compiles without errors
