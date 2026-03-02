# TODO-325: LinkedIn Insight Tag

**Priority:** P1  
**Effort:** 15 min  
**Repo:** signalhaus-website  
**Status:** pending  

## Description
Add LinkedIn Insight Tag to `layout.tsx`. Essential for B2B retargeting — enterprise buyers are on LinkedIn. Zero cost to add; unlocks LinkedIn retargeting campaigns when Nathan is ready to run ads.

## Setup Steps
1. Nathan: Go to LinkedIn Campaign Manager → Account Assets → Insight Tag → Copy Partner ID
2. Add to `.env.example`: `NEXT_PUBLIC_LINKEDIN_PARTNER_ID=your_partner_id`

## Coding Prompt (Agent-Executable)

```
In /data/workspace/projects/signalhaus-website/:

1. Create src/components/LinkedInInsightTag.tsx:
   'use client'
   import Script from 'next/script'
   export function LinkedInInsightTag({ partnerId }: { partnerId: string }) {
     if (!partnerId) return null
     return (
       <>
         <Script id="linkedin-insight" strategy="afterInteractive">
           {`_linkedin_partner_id = "${partnerId}"; window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || []; window._linkedin_data_partner_ids.push(_linkedin_partner_id);`}
         </Script>
         <Script src="https://snap.licdn.com/li.lms-analytics/insight.min.js" strategy="afterInteractive" />
         <noscript>
           <img height="1" width="1" style={{display:'none'}} alt="" src={`https://px.ads.linkedin.com/collect/?pid=${partnerId}&fmt=gif`} />
         </noscript>
       </>
     )
   }

2. In src/app/layout.tsx, import and add:
   <LinkedInInsightTag partnerId={process.env.NEXT_PUBLIC_LINKEDIN_PARTNER_ID || ''} />

3. Add NEXT_PUBLIC_LINKEDIN_PARTNER_ID to .env.example
```

## Acceptance Criteria
- [ ] Component exists and renders conditionally
- [ ] Fires on production (verify in LinkedIn Campaign Manager)
- [ ] No console errors

## Dependencies
None (requires Nathan to set up LinkedIn Campaign Manager)
