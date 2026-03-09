# 858 — Rotate ALL Exposed API Keys (Ultrafone)

**Priority:** P0 — CRITICAL SECURITY  
**Repo:** Ultrafone  
**Effort:** 2 hours  

## Description
Real API keys for Groq, Deepgram, Twilio, and Fish Audio — plus Nathan's personal phone number — are committed in `backend/.env.development` in the git history. These must be rotated immediately and purged from history.

## Coding Prompt
```
1. Go to each service dashboard and rotate keys:
   - Groq: https://console.groq.com
   - Deepgram: https://console.deepgram.com  
   - Twilio: https://console.twilio.com (Auth Token rotation)
   - Fish Audio: https://fish.audio

2. Update Railway environment variables with new keys

3. Purge .env.development from git history:
   pip install git-filter-repo
   git filter-repo --path backend/.env.development --invert-paths
   git push origin --force --all

4. Add to .gitignore:
   .env.development
   .env.production
   .env.local

5. Install gitleaks pre-commit hook to prevent future leaks
```

## Acceptance Criteria
- [ ] All old keys disabled in service dashboards
- [ ] `git log --all --full-diff -p | grep "gsk_Pk"` returns nothing
- [ ] New keys working in Railway deployment
- [ ] `.env.development` in `.gitignore`
