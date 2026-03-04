# TODO-484: State Management Contract — Document Redux/React Query Boundaries

**Project:** signal-builder-frontend
**Priority:** P1 (MEDIUM impact, S effort)
**Estimated Effort:** 2-3 hours
**Dependencies:** None

## Description

State management is mixed ad-hoc between Redux Toolkit (canvas state), React Query (server cache), and possibly local state. Document clear boundaries and add lint rules to enforce them. Create STATE_MANAGEMENT.md decision record.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Document and enforce state management boundaries.

STEPS:
1. Audit current state usage:
   - Read src/redux/ — understand what's in Redux (builder, auth slices)
   - grep -r "useQuery\|useMutation\|createApi" src/ — find React Query/RTK Query usage
   - grep -r "useState\|useReducer" src/ | head -30 — find local state patterns

2. Create docs/STATE_MANAGEMENT.md:
   # State Management Contract

   ## Rules
   | State Type | Tool | Examples |
   |------------|------|----------|
   | Canvas/builder state | Redux Toolkit | Node positions, edges, selected node, undo/redo |
   | Auth state | Redux Toolkit | User token, profile, login status |
   | Server data (signals, templates) | RTK Query | Signal list, signal details, API responses |
   | Ephemeral UI state | React useState | Modal open/close, form inputs, hover states |

   ## Anti-patterns (DO NOT)
   - Don't put server data in Redux slices (use RTK Query)
   - Don't put ephemeral UI state in Redux
   - Don't duplicate server state between Redux and RTK Query

   ## Migration Notes
   - [List any current violations found in audit]

3. Add ESLint rule or comment convention to flag violations

4. If any obvious violations exist (server data in Redux slices), document them as tech debt with migration plan

CONSTRAINTS:
- This is documentation + audit, not a refactor
- Don't move state around yet — just document what should change
- Be specific about which files violate the contract
```

## Acceptance Criteria
- [ ] docs/STATE_MANAGEMENT.md exists with clear rules
- [ ] Current violations documented with file paths
- [ ] Migration plan for each violation
- [ ] Team can reference this for all future state decisions
