# 216 — Signal Studio Next.js Integration: Document + Implement Template Loading in UI

**Priority:** high  
**Project:** signal-studio-templates + Signal Studio Next.js  
**Repo:** /data/workspace/projects/signal-studio-templates/ + signal-studio (Next.js)  
**Status:** pending  
**Estimated Effort:** 5h  

---

## Context

The signal-studio-templates library is built but there is **no defined integration path** for loading these templates into the Signal Studio Next.js UI (Railway: signal-studio-production-a258.up.railway.app). Users can't browse, select, or configure the 20 pre-built templates from the frontend. This gap means all that template work is currently inaccessible from the product.

---

## Task Description

### Part 1: Integration Documentation

Create `INTEGRATION.md` in the signal-studio-templates repo explaining:
- How the library exports templates (TypeScript ESM/CJS)
- How Next.js should import the library (npm install / local package link)
- The data flow: template selection → parameter form → execute() → render results
- How to add a new template (developer guide)

### Part 2: Next.js Template Browser Component

In the Signal Studio Next.js repo (`/data/workspace/projects/signal-studio/` or similar):

1. Install the templates library (local npm link or copy dist/):
   ```bash
   npm install ../signal-studio-templates
   ```
   Or add as a workspace dependency.

2. Create `components/templates/TemplateBrowser.tsx`:
   - Fetches templates from Django API (`/api/v1/signal-templates/`)
   - Renders a grid of template cards with name, description, category
   - Filter by category (equity, fixed-income, macro, etc.)
   - Search by name

3. Create `components/templates/TemplateConfigForm.tsx`:
   - Given a selected template, renders a dynamic form from `parameter_schema`
   - Uses `react-hook-form` + `zod` for validation
   - Shows field descriptions, constraints, default values

4. Create `components/templates/TemplateRunner.tsx`:
   - Takes configured params, calls `execute()` via API (`POST /api/v1/signals/run-template/`)
   - Shows loading state, error state, results table
   - Allows saving results as a signal

5. Wire into existing Signal Studio page routing (check existing routes).

---

## Coding Prompt (Autonomous Agent)

```
You are integrating signal-studio-templates into the Signal Studio Next.js frontend.

SIGNAL STUDIO NEXT.JS REPO: find it at /data/workspace/projects/ (look for signal-studio)
TEMPLATES REPO: /data/workspace/projects/signal-studio-templates/

Steps:
1. Find the Signal Studio Next.js project: ls /data/workspace/projects/
2. Read its package.json to understand current deps and structure
3. Create /data/workspace/projects/signal-studio-templates/INTEGRATION.md documenting:
   - Installation: `npm install signal-studio-templates`
   - Usage: import { TemplateEngine, templates } from 'signal-studio-templates'
   - Integration pattern: fetch template list → render form → POST to execute API
   - Adding new templates: step-by-step guide
4. In the Next.js repo:
   a. Create components/templates/TemplateBrowser.tsx
      - Use SWR or React Query to fetch GET /api/v1/signal-templates/
      - Render a responsive grid of template cards
      - Include category filter tabs and search input
   b. Create components/templates/TemplateConfigForm.tsx
      - Accept templateId prop
      - Dynamically render form fields from parameter_schema
      - Validate with zod schema generated from parameter_schema
   c. Create app/templates/page.tsx (or pages/templates.tsx) wiring Browser + Form + Runner
5. Add API route app/api/templates/route.ts that proxies to Django backend
6. Test: ensure the page loads, templates list appears, form renders for one template
7. Report: files created, route path, any blockers found
```

---

## Dependencies

- **211** (dist/ must exist for npm install to work)
- **215** (Django API must serve templates for the browser to fetch)

---

## Acceptance Criteria

- [ ] `INTEGRATION.md` exists in signal-studio-templates repo
- [ ] `TemplateBrowser` component renders list of templates with category filter
- [ ] `TemplateConfigForm` dynamically renders fields from `parameter_schema`
- [ ] Templates page accessible at `/templates` route in Signal Studio
- [ ] API proxy route correctly forwards auth headers to Django backend
- [ ] TypeScript: zero `any` types in new components
- [ ] Responsive layout (mobile + desktop)
