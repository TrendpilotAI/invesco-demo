# TODO-637 DONE: Remove duplicate reactflow@11 from signal-studio

## Status: ✅ COMPLETED

## Summary
Successfully removed `reactflow@11.11.4` from signal-studio, keeping only `@xyflow/react@12.9.0`. This saves ~300KB from the JS bundle.

## Changes Made

### Files Updated (import migration)
- `src/components/SignalCanvas/SignalCanvas.tsx` — `from 'reactflow'` → `from '@xyflow/react'`, fixed default→named import, updated CSS path
- `src/components/SignalCanvas/nodes/ConditionNode.tsx` — import updated
- `src/components/SignalCanvas/nodes/FilterNode.tsx` — import updated
- `src/components/SignalCanvas/nodes/OutputNode.tsx` — import updated
- `src/components/SignalCanvas/types.ts` — import updated
- `src/components/SignalCanvas/__tests__/SignalCanvas.test.tsx` — jest.mock updated
- `src/components/SignalCanvas/__tests__/nodes.test.tsx` — jest.mock updated
- `components/visual-editor/reactflow-editor.tsx` — import updated, default→named
- `components/visual-editor/custom-nodes.tsx` — import updated
- `components/visual-editor/visual-builder-chat.tsx` — import updated
- `app/signals/canvas/page.tsx` — import updated, default→named
- `app/visual-builder/builder/page.tsx` — import updated
- `app/visual-builder/enhanced/page.tsx` — import updated
- `lib/services/node-executor.ts` — import updated

### Package Changes
- Removed `reactflow@11.11.4` from `package.json` and `pnpm-lock.yaml`

### Key Fix
In `@xyflow/react@12`, `ReactFlow` is a named export (not default). Changed `import ReactFlow, {...}` → `import { ReactFlow, ...}` in 3 files.

## Build Notes
- Reactflow-related build errors resolved
- Remaining build errors are pre-existing (middleware crypto/Edge Runtime issue, thread-stream unrelated module types)

## Commit
`37ff9fe` — "TODO-637: remove duplicate reactflow@11, keep @xyflow/react@12 (~300KB savings)"
Pushed to: bitbucket.org/forwardlane/signal-studio (main branch)

## Date Completed
2026-03-06
