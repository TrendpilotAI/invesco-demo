# 433 — CRITICAL: Rotate Leaked API Keys in Ultrafone

**Priority:** CRITICAL  
**Repo:** Ultrafone  
**Effort:** XS (1-2 hours)  

## Description

Real API keys and credentials are committed in `backend/.env.development` in the Ultrafone git repository. These must be rotated immediately and the file removed from git history.

## Exposed Credentials

- `GROQ_API_KEY` — Groq API key
- `FISH_API_KEY` — Fish Audio key
- `DEEPGRAM_API_KEY` — Deepgram key
- `TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN` — Twilio credentials
- `TWILIO_PHONE_NUMBER` — Real Twilio number (+19129129545)
- `NATHAN_REAL_PHONE` — Nathan's personal number (+13107798590)

## Execution Steps

```bash
# 1. Rotate all keys in their respective dashboards:
#    - https://console.groq.com → API Keys → Revoke + Create new
#    - https://platform.deepgram.com → API Keys → Revoke + Create new
#    - https://console.twilio.com → Account → Auth Tokens → Rotate
#    - Fish Audio dashboard → Regenerate key

# 2. Remove file from git history
cd /data/workspace/projects/Ultrafone
git filter-repo --path backend/.env.development --invert-paths --force

# 3. Add to .gitignore
echo "backend/.env.development" >> .gitignore
echo "backend/.env.production" >> .gitignore

# 4. Store new secrets in Railway env vars
railway variables set GROQ_API_KEY=<new_key> ...

# 5. Update .env.example with placeholder values only
```

## Acceptance Criteria
- [ ] All listed API keys rotated in their respective dashboards
- [ ] `backend/.env.development` removed from git history
- [ ] File added to `.gitignore`
- [ ] New secrets stored in Railway env vars (not files)
- [ ] `.env.example` updated with placeholder format
