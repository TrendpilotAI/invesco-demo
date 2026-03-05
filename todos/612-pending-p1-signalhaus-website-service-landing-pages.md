# TODO-612: Individual Service Landing Pages (SEO)

**Repo:** signalhaus-website  
**Priority:** P1  
**Effort:** M (1-2 days)  
**Status:** pending

## Description
All services are on one `/services` page. Individual landing pages unlock long-tail SEO keywords and enable paid search campaigns per service.

## Pages to Create
- `/services/ai-strategy` — "AI Strategy Consulting for Enterprise"
- `/services/data-integration` — "Enterprise Data Integration Services"  
- `/services/workflow-automation` — "AI Workflow Automation Consulting"
- `/services/custom-ai-agents` — "Custom AI Agent Development"
- `/services/fractional-cto` — "Fractional CTO Services"

## Each Page Structure
1. Hero: problem statement + value prop
2. What you get (deliverables)
3. How it works (3-step process)
4. Results / case study excerpt
5. Pricing signal
6. FAQ (with FAQ schema JSON-LD)
7. CTA: Book consultation

## Coding Prompt
Use dynamic routes: `src/app/services/[slug]/page.tsx`
Define service data in `src/lib/services.ts` with full content per service.
Add FAQ schema JSON-LD per service for SERP features.
Add canonical URLs and unique OG metadata per page.

## Acceptance Criteria
- [ ] 5 service pages exist with unique content
- [ ] Each page has unique title, description, OG
- [ ] FAQ schema added
- [ ] Internal links from main /services page
- [ ] Sitemap updated (auto via dynamic sitemap)

## Dependencies
- TODO-607 (Search Console to track indexing)
