# TODO 104 — Integrate Template Gallery into Signal Studio Frontend (P2)

**Repo:** signal-studio (Next.js) uses signal-studio-templates  
**Priority:** P2  
**Effort:** L (3-5 days)  
**Status:** pending

---

## Autonomous Coding Prompt

```
Integrate @forwardlane/signal-studio-templates into the signal-studio Next.js frontend
at /data/workspace/projects/signal-studio/

STEPS:

1. In signal-studio, add local package reference:
   package.json: "@forwardlane/signal-studio-templates": "file:../signal-studio-templates"
   Run: pnpm install

2. Create page: app/signals/templates/page.tsx
   Import TemplateGallery from "@forwardlane/signal-studio-templates/components/template-gallery"
   
   Wire handlers:
   - onUseTemplate: navigate to /signals/builder?templateId={id}
   - onCustomizeTemplate: open customize modal, POST to /api/templates/{id}/customize
   - availableDataSources: fetch from /api/data-sources (Django backend)

3. Create API route: app/api/templates/[id]/execute/route.ts
   - Proxy POST to Django backend: http://Django-Backend.railway.internal:8000/api/signals/execute/
   - Pass templateId, parameters, includeTalkingPoints
   - Handle auth: forward JWT from request headers

4. Create API route: app/api/data-sources/route.ts
   - Proxy GET to Django: /api/data-sources/available/
   - Returns list of DataSource strings available for current user/org

5. In signal builder (signals/builder), add "Load Template" button:
   - Opens template gallery in a modal
   - On template select: pre-populate builder fields from template SQL + parameters
   - Show template complexity badge and estimated run time

6. Add loading skeleton for TemplateGallery while data sources load.

7. Add error boundary around TemplateGallery.

TESTING:
- Test page renders without errors
- Test that selecting a template navigates correctly
- Test API proxy routes handle Django errors gracefully
```

## Acceptance Criteria
- [ ] /signals/templates page renders TemplateGallery
- [ ] Data sources fetched from Django backend
- [ ] Execute flows through to Django Analytical DB
- [ ] Signal builder can load a template pre-populated
- [ ] Error states handled (missing data sources, failed execution)

## Dependencies
- TODO 100 (SQL bug fix)
- TODO 101 (auth — JWT must be forwarded to Django)
- signal-studio Next.js project must be accessible
