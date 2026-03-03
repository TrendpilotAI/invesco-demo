# TODO-447: FAQ Accordion + FAQPage JSON-LD on Pricing Page

**Repo:** signalhaus-website  
**Priority:** P2 (SEO + UX)  
**Effort:** S (~1.5 hours)  
**Status:** pending

## Description
Add FAQ accordion to pricing page addressing common objections. Add FAQPage JSON-LD schema for rich results eligibility in Google SERPs (Google can show FAQ answers directly in search results).

## Acceptance Criteria
- [ ] Pricing page has FAQ section with 6-8 questions
- [ ] Accordion collapses/expands with smooth animation (no external library)
- [ ] FAQPage JSON-LD in <head> for the pricing page
- [ ] Mobile-responsive

## FAQ Questions to Include
1. How long does implementation take?
2. Do I need an existing data team to work with SignalHaus?
3. What does "up to 3 automations" mean exactly?
4. Can we start with QuickStart and upgrade later?
5. Do you work with companies outside financial services?
6. What's included in the 30-day support?
7. How is SignalHaus different from hiring an in-house AI team?
8. Is there a contract or can I cancel anytime?

## Coding Prompt
```
1. Create src/components/FAQAccordion.tsx:
   - Props: items: Array<{ question: string; answer: string }>
   - Use React useState for open/close tracking (array of booleans or active index)
   - Smooth max-height transition with Tailwind: transition-all duration-300
   - Plus/minus icon (or chevron) to indicate open/closed
   - aria-expanded attribute for accessibility

2. Add FAQ section to src/app/pricing/page.tsx:
   - Import FAQAccordion
   - Define faqItems array with 8 Q&As above
   - Render below pricing tiers with heading "Frequently Asked Questions"

3. Add FAQPage JSON-LD to pricing page metadata:
   In pricing/page.tsx, add a <Script> tag with type="application/ld+json":
   {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "mainEntity": faqItems.map(item => ({
       "@type": "Question",
       "name": item.question,
       "acceptedAnswer": { "@type": "Answer", "text": item.answer }
     }))
   }
   Use next/script with id="faq-schema" strategy="afterInteractive"
```
