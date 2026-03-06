# TODO-648: Signal Templates Library Feature

**Repo:** signal-builder-frontend  
**Priority:** P2  
**Effort:** Large (1-2 weeks)  
**Category:** New Feature / Revenue

## Description
Pre-built signal templates dramatically reduce time-to-value for new users. Users can browse a template gallery, clone a template, and customize it. Major adoption driver.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-frontend/src/:
1. Create pages/templates/ — template gallery page
2. Create entities/template/ — Template types, API calls
3. Templates list: GET /api/templates → shows cards with preview
4. Template clone: POST /api/templates/{id}/clone → creates new signal
5. Add 'Templates' nav link in LayoutWithNav
6. Template card component: name, category, node count, preview thumbnail
7. Filter by category: momentum, fundamental, ML-based, etc.
8. Add route PATH_TYPES.TEMPLATES = '/templates'
```

## Acceptance Criteria
- [ ] Templates page accessible from nav
- [ ] Template gallery with cards
- [ ] Category filtering works
- [ ] Clone template → opens in builder
- [ ] Unit tests for template API calls

## Dependencies
- Backend: Templates API endpoint must exist
