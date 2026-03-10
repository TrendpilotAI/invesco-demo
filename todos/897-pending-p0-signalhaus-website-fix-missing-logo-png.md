# TODO-897: Fix Missing logo.png (JSON-LD 404)
**Repo:** signalhaus-website  
**Priority:** P0 (Quick Win)  
**Status:** pending  
**Effort:** 15 minutes

## Problem
`src/app/layout.tsx` references `https://www.signalhaus.ai/logo.png` in the Organization JSON-LD schema:
```typescript
logo: {
  "@type": "ImageObject",
  url: "https://www.signalhaus.ai/logo.png",  // ← 404!
  width: 200,
  height: 60,
},
```

The file `/public/logo.png` does NOT exist. This causes:
- Google's structured data parser to fail on the logo field
- A 404 hit visible in Google Search Console
- Broken Organization rich results
- Potential downgrade in Google's trust of structured data

## Task
Create or export a SignalHaus logo PNG and place it at `/public/logo.png`.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website:

Option A — Create from existing branding:
  Export the SignalHaus wordmark as a PNG file (200x60px, transparent background)
  Save to /public/logo.png

Option B — Generate a simple text-based logo SVG, convert to PNG:
  Create a 200x60px image with "SignalHaus" text in white on transparent background
  Save to /public/logo.png

Option C — Use next/og to generate the logo image dynamically:
  Create /src/app/logo.png/route.ts returning an ImageResponse with the SignalHaus logo

After adding the file, verify:
1. GET /logo.png returns 200
2. The JSON-LD in layout.tsx is valid
3. Test in Google's Rich Results Test: https://search.google.com/test/rich-results

Also verify and fix: layout.tsx currently has no <link rel="alternate"> for the RSS feed.
Add to layout.tsx in the <head>:
  <link rel="alternate" type="application/rss+xml" title="SignalHaus Blog" href="/feed.xml" />
```

## Dependencies
- None — standalone asset fix

## Acceptance Criteria
- `GET https://www.signalhaus.ai/logo.png` returns 200 with a real PNG
- Google Rich Results Test validates Organization schema
- No 404 in Google Search Console for /logo.png
- RSS feed linked in `<head>` for discoverability
