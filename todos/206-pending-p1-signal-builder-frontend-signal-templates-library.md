---
status: pending
priority: p1
issue_id: "206"
tags: [feature, templates, catalog, signal-builder-frontend]
dependencies: ["203", "207"]
---

# 206 — Signal Templates Library

## Problem Statement

New users of the Signal Builder face an empty canvas with no starting points. The onboarding tour (react-joyride) walks through the UI but doesn't help users build their first meaningful signal. A curated library of pre-built signal templates ("ESG Filter", "Earnings Momentum", "Sector Rotation") would dramatically reduce time-to-value and drive user activation.

## Findings

- `src/pages/catalog/` and `src/modules/catalog/` exist — a "Templates" tab can be added here
- `TTab` type has `data: { nodes: Node<TNodeData>[], edges: Edge[] }` — templates are just pre-populated tabs
- `createSignal` mutation creates a new signal — templates would call this + populate with template data
- The Catalog already renders a table of signals — template browsing can reuse this UI
- Backend would need a `/api/v1/templates/` endpoint returning pre-defined signal configurations

## Proposed Solutions

### Option A: Frontend-only templates (JSON file) — Quick Win
Store template definitions as JSON in the frontend codebase. No backend changes needed for MVP.
- **Pros:** Fast to ship, no backend dependency
- **Cons:** Non-customizable per client, no admin management
- **Effort:** M (~6-8h)
- **Risk:** Low

### Option B: Backend-driven templates
Backend returns template catalog via API. Admins can manage templates.
- **Pros:** Flexible, client-customizable
- **Cons:** Requires backend work (separate TODO for backend repo)
- **Effort:** L frontend + L backend
- **Risk:** Medium

## Recommended Action

Phase 1: Option A (frontend JSON templates) to ship quickly. Phase 2: migrate to backend API.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

Task: Build the Signal Templates Library feature (Phase 1: frontend-only)

1. Create template definitions file src/modules/catalog/data/signal-templates.ts:
   Define 5 templates with pre-populated node/edge graphs:
   - ESG Filter: filters by ESG score > threshold
   - Earnings Momentum: filters by earnings growth > industry median
   - Sector Rotation: identifies sector overweight vs benchmark
   - Revenue Defense: flags clients with declining revenue
   - Cross-Sell ETF: identifies clients underexposed to ETF products
   
   Each template has shape:
   {
     id: string;
     name: string;
     description: string;
     category: 'risk' | 'opportunity' | 'compliance';
     thumbnail?: string;
     tab: Omit<TTab, 'id'>; // pre-populated nodes and edges
   }

2. Create src/modules/catalog/components/TemplatesTab/TemplatesTab.tsx:
   - Grid layout showing template cards (name, description, category badge)
   - "Use Template" button on each card
   - On click: calls createSignal mutation, then populates with template data
   - Loading state during creation

3. Create src/modules/catalog/components/TemplatesTab/TemplateCard.tsx:
   - Card component with category color coding
   - Template name, description
   - "Use Template" CTA button

4. Add "Templates" tab to the Catalog page:
   - Find src/pages/catalog/index.tsx (or equivalent)
   - Add tab selector: "All Signals" | "Templates"
   - Conditionally render TemplatesTab when "Templates" selected

5. On "Use Template" action:
   a. Call createSignal mutation with a generated name (e.g., "New ESG Filter Signal")
   b. After signal is created, dispatch Redux action to populate the new tab with template nodes
   c. Navigate to /builder/{newSignalId}

6. Add route: no new routes needed — templates use existing /builder/:id route

7. Write Storybook story: src/modules/catalog/components/TemplatesTab/TemplatesTab.stories.tsx

8. Run: yarn typecheck && yarn build
   Ensure no TypeScript errors.
```

## Dependencies

- 203 (eliminate any types) — ensures proper typing for template tab data
- 207 (signal version history) — templates should initialize at version 1

## Estimated Effort

**Medium** — 6-8 hours

## Acceptance Criteria

- [ ] At least 5 signal templates are defined in `src/modules/catalog/data/signal-templates.ts`
- [ ] Templates Tab is accessible from the Catalog page
- [ ] Clicking "Use Template" creates a new signal and populates it with template nodes/edges
- [ ] User is navigated to `/builder/{signalId}` after template creation
- [ ] Template cards display: name, description, category badge
- [ ] Loading state shown during signal creation
- [ ] TypeScript types are explicit (no `any`)
- [ ] Storybook story exists for TemplatesTab
- [ ] `yarn typecheck` passes

## Work Log

### 2026-02-26 — Todo created

**By:** Planning Agent

**Actions:**
- Confirmed TTab type supports pre-populated nodes/edges
- Confirmed Catalog page exists and can host a Templates tab
- Identified createSignal mutation as the entry point for template instantiation
