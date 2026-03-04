# TODO-493: Signal Version History UI

**Project:** signal-builder-frontend
**Priority:** P3 (MEDIUM impact, M effort)
**Estimated Effort:** 8-10 hours
**Dependencies:** TODO-204 (backend versioning — ✅ DONE), TODO-483 (ReactFlow v12)

## Description

Snapshot signal graphs on save/publish. Visual diff between versions (highlight changed nodes). Rollback to prior version. Compliance audit trail for regulated advisors.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Build signal version history UI.

STEPS:
1. Create src/modules/builder/containers/VersionHistory/:
   - VersionPanel.tsx — sidebar panel listing version history
   - VersionDiff.tsx — visual diff view (two ReactFlow canvases side-by-side)
   - VersionEntry.tsx — single version row (timestamp, author, change summary)

2. Wire to backend versioning API (already built — TODO-204):
   - GET /signals/{id}/versions — list versions
   - GET /signals/{id}/versions/{version_id} — get specific version
   - POST /signals/{id}/rollback/{version_id} — rollback

3. Visual diff:
   - Side-by-side ReactFlow canvases (before/after)
   - Green highlight: added nodes/edges
   - Red highlight: removed nodes/edges
   - Yellow highlight: modified node configs
   - Compute diff from two version snapshots

4. Rollback UX:
   - "Restore this version" button with confirmation modal
   - Shows what will change before confirming
   - Creates new version on rollback (never destructive)

5. Add version history button to builder header (clock icon)
6. Add E2E test: create signal → publish → modify → publish → view diff → rollback

CONSTRAINTS:
- Version history is read-only except rollback
- Diff computation happens client-side
- Max 50 versions loaded (paginate if more)
- Rollback creates a new version (append-only history)
```

## Acceptance Criteria
- [ ] Version history panel shows all versions
- [ ] Visual diff highlights added/removed/modified nodes
- [ ] Rollback works with confirmation
- [ ] Compliance audit trail visible
- [ ] E2E test covers full version lifecycle
