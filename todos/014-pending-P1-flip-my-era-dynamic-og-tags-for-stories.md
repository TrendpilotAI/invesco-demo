---
status: pending
priority: P1
issue_id: "014"
tags: [flip-my-era, seo, og-tags, sharing, social, supabase-edge]
dependencies: []
---

# 014 — Dynamic OG Meta Tags for Shared Story/Ebook Links

## Overview

When a user shares a FlipMyEra story or ebook link (e.g., `https://flipmyera.com/ebook/abc123/preview`), social media platforms (Twitter/X, Facebook, Discord, iMessage) scrape the URL for Open Graph meta tags to generate a rich preview card. Currently, `ShareablePreview.tsx` fetches ebook data from Supabase client-side, but OG tags are **baked into `index.html`** at build time and are the same for every URL. Social scrapers see the generic homepage OG tags, not the individual story's title, era image, and description.

**Why P1:** This directly impacts viral growth. A shareable story link should show the story's cover art and title in Discord/Twitter previews, not just the generic FlipMyEra homepage card. This is the difference between a bland link and a compelling click-through.

## Coding Prompt

You are working on FlipMyEra, a React 18 + TypeScript + Vite + Supabase SaaS app at `/data/workspace/projects/flip-my-era/`.

**Task:** Implement dynamic per-story OG meta tags using a Supabase Edge Function that serves HTML with proper OG tags for social scrapers.

### Architecture

Social scrapers (bots) do NOT execute JavaScript — they only read raw HTML. Since this is a React SPA (rendered by Vite/JS), we need a server-side solution. The cleanest approach for a Supabase-hosted app:

**Option A (Recommended): Supabase Edge Function as OG tag renderer**
- Create a new Edge Function `og-preview` that handles `/ebook/:id/preview` requests from bots
- Netlify (or Cloudflare) can rewrite bot requests to this function
- The function fetches ebook metadata from DB and returns pre-rendered HTML with OG tags

**Option B: Netlify redirect + Edge Function**
- Add Netlify `_redirects` rules to detect social media bot user-agents and proxy to the edge function

Implement Option A + B together.

### Step 1 — Create Edge Function

Create `supabase/functions/og-preview/index.ts`:

```typescript
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  const url = new URL(req.url)
  const ebookId = url.searchParams.get('id')
  
  if (!ebookId) {
    return new Response('Missing id', { status: 400 })
  }

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
  )

  const { data: ebook, error } = await supabase
    .from('ebooks')
    .select('id, title, era, cover_image_url, description, creator_name')
    .eq('id', ebookId)
    .single()

  if (error || !ebook) {
    // Return generic OG tags if not found
    return new Response(getGenericHtml(), { 
      headers: { ...corsHeaders, 'Content-Type': 'text/html' } 
    })
  }

  const ogTitle = `${ebook.title} — FlipMyEra`
  const ogDescription = ebook.description || `A ${ebook.era} era story created on FlipMyEra`
  const ogImage = ebook.cover_image_url || 'https://flipmyera.com/og-image.png'
  const ogUrl = `https://flipmyera.com/ebook/${ebook.id}/preview`

  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>${ogTitle}</title>
  <meta property="og:title" content="${escapeHtml(ogTitle)}" />
  <meta property="og:description" content="${escapeHtml(ogDescription)}" />
  <meta property="og:image" content="${escapeHtml(ogImage)}" />
  <meta property="og:url" content="${escapeHtml(ogUrl)}" />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="${escapeHtml(ogTitle)}" />
  <meta name="twitter:description" content="${escapeHtml(ogDescription)}" />
  <meta name="twitter:image" content="${escapeHtml(ogImage)}" />
  <meta http-equiv="refresh" content="0; url=${escapeHtml(ogUrl)}" />
</head>
<body>Redirecting...</body>
</html>`

  return new Response(html, {
    headers: { ...corsHeaders, 'Content-Type': 'text/html' }
  })
})

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function getGenericHtml(): string {
  return `<!DOCTYPE html><html><head>
  <meta property="og:title" content="FlipMyEra — AI-Powered Era Storybooks" />
  <meta property="og:description" content="Create personalized AI storybooks in Taylor Swift's eras." />
  <meta property="og:image" content="https://flipmyera.com/og-image.png" />
  <meta http-equiv="refresh" content="0; url=https://flipmyera.com" />
</head><body>Redirecting...</body></html>`
}
```

### Step 2 — Update Netlify headers/redirects

Update `public/_headers` to include cache-control for the og-preview function.

Create or update `public/_redirects` (Netlify redirect rules):

```
# Bot detection for OG preview — redirect social scrapers to edge function
/ebook/:id/preview  /.netlify/functions/og-preview?id=:id  200  X-User-Agent-Match:facebookexternalhit|Twitterbot|LinkedInBot|Slackbot|TelegramBot|Discordbot|WhatsApp
```

**Note:** Netlify's `_redirects` does not support User-Agent matching natively. Instead, use a Netlify Function or Edge Function. The recommended approach for Netlify is:

Create `netlify/edge-functions/og-preview.ts`:

```typescript
import type { Context } from "https://edge.netlify.com"

const BOT_AGENTS = ['facebookexternalhit', 'Twitterbot', 'LinkedInBot', 'Slackbot', 'Discordbot', 'WhatsApp', 'Googlebot']

export default async (request: Request, context: Context) => {
  const url = new URL(request.url)
  const pathMatch = url.pathname.match(/^\/ebook\/([^/]+)\/preview$/)
  
  if (!pathMatch) return context.next()
  
  const userAgent = request.headers.get('user-agent') || ''
  const isBot = BOT_AGENTS.some(bot => userAgent.toLowerCase().includes(bot.toLowerCase()))
  
  if (!isBot) return context.next()
  
  const ebookId = pathMatch[1]
  const supabaseUrl = Deno.env.get('VITE_SUPABASE_URL') || ''
  const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || ''
  
  // Fetch and return OG preview HTML
  // (same logic as supabase edge function above)
  const response = await fetch(`${supabaseUrl}/functions/v1/og-preview?id=${ebookId}`, {
    headers: { Authorization: `Bearer ${supabaseKey}` }
  })
  
  return response
}

export const config = { path: "/ebook/:id/preview" }
```

Create `netlify.toml` (or update if it exists):
```toml
[build]
  publish = "dist"

[[edge_functions]]
  path = "/ebook/:id/preview"
  function = "og-preview"
```

### Step 3 — Update ShareablePreview to set OG tags dynamically

In `src/modules/sharing/ShareablePreview.tsx`, ensure the `<Helmet>` tags are set dynamically once ebook data loads (for the benefit of server-side rendering in the future):

```tsx
<Helmet>
  <title>{ebook.title} | FlipMyEra</title>
  <meta property="og:title" content={`${ebook.title} — FlipMyEra`} />
  <meta property="og:description" content={ebook.description || `A ${ebook.era} era story`} />
  {ebook.cover_image_url && <meta property="og:image" content={ebook.cover_image_url} />}
  <meta property="og:url" content={shareUrl} />
  <meta name="twitter:card" content="summary_large_image" />
</Helmet>
```

This is already partially done but ensure it's correct.

### Step 4 — Add the edge function to deploy workflow

In `.github/workflows/supabase-deploy.yml`, add `og-preview` to the list of deployed functions.

## Dependencies

None (though TODO #010 Gallery wiring is related).

## Effort

M (1-2 days)

## Acceptance Criteria

- [ ] Supabase Edge Function `og-preview` created and deployable
- [ ] Netlify Edge Function (or equivalent) detects social bots and returns OG HTML
- [ ] When pasting a story URL into Discord/Twitter, the preview shows the story title, era, and cover image
- [ ] Non-bot requests (real users) pass through to the React SPA normally
- [ ] `npm run typecheck` passes
- [ ] Edge function tests added to `supabase/functions/tests/`
- [ ] Deploy workflow updated to include new edge function
