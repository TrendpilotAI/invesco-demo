# TODO 323 — Replace Static Sitemap with Dynamic Next.js Sitemap

**Priority:** P2 — Medium  
**Repo:** signalhaus-website  
**Effort:** S (30-60 min)  
**Dependencies:** None

---

## Description

`public/sitemap.xml` is static and won't include new blog posts added as MDX files. Replace with `src/app/sitemap.ts` using Next.js built-in sitemap generation that auto-includes all blog posts.

---

## Coding Prompt

```
In /data/workspace/projects/signalhaus-website/:

1. Delete `public/sitemap.xml` (or rename to `public/sitemap.xml.bak`)

2. Create `src/app/sitemap.ts`:
   ```ts
   import { MetadataRoute } from 'next'
   import { getAllPosts } from '@/lib/mdx'
   
   const BASE_URL = 'https://signalhaus.ai'
   
   export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
     const posts = await getAllPosts()
     
     const staticRoutes: MetadataRoute.Sitemap = [
       { url: BASE_URL, lastModified: new Date(), changeFrequency: 'weekly', priority: 1 },
       { url: `${BASE_URL}/about`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
       { url: `${BASE_URL}/services`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.9 },
       { url: `${BASE_URL}/pricing`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.9 },
       { url: `${BASE_URL}/case-studies`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
       { url: `${BASE_URL}/blog`, lastModified: new Date(), changeFrequency: 'weekly', priority: 0.7 },
       { url: `${BASE_URL}/contact`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
       { url: `${BASE_URL}/roi-calculator`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.7 },
     ]
     
     const blogRoutes: MetadataRoute.Sitemap = posts.map(post => ({
       url: `${BASE_URL}/blog/${post.slug}`,
       lastModified: post.frontmatter.date ? new Date(post.frontmatter.date) : new Date(),
       changeFrequency: 'monthly' as const,
       priority: 0.6,
     }))
     
     return [...staticRoutes, ...blogRoutes]
   }
   ```

3. Verify `getAllPosts()` in `src/lib/mdx.ts` returns slugs and frontmatter correctly.

4. Run `yarn build` — Next.js will generate `/sitemap.xml` at build time.

5. Verify the sitemap output includes all pages + blog posts.
```

---

## Acceptance Criteria
- [ ] `src/app/sitemap.ts` exists
- [ ] `public/sitemap.xml` removed (Next.js sitemap takes precedence)
- [ ] `yarn build` generates sitemap that includes blog post URLs
- [ ] All static pages listed with correct priorities
