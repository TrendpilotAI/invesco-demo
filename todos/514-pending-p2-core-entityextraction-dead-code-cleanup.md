# TODO-514: Dead Code Cleanup

**Repo:** core-entityextraction
**Priority:** P2
**Effort:** S (30min)
**Dependencies:** None
**Blocks:** None

## Description
Audit `services/ml_entity_extraction_service/` for dead code left from Flask migration. Remove unused files.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Audit services/ directory for unused wrapper files from Flask era
2. Check for imports — if nothing imports a file, it's dead
3. Check uwsgi.ini.example — likely dead after FastAPI migration
4. Check Vagrantfile — likely unused if deploying via Docker/Railway
5. Remove dead files (use git rm)
6. Update any stale references in README.md
```

## Acceptance Criteria
- [ ] No unused Python files remain
- [ ] No Flask-era config files remain (unless needed)
- [ ] All imports verified
