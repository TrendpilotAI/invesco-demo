# SignalHaus.ai — Full SEO & Site Audit Report
**Date:** February 17, 2026  
**Audited by:** Honey 🍯  
**Tools:** Manual review, ClawHub seo-optimizer analyzer, curl headers analysis

---

## Executive Summary

SignalHaus.ai is a Framer-hosted site with **4 pages** that loads fast (56ms TTFB) but has significant SEO, copy, and UX issues that are hurting discoverability and credibility. The site looks professional but has leftover Framer template artifacts, grammatical errors, pricing inconsistencies, and missing SEO fundamentals.

**Scores:**
- Performance: ⭐⭐⭐⭐ (fast, reasonable size)
- SEO: ⭐⭐ (missing OG images, schema, weak titles/descriptions)
- Content: ⭐⭐ (typos, template leftovers, pricing confusion)
- Trust: ⭐⭐⭐ (good social proof, but generic bio + contact form issues)

---

## Critical Issues (Fix Immediately)

### 1. Grammar/Typos in Body Copy
**Location:** Homepage → "Experienced and Award Winning Team" section

**Current (broken):**
> "We are understand sales and GTM with CRO-level expertise gleaned from OpenTable, Booker and VTS as well aas Greyscale and the Ned private members club."

**Fixed:**
> "We understand sales and GTM with CRO-level expertise gleaned from OpenTable, Booker, and VTS, as well as Greyscale and the Ned private members club."

### 2. All 6 Images Missing Alt Text
Every image on the homepage (logos, founder photo, etc.) has no alt attribute — bad for accessibility and SEO.

### 3. Multiple H1 Tags Per Page
| Page | H1 Count | Should Be |
|------|----------|-----------|
| Homepage | 8 | 1 |
| Pricing | 3 | 1 |
| Service Catalog | 22 | 1 |
| /page | 0 | 1 |

This is a Framer responsive rendering issue (3 variants × each section). Still hurts SEO.

### 4. No OG Image on Any Page
Zero pages have `og:image` — any social share (LinkedIn, Twitter, Slack) will have no visual preview.

### 5. `/page` Route is Empty
In the sitemap but contains zero content. Google is indexing a blank page.

---

## SEO Issues

### Weak/Generic Title Tags
| Page | Current Title | Recommended |
|------|--------------|-------------|
| Homepage | "AI Agency & Data Automation Consultancy" | "SignalHaus — AI Strategy, Data Integration & Automation Consultancy" |
| Pricing | "Pricing" | "Pricing Plans — SignalHaus AI Consultancy" |
| Service Catalog | "Service Catalog" | "AI & Automation Service Catalog — SignalHaus" |
| /page | "SignalHaus - AI and Data Consulting Technology" | Delete this page or redirect to / |

### Meta Description Issues
| Page | Current | Issue |
|------|---------|-------|
| Homepage | "Homepage for an AI agency..." | Reads like internal notes, not marketing copy |
| Pricing | Good (128 chars) | ✅ OK |
| Service Catalog | Good but short (100 chars) | Could be longer |
| /page | "Supercharge your GTM..." (66 chars) | Too short + page is empty |

**Recommended homepage meta description:**
> "SignalHaus helps enterprises accelerate growth with custom AI strategy, data integrations, and intelligent automation. From rapid prototypes to enterprise-scale AI orchestration. Book a free consultation."

### No Schema.org Structured Data
None of the 4 pages have JSON-LD structured data. Recommend adding:

**Homepage — Organization + ProfessionalService:**
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "SignalHaus",
  "url": "https://www.signalhaus.ai",
  "founder": {
    "@type": "Person",
    "name": "Nathan Stevenson"
  },
  "description": "AI strategy, data integration, and workflow automation consultancy",
  "areaServed": "US",
  "priceRange": "$1,250 - $100,000+"
}
```

**Pricing — Offer schema for each tier**

### Missing Canonical Tags
No proper canonical URLs set. Risk of duplicate content issues (www vs non-www is handled by redirect, but pages should still have canonical).

---

## UX / Design Issues

### Framer Template Nav Artifacts
The header dropdown menus show:
- **Product:** Design, Content, Publish → **These don't exist**
- **Resources:** Blog, Careers, Docs, About → **These don't exist**
- **Community:** Join, Events, Experts → **These don't exist**

These are clearly from the Framer template and were never customized. Makes the site look unfinished.

### Contact Form Has Placeholder Text
The contact section shows **"Subtitle."** twice — placeholder text that was never replaced.

### Founder Bio is Generic
**Current:**
> "I love turning complex problems into simple, beautiful, and user-friendly experiences. With a strong focus on UX/UI, I design products that not only look great but also feel effortless to use."

This sounds like a generic designer bio template. It doesn't mention Nathan's actual background (ForwardLane, fintech, AI, Harvard, WEF, etc.)

**Recommended:**
> "I've spent 15+ years building AI and data products for the world's leading financial institutions. As founder of ForwardLane, I led enterprise AI implementations for firms like BNY Pershing, Invesco, and LPL Financial. Now at SignalHaus, I help companies cut through the AI noise and ship solutions that actually drive revenue."

### Inconsistent Brand Casing
- Header shows "Signalhaus" (lowercase h)
- Some sections show "SignalHaus" (camelCase)
- Pick one and be consistent (recommend **SignalHaus**)

---

## Pricing Inconsistency

The homepage and service catalog present **different pricing models** without explanation:

### Homepage Pricing
| Tier | Price |
|------|-------|
| QuickStart Automation | $1,250 flat |
| Growth Engine Suite | from $4,800/month |
| Intelligent Enterprise OS | $25K–$100K+ |

### Service Catalog Pricing
| Tier | Price |
|------|-------|
| Starter | $5,000–$10,000 |
| Growth | $15,000–$30,000 |
| Enterprise | $50,000+ |

These are clearly different offerings (homepage = subscription/retainer, catalog = project-based), but a visitor bouncing between pages would be confused. Need to either:
1. Reconcile into one model
2. Clearly label: "Monthly Plans" vs "Project Engagements"

---

## Security Headers

| Header | Status |
|--------|--------|
| HSTS | ✅ max-age=31536000 |
| X-Content-Type-Options | ✅ nosniff |
| Content-Security-Policy | ❌ Missing |
| X-Frame-Options | ❌ Missing |
| Permissions-Policy | ❌ Missing |
| Referrer-Policy | ❌ Missing |

Limited control since Framer-hosted.

---

## Performance

| Metric | Value | Rating |
|--------|-------|--------|
| TTFB | 56ms | ⭐⭐⭐⭐⭐ |
| Page Size | 380KB | ⭐⭐⭐⭐ |
| SSL | ✅ | ⭐⭐⭐⭐⭐ |
| HTTP/2 | ✅ | ⭐⭐⭐⭐⭐ |
| Redirect (apex→www) | 308 | ⭐⭐⭐⭐⭐ |

Performance is excellent. Framer handles this well.

---

## Site Structure (Sitemap)

```
signalhaus.ai/
├── / (homepage) — 380KB
├── /pricing — 230KB  
├── /service-catalog — 354KB
└── /page — 138KB (EMPTY — remove from sitemap)
```

Only 4 pages total. Extremely thin for SEO. Missing:
- Blog (essential for organic traffic)
- About/Team page
- Case studies
- Individual service pages

---

## Priority Action Plan

### 🔴 Quick Wins (10 minutes in Framer)
1. Fix "We are understand" → "We understand"
2. Fix "aas" → "as"
3. Remove or hide Product/Resources/Community dropdown menus
4. Fix "Subtitle." placeholder in contact section
5. Delete or unlist `/page` from sitemap
6. Fix founder bio — use Nathan's real background
7. Standardize "SignalHaus" casing

### 🟡 Medium Effort (1-2 hours)
8. Add OG image to all pages (create a branded social card)
9. Rewrite all title tags (see recommendations above)
10. Rewrite homepage meta description
11. Add alt text to all 6 images
12. Add JSON-LD structured data (Organization + ProfessionalService)
13. Reconcile pricing between homepage and service catalog
14. Add canonical URLs

### 🟢 Bigger Lifts (Week+)
15. Add a blog section (critical for SEO — even 1 post/week)
16. Build out About/Team page
17. Create 2-3 case studies with client outcomes
18. Add individual service detail pages
19. Consider migrating to Next.js for better SEO control
20. Set up Google Search Console + Analytics

---

*Report generated from signalhaus.ai audit on Feb 17, 2026*
