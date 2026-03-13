# TODO: Rotate and Purge All Leaked API Keys from Git History

## Priority: P0 CRITICAL
## Repo: Ultrafone

### Problem
Real API keys committed to git history including Twilio auth tokens, Groq API keys, Deepgram API keys, Fish Audio keys, and personal phone numbers. These are LIVE CREDENTIALS that can be extracted by anyone with repo access.

### Action Items
1. IMMEDIATELY rotate all exposed keys in their respective dashboards:
   - Twilio: rotate account auth token
   - Groq: regenerate API key
   - Deepgram: regenerate API key
   - Fish Audio: regenerate API key
2. Use BFG Repo Cleaner or `git filter-branch` to purge secrets from git history
3. Force-push cleaned history to all remotes
4. Verify .env is in .gitignore
5. Add pre-commit hook with `detect-secrets` or `truffleHog`
6. Move all credentials to Railway environment variables

### Impact
- LIVE SECURITY INCIDENT: credentials are currently exposed
- Any rotation must happen before next deployment
- Cannot go to production without resolving this

### References
- SECRETS_ROTATION.md
- AUDIT.md critical section
- TODO-622, TODO-568, TODO-433, TODO-858, TODO-859
