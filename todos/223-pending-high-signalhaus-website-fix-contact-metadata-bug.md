# Fix Contact Page Metadata Bug (use client + metadata conflict)

**Priority:** HIGH  
**Effort:** 30 minutes  
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Problem
`src/app/contact/page.tsx` uses `"use client"` (for useState) but tries to set SEO metadata via raw `<head>` JSX tags. Next.js App Router ignores this pattern — the contact page has no proper metadata in production.

Also imports `type { Metadata }` but never uses it.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/src/app/contact/:

1. Create ContactForm.tsx (client component):
   - Move "use client" directive here
   - Move useState, form JSX, and submit handler from page.tsx
   - Export as default ContactForm

2. Update page.tsx to server component:
   - Remove "use client"
   - Export proper metadata object:
     export const metadata: Metadata = {
       title: "Contact | SignalHaus",
       description: "Book a free 30-minute AI consultation...",
       alternates: { canonical: "https://www.signalhaus.ai/contact" },
       openGraph: { ... }
     }
   - Import and render <ContactForm /> 
   - Remove the raw <head> JSX tags

3. Remove the unused `import type { Metadata }` from the old page.tsx
```

## Acceptance Criteria
- [ ] Contact page exports proper metadata (verify with `next build` output)
- [ ] Form still works (useState in client component)
- [ ] No TypeScript errors
