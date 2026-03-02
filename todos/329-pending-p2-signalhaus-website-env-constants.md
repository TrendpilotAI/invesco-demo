# TODO-329: Type-Safe Env + Constants Module

**Priority:** P2  
**Effort:** 30 min  
**Repo:** signalhaus-website  
**Status:** pending  

## Description
Create `src/lib/constants.ts` and `src/lib/env.ts` to centralize site constants and add type-safe environment variable access with startup validation.

## Coding Prompt (Agent-Executable)

```
In /data/workspace/projects/signalhaus-website/:

1. Create src/lib/constants.ts:
   export const SITE_URL = 'https://www.signalhaus.ai'
   export const SITE_NAME = 'SignalHaus'
   export const OG_IMAGE = '/og-image.png'
   export const OG_IMAGE_FULL = `${SITE_URL}${OG_IMAGE}`
   export const CONTACT_EMAIL_FALLBACK = 'nathan@signalhaus.ai'
   export const CALENDLY_URL = 'https://calendly.com/signalhaus'

2. Create src/lib/env.ts:
   // Server-side env (API routes only)
   export function getServerEnv() {
     const RESEND_API_KEY = process.env.RESEND_API_KEY
     const CONTACT_EMAIL = process.env.CONTACT_EMAIL
     const SLACK_WEBHOOK_URL = process.env.SLACK_WEBHOOK_URL  // optional
     
     if (!RESEND_API_KEY) throw new Error('RESEND_API_KEY is required')
     if (!CONTACT_EMAIL) throw new Error('CONTACT_EMAIL is required')
     
     return { RESEND_API_KEY, CONTACT_EMAIL, SLACK_WEBHOOK_URL }
   }
   
   // Public env (client-side)
   export const publicEnv = {
     GA_ID: process.env.NEXT_PUBLIC_GA_ID || '',
     CLARITY_ID: process.env.NEXT_PUBLIC_CLARITY_ID || '',
     LINKEDIN_PARTNER_ID: process.env.NEXT_PUBLIC_LINKEDIN_PARTNER_ID || '',
   }

3. Update src/app/api/contact/route.ts to use getServerEnv() instead of 
   individual process.env reads. Remove the silent CONTACT_EMAIL fallback.

4. Update any page metadata that hardcodes SITE_URL to use the constants.
```

## Acceptance Criteria
- [ ] `src/lib/constants.ts` created
- [ ] `src/lib/env.ts` created with server + public env exports
- [ ] contact/route.ts updated to use `getServerEnv()`
- [ ] `CONTACT_EMAIL` missing causes 500 (not silent fallback to personal email)
- [ ] TypeScript compiles without errors

## Dependencies
None
