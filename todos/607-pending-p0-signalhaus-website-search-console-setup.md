# TODO-607: Google Search Console + Sitemap Submission

**Repo:** signalhaus-website  
**Priority:** P0  
**Effort:** XS (30 min)  
**Status:** pending

## Description
Sitemap is dynamically generated at `/sitemap.xml` but has likely never been submitted to Google Search Console. This is a free SEO boost.

## Tasks
1. Verify ownership of signalhaus.ai in Google Search Console (DNS TXT record or HTML file method)
2. Add verification meta tag to `layout.tsx` if using HTML method
3. Submit sitemap URL: `https://www.signalhaus.ai/sitemap.xml`
4. Submit RSS feed: `https://www.signalhaus.ai/feed.xml`
5. Monitor for crawl errors

## Coding Prompt
Add to `layout.tsx` metadata:
```ts
verification: {
  google: 'YOUR_VERIFICATION_CODE',
},
```

## Acceptance Criteria
- [ ] Domain verified in Search Console
- [ ] Sitemap submitted and indexed
- [ ] No crawl errors shown
- [ ] Coverage report shows all pages indexed

## Dependencies
None
