# 238 · P2 · signal-builder-frontend · Signal Templates Library Feature

## Status
pending

## Priority
P2 — New users have no starting point beyond empty canvas; templates reduce time-to-value dramatically

## Description
The Catalog module already exists with a tab-based UI. This task adds a "Templates" tab to the Catalog that surfaces pre-built signal templates. Templates are pre-populated tab graphs stored backend-side and surfaced via a new API endpoint. This enables an enterprise premium-template upsell tier.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

ASSUMPTION: Backend has or will have a GET /api/templates/ endpoint returning TTemplate[]
If not available, use mock data in development.

Step 1: Define template types in `src/redux/builder/types/types.template.ts`
```typescript
export interface TTemplate {
  id: string;
  name: string;
  description: string;
  category: 'ESG' | 'Momentum' | 'Value' | 'Sector' | 'Custom';
  thumbnail_url?: string;
  is_premium: boolean;
  signal_ui: TSignalUIResponse; // the pre-populated tab graph
  created_at: string;
}

export interface TTemplatesResponse {
  count: number;
  results: TTemplate[];
}
```

Step 2: Add templates API endpoint to `src/redux/builder/api.ts`
```typescript
getTemplates: build.query<TTemplatesResponse, void>({
  query: () => '/api/templates/',
  providesTags: ['Templates'],
}),
applyTemplate: build.mutation<TSignal, { template_id: string; signal_name: string }>({
  query: ({ template_id, signal_name }) => ({
    url: '/api/templates/apply/',
    method: 'POST',
    body: { template_id, signal_name },
  }),
  invalidatesTags: ['Signal'],
}),
```

Step 3: Create the Templates tab in the Catalog module
Create `src/modules/catalog/containers/TemplatesTab/`:
- `TemplatesTab.tsx` — grid layout of template cards
- `TemplateCard.tsx` — displays name, category badge, description, "Use Template" CTA
- `TemplateModal.tsx` — preview modal before applying
- `templates.mock.ts` — mock templates for development

TemplateCard structure:
```tsx
<div className="template-card">
  <div className="template-card__header">
    <span className="template-card__category">{template.category}</span>
    {template.is_premium && <span className="template-card__premium">⭐ Premium</span>}
  </div>
  <h3>{template.name}</h3>
  <p>{template.description}</p>
  <button onClick={() => setPreviewTemplate(template)}>Preview & Use</button>
</div>
```

Step 4: Add Templates tab to the Catalog page
In `src/modules/catalog/containers/CatalogTabs/` or wherever tabs are rendered:
```tsx
<Tab key="templates" label="Templates">
  <TemplatesTab />
</Tab>
```

Step 5: Implement "Use Template" flow
When user clicks "Use Template" in the preview modal:
1. Call `applyTemplate` mutation with template_id + a default name
2. On success, navigate to `/builder/{newSignalId}`
3. Show loading state during creation
4. If backend doesn't support apply endpoint yet, create signal from template data client-side

Step 6: Add mock data for development
Create `src/modules/catalog/containers/TemplatesTab/templates.mock.ts` with 5–8 sample templates:
- ESG Filter Signal
- Earnings Momentum
- Sector Rotation
- Revenue Growth Leaders
- Dividend Quality

Commit: "feat: add Signal Templates Library to Catalog module"
```

## Dependencies
- 229 (type fixes) — ensures templates use properly typed API integration
- 230 (Sentry) — error tracking for template apply failures
- Backend must expose `/api/templates/` endpoint (coordinate with backend team)

## Effort Estimate
M (2–3 days frontend; backend scope separate)

## Acceptance Criteria
- [ ] Templates tab visible in Catalog with at least 5 mock templates
- [ ] TemplateCard displays name, category, description, premium badge
- [ ] Preview modal shows template details before applying
- [ ] "Use Template" button creates a new signal and navigates to the builder
- [ ] Loading and error states handled in the apply flow
- [ ] Mock data works when API endpoint is unavailable (graceful fallback)
