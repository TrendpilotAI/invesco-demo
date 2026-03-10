# TODO-886: Add Keyboard Shortcuts to Builder Canvas

**Repo:** signal-builder-frontend  
**Priority:** P2 (Medium)  
**Effort:** S (1 day)  
**Status:** pending

## Implementation

### Shortcuts to Implement
| Action | Windows/Linux | Mac |
|--------|--------------|-----|
| Delete selected node/edge | Backspace / Delete | Backspace / Delete |
| Undo (requires TODO-883) | Ctrl+Z | Cmd+Z |
| Redo (requires TODO-883) | Ctrl+Shift+Z / Ctrl+Y | Cmd+Shift+Z |
| Save signal | Ctrl+S | Cmd+S |
| Fit view to canvas | Ctrl+Shift+F | Cmd+Shift+F |
| Zoom in | Ctrl++ | Cmd++ |
| Zoom out | Ctrl+- | Cmd+- |
| Select all nodes | Ctrl+A | Cmd+A |
| Copy selected node | Ctrl+C | Cmd+C |
| Paste node | Ctrl+V | Cmd+V |
| Show shortcut help | ? | ? |

### Coding Prompt

```
Create src/modules/builder/hooks/useKeyboardShortcuts.ts:

import { useEffect, useCallback } from 'react';
import { useReactFlow } from 'reactflow';
import { useDispatch } from 'react-redux';

export const useKeyboardShortcuts = () => {
  const { fitView, zoomIn, zoomOut, getNodes, setNodes, getEdges, setEdges } = useReactFlow();
  const dispatch = useDispatch();

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    const isMac = navigator.platform.includes('Mac');
    const ctrl = isMac ? e.metaKey : e.ctrlKey;
    
    // Don't fire when typing in an input/textarea
    const target = e.target as HTMLElement;
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) return;

    if (ctrl && !e.shiftKey && e.key === 's') {
      e.preventDefault();
      dispatch(saveSignal()); // wire up to existing save action
    }
    
    if (ctrl && e.shiftKey && e.key.toLowerCase() === 'f') {
      e.preventDefault();
      fitView({ padding: 0.1, duration: 300 });
    }
    
    if (e.key === '?') {
      // dispatch(toggleShortcutHelp());
    }
    
    // Delete selected: handled by ReactFlow natively with deleteKeyCode prop
  }, [dispatch, fitView, zoomIn, zoomOut]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);
};

// In ReactFlow component, set:
// deleteKeyCode={['Backspace', 'Delete']}
// multiSelectionKeyCode="Shift"
// selectionKeyCode="Shift"

Also create a ShortcutHelpModal component that shows the shortcut table
when the ? key is pressed, similar to GitHub's keyboard shortcut dialog.
```

## Dependencies
- TODO-883 (undo/redo) — for Ctrl+Z/Ctrl+Shift+Z

## Acceptance Criteria
- [ ] Ctrl+S triggers save signal (with visual feedback)
- [ ] Ctrl+Shift+F fits canvas view
- [ ] Backspace/Delete removes selected node (ReactFlow native)
- [ ] ? key shows shortcut help modal
- [ ] Shortcuts don't fire when typing in input fields
- [ ] Works on both Mac (Cmd) and Windows/Linux (Ctrl)
