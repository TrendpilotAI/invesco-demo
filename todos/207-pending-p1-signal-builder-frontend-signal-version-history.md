---
status: pending
priority: p1
issue_id: "207"
tags: [feature, versioning, compliance, signal-builder-frontend]
dependencies: ["203", "202"]
---

# 207 — Signal Version History / Audit Trail

## Problem Statement

Financial clients must often explain *why* a signal was configured a certain way at a specific point in time (regulatory compliance, SOC2, client reporting). The existing `TSignal` type has `is_draft` / `is_published` flags suggesting a lifecycle exists, but there is no version history, diff view, or audit trail. This is a direct revenue driver for compliance-focused enterprise accounts.

## Findings

- `TSignal` type has `is_draft: boolean`, `is_published: boolean`, `key: string`, `id: string`
- Signal state is stored via `updateSignalUI` mutation (POST to `/api/v1/signals/{id}/ui/`)
- No `version` field exists in `TSignal` type
- No version history endpoint in `API_PATHS`
- Backend would need new DB columns + API endpoints (backend TODO separate)
- Frontend needs: version list sidebar, version preview, restore action, diff view

## Proposed Solutions

### Option A: Frontend UI with new backend API (Full solution)
Build the version history UI assuming backend returns `GET /api/v1/signals/{id}/versions/`.
- **Pros:** Complete solution
- **Cons:** Requires backend changes (coordinate with backend team)
- **Effort:** M frontend + M backend
- **Risk:** Medium (backend dependency)

### Option B: Client-side snapshot storage (MVP)
Store signal snapshots in browser localStorage keyed by signal ID + timestamp.
- **Pros:** No backend changes, ships immediately
- **Cons:** Not persistent across browsers/devices, not audit-trail grade
- **Effort:** S
- **Risk:** Low (but limited value for compliance)

## Recommended Action

Phase 1: Option B (localStorage snapshots) as an MVP to validate the UX. Phase 2: backend-driven version history. Create a companion TODO for the backend repo.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

Task: Implement Signal Version History — Phase 1 (localStorage snapshots)

1. Create src/shared/lib/signalVersions.ts:
   
   export interface SignalSnapshot {
     signalId: string;
     version: number;
     timestamp: number; // Unix ms
     label: string;     // e.g., "Auto-save" or "Before publish"
     tabData: TTab[];   // full Redux state snapshot
   }
   
   export const SignalVersionStore = {
     MAX_VERSIONS: 20,
     
     save(signalId: string, tabData: TTab[], label = 'Auto-save'): SignalSnapshot,
     list(signalId: string): SignalSnapshot[],
     getVersion(signalId: string, version: number): SignalSnapshot | null,
     restore(signalId: string, version: number): TTab[] | null,
     clear(signalId: string): void,
   };

2. Create src/modules/builder/containers/VersionHistory/VersionHistory.tsx:
   - Slide-in panel (right side or bottom of builder)
   - Lists saved snapshots with timestamp and label
   - "Restore" button on each snapshot
   - "Save Snapshot" button in the header (manual save)
   - Shows diff summary: "X nodes, Y edges"

3. Create src/modules/builder/containers/VersionHistory/VersionHistoryPanel.tsx:
   - Collapsible panel with toggle button in the Builder header
   - Version list with relative timestamps ("2 hours ago", "Yesterday")

4. Auto-save snapshots on key events:
   In builder.hook.tabs.ts or the relevant hook, call SignalVersionStore.save() on:
   - Before publish (label: "Before publish")
   - Every 5 minutes of active editing (label: "Auto-save")
   - Before delete of a node (label: "Before node deletion")

5. Add "Version History" button to Builder Header:
   In src/modules/builder/containers/Header/Header.container.tsx:
   - Add a clock icon button that opens the VersionHistoryPanel

6. On "Restore" action:
   - Load the snapshot's tabData into Redux state
   - Show a toast: "Restored to version from {timestamp}"
   - The restored state is NOT auto-saved (user must manually save/publish)

7. Wire up Storybook story for VersionHistory component.

8. Run: yarn typecheck && yarn lint
```

## Dependencies

- 203 (eliminate any types) — ensures TTab is properly typed when serializing to localStorage
- 202 (Sentry) — version restore errors should be tracked

## Estimated Effort

**Medium** — 5-8 hours (Phase 1 localStorage only)

## Acceptance Criteria

- [ ] `src/shared/lib/signalVersions.ts` exports `SignalVersionStore` with save/list/restore/clear
- [ ] Version history panel is accessible from the Builder header
- [ ] Snapshots are auto-saved before publish and every 5 minutes
- [ ] "Restore" action loads the snapshot into Redux state
- [ ] Max 20 versions are stored per signal (oldest purged)
- [ ] Snapshots persist across page refreshes (localStorage)
- [ ] Relative timestamps are displayed ("2 hours ago")
- [ ] `yarn typecheck` passes
- [ ] Toast notification shown on restore

## Work Log

### 2026-02-26 — Todo created

**By:** Planning Agent

**Actions:**
- Confirmed TSignal type has no version field
- Identified auto-save trigger points in builder hooks
- Chose localStorage approach for Phase 1 to avoid backend dependency
