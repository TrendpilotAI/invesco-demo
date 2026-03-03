# TODO-448: Author Bio Page /team/nathan-stevenson

**Repo:** signalhaus-website  
**Priority:** P2 (SEO — E-E-A-T)  
**Effort:** S (~1.5 hours)  
**Status:** pending

## Description
Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) ranking factor weighs author credibility heavily for business/finance content. Adding a detailed author bio page and linking blog posts to it signals expertise to Google.

## Acceptance Criteria
- [ ] `/team/nathan-stevenson` page with full bio
- [ ] Bio includes: Harvard alumni, WEF Technology Pioneer, ForwardLane founder, enterprise AI background (BNY Pershing, Invesco, LPL Financial)
- [ ] `Person` JSON-LD schema on the page
- [ ] Blog post pages link to `/team/nathan-stevenson` as author
- [ ] `/team/` index page or redirect to Nathan's page
- [ ] Sitemap includes `/team/nathan-stevenson`

## Coding Prompt
```
1. Create src/app/team/nathan-stevenson/page.tsx:
   - Full page bio layout with photo placeholder (next/image)
   - Sections: About, Background, Recognition, Publications, Connect (LinkedIn)
   - Person JSON-LD:
     {
       "@type": "Person",
       "name": "Nathan Stevenson",
       "jobTitle": "Founder & CEO",
       "worksFor": { "@type": "Organization", "name": "SignalHaus" },
       "alumniOf": { "@type": "CollegeOrUniversity", "name": "Harvard University" },
       "award": "World Economic Forum Technology Pioneer",
       "sameAs": ["https://linkedin.com/in/nathanstevenson", "https://twitter.com/nathanstevenson"]
     }
   - Metadata: title "Nathan Stevenson | Founder, SignalHaus AI Consulting"

2. Update src/app/blog/[slug]/page.tsx:
   - Add author byline below post title: "By Nathan Stevenson" linking to /team/nathan-stevenson
   - Update Article JSON-LD to include "author": { "@type": "Person", "name": "Nathan Stevenson", "url": "https://www.signalhaus.ai/team/nathan-stevenson" }

3. Update src/app/sitemap.ts to include /team/nathan-stevenson

4. Create src/app/team/page.tsx as simple redirect or index page pointing to Nathan's bio.
```
