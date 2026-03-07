# TODO-827: Create Service Detail Pages (3 pages)
**Repo:** signalhaus-website  
**Priority:** P1 (High)  
**Status:** pending  
**Effort:** 3 days

## Problem
`/services` is a single overview page. No individual pages for AI Strategy, Data Integration, or Workflow Automation. Missing high-intent SEO keywords and specific conversion paths per service.

## Task
Create 3 individual service detail pages with full content, SEO metadata, and conversion CTAs.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website, create three service detail pages:

1. /src/app/services/ai-strategy/page.tsx
2. /src/app/services/data-integration/page.tsx
3. /src/app/services/workflow-automation/page.tsx

Each page structure:
- export const metadata: Metadata = { title, description, alternates: {canonical}, openGraph }
- Hero: H1 with service name, 2-sentence description, "Book a Free Strategy Call" CTA → /contact
- Section "The Problem": 3-4 pain points as a list (dark card)
- Section "How We Solve It": Our approach, what we actually do
- Section "What You Get": Deliverables bulleted list
- Section "Timeline": Typical engagement (e.g. "2-week assessment → 4-week pilot → ongoing")
- Section "Case Study Excerpt": Pull a relevant case study card with link to /case-studies
- CTA Section: "Ready to get started?" with link to /contact and /pricing
- JSON-LD: Service schema with serviceType, provider (Organization), areaServed

Content per service:

AI STRATEGY:
- Pain points: AI hype without ROI, no roadmap, board asking for AI plan, past AI projects failed
- Deliverables: AI readiness assessment, 90-day roadmap, vendor evaluation matrix, board presentation
- Timeline: 2-week assessment, 2-week roadmap delivery, optional 30-day pilot

DATA INTEGRATION:
- Pain points: Data in silos, manual CSV exports, reporting takes days, conflicting numbers from different tools
- Deliverables: Data architecture diagram, unified pipeline, Salesforce/warehouse connectors, automated reconciliation
- Timeline: 1-week discovery, 3-week build, 2-week QA and handoff

WORKFLOW AUTOMATION:
- Pain points: Manual processes burning headcount, errors from copy/paste, staff doing robot work
- Deliverables: Process audit, 3-10 automations, AI agents for outreach/qualification/reporting, monitoring dashboard
- Timeline: 1-week audit, 2-week build, 1-week testing, ongoing support

Update /src/app/services/page.tsx service cards to link to respective detail pages.
Update /src/components/Footer.tsx service links to point to detail pages.
Update sitemap.ts to include new pages.
```

## Acceptance Criteria
- 3 service detail pages render without errors
- Each has unique metadata and OG tags
- Each links to /contact with pre-filled service context if possible
- Footer and services overview page link to detail pages
- Sitemap includes new URLs

## Dependencies
- None (can be built independently)
