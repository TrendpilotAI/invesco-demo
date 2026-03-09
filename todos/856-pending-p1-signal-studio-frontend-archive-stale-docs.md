# Archive Stale Root Markdown Documents

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (10 min)

## Description
20+ planning/implementation markdown files clutter the project root. They were created during development milestones and are no longer actionable. Move to `docs/archive/`.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend:
1. mkdir -p docs/archive
2. Move these files to docs/archive/:
   AI-CHAT-FINAL.md AI-CHAT-IMPLEMENTATION-COMPLETE.md BRANCH-COMPLETE.md
   ENHANCED-VISUAL-BUILDER.md IMPLEMENTATION-COMPLETE.md IMPLEMENTATION-ROADMAP.md
   IMPLEMENTATION-SUMMARY.md INTEGRATION-DISCOVERY-SESSION.md MVP-COMPLETION-PLAN.md
   MVP-COMPLETION-SUMMARY.md MVP-FINAL-STATUS.md MVP-ORACLE-26AI.md
   MVP-PROGRESS-REPORT.md OML-SETUP.md ORACLE-AI-SETUP-STATUS.md ORACLE-SETUP.md
   PHASE3-COMPLETE.md PHASE3-PR-DESCRIPTION.md PHASE3-PR-READY.md
   REACT-FLOW-NODE-MAPPING.md VISUAL-BUILDER-ARCHITECTURE-REVIEW.md WARP.md
3. Keep: README.md, CONTRIBUTING.md, CODEOWNERS, GRANT-ACCESS-README.md,
         PLATFORM-DESCRIPTION.md, BRAINSTORM.md, PLAN.md, AUDIT.md
4. Commit: "chore: archive stale planning docs to docs/archive/"
```

## Acceptance Criteria
- [ ] Root only contains essential docs (README, CONTRIBUTING, CODEOWNERS)
- [ ] `docs/archive/` contains 20+ historical docs
- [ ] Build passes

## Dependencies
None
