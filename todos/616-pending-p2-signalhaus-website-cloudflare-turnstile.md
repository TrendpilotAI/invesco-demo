# TODO-616: Cloudflare Turnstile CAPTCHA on Contact Form

**Repo:** signalhaus-website  
**Priority:** P2  
**Effort:** S (2-3 hours)  
**Status:** pending

## Description
Contact form has rate limiting but no CAPTCHA. Bots can still send spam submissions. Cloudflare Turnstile is free, privacy-friendly, and doesn't require solving puzzles.

## Tasks
1. Register for Cloudflare Turnstile (free)
2. Get site key + secret key
3. Add Turnstile widget to contact form
4. Validate token server-side in `/api/contact/route.ts`

## Coding Prompt
In `ContactForm.tsx`:
```tsx
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async></script>
<div className="cf-turnstile" data-sitekey={process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY} />
```

In API route, add validation before processing:
```ts
const token = body.turnstileToken
const verifyResp = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
  method: 'POST',
  body: new URLSearchParams({ secret: process.env.TURNSTILE_SECRET_KEY!, response: token })
})
const { success } = await verifyResp.json()
if (!success) return NextResponse.json({ error: 'Bot detected' }, { status: 403 })
```

## Acceptance Criteria
- [ ] Turnstile widget renders on contact form
- [ ] Server validates token before processing
- [ ] Bot submissions return 403
- [ ] Legitimate submissions unaffected
- [ ] Works in CI test environment (test keys)

## Dependencies
- Cloudflare account (free)
- TURNSTILE_SECRET_KEY env var in Vercel
