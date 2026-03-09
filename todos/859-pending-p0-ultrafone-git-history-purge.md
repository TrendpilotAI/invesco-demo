# 859 — Purge .env.development from Git History

**Priority:** P0 — CRITICAL SECURITY  
**Repo:** Ultrafone  
**Effort:** 1 hour  
**Depends on:** 858 (key rotation must happen first)

## Description
After rotating keys, use git-filter-repo to permanently remove `.env.development` from all git history commits. Force-push cleaned history to GitHub.

## Commands
```bash
pip install git-filter-repo
cd /data/workspace/projects/Ultrafone
git filter-repo --path backend/.env.development --invert-paths
git remote add origin git@github.com:TrendpilotAI/Ultrafone.git
git push origin --force --all --tags
```

## Acceptance Criteria
- [ ] `git log --all --full-diff -p | grep "GROQ_API_KEY"` returns nothing
- [ ] GitHub repo history clean
- [ ] All collaborators notified to re-clone
