# TODO-579: Add Keyboard Shortcuts + Command Palette (Cmd+K)

**Repo:** signal-builder-frontend  
**Priority:** P2  
**Effort:** S (1-2 days)  
**Status:** pending

## Task Description
Add a Cmd+K command palette to the Signal Builder canvas for power users. Enables fast node insertion, canvas navigation, and action execution without mouse. Significant UX improvement for enterprise users who live in the builder.

## Acceptance Criteria
- [ ] Cmd+K (Mac) / Ctrl+K (Windows/Linux) opens command palette
- [ ] Palette shows searchable list of: node types, canvas actions, navigation
- [ ] Keyboard navigation (arrow keys + Enter) through results
- [ ] Esc closes palette
- [ ] Common canvas shortcuts documented: Delete node, Undo, Redo, Zoom fit
- [ ] Palette accessible via ARIA (role=dialog, labelled)

## Coding Prompt (Agent-Executable)
```
Navigate to /data/workspace/projects/signal-builder-frontend/

1. Install cmdk (shadcn command palette):
   yarn add cmdk

2. Create component at src/shared/ui/CommandPalette/CommandPalette.tsx:
   - Use cmdk's <Command> component
   - Register global keydown listener for Cmd+K / Ctrl+K
   - Populate with: node types from Redux builder state, canvas actions

3. Create src/shared/ui/CommandPalette/index.ts

4. Mount in builder page layout (src/pages/builder/)

5. Wire up commands to dispatch Redux actions or call ReactFlow API:
   - "Add Filter Node" → dispatch(addNode({type: 'filter'}))
   - "Fit View" → reactFlowInstance.fitView()
   - "Delete Selected" → dispatch(deleteSelectedNodes())
   - "Undo" → dispatch(undo())

6. Add keyboard shortcut hints to existing UI buttons

7. Write unit test for CommandPalette keyboard interaction
```

## Dependencies
- Familiarity with ReactFlow instance API (useReactFlow hook)
- Redux builder slice structure

## Notes
- cmdk is used by Vercel, Linear, Raycast — proven pattern
- Alternatively use kbar library for more features
