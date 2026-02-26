---
status: pending
priority: p2
issue_id: "013"
tags: [analytics, nextjs, vercel, plausible, signalhaus-website]
dependencies: []
---

# Add Analytics Integration (Vercel Analytics or Plausible)

## Problem Statement

The SignalHaus website has zero analytics integration. There is no way to know how many people visit the site, which pages they view, where they come from, or whether the contact form is being found. Without analytics, there's no data to optimize conversions, measure SEO progress, or justify marketing spend. This is a P2 priority — site traffic is unmeasurable until resolved.

## Findings

- No analytics script, provider, or package in the codebase
- No `<Analytics />` component in `src/app/layout.tsx`
- `package.json` has no analytics dependencies
- BRAINSTORM.md recommends Vercel Analytics (easiest) or PostHog (most powerful)
- Site is likely to be deployed on Vercel — native integration available in 2 lines of code

## Proposed Solutions

### Option 1: Vercel Analytics (Recommended for quick win)

**Approach:** Install `@vercel/analytics` and add `<Analytics />` to root layout.

**Pros:**
- 2 minutes to implement
- No configuration needed on Vercel deployment
- Free tier: unlimited pageviews for hobby/pro projects
- Privacy-friendly (no cookies, GDPR compliant)
- Shows pageviews, unique visitors, top pages, referrers

**Cons:**
- Limited to Vercel deployment
- Less powerful than PostHog (no event tracking, funnels, etc.)

**Effort:** 30 minutes

**Risk:** Very Low

---

### Option 2: Plausible Analytics

**Approach:** Add Plausible script via `next/script` in root layout.

**Pros:**
- Privacy-first, GDPR compliant, no cookies
- Beautiful dashboard
- Goal tracking (contact form submissions)
- Works on any hosting

**Cons:**
- $9/month after 30-day trial
- Requires account setup

**Effort:** 1 hour

**Risk:** Very Low

---

### Option 3: Google Analytics 4

**Approach:** Add GA4 via `@next/third-parties/google` (Next.js 14+ built-in).

**Pros:**
- Free
- Industry standard
- Deep funnel analysis

**Cons:**
- Privacy concerns (GDPR issues in EU)
- Cookie consent banner required
- More complex setup

**Effort:** 1-2 hours (including consent banner)

**Risk:** Low-Medium

---

### Option 4: PostHog (Most powerful)

**Approach:** Install `posthog-js` + `posthog-nextjs` for full product analytics.

**Pros:**
- Session recordings, heatmaps, funnels, feature flags
- Free up to 1M events/month
- Self-hostable

**Cons:**
- More complex setup (provider wrapper needed)
- Overkill for initial launch

**Effort:** 2-3 hours

**Risk:** Low

---

## Recommended Action

Implement Option 1 (Vercel Analytics) immediately for zero-friction baseline metrics, then add PostHog (Option 4) in a follow-up task for event-level tracking (contact form completions, CTA clicks). The combination gives both pageview trends AND behavioral analytics.

**Phase 1 (this TODO):** Vercel Analytics + Vercel Speed Insights
**Phase 2 (future TODO):** PostHog for event tracking and conversion funnels

## Technical Details

**Affected files:**
- `src/app/layout.tsx` — add `<Analytics />` and `<SpeedInsights />` components
- `package.json` — add `@vercel/analytics` and `@vercel/speed-insights`

**Implementation:**
```bash
npm install @vercel/analytics @vercel/speed-insights
```

```tsx
// src/app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {/* existing layout */}
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

**To also track custom events (e.g., contact form submission):**
```typescript
import { track } from '@vercel/analytics';

// In contact form onSubmit success:
track('contact_form_submitted', { budget: selectedBudget });
```

**Google Search Console setup (do alongside):**
1. Go to https://search.google.com/search-console
2. Add property: `https://www.signalhaus.ai`
3. Verify via HTML tag in `<head>` or DNS TXT record
4. Submit `sitemap.xml` (check if it exists at `/sitemap.xml` — Next.js can auto-generate)

**Add sitemap generation if not present:**
```typescript
// src/app/sitemap.ts
import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: 'https://www.signalhaus.ai', lastModified: new Date(), changeFrequency: 'monthly', priority: 1 },
    { url: 'https://www.signalhaus.ai/services', lastModified: new Date(), changeFrequency: 'monthly', priority: 0.9 },
    { url: 'https://www.signalhaus.ai/pricing', lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
    { url: 'https://www.signalhaus.ai/blog', lastModified: new Date(), changeFrequency: 'weekly', priority: 0.8 },
    { url: 'https://www.signalhaus.ai/about', lastModified: new Date(), changeFrequency: 'monthly', priority: 0.7 },
    { url: 'https://www.signalhaus.ai/contact', lastModified: new Date(), changeFrequency: 'monthly', priority: 0.9 },
  ];
}
```

## Resources

- Vercel Analytics docs: https://vercel.com/docs/analytics
- @vercel/analytics npm: https://www.npmjs.com/package/@vercel/analytics
- Next.js sitemap: https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap
- Google Search Console: https://search.google.com/search-console

## Acceptance Criteria

- [ ] `@vercel/analytics` and `@vercel/speed-insights` installed
- [ ] `<Analytics />` component rendered in root layout (`src/app/layout.tsx`)
- [ ] `<SpeedInsights />` component rendered in root layout
- [ ] Analytics appear in Vercel dashboard after deployment
- [ ] `src/app/sitemap.ts` exists and generates valid sitemap
- [ ] `/sitemap.xml` returns valid XML on the deployed site
- [ ] Contact form submission tracked as custom event (`track('contact_form_submitted')`)
- [ ] Google Search Console property verified and sitemap submitted (manual step — document in README)

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Confirmed zero analytics in codebase
- Evaluated 4 analytics options
- Recommended Vercel Analytics + Speed Insights as fastest path to baseline metrics
- Added sitemap generation as a bonus (needed for Search Console)

**Learnings:**
- Vercel Analytics is the easiest win possible — literally 2 imports + 2 JSX tags
- Sitemap generation is built into Next.js App Router via `sitemap.ts` convention
