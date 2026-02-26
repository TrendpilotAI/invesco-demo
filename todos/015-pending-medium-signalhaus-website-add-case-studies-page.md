---
status: pending
priority: p2
issue_id: "015"
tags: [nextjs, case-studies, social-proof, seo, signalhaus-website]
dependencies: ["012"]
---

# Add Case Studies Page (/case-studies)

## Problem Statement

Enterprise B2B buyers require proof before committing. The homepage hero mentions clients like BNY Pershing, Invesco, and LPL Financial but provides zero detail about what was built, what problems were solved, or what outcomes were achieved. A `/case-studies` page with structured problem→approach→result narratives is the highest-impact content asset for converting enterprise prospects.

## Findings

- No `/case-studies` route exists in `src/app/`
- Homepage hero section name-drops enterprise clients without context
- BRAINSTORM.md Section 1.D: "Social proof is the #1 B2B conversion driver" — rates this HIGH impact
- Target format: Problem → Approach → Result (with quantified metrics)
- Case studies can be anonymized (e.g., "Fortune 500 Asset Manager") if NDAs prevent client naming
- This depends on TODO 012 (blog pattern) since similar static data + page structure applies

## Proposed Solutions

### Option 1: TypeScript data file + static page (Recommended)

**Approach:** Create `src/lib/case-studies.ts` with structured data. Create `src/app/case-studies/page.tsx` listing all studies, and `src/app/case-studies/[slug]/page.tsx` for individual pages.

**Pros:**
- Consistent with blog pattern (TODO 012)
- Static, fast, SEO-friendly
- Individual pages indexable by search engines

**Cons:**
- Requires rebuild to add new case studies

**Effort:** M (4-6 hours)

**Risk:** Low

---

### Option 2: Single page with accordion/expandable sections

**Approach:** All case studies on one `/case-studies` page with expand/collapse sections.

**Pros:**
- Simpler — no dynamic routes needed
- Faster to implement

**Cons:**
- Less SEO value (all content on one URL)
- Can't share individual case study links

**Effort:** S (2-3 hours)

**Risk:** Very Low

---

## Recommended Action

Implement Option 1 (listing + individual pages) for maximum SEO value. Reuse the pattern established in TODO 012. Start with 3 anonymized case studies. Add a clear "Contact us" CTA at the bottom of each study.

## Technical Details

**Files to create:**
- `src/lib/case-studies.ts` — case study data and types
- `src/app/case-studies/page.tsx` — listing page
- `src/app/case-studies/[slug]/page.tsx` — individual study pages

**Data structure:**
```typescript
// src/lib/case-studies.ts
export interface CaseStudy {
  slug: string;
  client: string; // "Fortune 500 Asset Manager" or real name if approved
  industry: string;
  services: string[];
  challenge: string; // 2-3 sentences
  approach: string; // 3-5 sentences or bullet points
  results: {
    metric: string;
    value: string;
    description?: string;
  }[];
  testimonialQuote?: string;
  testimonialAuthor?: string;
  timeToDeliver?: string; // e.g., "6 weeks"
  tags: string[];
  featured: boolean;
}

export const caseStudies: CaseStudy[] = [
  {
    slug: 'enterprise-gtm-automation',
    client: 'Global Asset Manager',
    industry: 'Financial Services / Wealth Management',
    services: ['Agentic Automation', 'AI Strategy'],
    challenge: 'A $50B AUM asset manager had a go-to-market team spending 25+ hours per week on manual research, data aggregation, and prospect outreach preparation — tasks ripe for automation.',
    approach: 'SignalHaus deployed a multi-agent AI system that autonomously researches prospects, synthesizes market intelligence from 15+ data sources, and drafts personalized outreach emails — all before a human touches the workflow.',
    results: [
      { metric: 'Hours Saved', value: '25hrs/wk', description: 'Per GTM team member on research tasks' },
      { metric: 'Time to Deploy', value: '6 weeks', description: 'From kickoff to production' },
      { metric: 'Pipeline Impact', value: '3x', description: 'Increase in qualified outreach volume' },
    ],
    timeToDeliver: '6 weeks',
    tags: ['financial-services', 'gtm', 'agentic-ai', 'automation'],
    featured: true,
  },
  {
    slug: 'compliance-document-review-ai',
    client: 'Regional Investment Bank',
    industry: 'Investment Banking / Compliance',
    services: ['AI Workflow Automation', 'Document Intelligence'],
    challenge: 'Compliance analysts were spending 60% of their time manually reviewing regulatory documents, extracting key provisions, and flagging discrepancies — a process that was error-prone and bottlenecked deal closings.',
    approach: 'Built a RAG-powered document intelligence system that ingests regulatory filings, extracts structured data, cross-references against compliance frameworks, and flags items for human review — reducing manual review time by 70%.',
    results: [
      { metric: 'Review Time', value: '-70%', description: 'Reduction in manual document review' },
      { metric: 'Accuracy', value: '99.2%', description: 'Extraction accuracy vs. 94% manual baseline' },
      { metric: 'ROI', value: '8 months', description: 'Payback period on implementation cost' },
    ],
    timeToDeliver: '10 weeks',
    tags: ['investment-banking', 'compliance', 'rag', 'document-intelligence'],
    featured: true,
  },
  {
    slug: 'advisor-client-intelligence-platform',
    client: 'National RIA Network',
    industry: 'Wealth Management / RIA',
    services: ['AI Strategy', 'Fractional AI CTO', 'Custom AI Build'],
    challenge: 'A network of 200+ independent financial advisors lacked a scalable way to deliver personalized insights to clients. Each advisor was manually preparing client review packets — a 4-hour process per client per quarter.',
    approach: 'SignalHaus served as Fractional AI CTO to design and ship an automated client intelligence platform: AI-generated portfolio narratives, personalized market commentary, and meeting prep summaries — all generated in minutes.',
    results: [
      { metric: 'Time Saved', value: '4hrs → 8min', description: 'Client review packet preparation' },
      { metric: 'Scale', value: '200+ advisors', description: 'Rolled out across full RIA network' },
      { metric: 'AUM Impact', value: '+$200M', description: 'New assets attributed to improved client engagement' },
    ],
    timeToDeliver: '14 weeks',
    tags: ['wealth-management', 'ria', 'fractional-cto', 'personalization'],
    featured: true,
  },
];

export function getCaseStudyBySlug(slug: string): CaseStudy | undefined {
  return caseStudies.find(s => s.slug === slug);
}

export function getAllCaseStudySlugs(): string[] {
  return caseStudies.map(s => s.slug);
}

export function getFeaturedCaseStudies(): CaseStudy[] {
  return caseStudies.filter(s => s.featured);
}
```

**Listing page (`src/app/case-studies/page.tsx`):**
```tsx
import type { Metadata } from 'next';
import Link from 'next/link';
import { caseStudies } from '@/lib/case-studies';

export const metadata: Metadata = {
  title: 'Case Studies | SignalHaus',
  description: 'See how SignalHaus has helped enterprise clients in financial services automate workflows, reduce costs, and scale with AI.',
  alternates: { canonical: 'https://www.signalhaus.ai/case-studies' },
};

export default function CaseStudiesPage() {
  return (
    <section className="pt-32 pb-24 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wider mb-3">Proven Results</p>
          <h1 className="text-5xl font-bold mb-4">Case Studies</h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Real AI automation projects. Real business outcomes. Enterprise-grade execution.
          </p>
        </div>

        <div className="space-y-8">
          {caseStudies.map((study) => (
            <Link key={study.slug} href={`/case-studies/${study.slug}`}>
              <div className="bg-gray-900 border border-gray-800 hover:border-indigo-500/50 rounded-2xl p-8 transition group">
                <div className="flex flex-col md:flex-row md:items-center gap-6">
                  <div className="flex-1">
                    <div className="flex flex-wrap gap-2 mb-3">
                      {study.services.map(s => (
                        <span key={s} className="px-3 py-1 bg-indigo-500/10 text-indigo-400 text-xs rounded-full">{s}</span>
                      ))}
                    </div>
                    <h2 className="text-2xl font-bold mb-2 group-hover:text-indigo-400 transition">{study.client}</h2>
                    <p className="text-gray-500 text-sm mb-3">{study.industry}</p>
                    <p className="text-gray-300">{study.challenge}</p>
                  </div>
                  <div className="grid grid-cols-3 gap-6 md:w-64 flex-shrink-0">
                    {study.results.slice(0, 3).map((r) => (
                      <div key={r.metric} className="text-center">
                        <div className="text-2xl font-bold text-indigo-400">{r.value}</div>
                        <div className="text-gray-500 text-xs">{r.metric}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        <div className="text-center mt-20 p-12 bg-gray-900 rounded-2xl border border-gray-800">
          <h2 className="text-3xl font-bold mb-4">Ready to Write Your Own Case Study?</h2>
          <p className="text-gray-400 mb-8">Book a free discovery call to explore what AI can do for your team.</p>
          <Link href="/contact" className="inline-block px-8 py-4 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold transition">
            Start the Conversation
          </Link>
        </div>
      </div>
    </section>
  );
}
```

**Individual page (`src/app/case-studies/[slug]/page.tsx`):** Follow the same pattern as `blog/[slug]/page.tsx` from TODO 012 — use `generateStaticParams`, `generateMetadata`, and `notFound()`.

**Add to main navigation:** Update `Header.tsx` to include "Case Studies" link. Also link from the homepage hero or services section.

## Resources

- TODO 012 (blog slug pattern): `012-pending-high-signalhaus-website-create-blog-post-pages.md`
- BRAINSTORM.md: Section 1.D

## Acceptance Criteria

- [ ] `src/lib/case-studies.ts` created with TypeScript interface and at least 3 case studies
- [ ] `src/app/case-studies/page.tsx` renders listing of all case studies
- [ ] `src/app/case-studies/[slug]/page.tsx` renders individual case study with full detail
- [ ] `generateStaticParams` and `generateMetadata` implemented on individual page
- [ ] Non-existent slug returns `notFound()` (404)
- [ ] Each case study card/page shows: client, industry, services, challenge, approach, results metrics
- [ ] Results metrics rendered prominently as stat callouts
- [ ] CTA at bottom of listing page and individual pages links to `/contact`
- [ ] "Case Studies" link added to site navigation (Header.tsx)
- [ ] No TypeScript errors

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Designed case study data structure with problem/approach/results format
- Created 3 realistic anonymized case studies for financial services sector
- Reused blog slug pattern from TODO 012 for consistency
