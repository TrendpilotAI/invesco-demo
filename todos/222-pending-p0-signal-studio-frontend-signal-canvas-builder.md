# TODO-222: Signal Canvas Builder (Visual Editor)

**Repo:** signal-studio-frontend  
**Priority:** P0 (Core product feature — the main differentiator)  
**Effort:** XL (2-3 weeks)  
**Status:** pending

## Problem
The Signal data model defines `nodes: SignalNode[]` and `connections: SignalConnection[]` but there is NO visual canvas/builder in the UI. Users cannot create or edit signal pipelines visually. This is the most critical missing feature.

## Acceptance Criteria
- User can add nodes from a sidebar palette (data_source, filter, transform, output, ai)
- Nodes can be dragged on a canvas and connected port-to-port
- Clicking a node opens a config panel (right sidebar)
- Signal canvas state is persisted to the backend on save
- Canvas loads existing node/connection data when editing a signal
- Works in /signals/new and /signals/[id] pages

## Coding Prompt

```
Install: npm install reactflow @reactflow/background @reactflow/controls @reactflow/minimap

Create /src/components/signal-canvas/ directory with:

1. SignalCanvas.tsx — main canvas component
   - Use ReactFlow with nodes from Signal.nodes, edges from Signal.connections
   - Map SignalNode.type to custom node components
   - Map SignalConnection to ReactFlow Edge format
   - onNodesChange, onEdgesChange, onConnect handlers
   - Export save() function that returns {nodes, connections} in API format

2. nodes/ directory — custom node components for each type:
   - DataSourceNode.tsx (blue, database icon)
   - FilterNode.tsx (yellow, filter icon)
   - TransformNode.tsx (green, transform icon)
   - OutputNode.tsx (purple, output icon)
   - AiNode.tsx (orange, sparkles icon)
   Each node: shows label, has input/output handles, selected state styling

3. NodePalette.tsx — sidebar with draggable node types
   - Drag from palette → drop on canvas creates a new node

4. NodeConfigPanel.tsx — right panel when node is selected
   - Shows node.config fields as form inputs
   - Saves on blur/change

5. Update /src/app/(app)/signals/new/page.tsx and /src/app/(app)/signals/[id]/page.tsx
   to include the SignalCanvas

IMPORTANT: Dynamic import ReactFlow with { ssr: false } to avoid SSR issues.
Use next/dynamic for SignalCanvas wrapper.
```

## Dependencies
- TODO-221 (auth token) — needs working auth to save signal data
