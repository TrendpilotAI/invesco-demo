# 228 · P1 · signal-builder-frontend · Fix .env Git Tracking & Dev Auth Security

## Status
pending

## Priority
P1 — Critical security: `.env` is tracked in git, dev auth credentials could leak

## Description
Two critical security issues found in the audit:
1. `.env` is committed to the repository (exposes QA URLs, risks future credential leaks)
2. Dev auth method sends plaintext credentials at runtime with no production guard

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

TASK 1: Remove .env from git tracking
1. Run: git rm --cached .env
2. Add `.env` and `.env.local` to `.gitignore` if not already present
3. Verify `.env.schema` and `.env.example` remain tracked (these should stay)
4. Create `.env.example` from `.env.schema` if it doesn't exist, with all values blanked

TASK 2: Guard dev auth method against production use
In `src/shared/lib/auth.ts`, find the `isDevAuthMethod` check:
  if (APP_CONFIG.isDevAuthMethod) { ... post credentials ... }

Add a guard BEFORE the dev auth block:
  if (APP_CONFIG.isDevAuthMethod && process.env.NODE_ENV === 'production') {
    throw new Error('[Security] Dev auth method must not be used in production builds. Set REACT_APP_IS_DEV_AUTH_METHOD=false.');
  }

TASK 3: Add CI build assertion
In `bitbucket-pipelines.yml`, before the build step for QA/Demo, add:
  - step:
      name: Security Assertions
      script:
        - if [ "$REACT_APP_IS_DEV_AUTH_METHOD" = "true" ] && [ "$NODE_ENV" = "production" ]; then echo "ERROR: Dev auth in prod!"; exit 1; fi

TASK 4: Fix auth.ts type safety
Change `const result: any` to `const result: { data: { token: string } }` in the dev auth login call.
Change `catch (error: any)` to `catch (error: unknown)` and narrow the type before accessing properties.

Commit with message: "security: remove .env from git, add prod guard for dev auth"
```

## Dependencies
- None (standalone security fix)

## Effort Estimate
S (2–4 hours)

## Acceptance Criteria
- [ ] `git ls-files .env` returns nothing (file not tracked)
- [ ] `.gitignore` contains `.env` and `.env.local`
- [ ] `auth.ts` throws if `isDevAuthMethod=true` in production build
- [ ] CI pipeline assertion fails if dev auth is set in prod environment
- [ ] TypeScript types improved in `auth.ts` (no `any` in catch block)
