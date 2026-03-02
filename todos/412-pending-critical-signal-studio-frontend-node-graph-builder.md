# TODO-412: Visual Node Graph Builder — Signal Studio Frontend

**Priority:** Critical  
**Repo:** signal-studio-frontend  
**Status:** pending  
**Effort:** L (1 week)

## Description

The signal creation page (`/signals/new`) has a placeholder drag canvas div but no actual node graph builder. This is the core UX differentiator for Signal Studio — a visual drag-and-drop builder for composing signal pipelines from typed nodes.

The type system is already defined in `src/lib/api/types.ts`:
- `SignalNode`: `id, type (data_source|filter|transform|ai|output), label, config, position`
- `SignalConnection`: `id, from_node, to_node, from_port, to_port`

## Implementation Plan

1. Install React Flow: `npm install @xyflow/react`
2. Create `src/components/signal-builder/` with:
   - `SignalCanvas.tsx` — main React Flow canvas
   - `nodes/DataSourceNode.tsx` — styled node for data sources
   - `nodes/FilterNode.tsx` — filter/transform node
   - `nodes/AiNode.tsx` — AI processing node
   - `nodes/OutputNode.tsx` — webhook/export output node
   - `NodePalette.tsx` — left panel to drag new nodes from
   - `NodeConfigPanel.tsx` — right panel for selected node config
3. Wire save to `useCreateSignal` mutation
4. Wire load to `useSignal` for editing existing signals

## Autonomous Coding Prompt

```
You are working on /data/workspace/projects/signal-studio-frontend/.

TASK: Build a visual node graph builder using React Flow for the signal creation page.

1. Install: npm install @xyflow/react

2. Create src/components/signal-builder/SignalCanvas.tsx:
   - Use ReactFlow from @xyflow/react
   - Support node types: data_source, filter, transform, ai, output
   - Each node maps to SignalNode type from @/lib/api/types
   - Connections map to SignalConnection type
   - Expose onSave callback with { nodes: SignalNode[], connections: SignalConnection[] }

3. Create styled node components for each type with:
   - Color-coded by type (blue=data_source, yellow=filter, purple=ai, green=output)
   - Input/output ports
   - Label and config summary display

4. Create NodePalette.tsx sidebar with draggable node type buttons

5. Replace the placeholder div in src/app/(app)/signals/new/page.tsx with <SignalCanvas>

6. On save, call useCreateSignal with nodes and connections from canvas state

Style: Tailwind classes, dark background canvas (#0f1117), node cards with border-2
```

## Acceptance Criteria

- [ ] Users can drag nodes from palette onto canvas
- [ ] Users can connect nodes by dragging between ports
- [ ] Node types visually distinct with icons
- [ ] Clicking a node opens config panel
- [ ] Save button calls API with correctly shaped payload
- [ ] Works on mobile (touch drag)

## Dependencies

- TODO-411 (API wiring) should be done first so save actually persists
