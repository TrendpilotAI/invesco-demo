# TODO-729: Cleanup Debug & Test Files at Repo Root

**Repo:** flip-my-era  
**Priority:** P2  
**Effort:** XS (30 min)  
**Status:** pending

## Description
Multiple debug HTML files and redundant test scripts are cluttering the repo root. These should be removed or gitignored before production.

## Files to Remove
```bash
# Debug HTML files (not part of the app)
rm /data/workspace/projects/flip-my-era/image-manager.html
rm /data/workspace/projects/flip-my-era/image-manager-pro.html
rm /data/workspace/projects/flip-my-era/image-manager-ultimate.html
rm /data/workspace/projects/flip-my-era/image-manager-pro.html
rm /data/workspace/projects/flip-my-era/debug-image-viewer.html
rm /data/workspace/projects/flip-my-era/debug-ultimate.html
rm /data/workspace/projects/flip-my-era/test-auth.html
rm /data/workspace/projects/flip-my-era/test-image-load.html
rm /data/workspace/projects/flip-my-era/generated-images-viewer.html

# Redundant E2E scripts (use playwright instead)
rm /data/workspace/projects/flip-my-era/e2e-test.mjs
rm /data/workspace/projects/flip-my-era/e2e-test-v2.mjs
rm /data/workspace/projects/flip-my-era/e2e-test-v3.mjs

# Strip console.logs from production code
cd /data/workspace/projects/flip-my-era
grep -rn "console.log" src/ --include="*.ts" --include="*.tsx" | grep -v "test" | grep -v "spec"
# Replace with conditional: if (import.meta.env.DEV) { console.log(...) }
```

## Coding Prompt
```
In /data/workspace/projects/flip-my-era/:

1. Delete all debug HTML files listed above
2. Delete redundant e2e-test*.mjs files (playwright e2e/ directory is canonical)
3. Find all console.log() calls in src/ (excluding test files)
4. Replace with either:
   - Remove entirely (noise logs)
   - Wrap in: if (import.meta.env.DEV) { console.log(...) }
   - Replace with proper logger: import { logger } from '@/core/utils/logger'
5. Run: pnpm lint && pnpm typecheck to verify no breakage
6. Commit: "chore: remove debug files and strip production console.logs"
```

## Acceptance Criteria
- [ ] No debug HTML files in repo root
- [ ] No unguarded console.log() in src/ production code
- [ ] All tests still pass after cleanup
- [ ] ESLint no-console rule enforced going forward
