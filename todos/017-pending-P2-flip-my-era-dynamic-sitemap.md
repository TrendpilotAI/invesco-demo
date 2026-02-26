---
status: pending
priority: P2
issue_id: "017"
tags: [flip-my-era, seo, sitemap, edge-function, netlify]
dependencies: ["014"]
---

# 017 — Dynamic Sitemap.xml Generation

## Overview

FlipMyEra has a static `public/sitemap.xml` that is baked at build time and contains only hardcoded pages. As new public stories/ebooks are created by users and new SEO landing pages are added, the sitemap goes stale. A dynamic sitemap that queries Supabase for public ebooks would enable Google to index user-generated content, driving organic traffic.

**Why P2:** SEO is a compounding growth channel. Indexing user stories creates a long tail of organic search traffic ("Midnights era story," "Taylor Swift folklore ebook," etc.). A static sitemap misses all of this. Depends on TODO #014 (shareable preview pages) existing for there to be URLs worth indexing.

## Coding Prompt

You are working on FlipMyEra, a React 18 + TypeScript + Vite + Supabase SaaS app at `/data/workspace/projects/flip-my-era/`.

**Task:** Implement a dynamic sitemap that includes both static routes and user-generated public ebooks.

### Step 1 — Audit existing sitemap

Read `public/sitemap.xml` to understand the current static pages listed. Note all existing URLs.

### Step 2 — Create Supabase Edge Function for dynamic sitemap

Create `supabase/functions/sitemap/index.ts`:

```typescript
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const STATIC_PAGES = [
  { url: '/', priority: '1.0', changefreq: 'weekly' },
  { url: '/plans', priority: '0.9', changefreq: 'monthly' },
  { url: '/gallery', priority: '0.8', changefreq: 'daily' },
  { url: '/pricing', priority: '0.9', changefreq: 'monthly' },
  // SEO pages
  { url: '/eras-tour-ebook', priority: '0.7', changefreq: 'monthly' },
  { url: '/custom-taylor-swift-gifts', priority: '0.7', changefreq: 'monthly' },
  { url: '/swiftie-birthday-presents', priority: '0.7', changefreq: 'monthly' },
  { url: '/taylor-swift-fan-art-book', priority: '0.7', changefreq: 'monthly' },
  { url: '/eras-tour-memories-book', priority: '0.7', changefreq: 'monthly' },
  { url: '/personalized-eras-tour-photo-book', priority: '0.7', changefreq: 'monthly' },
  { url: '/taylor-swift-concert-keepsake', priority: '0.7', changefreq: 'monthly' },
  { url: '/swiftie-graduation-gift', priority: '0.7', changefreq: 'monthly' },
  { url: '/friendship-bracelet-book', priority: '0.7', changefreq: 'monthly' },
  { url: '/eras-tour-scrapbook', priority: '0.7', changefreq: 'monthly' },
];

const BASE_URL = 'https://flipmyera.com';

Deno.serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
  )

  // Fetch public ebooks (limit to 1000 for sitemap sanity)
  const { data: ebooks } = await supabase
    .from('ebooks')
    .select('id, updated_at')
    .eq('is_public', true)  // adjust column name as needed
    .order('updated_at', { ascending: false })
    .limit(1000)

  const staticEntries = STATIC_PAGES.map(page => `
  <url>
    <loc>${BASE_URL}${page.url}</loc>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('')

  const dynamicEntries = (ebooks || []).map(ebook => `
  <url>
    <loc>${BASE_URL}/ebook/${ebook.id}/preview</loc>
    <lastmod>${new Date(ebook.updated_at).toISOString().split('T')[0]}</lastmod>
    <changefreq>never</changefreq>
    <priority>0.5</priority>
  </url>`).join('')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${staticEntries}
${dynamicEntries}
</urlset>`

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
    }
  })
})
```

### Step 3 — Configure Netlify to serve sitemap from edge function

Add to `netlify.toml`:
```toml
[[redirects]]
  from = "/sitemap.xml"
  to = "https://{SUPABASE_PROJECT_REF}.supabase.co/functions/v1/sitemap"
  status = 200
  force = true
```

Or use a Netlify Edge Function in `netlify/edge-functions/sitemap.ts` that proxies to the Supabase function.

**Simpler approach (if preferred):** Generate the sitemap at build time using a Vite plugin or build script:

Create `scripts/generate-sitemap.ts`:
```typescript
// Fetches public ebooks from Supabase at build time and writes sitemap.xml to public/
import { createClient } from '@supabase/supabase-js';
import { writeFileSync } from 'fs';

// ... (same logic as edge function but runs during `npm run build`)
```

Add to `package.json`:
```json
"build": "npm run generate-sitemap && vite build",
"generate-sitemap": "tsx scripts/generate-sitemap.ts"
```

This approach is simpler but sitemap is only as fresh as the last build.

**Recommendation:** Implement both — build-time script for the static pages (immediate fix), then the edge function for real-time updates.

### Step 4 — Remove or replace static sitemap

Replace `public/sitemap.xml` with a minimal file that will be overwritten by the build script, OR update it to serve as fallback.

### Step 5 — Add to Supabase deploy workflow

Deploy the `sitemap` edge function in `.github/workflows/supabase-deploy.yml`.

### Step 6 — Verify with Google Search Console

After deployment, submit the sitemap URL to Google Search Console (manual step — document this in PLAN.md).

## Dependencies

- TODO #014 — Shareable preview pages must exist before ebook URLs are worth indexing

## Effort

S (3-5 hours)

## Acceptance Criteria

- [ ] `GET /sitemap.xml` returns valid XML
- [ ] Sitemap includes all current static/SEO pages
- [ ] Sitemap includes public ebook preview URLs (if any exist)
- [ ] Sitemap validates at https://www.xml-sitemaps.com/validate-xml-sitemap.html
- [ ] Sitemap is reachable at `https://flipmyera.com/sitemap.xml`
- [ ] Google Search Console can fetch and parse the sitemap
- [ ] `robots.txt` references the sitemap URL (check `public/robots.txt`)
