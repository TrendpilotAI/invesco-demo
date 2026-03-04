# TODO-492: Signal Templates Library UI

**Project:** signal-builder-frontend
**Priority:** P2 (HIGH revenue impact, M effort)
**Estimated Effort:** 8-10 hours
**Dependencies:** TODO-476 (E2E tests), INFRA-005 (templates package)

## Description

Pre-built signal templates: momentum, value, quality, ESG, dividend. Template picker with preview, one-click instantiation into builder canvas. Wire to signal-studio-templates package.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Build signal templates library UI in the Catalog module.

STEPS:
1. Create src/modules/catalog/containers/TemplateLibrary/:
   - TemplateList.tsx — grid/list view of available templates
   - TemplateCard.tsx — card showing template name, description, category, node count
   - TemplatePreview.tsx — modal showing template graph preview (read-only ReactFlow canvas)
   - TemplateFilters.tsx — filter by category (momentum, value, quality, ESG, dividend)

2. Create RTK Query endpoint for templates:
   - GET /api/v1/templates — list all templates
   - GET /api/v1/templates/:id — template detail with node/edge config

3. One-click instantiation:
   - "Use Template" button on card/preview
   - Loads template nodes + edges into builder canvas
   - Navigates to builder page with pre-populated graph
   - User can modify before publishing

4. Template preview:
   - Read-only ReactFlow canvas in modal
   - Shows node types, connections, and filter configurations
   - "Use This Template" CTA button

5. Add route: /templates in router
6. Add navigation link in sidebar/nav

7. Add E2E test: browse templates → preview → instantiate → verify in builder

CONSTRAINTS:
- Templates are read-only until instantiated
- Instantiation creates a copy (doesn't modify template)
- Category filter persists in URL params
- Responsive grid layout (1 col mobile, 2 tablet, 3 desktop)
```

## Acceptance Criteria
- [ ] /templates route shows template grid
- [ ] Category filter works
- [ ] Template preview modal shows read-only graph
- [ ] "Use Template" loads nodes into builder
- [ ] E2E test covers browse → instantiate flow
- [ ] Mobile responsive
