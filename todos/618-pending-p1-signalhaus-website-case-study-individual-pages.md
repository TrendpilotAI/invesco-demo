# TODO 618 — Individual Case Study Pages /case-studies/[slug]

**Repo:** signalhaus-website
**Priority:** P1
**Effort:** M (2-3 days)
**Status:** pending

## Problem
All case studies live on a single `/case-studies` page. There are no individual case study pages that can be shared, linked to from sales emails, or indexed individually by search engines.

## Task
1. Create MDX content files in `/content/case-studies/` for each case study
2. Build dynamic route `src/app/case-studies/[slug]/page.tsx`
3. Each page should have: challenge, solution, results, quotes, CTA, JSON-LD Article schema
4. Update `/case-studies` listing page to link to individual pages
5. Add individual case studies to sitemap

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/:

1. Create /content/case-studies/ directory with MDX files:
   - hedge-fund-lead-qual.mdx
   - insurance-claims-automation.mdx
   - wealth-mgmt-workflow.mdx
   
   Frontmatter format:
   ---
   title: "How a Hedge Fund Automated Lead Qualification"
   client: "Mid-size Hedge Fund"
   industry: "Financial Services"
   results: ["80% reduction in manual workflow time", "$2M pipeline unblocked"]
   date: "2026-02-01"
   excerpt: "Short description..."
   ---

2. Create src/app/case-studies/[slug]/page.tsx:
   - Use getMdxContent from src/lib/mdx.ts
   - generateStaticParams to pre-render all slugs
   - generateMetadata for SEO (title, description, OG)
   - JSON-LD Article schema
   - CTA section: "Ready to achieve similar results? Book a call"

3. Update src/app/case-studies/page.tsx to link to individual pages

4. Update src/app/sitemap.ts to include case study slugs
```

## Acceptance Criteria
- [ ] `/case-studies/[slug]` renders for each case study
- [ ] generateStaticParams pre-builds all pages
- [ ] Each page has proper SEO metadata + OG
- [ ] Listing page links to individual pages
- [ ] Sitemap includes individual case study URLs
- [ ] JSON-LD Article schema on each case study page
