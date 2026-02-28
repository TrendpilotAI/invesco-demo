# TODO 316: SignalHaus Website — Testimonials & Case Studies

**Priority:** P1 (Conversion)
**Effort:** M (1-2 days)
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Description
The homepage has no social proof beyond badge names (rendered as text). Adding testimonials and a case studies page will dramatically improve conversion rates for enterprise B2B buyers.

## Acceptance Criteria
- [ ] Testimonials section on homepage (3-5 testimonials with name, title, company, quote)
- [ ] `/case-studies` page with 2-3 detailed case studies
- [ ] Each case study: client overview, problem, solution, measurable results
- [ ] Case studies linked from homepage hero and services page
- [ ] Responsive design matching existing dark theme

## Coding Prompt

```
In /data/workspace/projects/signalhaus-website/src/:

1. Add testimonials section to src/app/page.tsx:
   - Create const testimonials = [{ quote, name, title, company }] with 3-5 placeholder entries (Nathan to fill real ones)
   - Add section between "Pricing Preview" and "CTA" sections
   - Card design: dark bg, quote in large text, attribution below with avatar initials circle
   - Add subtle animation: opacity fade-in on scroll using CSS

2. Create src/app/case-studies/page.tsx:
   - Add metadata with SEO title/description
   - 3 case studies: "Wealth Management Firm", "RIA Automation", "Enterprise Data Integration"
   - Each card links to individual case study page
   - Include: industry, challenge, solution, results (percentage improvements)

3. Create src/app/case-studies/[slug]/page.tsx for individual case study detail pages
   - Static params for the 3 initial studies
   - Full narrative: problem → approach → implementation → results

4. Update Header.tsx navigation to add "Case Studies" link
5. Update sitemap.xml to include new pages
```

## Dependencies
None (standalone feature)
