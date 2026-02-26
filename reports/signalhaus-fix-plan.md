# SignalHaus.ai — Fix & Upgrade Plan
**Priority order. Copy-paste ready for Framer.**

---

## Phase 1: Quick Wins (10 min in Framer)

### Fix 1: Grammar Typos
**Location:** Homepage → "Experienced and Award Winning Team" section

**Find:** "We are understand sales and GTM"
**Replace with:** "We understand sales and GTM"

**Find:** "as well aas Greyscale"  
**Replace with:** "as well as Greyscale"

### Fix 2: Remove Template Nav Dropdowns
In Framer, delete or hide these dropdown menus from the header:
- Product (Design, Content, Publish)
- Resources (Blog, Careers, Docs, About)
- Community (Join, Events, Experts)
- Changelog

**Keep only:** Home, Expertise/Services, Pricing, Contact

### Fix 3: Fix Contact Section Placeholder
**Find:** "Subtitle." (appears twice in contact form area)
**Replace with:** "Let's discuss how AI can accelerate your business."

### Fix 4: Delete /page
In Framer, delete the "/page" route entirely, or redirect it to homepage. It's an empty page being indexed by Google.

### Fix 5: Fix Founder Bio
**Current (generic template):**
> "I love turning complex problems into simple, beautiful, and user-friendly experiences. With a strong focus on UX/UI, I design products that not only look great but also feel effortless to use."

**Replace with:**
> "I've spent 15+ years building AI and data products for the world's leading financial institutions. As founder and former CEO of ForwardLane, I led enterprise AI implementations for BNY Pershing, Invesco, LPL Financial, Columbia Threadneedle, and dozens more. A Harvard alum, Techstars graduate, and World Economic Forum Technology Pioneer — I started SignalHaus to help companies cut through the AI noise and ship solutions that actually drive revenue."

### Fix 6: Standardize Brand Name
Search all pages for "Signalhaus" (lowercase h) and replace with "SignalHaus"

### Fix 7: Fix "Experienced and Awarded Team" Header
**Current:** Appears as both "Experienced and Award Winning Team" AND "Experienced and Awarded Team" (inconsistent)
**Replace both with:** "Experienced & Award-Winning Team"

---

## Phase 2: SEO Fixes (1-2 hours in Framer)

### Fix 8: Title Tags
Set in Framer page settings for each page:

**Homepage:**
```
SignalHaus — AI Strategy, Data Integration & Automation Consultancy
```

**Pricing:**
```
Pricing Plans | SignalHaus AI Consultancy
```

**Service Catalog:**
```
AI & Automation Service Catalog | SignalHaus
```

### Fix 9: Meta Descriptions
Set in Framer page settings:

**Homepage:**
```
SignalHaus helps enterprises accelerate growth with custom AI strategy, data integrations, and intelligent automation. From rapid prototypes to enterprise-scale AI orchestration. Founded by Nathan Stevenson.
```

**Pricing:**
```
Simple, scalable AI consulting plans from $1,250. QuickStart automations, Growth Engine suites, and enterprise AI orchestration. See what fits your business.
```

**Service Catalog:**
```
Explore SignalHaus AI consulting services: Discovery Sprints, Integration Packs, Agent Deployment, Data Intelligence, and Fractional AI CTO. Tiered pricing from Starter to Enterprise.
```

### Fix 10: OG Image
Create a branded social card (1200×630px) with:
- SignalHaus logo
- Tagline: "Pragmatic AI. Real Impact."
- Dark background matching site palette
- Upload to Framer and set as og:image on all pages

### Fix 11: Alt Text for Images
In Framer, add alt text to every image on the homepage:
- Logo → "SignalHaus logo"
- AI Hot 100 badge → "AI Hot 100 award badge"
- Harvard Alumni badge → "Harvard Alumni badge"
- World Economic Forum badge → "World Economic Forum Technology Pioneer badge"
- AWS badge → "AWS partner badge"
- AudienceLab badge → "AudienceLab partner badge"
- Founder photo → "Nathan Stevenson, founder of SignalHaus"

### Fix 12: Schema Markup (JSON-LD)
Add this to the homepage `<head>` via Framer's custom code injection:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "SignalHaus",
  "alternateName": "SignalHaus AI",
  "url": "https://www.signalhaus.ai",
  "logo": "https://www.signalhaus.ai/logo.png",
  "description": "AI strategy, data integration, and workflow automation consultancy for enterprises",
  "founder": {
    "@type": "Person",
    "name": "Nathan Stevenson",
    "jobTitle": "Founder & CEO",
    "alumniOf": {
      "@type": "Organization",
      "name": "Harvard University"
    }
  },
  "parentOrganization": {
    "@type": "Organization",
    "name": "ForwardLane Inc",
    "url": "https://forwardlane.com"
  },
  "areaServed": {
    "@type": "Country",
    "name": "United States"
  },
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Fort Lauderdale",
    "addressRegion": "FL",
    "addressCountry": "US"
  },
  "priceRange": "$1,250 - $100,000+",
  "serviceType": ["AI Strategy", "Data Integration", "Workflow Automation", "AI Consulting"],
  "knowsAbout": ["Artificial Intelligence", "Data Integration", "Enterprise Automation", "Financial Technology"],
  "award": ["AI Hot 100", "WealthTech 100", "AI Fintech 100", "KPMG Top 50 Fintechs", "World Economic Forum Technology Pioneer"]
}
</script>
```

Add this to the **Pricing** page:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "SignalHaus Pricing Plans",
  "itemListElement": [
    {
      "@type": "Offer",
      "name": "QuickStart Automation",
      "price": "1250",
      "priceCurrency": "USD",
      "description": "Up to 3 custom automations, 1 voice or chat agent, intent data from AudienceLab"
    },
    {
      "@type": "Offer",
      "name": "Growth Engine Suite",
      "price": "4800",
      "priceCurrency": "USD",
      "priceSpecification": {
        "@type": "UnitPriceSpecification",
        "billingIncrement": 1,
        "billingDuration": "P1M"
      },
      "description": "10 automations + 5 AI agents, CRM + data integration, monthly optimization"
    },
    {
      "@type": "Offer",
      "name": "Intelligent Enterprise OS",
      "price": "25000",
      "priceCurrency": "USD",
      "description": "Multi-agent orchestration, predictive analytics, SOC2-ready automation"
    }
  ]
}
</script>
```

### Fix 13: Reconcile Pricing
Add a clarifying note on the **Service Catalog** page:
```
Note: Service Catalog pricing reflects project-based engagements. 
For monthly subscription plans, see our Pricing page.
```

### Fix 14: Canonical URLs
In Framer settings, ensure canonical URLs are set:
- Homepage: `https://www.signalhaus.ai/`
- Pricing: `https://www.signalhaus.ai/pricing`
- Service Catalog: `https://www.signalhaus.ai/service-catalog`

---

## Phase 3: Upgrade Plan (Week+)

### 1. Add Blog Section
- Use Framer CMS or integrate a headless CMS
- Start with 4 cornerstone posts:
  - "How We Built an AI Agent That Replaced 3 Manual Workflows"
  - "Enterprise AI Integration: Lessons from BNY Pershing, Invesco, and LPL"
  - "The $1,250 AI QuickStart: What You Get and Why It Works"
  - "Agentic Automation: Why Voice Workflows Are the Future of GTM"
- Publish 1 post/week minimum
- Use NarrativeReactor to generate drafts!

### 2. Case Studies Page
Create 2-3 case studies (anonymized if needed):
- Financial services AI implementation
- Sales automation ROI story
- Data integration for regulated industry

### 3. About / Team Page
- Nathan's full bio with photo
- Company story (ForwardLane → SignalHaus evolution)
- Values/approach section
- Logos of enterprise clients (with permission)

### 4. Individual Service Pages
Break out the service catalog into standalone pages:
- `/services/ai-strategy`
- `/services/data-integration`
- `/services/automation`
- `/services/rapid-prototyping`
- `/services/fractional-cto`

Each with: description, process, deliverables, pricing, CTA

### 5. Google Search Console + Analytics
- Verify site in Google Search Console
- Submit sitemap
- Set up Google Analytics 4 (or Plausible for privacy)
- Monitor Core Web Vitals

### 6. Consider Next.js Migration (Longer Term)
Benefits over Framer:
- Full SEO control (SSR, dynamic meta, programmatic pages)
- Blog with MDX
- API routes for contact form
- NarrativeReactor integration for content
- Custom analytics
- Deploy on Vercel or Railway

---

## Phase 4: Growth Engine

### Content Pipeline (Use NarrativeReactor)
- Auto-generate weekly blog posts from trending AI topics
- Cross-publish to LinkedIn, Twitter via Postiz
- Track engagement, optimize topics

### Lead Capture
- Add lead magnet: "Free AI Readiness Assessment" or "Enterprise AI Playbook PDF"
- Email capture → drip campaign
- Calendly integration for "Book a Meeting" CTAs

### SEO Growth Targets
| Timeframe | Target |
|-----------|--------|
| Month 1 | Fix all technical SEO issues, add schema, 4 blog posts |
| Month 3 | 12 blog posts, 2 case studies, ranking for "AI consulting" long-tails |
| Month 6 | 30+ posts, backlinks from guest posts, featured in directories |
| Month 12 | Page 1 for "AI automation consultancy", 1000+ organic visits/mo |

---

*Plan created Feb 17, 2026 — Honey 🍯*
