# TODO-610: Delete Dead Code — Root Test Scripts + Stale Docs

**Repo:** signal-studio-frontend  
**Priority:** P1 (Cleanup)  
**Effort:** XS (30 min)  
**Status:** pending

## Description

13 root-level ad-hoc test scripts and 30+ stale markdown phase/PR docs are cluttering the repo root. Delete them.

## Files to Delete

### Root test scripts (move useful ones to scripts/, delete the rest):
- test-oracle-connection.js
- test-oml-connection.js  
- test-incremental.js
- test-minimal.js
- test-direct-insert.js
- test-fix.js
- test-vector-workaround.js
- test-ords.js
- check-admin-table-access.js
- check-user-privileges.js
- show-accessible-objects.js
- setup-ords.js
- bitbucket-auth.html

### Stale docs to delete:
- PHASE-1-COMPLETE.md, PHASE-3-COMPLETE.md, PHASE3-COMPLETE.md
- PR-CREATION-GUIDE.md, PR-CREATION-NOTE.md, PR-DESCRIPTION.md, PR-READY-TO-CREATE.md, PR_DESCRIPTION.md
- PHASE3-PR-DESCRIPTION.md, PHASE3-PR-READY.md
- BRANCH-COMPLETE.md
- MVP-COMPLETION-PLAN.md, MVP-COMPLETION-SUMMARY.md, MVP-PROGRESS-REPORT.md
- AI-CHAT-FINAL.md, AI-CHAT-IMPLEMENTATION-COMPLETE.md
- IMPLEMENTATION-COMPLETE.md, IMPLEMENTATION-SUMMARY.md
- GRANT-ACCESS-README.md, OML-SETUP.md (if covered by README)

## Coding Prompt
```bash
cd /data/workspace/projects/signal-studio-frontend
# Review each script - move if useful, delete if not
rm test-oracle-connection.js test-oml-connection.js test-incremental.js test-minimal.js \
   test-direct-insert.js test-fix.js test-vector-workaround.js test-ords.js \
   check-admin-table-access.js check-user-privileges.js show-accessible-objects.js \
   setup-ords.js bitbucket-auth.html
rm PHASE-1-COMPLETE.md PHASE-3-COMPLETE.md PHASE3-COMPLETE.md \
   PR-CREATION-GUIDE.md PR-CREATION-NOTE.md PR-DESCRIPTION.md PR-READY-TO-CREATE.md \
   PR_DESCRIPTION.md PHASE3-PR-DESCRIPTION.md PHASE3-PR-READY.md BRANCH-COMPLETE.md \
   MVP-COMPLETION-PLAN.md MVP-COMPLETION-SUMMARY.md MVP-PROGRESS-REPORT.md \
   AI-CHAT-FINAL.md AI-CHAT-IMPLEMENTATION-COMPLETE.md \
   IMPLEMENTATION-COMPLETE.md IMPLEMENTATION-SUMMARY.md
git add -A && git commit -m "chore: remove dead code and stale docs"
```

## Dependencies
- None
