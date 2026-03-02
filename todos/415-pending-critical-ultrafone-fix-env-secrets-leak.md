# TODO 415: Fix .env.development Secrets Leak

**Repo:** Ultrafone  
**Priority:** Critical  
**Effort:** XS (30 min)  
**Dependencies:** None

## Description
`backend/.env.development` appears to be committed to the repo and may contain real API keys (Groq, Deepgram, Fish Audio, Supabase, Twilio). This is a critical security vulnerability.

## Coding Prompt
```
1. Check git log for backend/.env.development to see if it was ever committed with real secrets
2. If real secrets found: rotate ALL affected API keys immediately (Groq, Deepgram, Fish Audio, Twilio, Supabase)
3. Add backend/.env.development and backend/.env to .gitignore (if not already)
4. Use git-filter-repo or BFG to purge secrets from git history
5. Set up Railway environment variables instead of local .env files
6. Update DEVELOPER.md to document the proper secrets management approach
```

## Acceptance Criteria
- No real API keys in git history
- .env files properly gitignored
- All secrets rotated if previously exposed
- CI/CD uses Railway environment variables
