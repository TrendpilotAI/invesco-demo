# TODO-883: Implement Undo/Redo for Builder Canvas

**Repo:** signal-builder-frontend  
**Priority:** P1 (High UX)  
**Effort:** M (2-3 days)  
**Status:** pending

## Problem

Users can accidentally delete nodes or edges on the ReactFlow canvas with no way to recover. This is a critical UX gap for enterprise clients building complex signal pipelines with many nodes.

## Implementation Plan

### Redux Builder Slice Changes

Add history state to `builderSlice`:
```ts
interface BuilderState {
  // existing...
  nodes: Node[];
  edges: Edge[];
  
  // NEW: history
  past: Array<{ nodes: Node[]; edges: Edge[] }>;
  future: Array<{ nodes: Node[]; edges: Edge[] }>;
  maxHistory: 50;
}

// New reducers:
saveSnapshot: (state) => {
  state.past.push({ nodes: state.nodes, edges: state.edges });
  if (state.past.length > state.maxHistory) state.past.shift();
  state.future = [];  // clear redo stack on new action
},
undo: (state) => {
  if (state.past.length === 0) return;
  state.future.unshift({ nodes: state.nodes, edges: state.edges });
  const prev = state.past.pop()!;
  state.nodes = prev.nodes;
  state.edges = prev.edges;
},
redo: (state) => {
  if (state.future.length === 0) return;
  state.past.push({ nodes: state.nodes, edges: state.edges });
  const next = state.future.shift()!;
  state.nodes = next.nodes;
  state.edges = next.edges;
},
```

### Hook: useBuilderHistory
```ts
// src/modules/builder/hooks/useBuilderHistory.ts
export const useBuilderHistory = () => {
  const dispatch = useDispatch();
  const canUndo = useSelector(selectCanUndo);
  const canRedo = useSelector(selectCanRedo);
  
  const undo = useCallback(() => dispatch(builderSlice.actions.undo()), [dispatch]);
  const redo = useCallback(() => dispatch(builderSlice.actions.redo()), [dispatch]);
  const saveSnapshot = useCallback(() => dispatch(builderSlice.actions.saveSnapshot()), [dispatch]);
  
  return { undo, redo, canUndo, canRedo, saveSnapshot };
};
```

### Keyboard Shortcuts
```ts
// Call saveSnapshot() before mutating state
// Then bind:
useEffect(() => {
  const handler = (e: KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
      e.preventDefault();
      undo();
    }
    if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
      e.preventDefault();
      redo();
    }
  };
  window.addEventListener('keydown', handler);
  return () => window.removeEventListener('keydown', handler);
}, [undo, redo]);
```

### UI: Toolbar Undo/Redo Buttons
- Add undo (↩) and redo (↪) buttons to builder canvas toolbar
- Disable undo button when `canUndo = false`
- Disable redo button when `canRedo = false`

### Trigger snapshot before:
- `addNode`, `deleteNode`, `connectNodes`, `disconnectEdge`, `updateNodeConfig`

## Acceptance Criteria
- [ ] Ctrl+Z undoes last canvas operation
- [ ] Ctrl+Shift+Z / Ctrl+Y redoes
- [ ] Toolbar buttons work + disable when unavailable
- [ ] History limited to 50 states (no memory leak)
- [ ] Redo stack clears on new operation (correct UX)
- [ ] Snapshot taken before each mutating action
