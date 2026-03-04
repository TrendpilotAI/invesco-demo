# TODO-491: AI-Assisted Filter Suggestions

**Project:** signal-builder-frontend
**Priority:** P2 (HIGH revenue impact, L effort — after core quality)
**Estimated Effort:** 12-16 hours
**Dependencies:** TODO-474 (DRY FilterContent), TODO-476 (E2E tests), TODO-487 (API coverage audit)

## Description

LLM-powered prompt → auto-populate signal filter nodes. "Find growth stocks with momentum > 20%" translates to a filter graph. Connect to signal-builder-backend AI endpoint. Show confidence scores on suggested nodes.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Build AI-assisted filter suggestion feature.

STEPS:
1. Create src/modules/builder/containers/AISuggestions/ component:
   - Text input with placeholder "Describe your signal in plain English..."
   - Submit button
   - Loading state with streaming indicator
   - Results panel showing suggested nodes with confidence scores

2. Create RTK Query endpoint:
   - POST /api/v1/signals/suggest (or whatever backend AI endpoint exists)
   - Request: { prompt: string }
   - Response: { nodes: Array<{ type, config, confidence }>, edges: Array<{ source, target }> }

3. On suggestion acceptance:
   - Map suggested nodes to ReactFlow node format
   - Add to canvas with auto-layout (dagre or elkjs)
   - Connect edges per suggestion
   - Highlight new nodes briefly (pulse animation)

4. Confidence display:
   - Green badge (>80% confidence)
   - Yellow badge (50-80%)
   - Red badge (<50%) with tooltip explaining uncertainty

5. Add to builder UI:
   - Floating action button or sidebar panel
   - Keyboard shortcut: Ctrl+K or Cmd+K to open
   - Dismissable with Esc

6. Add E2E test: type prompt → verify nodes appear on canvas

CONSTRAINTS:
- Graceful fallback if backend AI endpoint is unavailable
- Rate limit: max 1 request per 5 seconds (debounce)
- Max 20 suggested nodes per request
- Must work with existing node types (Filter, Dataset, GroupFunction, Target)
```

## Acceptance Criteria
- [ ] AI prompt input accessible from builder
- [ ] Suggestions rendered as nodes on canvas
- [ ] Confidence scores displayed per node
- [ ] Loading and error states handled
- [ ] E2E test covers happy path
- [ ] Works with existing node type system
