# TODO-323: Dynamic Sitemap for signalhaus-website

**Priority:** P1  
**Effort:** 30 min  
**Repo:** signalhaus-website  
**Status:** pending  

## Description
Replace `public/sitemap.xml` (static) with `src/app/sitemap.ts` using Next.js built-in dynamic sitemap generation. The static file won't auto-update when new MDX blog posts are added — this will.

## Coding Prompt (Agent-Executable)

```
In /data/workspace/projects/signalhaus-website/:

1. Create src/app/sitemap.ts:
   - Import getAllPostsMeta from @/lib/mdx
   - Return MetadataRoute.Sitemap with:
     - Static routes: /, /about, /services, /pricing, /contact, /case-studies, /roi-calculator, /blog
     - Dynamic blog routes: map getAllPostsMeta() to /blog/[slug]
     - Set changeFrequency and priority per route type
     - Use SITE_URL = 'https://www.signalhaus.ai'

2. Update next.config.ts to ensure static sitemap is excluded (or delete public/sitemap.xml)

3. Verify: npm run build should generate /sitemap.xml in the build output
```

## Acceptance Criteria
- [ ] `src/app/sitemap.ts` exists and compiles without errors
- [ ] All static routes included
- [ ] Blog posts dynamically included
- [ ] `public/sitemap.xml` removed or superseded
- [ ] Build passes

## Dependencies
None
