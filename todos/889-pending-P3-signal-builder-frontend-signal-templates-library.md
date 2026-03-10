# TODO-889: Build Signal Templates Library

**Repo:** signal-builder-frontend  
**Priority:** P3 (Medium-High, Revenue)  
**Effort:** L (1 week)  
**Status:** pending

## Business Value

Pre-built signal configurations reduce time-to-value for new customers. A templates gallery can be a major selling point in demos and a premium tier differentiator.

## Implementation Plan

### Frontend (independent of backend — use MSW mocks first)

**New Route:** `/templates`

**Template Data Model:**
```ts
interface SignalTemplate {
  id: string;
  name: string;
  description: string;
  category: 'equity' | 'fixed-income' | 'macro' | 'alternatives' | 'esg';
  complexity: 'starter' | 'intermediate' | 'advanced';
  nodeCount: number;
  tags: string[];
  previewImageUrl?: string;
  createdAt: string;
  // Full signal definition for fork
  signalDefinition: SignalDefinition;
}
```

**Template Gallery Page:**
- Grid of TemplateCard components (image + name + description + complexity badge + tags)
- Filter bar: by category, complexity, tags
- Search: full-text search on name + description
- "Use Template" button: fork the template into a new editable signal

**Template Card Component:**
- Canvas preview thumbnail (SVG or screenshot of signal DAG)
- Name, description, complexity pill
- Tag chips (industry, use case)
- "Use Template" CTA button
- Hover state: preview animation

**Fork Flow:**
1. User clicks "Use Template"
2. Modal: "Name your signal" (pre-filled with template name)
3. On confirm: POST /signals with signal definition from template
4. Redirect to `/builder/{newSignalId}`

### MSW Mocks
```ts
// src/modules/templates/api/templates.api.mock.ts
http.get('/api/v1/signal-templates', () => HttpResponse.json([
  { id: 'tmpl-1', name: 'Equity Momentum Signal', ... },
  { id: 'tmpl-2', name: 'ESG Screen', ... },
])),
```

### Navigation
- Add "Templates" link to left sidebar navigation
- Icon: grid/library icon

## Acceptance Criteria
- [ ] `/templates` page loads with template grid
- [ ] Filter by category works
- [ ] Search filters templates in real-time
- [ ] "Use Template" creates new signal and redirects to builder
- [ ] At least 5 mock templates exist for demo
- [ ] Mobile-responsive grid (2-col on mobile, 3+ on desktop)
- [ ] MSW mock works in dev; real API integrated when backend ready
