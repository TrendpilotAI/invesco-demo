# 872 — Archive 20+ Stale Markdown Docs from Project Root

**Repo:** signal-studio  
**Priority:** P2 — Low  
**Effort:** 0.5 day  
**Status:** pending

## Problem
The project root contains 20+ stale markdown files from development phases, PRs, and implementation notes. These clutter `git status`, confuse new contributors, and make the README harder to find.

## Files to Archive
```
AI-CHAT-FINAL.md
AI-CHAT-IMPLEMENTATION-COMPLETE.md
BRANCH-COMPLETE.md
ECOSYSTEM_ANALYSIS_AND_BACKEND_PROPOSAL.md
ENHANCED-VISUAL-BUILDER.md
GRANT-ACCESS-README.md
ICON-DESCRIPTION.md
IMPLEMENTATION-COMPLETE.md
IMPLEMENTATION-ROADMAP.md
IMPLEMENTATION-SUMMARY.md
INTEGRATION-DISCOVERY-SESSION.md
MVP-COMPLETION-PLAN.md
MVP-COMPLETION-SUMMARY.md
MVP-FINAL-STATUS.md
MVP-ORACLE-26AI.md
MVP-PROGRESS-REPORT.md
OML-SETUP.md
ORACLE-AI-SETUP-STATUS.md
ORACLE-SETUP.md
PHASE-1-COMPLETE.md
PHASE-3-COMPLETE.md
PHASE3-COMPLETE.md
PHASE3-PR-DESCRIPTION.md
PHASE3-PR-READY.md
PR-CREATION-GUIDE.md
PR-CREATION-NOTE.md
PR-DESCRIPTION.md
PR-READY-TO-CREATE.md
PR_DESCRIPTION.md
QODO-INSTALLATION-GUIDE.md
REACT-FLOW-NODE-MAPPING.md
README-MEMORY-SYSTEM.md
README-WORKSPACE.md
VISUAL-BUILDER-ARCHITECTURE-REVIEW.md
WARP.md
```

## Files to Keep in Root
```
README.md
CONTRIBUTING.md
CODEOWNERS
```

## Also: Move Root JS Test Scripts
These .js test files don't belong in project root:
```
check-admin-table-access.js
check-user-privileges.js
setup-ords.js
show-accessible-objects.js
test-direct-insert.js
test-fix.js
test-incremental.js
test-minimal.js
test-oml-connection.js
test-oracle-connection.js
test-ords.js
test-vector-workaround.js
```
→ Move to `scripts/db-setup/`

## Coding Prompt (for autonomous agent)
```bash
cd /data/workspace/projects/signal-studio

# Create archive directory
mkdir -p docs/archive

# Move stale markdown files
mv AI-CHAT-FINAL.md AI-CHAT-IMPLEMENTATION-COMPLETE.md BRANCH-COMPLETE.md \
   ECOSYSTEM_ANALYSIS_AND_BACKEND_PROPOSAL.md ENHANCED-VISUAL-BUILDER.md \
   GRANT-ACCESS-README.md ICON-DESCRIPTION.md IMPLEMENTATION-COMPLETE.md \
   IMPLEMENTATION-ROADMAP.md IMPLEMENTATION-SUMMARY.md \
   INTEGRATION-DISCOVERY-SESSION.md MVP-COMPLETION-PLAN.md \
   MVP-COMPLETION-SUMMARY.md MVP-FINAL-STATUS.md MVP-ORACLE-26AI.md \
   MVP-PROGRESS-REPORT.md OML-SETUP.md ORACLE-AI-SETUP-STATUS.md \
   ORACLE-SETUP.md PHASE-1-COMPLETE.md PHASE-3-COMPLETE.md PHASE3-COMPLETE.md \
   PHASE3-PR-DESCRIPTION.md PHASE3-PR-READY.md PR-CREATION-GUIDE.md \
   PR-CREATION-NOTE.md PR-DESCRIPTION.md PR-READY-TO-CREATE.md PR_DESCRIPTION.md \
   QODO-INSTALLATION-GUIDE.md REACT-FLOW-NODE-MAPPING.md README-MEMORY-SYSTEM.md \
   README-WORKSPACE.md VISUAL-BUILDER-ARCHITECTURE-REVIEW.md WARP.md \
   docs/archive/

# Move root JS test scripts
mkdir -p scripts/db-setup
mv check-admin-table-access.js check-user-privileges.js setup-ords.js \
   show-accessible-objects.js test-direct-insert.js test-fix.js \
   test-incremental.js test-minimal.js test-oml-connection.js \
   test-oracle-connection.js test-ords.js test-vector-workaround.js \
   scripts/db-setup/

git add -A
git commit -m "chore: archive stale docs and move db test scripts to scripts/db-setup/"
```

## Acceptance Criteria
- [ ] Root directory contains only README.md, CONTRIBUTING.md, CODEOWNERS + source files
- [ ] Archived files still accessible in docs/archive/
- [ ] DB test scripts accessible in scripts/db-setup/
- [ ] `git status` is clean after archive
