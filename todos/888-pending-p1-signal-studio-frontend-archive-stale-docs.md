# TODO-888: Archive 20+ Stale Planning Docs + Root Cleanup

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** XS (10-15 minutes)  
**Status:** pending  
**Identified:** 2026-03-10 by Judge Agent v2

## Problem

The project root contains 20+ historical planning documents and debug scripts that:
1. Clutter the root directory (50+ files at root level)
2. Confuse new contributors about the actual architecture
3. Contain stale/incorrect information that contradicts current implementation

## Coding Prompt

```bash
cd /data/workspace/projects/signal-studio-frontend

# Archive stale planning docs
mkdir -p docs/archive
mv AI-CHAT-FINAL.md docs/archive/
mv AI-CHAT-IMPLEMENTATION-COMPLETE.md docs/archive/
mv BRANCH-COMPLETE.md docs/archive/
mv ENHANCED-VISUAL-BUILDER.md docs/archive/
mv IMPLEMENTATION-COMPLETE.md docs/archive/
mv IMPLEMENTATION-ROADMAP.md docs/archive/
mv IMPLEMENTATION-SUMMARY.md docs/archive/
mv INTEGRATION-DISCOVERY-SESSION.md docs/archive/
mv MVP-COMPLETION-PLAN.md docs/archive/
mv MVP-COMPLETION-SUMMARY.md docs/archive/
mv MVP-FINAL-STATUS.md docs/archive/
mv MVP-ORACLE-26AI.md docs/archive/
mv MVP-PROGRESS-REPORT.md docs/archive/
mv OML-SETUP.md docs/archive/
mv ORACLE-AI-SETUP-STATUS.md docs/archive/
mv ORACLE-SETUP.md docs/archive/
mv PHASE3-COMPLETE.md docs/archive/
mv PHASE3-PR-DESCRIPTION.md docs/archive/
mv PHASE3-PR-READY.md docs/archive/
mv REACT-FLOW-NODE-MAPPING.md docs/archive/
mv VISUAL-BUILDER-ARCHITECTURE-REVIEW.md docs/archive/
mv WARP.md docs/archive/

# Move debug scripts out of root
mkdir -p scripts/debug
mv test-direct-insert.js scripts/debug/
mv test-fix.js scripts/debug/
mv test-incremental.js scripts/debug/
mv test-minimal.js scripts/debug/
mv test-oml-connection.js scripts/debug/
mv test-oracle-connection.js scripts/debug/
mv test-ords.js scripts/debug/
mv test-vector-workaround.js scripts/debug/
mv check-admin-table-access.js scripts/debug/
mv check-user-privileges.js scripts/debug/
mv show-accessible-objects.js scripts/debug/
mv setup-ords.js scripts/debug/

# Archive SQL setup files (keep for reference in docs)
mkdir -p docs/sql
mv find-admin-tables.sql docs/sql/
mv grant-admin-tables-to-signalstudio.sql docs/sql/
mv grant-tablespace-quota.sql docs/sql/
mv grant-user-privileges.sql docs/sql/
mv quick-grant.sql docs/sql/

# Commit the cleanup
git add -A
git commit -m "chore: archive stale docs + move debug scripts out of root"
git push origin main
```

## Acceptance Criteria
- [ ] 20+ stale docs moved to `docs/archive/`
- [ ] Debug JS scripts moved to `scripts/debug/`
- [ ] SQL files moved to `docs/sql/`
- [ ] Project root has <15 files/directories
- [ ] `pnpm build` still passes after move
- [ ] Changes committed and pushed

## Notes
- Keep: README.md, AUDIT.md, BRAINSTORM.md, PLAN.md, CONTRIBUTING.md, Dockerfile, package.json, etc.
- The `src/middleware.ts` vs root `middleware.ts` conflict should be resolved separately
