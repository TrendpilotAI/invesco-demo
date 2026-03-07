# TODO-815: Remove dump.rdb from Signal Studio repo

**Priority**: CRITICAL (P0)
**Repo**: signal-studio
**Source**: AUDIT.md → AUDIT-001

## Description
`dump.rdb` (Redis data file) is committed to the repository. This file contains all Redis in-memory data at the time of the dump, potentially including session tokens, cached credentials, or rate limiter state. This is a security risk.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Add dump.rdb to .gitignore:
   echo "dump.rdb" >> .gitignore

2. Remove from git tracking:
   git rm --cached dump.rdb

3. Add to .gitignore and commit:
   git add .gitignore
   git commit -m "security: remove dump.rdb from tracking, add to .gitignore"

4. If this file has been in the repo for more than 1 commit, use git filter-repo to purge history:
   pip install git-filter-repo
   git filter-repo --invert-paths --path dump.rdb
   git push --force-with-lease

5. After removal, rotate any secrets that may have been in Redis (session tokens, API keys).
```

## Acceptance Criteria
- [ ] `dump.rdb` not present in any git commit going forward
- [ ] `.gitignore` contains `dump.rdb`
- [ ] Relevant Redis secrets rotated

## Effort
1 hour (plus secret rotation time)

## Dependencies
None
