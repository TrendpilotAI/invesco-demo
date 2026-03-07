# TODO-833: Salesforce-Embeddable Signal Widgets

**Repo**: signal-studio-frontend  
**Priority**: P0  
**Effort**: L (5-7 days)  
**Status**: pending  
**Business Case**: Craig Lieb (Invesco) explicitly requested. $300K+ retention.

## Description
Build iframe-safe signal widgets embeddable in Salesforce CRM. Invesco advisors need "easy buttons" to see signal data without leaving Salesforce.

## Coding Prompt
```
1. Create /app/embed/signal-widget/[id]/page.tsx:
   - Lightweight component, no heavy imports
   - Show: signal name, current value, trend arrow, last updated
   - Pure CSS (no Tailwind class purge issues in iframes)
   - Add <meta charset> and viewport for Salesforce canvas

2. Create /app/api/embed/signals/[id]/route.ts (public endpoint):
   - No auth required (add rate limiting instead)
   - Returns: { id, name, value, trend, lastUpdated, description }
   - Cache with Cache-Control: max-age=60

3. Add CORS + frame headers in next.config.mjs:
   {
     source: '/embed/:path*',
     headers: [
       { key: 'Access-Control-Allow-Origin', value: '*' },
       { key: 'Content-Security-Policy', value: "frame-ancestors *.salesforce.com *.force.com 'self'" }
     ]
   }

4. Rate limiting middleware for /embed/* routes (100 req/min per IP)

5. Create docs/salesforce-integration.md with:
   - How to create a Salesforce Lightning Web Component wrapper
   - How to use the iframe embed URL
   - Example Visualforce page

6. E2E test: verify widget loads in iframe without errors
```

## Acceptance Criteria
- Widget URL: `/embed/signal-widget/[id]` renders without errors in an iframe
- API returns JSON without authentication
- CORS headers allow Salesforce domains
- Docs guide Invesco team on embedding
- Rate limiting active
