# 871 — Remove Legacy reactflow v11 (Keep @xyflow/react v12)

**Repo:** signal-studio  
**Priority:** P2 — Medium  
**Effort:** 0.5 day  
**Status:** pending

## Problem
Both `reactflow@11` and `@xyflow/react@12` are installed simultaneously.
- `@xyflow/react` v12 is the current/maintained version
- `reactflow` v11 is the legacy version (same lib, renamed)
- Having both adds ~200KB to node_modules and risks API confusion

## Task
Remove `reactflow` v11, migrate any imports to `@xyflow/react`.

## Coding Prompt (for autonomous agent)
```bash
# 1. Find all imports of reactflow v11
cd /data/workspace/projects/signal-studio
grep -rn "from 'reactflow'\|from \"reactflow\"\|require('reactflow')" --include="*.ts" --include="*.tsx" | grep -v node_modules

# 2. For each file, update the import:
# Before:
import { ReactFlow, Handle, Position } from 'reactflow'
import 'reactflow/dist/style.css'

# After:
import { ReactFlow, Handle, Position } from '@xyflow/react'
import '@xyflow/react/dist/style.css'

# Note: @xyflow/react v12 has some API changes from reactflow v11
# Check migration guide: https://reactflow.dev/learn/migrate-to-v12

# 3. Remove reactflow from package.json
pnpm remove reactflow

# 4. Run build to confirm no import errors
pnpm build

# 5. Test visual-builder page and canvas page manually
```

## Acceptance Criteria
- [ ] `reactflow` removed from package.json
- [ ] `pnpm build` succeeds with no import errors
- [ ] Visual Builder page renders correctly
- [ ] Canvas page renders correctly
- [ ] No visual regressions in node-based UI

## Dependencies
- None (independent)
