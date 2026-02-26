---
status: pending
priority: p1
issue_id: "012"
tags: [nextjs, blog, seo, dynamic-routes, signalhaus-website]
dependencies: []
---

# Create Blog Post Dynamic Route Pages (/blog/[slug])

## Problem Statement

The blog listing page at `/blog` exists and renders post cards, but clicking any post leads to a 404. The dynamic route `src/app/blog/[slug]/page.tsx` does not exist. This is a broken user experience for anyone who reads the blog preview and clicks through, and it means existing blog content provides zero SEO value as individual pages.

The site has at least one blog post defined in its data source ("Agentic Automation — the Future of GTM") with no way to actually read it.

## Findings

- `src/app/blog/page.tsx` exists and renders blog card components
- `src/app/blog/[slug]/` directory does **not exist**
- No dynamic route handler for individual posts
- Blog post data source needs investigation: likely hardcoded in blog page or a `lib/posts.ts` file
- SEO opportunity lost: each blog post should be a standalone indexed page with proper metadata
- BRAINSTORM.md rates blog content as HIGH impact for lead gen

## Proposed Solutions

### Option 1: Static blog posts in `lib/blog-posts.ts` with `generateStaticParams` (Recommended)

**Approach:** Define all blog posts in a TypeScript data file. Create `src/app/blog/[slug]/page.tsx` that uses `generateStaticParams` to pre-render all posts at build time.

**Pros:**
- Zero external dependencies — no CMS needed
- Fully static, fast as possible
- Easy to add posts (just add to the data array)
- SEO-optimal (SSG pages)

**Cons:**
- Requires rebuild to publish new posts
- Not suitable if content team needs a CMS

**Effort:** 3-4 hours

**Risk:** Low

---

### Option 2: MDX files + gray-matter frontmatter

**Approach:** Store each post as `.mdx` in `content/blog/`. Parse with `gray-matter` + `next-mdx-remote`.

**Pros:**
- Rich markdown/MDX authoring
- Posts are files, easy to version control
- Supports React components in posts

**Cons:**
- Adds `next-mdx-remote` and `gray-matter` dependencies
- More complex setup

**Effort:** 5-6 hours

**Risk:** Low-Medium

---

### Option 3: Headless CMS (Contentful/Sanity)

**Approach:** Connect to a CMS for content management.

**Cons:**
- Overkill for a consultancy blog with ~2 posts/month
- External dependency, cost, API setup

**Effort:** L (1-2 days)

**Risk:** Medium

---

## Recommended Action

Implement Option 1 (static TypeScript data file + `generateStaticParams`). For a consultancy site with infrequent posts, this is the simplest, fastest, most maintainable approach. The blog data file becomes the single source of truth for both the listing page and individual post pages.

## Technical Details

**Files to create:**
- `src/lib/blog-posts.ts` — blog post data (or extend if already exists)
- `src/app/blog/[slug]/page.tsx` — dynamic route with `generateStaticParams`

**Files to modify:**
- `src/app/blog/page.tsx` — import from `lib/blog-posts.ts` instead of local data

**Blog post data structure:**
```typescript
// src/lib/blog-posts.ts
export interface BlogPost {
  slug: string;
  title: string;
  date: string;
  author: string;
  excerpt: string;
  readTime: string;
  category: string;
  tags: string[];
  content: string; // HTML or markdown string
  ogImage?: string;
}

export const blogPosts: BlogPost[] = [
  {
    slug: 'agentic-automation-future-gtm',
    title: 'Agentic Automation — the Future of GTM',
    date: '2025-01-15',
    author: 'Nathan',
    excerpt: 'How autonomous AI agents are transforming go-to-market strategies for enterprise companies.',
    readTime: '6 min read',
    category: 'AI Strategy',
    tags: ['agentic-ai', 'gtm', 'automation', 'enterprise'],
    content: `
      <p>...</p>
    `,
  },
  // Add more posts here
];

export function getPostBySlug(slug: string): BlogPost | undefined {
  return blogPosts.find(post => post.slug === slug);
}

export function getAllSlugs(): string[] {
  return blogPosts.map(post => post.slug);
}
```

**Dynamic route page:**
```typescript
// src/app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation';
import { getPostBySlug, getAllSlugs, type BlogPost } from '@/lib/blog-posts';
import type { Metadata } from 'next';

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return getAllSlugs().map(slug => ({ slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) return {};

  return {
    title: `${post.title} | SignalHaus Blog`,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.date,
      authors: [post.author],
      images: [{ url: post.ogImage || '/og-image.png', width: 1200, height: 630 }],
    },
    alternates: {
      canonical: `https://www.signalhaus.ai/blog/${slug}`,
    },
  };
}

export default async function BlogPostPage({ params }: Props) {
  const { slug } = await params;
  const post = getPostBySlug(slug);

  if (!post) notFound();

  return (
    <article className="pt-32 pb-24 px-6">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center gap-3 text-sm text-gray-400 mb-4">
            <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 rounded-full">{post.category}</span>
            <span>{post.date}</span>
            <span>·</span>
            <span>{post.readTime}</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-gray-400">{post.excerpt}</p>
        </div>

        {/* Content */}
        <div
          className="prose prose-invert prose-lg max-w-none
            prose-headings:font-bold prose-headings:text-white
            prose-p:text-gray-300 prose-p:leading-relaxed
            prose-a:text-indigo-400 prose-a:no-underline hover:prose-a:underline
            prose-code:text-indigo-300 prose-code:bg-gray-900 prose-code:px-1 prose-code:rounded
            prose-pre:bg-gray-900 prose-pre:border prose-pre:border-gray-800"
          dangerouslySetInnerHTML={{ __html: post.content }}
        />

        {/* CTA */}
        <div className="mt-16 p-8 bg-gray-900 rounded-2xl border border-gray-800 text-center">
          <h2 className="text-2xl font-bold mb-3">Ready to Automate Your Business?</h2>
          <p className="text-gray-400 mb-6">Book a free 30-minute discovery call with Nathan.</p>
          <a
            href="/contact"
            className="inline-block px-8 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold transition"
          >
            Book a Call
          </a>
        </div>
      </div>
    </article>
  );
}
```

**Note:** Also add `@tailwindcss/typography` plugin for prose styles:
```bash
npm install @tailwindcss/typography
```
Add to `tailwind.config.ts`: `plugins: [require('@tailwindcss/typography')]`

## Resources

- Next.js dynamic routes: https://nextjs.org/docs/app/building-your-application/routing/dynamic-routes
- `generateStaticParams`: https://nextjs.org/docs/app/api-reference/functions/generate-static-params
- @tailwindcss/typography: https://tailwindcss.com/docs/typography-plugin

## Acceptance Criteria

- [ ] `src/app/blog/[slug]/page.tsx` exists
- [ ] `src/lib/blog-posts.ts` (or equivalent) defines all blog posts with slug, title, date, excerpt, content, and metadata
- [ ] `generateStaticParams` returns all post slugs for static pre-rendering
- [ ] `generateMetadata` returns proper `title`, `description`, `openGraph`, and `canonical` for each post
- [ ] Visiting `/blog/agentic-automation-future-gtm` renders the full post (not 404)
- [ ] Blog listing page (`/blog`) imports from the same data source (no duplication)
- [ ] Visiting a non-existent slug returns `notFound()` (404 page)
- [ ] Post page includes: category badge, date, read time, title, excerpt, content, CTA section
- [ ] `@tailwindcss/typography` installed and applied for readable prose styles
- [ ] All existing blog post data from the listing page is preserved and routable

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Confirmed `/blog/[slug]` directory does not exist
- Designed TypeScript data file approach with `generateStaticParams`
- Provided full implementation for dynamic route page with metadata, prose styles, and CTA

**Learnings:**
- Next.js 15 `params` is a Promise — must `await params` in async components
- `@tailwindcss/typography` is essential for blog post prose readability
