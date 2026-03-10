# TODO-896: Extract src/lib/seo.ts Constants (DRY Fix)
**Repo:** signalhaus-website  
**Priority:** P2  
**Status:** pending  
**Effort:** 30min

## Problem
Multiple page metadata files repeat the same values inline:
- `"https://www.signalhaus.ai"` site URL — 8+ occurrences
- `{ url: "/og-image.png", width: 1200, height: 630 }` OG image — 5+ occurrences
- Site name, Twitter handle, default description

If these change (e.g., OG image path updates), every file must be manually edited.

## Task
Extract shared SEO constants into `src/lib/seo.ts` and update all pages to import from it.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website:

1. Create src/lib/seo.ts:
   export const siteConfig = {
     url: 'https://www.signalhaus.ai',
     name: 'SignalHaus',
     twitterHandle: '@signalhaus_ai',
     defaultOgImage: {
       url: '/og-image.png',
       width: 1200,
       height: 630,
       alt: 'SignalHaus — Pragmatic AI. Real Impact.',
     },
     defaultDescription: 'SignalHaus helps enterprises accelerate growth with custom AI strategy, data integrations, and intelligent automation.',
   } as const

2. Update all pages that repeat these values:
   - src/app/pricing/page.tsx
   - src/app/services/page.tsx  
   - src/app/about/page.tsx
   - src/app/case-studies/page.tsx
   - src/app/blog/page.tsx
   - src/app/contact/page.tsx
   - src/app/roi-calculator/page.tsx
   - src/app/layout.tsx
   
   Replace inline values with imports:
   import { siteConfig } from '@/lib/seo'
   // then use siteConfig.url, siteConfig.defaultOgImage, etc.

3. Update canonical URLs to use siteConfig.url:
   alternates: { canonical: `${siteConfig.url}/pricing` }
```

## Dependencies
- None — pure refactor, no behavior change

## Acceptance Criteria
- No repeated `"https://www.signalhaus.ai"` strings outside of seo.ts
- No repeated OG image objects outside of seo.ts
- `npm run build` and `npm run typecheck` pass
- No metadata values changed (just sourced from constants)
