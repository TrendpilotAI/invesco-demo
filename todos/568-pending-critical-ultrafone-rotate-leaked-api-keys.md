# TODO 568 — CRITICAL: Rotate Leaked API Keys in Ultrafone

**Priority:** CRITICAL  
**Repo:** Ultrafone  
**Effort:** 1-2 hours  
**Status:** pending

## Description
Real API credentials are committed in `backend/.env.development` and likely in git history. All must be rotated immediately and the file removed from tracking.

## Affected Credentials
- `GROQ_API_KEY` — Groq (rotate at console.groq.com)
- `FISH_API_KEY` — Fish Audio (rotate at fish.audio)
- `DEEPGRAM_API_KEY` — Deepgram (rotate at console.deepgram.com)
- `TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN` — Twilio (rotate at console.twilio.com)
- `TWILIO_PHONE_NUMBER` — Real phone number (note: can't change but document it)
- `NATHAN_REAL_PHONE` — Nathan's personal number

## Coding Prompt
```bash
# Step 1: Add to .gitignore
echo "backend/.env.development" >> /data/workspace/projects/Ultrafone/.gitignore
echo "backend/.env" >> /data/workspace/projects/Ultrafone/.gitignore

# Step 2: Remove from git tracking
git -C /data/workspace/projects/Ultrafone rm --cached backend/.env.development

# Step 3: Remove from history (DESTRUCTIVE — do after rotating keys)
# cd /data/workspace/projects/Ultrafone
# git filter-repo --path backend/.env.development --invert-paths

# Step 4: Add gitleaks pre-commit hook
cat > /data/workspace/projects/Ultrafone/.pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
EOF

# Step 5: Move secrets to Railway env vars
# Log into railway.app → project → Variables → add all from .env.development
```

## Acceptance Criteria
- [ ] All listed keys rotated at their respective consoles
- [ ] `backend/.env.development` removed from git tracking
- [ ] File added to `.gitignore`
- [ ] gitleaks pre-commit hook installed
- [ ] Secrets moved to Railway environment variables

## Dependencies
None — do this first before anything else
