# TODO-324: Microsoft Clarity Heatmaps

**Priority:** P1  
**Effort:** 15 min  
**Repo:** signalhaus-website  
**Status:** pending  

## Description
Add Microsoft Clarity for free session recording and heatmaps. Zero performance cost (async script). Reveals scroll depth, click maps, rage clicks, and session recordings. More actionable than GA4 alone for CRO.

## Setup Steps
1. Nathan: Go to https://clarity.microsoft.com → Create project → Copy Project ID
2. Add to `.env.example`: `NEXT_PUBLIC_CLARITY_ID=your_clarity_id`

## Coding Prompt (Agent-Executable)

```
In /data/workspace/projects/signalhaus-website/:

1. Create src/components/MicrosoftClarity.tsx:
   'use client'
   import Script from 'next/script'
   export function MicrosoftClarity({ clarityId }: { clarityId: string }) {
     if (!clarityId) return null
     return (
       <Script id="ms-clarity" strategy="afterInteractive">
         {`(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","${clarityId}");`}
       </Script>
     )
   }

2. In src/app/layout.tsx, import and add:
   <MicrosoftClarity clarityId={process.env.NEXT_PUBLIC_CLARITY_ID || ''} />

3. Add NEXT_PUBLIC_CLARITY_ID to .env.example
```

## Acceptance Criteria
- [ ] Component exists and renders without errors
- [ ] Script fires on production (verify in Clarity dashboard)
- [ ] Doesn't block page load (strategy="afterInteractive")

## Dependencies
None (requires Nathan to create Clarity account)
