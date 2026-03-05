# TODO-606: Create OG Image + Twitter Card Meta Tags

**Repo:** signalhaus-website  
**Priority:** P0  
**Effort:** XS (1-2 hours)  
**Status:** pending

## Description
Pages reference `/og-image.png` in OG metadata but the file may not exist. Also missing Twitter Card meta tags across all pages.

## Tasks
1. Create `/public/og-image.png` — 1200x630 branded image (dark bg, SignalHaus logo, tagline "Pragmatic AI. Real Impact.")
2. Add `twitter:card`, `twitter:site`, `twitter:title`, `twitter:description`, `twitter:image` to root layout metadata
3. Create `opengraph-image.tsx` at app root for dynamic OG generation OR confirm static PNG exists
4. Verify each page's OG title/description is unique and compelling

## Coding Prompt
In `src/app/layout.tsx`, add to the `metadata` export:
```ts
twitter: {
  card: 'summary_large_image',
  site: '@signalhausai',
  title: 'SignalHaus AI — Pragmatic AI. Real Impact.',
  description: 'Enterprise AI consulting. Strategy, automation, and data integration built by operators who\'ve shipped AI at scale.',
  images: ['/og-image.png'],
},
```
Then create `/public/og-image.png` using a design tool or Satori-based generator.

## Acceptance Criteria
- [ ] `/public/og-image.png` exists (1200x630, branded)
- [ ] Twitter Card meta tags in layout.tsx
- [ ] Test with https://cards-dev.twitter.com/validator
- [ ] Test with https://developers.facebook.com/tools/debug/

## Dependencies
None
