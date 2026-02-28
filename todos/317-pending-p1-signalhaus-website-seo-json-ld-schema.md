# TODO 317: SignalHaus Website — JSON-LD Structured Data

**Priority:** P1 (SEO)
**Effort:** S (2-4 hours)
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Description
No structured data exists. Adding JSON-LD Organization and Service schemas improves Google rich results eligibility and SEO signals.

## Acceptance Criteria
- [ ] Organization schema on homepage (name, url, logo, sameAs for LinkedIn/Twitter)
- [ ] Service schema on /services page for each service offering
- [ ] ProfessionalService schema on /about page
- [ ] FAQPage schema if FAQ section added
- [ ] Valid schema (test with Google Rich Results Test)

## Coding Prompt

```
In /data/workspace/projects/signalhaus-website/src/:

1. Create src/components/JsonLd.tsx:
   - Generic component: <JsonLd data={object} />
   - Renders: <script type="application/ld+json">{JSON.stringify(data)}</script>

2. Add to src/app/layout.tsx (global Organization schema):
   {
     "@context": "https://schema.org",
     "@type": "Organization",
     "name": "SignalHaus",
     "url": "https://www.signalhaus.ai",
     "logo": "https://www.signalhaus.ai/og-image.png",
     "description": "AI consulting for enterprises...",
     "sameAs": ["https://www.linkedin.com/company/signalhaus"]
   }

3. Add to src/app/services/page.tsx (Service schemas for each offering):
   {
     "@context": "https://schema.org",
     "@type": "Service",
     "name": "AI Strategy Consulting",
     "provider": { "@type": "Organization", "name": "SignalHaus" },
     "description": "..."
   }

4. Add dynamic sitemap at src/app/sitemap.ts (Next.js built-in) replacing static public/sitemap.xml:
   - Automatically includes all routes + blog posts
```

## Dependencies
None
