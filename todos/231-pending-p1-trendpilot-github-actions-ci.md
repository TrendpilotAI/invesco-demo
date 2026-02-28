# TODO: Trendpilot — GitHub Actions CI Pipeline

**Priority:** P1 — Engineering hygiene blocker  
**Repo:** /data/workspace/projects/Trendpilot/  
**Effort:** 0.5-1 day  
**Dependencies:** None

## Description
Trendpilot has 423 tests and TypeScript strict mode but ZERO CI pipeline. Every push is unvalidated. Add GitHub Actions for test + lint + type-check + Railway deploy.

## Coding Prompt (Autonomous Execution)
```
Create .github/workflows/ci.yml in /data/workspace/projects/Trendpilot/:

Jobs:
1. test:
   - Node 22
   - npm ci
   - npm run build:server (tsc type check)
   - NODE_ENV=test npm test
   - Upload coverage report

2. lint:
   - Install eslint + @typescript-eslint (if not present)
   - Run eslint src/ dashboard/src/
   - Add .eslintrc.json if missing

3. deploy (on main branch merge only):
   - Trigger Railway deployment via RAILWAY_TOKEN
   - Use railway CLI: railway up --service trendpilot

Add secrets to GitHub repo:
- RAILWAY_TOKEN
- SUPABASE_URL (test env)
- SUPABASE_ANON_KEY (test env)

Also add .eslintrc.json if missing, and ensure tsconfig strict mode is enforced in CI.
```

## Acceptance Criteria
- [ ] CI runs on every PR
- [ ] Type errors block merge
- [ ] Test failures block merge
- [ ] Deploy triggers automatically on main branch
- [ ] Badge added to README.md
