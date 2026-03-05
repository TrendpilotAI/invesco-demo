# TODO 622 — CRITICAL: Purge API Keys from Git History

**Repo:** Ultrafone  
**Priority:** CRITICAL  
**Effort:** 1 hour  
**Depends on:** 568 (rotate keys)

## Problem
`backend/.env.development` with live API keys was committed to git. Even after `.gitignore` is updated, the file remains in git history and can be recovered by anyone with repo access.

## Task
Remove the file from ALL git history using `git filter-repo`.

## Execution Prompt
```bash
cd /data/workspace/projects/Ultrafone

# Install git-filter-repo if needed
pip install git-filter-repo

# Remove file from all history
git filter-repo --path backend/.env.development --invert-paths

# Force push (COORDINATE WITH TEAM first)
git push origin --force --all

# Verify
git log --all --full-history -- backend/.env.development
# Should return empty

# Add to gitignore if not already there
echo "backend/.env.development" >> .gitignore
echo "backend/.env.local" >> .gitignore
echo "backend/.env.*.local" >> .gitignore
git add .gitignore && git commit -m "security: prevent future env file commits"
```

## Acceptance Criteria
- [ ] `git log --all -- backend/.env.development` returns empty
- [ ] `.gitignore` includes `backend/.env*` patterns (except `.env.example`)
- [ ] All collaborators have re-cloned the repo (force push invalidates local histories)
- [ ] All exposed API keys have been rotated (see TODO 568)
