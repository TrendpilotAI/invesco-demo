# TODO: Archive Stale Root Documentation and Clean Up Debug Scripts

## Priority: P1
## Repo: signal-studio-frontend

### Problem
Numerous stale documentation files (AI-CHAT-*.md, IMPLEMENTATION-*.md, MVP-*.md, BRANCH-COMPLETE.md, etc.) and debug scripts clutter the repo root, making it hard to navigate and confusing for new contributors.

### Action Items
- Move all stale *.md files (AI-CHAT-*.md, IMPLEMENTATION-*.md, MVP-*.md, BRANCH-COMPLETE.md, GRANT-ACCESS-README.md, ICON-DESCRIPTION.md, INTEGRATION-DISCOVERY-SESSION.md, ENHANCED-VISUAL-BUILDER.md) to `docs/archive/`
- Remove or move debug scripts to scripts/
- Update README.md to be the single source of truth for setup/architecture
- Ensure CONTRIBUTING.md is accurate

### Impact
- Cleaner repo navigation
- Faster onboarding for new engineers
- Reduces confusion about project status
