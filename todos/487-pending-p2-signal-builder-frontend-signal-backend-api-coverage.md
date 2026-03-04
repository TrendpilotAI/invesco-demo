# TODO-487: Signal Backend API Coverage Audit

**Project:** signal-builder-frontend
**Priority:** P2 (HIGH impact, M effort)
**Estimated Effort:** 4-6 hours
**Dependencies:** None

## Description

Audit which backend endpoints are NOT yet consumed by the frontend. Likely gaps: tags, sharing, version history endpoints. Wire missing integrations.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.
Backend repo: /data/workspace/projects/signal-builder-backend/

TASK: Audit and wire missing backend API endpoints.

STEPS:
1. List all backend endpoints:
   grep -rn "@app\.\(get\|post\|put\|delete\|patch\)" /data/workspace/projects/signal-builder-backend/src/ | grep -v test

2. List all frontend API calls:
   grep -rn "apiPath\|baseUrl\|/api/" src/ --include="*.ts" --include="*.tsx"
   Also check RTK Query endpoint definitions in src/redux/

3. Create a matrix: endpoint → frontend usage (used/unused)

4. For each unused endpoint, either:
   a. Wire it into existing UI (if UI exists but isn't connected)
   b. Document it as a future feature with the UI needed

5. Key gaps to check:
   - Signal versioning endpoints (if TODO-204 is done)
   - Signal preview/dry-run endpoint
   - Audit log endpoint
   - Tags/categories endpoints
   - Sharing/collaboration endpoints

6. Create docs/API_COVERAGE.md with the full matrix

CONSTRAINTS:
- Only wire endpoints where UI already exists
- Document gaps that need UI work separately
- Don't create new UI in this TODO
```

## Acceptance Criteria
- [ ] docs/API_COVERAGE.md lists all backend endpoints with frontend coverage status
- [ ] Any quick-wire gaps (UI exists, not connected) are wired
- [ ] Missing UI features documented as separate TODOs
