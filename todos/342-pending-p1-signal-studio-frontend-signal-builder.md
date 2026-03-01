# TODO-342: Visual Signal Builder Page

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** L (2-3 days)  
**Dependencies:** TODO-337, TODO-338

## Description
The core product feature — a visual node-based canvas for building signals. Types for SignalNode and SignalConnection already exist in types.ts. Need to build the builder UI at /signals/new and /signals/[id]/edit.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. Install: npm install reactflow (or @xyflow/react)

2. Create src/components/signal-builder/ directory:
   - SignalCanvas.tsx — main React Flow canvas
   - NodePalette.tsx — left sidebar with draggable node types
   - NodeTypes/DataSourceNode.tsx
   - NodeTypes/FilterNode.tsx
   - NodeTypes/TransformNode.tsx
   - NodeTypes/AINode.tsx
   - NodeTypes/OutputNode.tsx
   - NodeConfigPanel.tsx — right panel for selected node config

3. Create src/app/(app)/signals/new/page.tsx:
   - Title bar with signal name input
   - SignalCanvas in center
   - NodePalette on left
   - NodeConfigPanel on right (slides in when node selected)
   - Save draft + Run buttons in header

4. Map SignalNode types to React Flow node types
5. Map SignalConnection[] to React Flow edges
6. On save: call useCreateSignal with nodes/connections

7. Create src/app/(app)/signals/[id]/edit/page.tsx:
   - Load existing signal with useSignal(id)
   - Pre-populate canvas with existing nodes/connections
   - Save updates useUpdateSignal
```

## Acceptance Criteria
- [ ] Can drag nodes onto canvas
- [ ] Can connect nodes with edges
- [ ] Can configure each node type
- [ ] Can save signal (draft or active)
- [ ] Can run signal from builder
- [ ] Mobile-responsive (at least usable on tablet)
