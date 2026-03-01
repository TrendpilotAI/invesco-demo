# TODO 358 — Signal Studio Frontend: Template Marketplace with Preview

**Status:** pending  
**Priority:** medium  
**Project:** signal-studio-frontend  
**Estimated Effort:** 1–2 days  

---

## Description

The templates page exists but likely shows a static list. This task builds a proper template marketplace with search/filter, a preview modal showing the signal graph/config, and a one-click "Use Template" action that creates a new signal from the template.

---

## Coding Prompt (Autonomous Agent)

```
Repo: /data/workspace/projects/signal-studio-frontend

Task: Build a functional template marketplace page with search, preview modal, and
      "Use Template" action.

Step 1 — API Hook
  Create/update `src/hooks/useTemplates.ts`:
  - `useTemplates(query?: string, category?: string)` — GET /api/templates with optional
    search and category filter params
  - `useTemplate(id: string)` — GET /api/templates/:id for full detail
  - `useCreateSignalFromTemplate()` — POST /api/signals { template_id } mutation

Step 2 — Template Card Component
  Create `src/components/templates/TemplateCard.tsx`:
  - Props: template object (id, name, description, category, preview_data)
  - Shows: name, description badge (category), "Preview" and "Use Template" buttons
  - Clicking "Preview" opens the TemplatePreviewModal
  - Clicking "Use Template" calls the mutation and toasts success, then navigates to
    the new signal's edit page

Step 3 — Preview Modal
  Create `src/components/templates/TemplatePreviewModal.tsx`:
  - Uses a Dialog (shadcn/ui or custom) to show template detail
  - Displays: name, description, category, a JSON pretty-print of preview_data
    (or a simplified node list if preview_data contains nodes)
  - Footer: "Close" and "Use This Template" CTA

Step 4 — Search & Filter Bar
  At the top of the templates page add:
  - Text search input (debounced 300ms, updates query param)
  - Category filter (select/tabs from distinct categories in template list)
  - Result count display

Step 5 — Templates Page Assembly
  Wire `src/app/templates/page.tsx` to use all of the above:
  - Show skeleton loaders while fetching
  - Show empty state if no templates match
  - Responsive grid layout (2 cols mobile, 3 cols desktop)

Step 6 — Verify
  `pnpm tsc --noEmit` + `pnpm build` pass.
```

---

## Dependencies

- TODO 356 (toast system) — needed for "Use Template" success/error feedback
- TODO 354 (dashboard real data) — establishes API hook patterns to follow

---

## Acceptance Criteria

- [ ] Templates page shows real data from API
- [ ] Search input filters templates (debounced)
- [ ] Category filter works
- [ ] Preview modal shows template detail
- [ ] "Use Template" creates a signal and navigates to it
- [ ] Skeleton loaders shown while fetching
- [ ] Empty state when no results
- [ ] `pnpm tsc --noEmit` passes, `pnpm build` succeeds
