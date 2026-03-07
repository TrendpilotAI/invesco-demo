# TODO-828: Case Study Detail Pages (MDX-based)
**Repo:** signalhaus-website  
**Priority:** P1 (High)  
**Status:** pending  
**Effort:** 2 days

## Problem
All 3 case studies live on a single `/case-studies` page as inline data. No individual URLs for deep linking, social sharing, or targeted SEO. Missing schema markup per case study.

## Task
Convert inline case study data to MDX files + individual detail pages.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website:

1. Create /content/case-studies/ directory

2. Create 3 MDX files with frontmatter:
   - wealth-management-reporting.mdx
   - asset-manager-lead-intelligence.mdx  
   - enterprise-data-onboarding.mdx

   Frontmatter schema:
   ---
   id: "wealth-management-reporting"
   title: "75% Reduction in Reporting Time for Fortune 500 Wealth Manager"
   client: "Global Wealth Manager"
   industry: "Financial Services"
   tag: "Workflow Automation"
   tagColor: "indigo"
   logo: "🏦"
   summary: "Short 1-sentence summary for card view"
   results:
     - metric: "75%"
       label: "Reduction in manual reporting time"
   quote: "We went from dreading quarter-end to not noticing it."
   quoteAuthor: "SVP of Operations"
   quoteCompany: "Fortune 500 Wealth Manager"
   publishedAt: "2024-01-15"
   ---

   Body: Expanded problem/solution narrative in markdown

3. Create /src/lib/case-studies.ts:
   - getAllCaseStudiesMeta() → reads frontmatter from all MDX files
   - getCaseStudy(slug) → returns frontmatter + compiled MDX content
   - Similar pattern to /src/lib/mdx.ts

4. Create /src/app/case-studies/[slug]/page.tsx:
   - generateStaticParams() → all case study slugs
   - generateMetadata() → unique title/description/OG per case study
   - Render: hero with client/industry/tag, metrics grid, problem/solution, quote, CTA
   - JSON-LD: Article schema with headline, author (Organization), datePublished

5. Update /src/app/case-studies/page.tsx:
   - Replace inline data array with getAllCaseStudiesMeta()
   - Make cards link to /case-studies/[slug]

6. Update /src/app/sitemap.ts to include case study URLs
```

## Acceptance Criteria
- 3 individual case study pages at /case-studies/[slug]
- Each has unique SEO metadata
- Cards on /case-studies link to detail pages
- generateStaticParams ensures SSG (no server-side rendering)
- Sitemap includes new URLs

## Dependencies
- None (independent of other TODOs)
