---
status: pending
priority: p1
issue_id: "007"
tags: [signal-studio, visual-builder, reactflow, api-integration]
dependencies: ["005", "006"]
---

# 007 — Signal Studio: Wire Visual Builder Node Executor to Real Signal API Endpoints

## Problem Statement

The Visual Builder (`app/visual-builder/builder/page.tsx`) has a sophisticated React Flow-based
node system with a `lib/services/node-executor.ts` that calls backend APIs. However, the "Run Flow"
button doesn't execute nodes end-to-end — there's no UI wiring connecting node execution results
to the canvas. Additionally, several API endpoints called by `node-executor.ts` may not exist
or return mock data:
- `/api/signals/prompt/compile` — needs verification
- `/api/signals/filter/generate` — needs verification  
- `/api/signals/aggregate/generate` — needs verification
- `/api/data/query` — needs verification
- `/api/ai/completion` — needs verification

## Findings

- `lib/services/node-executor.ts` — full topological execution engine exists, well-structured
- `components/visual-editor/flow-editor.tsx` — React Flow canvas component
- `components/visual-editor/reactflow-editor.tsx` — enhanced editor variant
- `components/visual-editor/properties-panel.tsx` — node config panel
- `components/visual-editor/preview-panel.tsx` — output preview pane
- `app/visual-builder/builder/page.tsx` — page orchestrating everything
- `app/api/visual-builder/chat/route.ts` — AI guidance route exists
- Missing: Execute button → `executeFlow()` connection → results → preview-panel

## Proposed Solutions

### Option A: Wire existing executor to UI (Recommended)
1. Add "Execute" button to `flow-editor.tsx` toolbar
2. Call `executeFlow(nodes, edges)` on click
3. Show per-node execution status (spinner → ✓ or ✗) overlaid on nodes
4. Pipe final output node result to `preview-panel.tsx`
5. Verify/fix all 5 API routes called by node-executor
- **Effort:** 8h | **Risk:** Medium

### Option B: WebSocket streaming execution
- Expensive, defer to later iteration

## Recommended Action

Option A: Wire the existing executor to the React Flow UI with per-node status feedback.

## Acceptance Criteria

- [ ] "Run Flow" / "Execute" button exists in `flow-editor.tsx` toolbar
- [ ] Clicking Execute calls `executeFlow()` from `lib/services/node-executor.ts`
- [ ] Each node shows execution status overlay: idle / running / success / error
- [ ] `preview-panel.tsx` displays final output node result after execution
- [ ] `/api/signals/prompt/compile` route exists and compiles Jinja-style templates
- [ ] `/api/signals/filter/generate` route exists and returns `{ sql: string }`
- [ ] `/api/signals/aggregate/generate` route exists and returns `{ sql: string }`
- [ ] `/api/data/query` route exists, validates table name, queries Oracle or returns mock
- [ ] `/api/ai/completion` route exists and calls OpenRouter/OpenAI
- [ ] Execution errors shown as toast notifications with node-level detail
- [ ] Flow results can be "saved as signal" via backend (connects to TODO 006)
- [ ] `__tests__/lib/node-executor.test.ts` with mock API assertions

## Files to Create/Modify

- `components/visual-editor/flow-editor.tsx` — add Execute button, node status overlays
- `components/visual-editor/preview-panel.tsx` — display execution results
- `components/visual-editor/custom-nodes.tsx` — add status indicator to node rendering
- `app/visual-builder/builder/page.tsx` — wire Execute state through component tree
- `app/api/signals/prompt/compile/route.ts` — verify/create: compile template with vars
- `app/api/signals/filter/generate/route.ts` — verify/create: generate WHERE clause SQL
- `app/api/signals/aggregate/generate/route.ts` — verify/create: generate GROUP BY SQL
- `app/api/data/query/route.ts` — verify/create: table query with column/filter support
- `app/api/ai/completion/route.ts` — verify/create: unified LLM completion endpoint
- `lib/services/node-executor.ts` — add AbortController for cancellation support
- `__tests__/lib/node-executor.test.ts` — NEW: unit tests

## Technical Details

```typescript
// In flow-editor.tsx — execution state management
const [isExecuting, setIsExecuting] = useState(false)
const [nodeStatuses, setNodeStatuses] = useState<Map<string, 'idle'|'running'|'success'|'error'>>(new Map())
const [executionResults, setExecutionResults] = useState<Map<string, NodeExecutionResult> | null>(null)

const handleExecute = async () => {
  if (!validateFlow(nodes, edges).valid) return toast.error('Fix validation errors first')
  setIsExecuting(true)
  setNodeStatuses(new Map(nodes.map(n => [n.id, 'idle'])))
  
  // Execute with per-node callbacks
  const results = await executeFlow(nodes, edges, {
    onNodeStart: (id) => setNodeStatuses(prev => new Map(prev).set(id, 'running')),
    onNodeComplete: (id, result) => setNodeStatuses(prev => new Map(prev).set(id, result.success ? 'success' : 'error')),
  })
  
  setExecutionResults(results)
  setIsExecuting(false)
}
```

## Estimated Effort

8 hours

## Work Log

### 2026-02-26 — Initial Planning

**By:** Honey Planning Agent

**Actions:**
- Traced node-executor.ts API call sites — 5 endpoints to verify/create
- Identified missing UI wiring between Execute button and executor
- Designed per-node status overlay approach
