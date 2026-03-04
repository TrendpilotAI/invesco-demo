# TODO-457: Gitignore dump.rdb Redis dump file

**Repo:** signal-studio  
**Priority:** low  
**Effort:** XS  
**Date:** 2026-03-04  

## Problem

`dump.rdb` (Redis persistence dump) is committed to the repo root. This file:
- May contain sensitive cached data (API responses, session tokens)
- Is a binary blob that bloats git history
- Should never be in source control

## Task

```bash
cd /data/workspace/projects/signal-studio
echo "dump.rdb" >> .gitignore
git rm --cached dump.rdb
git add .gitignore
git commit -m "chore: gitignore Redis dump file, remove from tracking"
```

## Acceptance Criteria
- [ ] `dump.rdb` added to `.gitignore`
- [ ] `dump.rdb` removed from git tracking (but not deleted from disk)
- [ ] Committed and pushed
