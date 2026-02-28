# TODO-315: Add E2E Playwright Tests for Critical User Flows

**Repo:** signal-studio
**Priority:** P2
**Effort:** L (2-3 days)
**Status:** pending

## Description
Playwright config exists (playwright.config.ts) but only smoke tests are present.
Critical user flows have zero E2E coverage. Must add tests for all primary paths.

## Acceptance Criteria
- 5+ E2E test suites covering critical flows
- All tests pass in CI (pnpm test:e2e)
- Tests added to bitbucket-pipelines.yml
- Tests use page object model pattern for maintainability

## Flows to Cover
1. **Auth flow**: Login page → valid credentials → redirect to signal library
2. **Signal library**: Browse signals, search, filter by category
3. **AI chat**: Open chat, send message, receive AI response
4. **Visual builder**: Open builder, add nodes, connect edges
5. **Oracle connect**: Enter connection string, browse tables
6. **Templates**: Browse templates gallery, apply template

## Coding Prompt
```
1. Review existing playwright config:
   cat /data/workspace/projects/signal-studio/playwright.config.ts
   ls /data/workspace/projects/signal-studio/tests/

2. Create tests/e2e/ directory structure:
   tests/e2e/auth.spec.ts
   tests/e2e/signal-library.spec.ts  
   tests/e2e/ai-chat.spec.ts
   tests/e2e/visual-builder.spec.ts
   tests/e2e/templates.spec.ts

3. Create tests/e2e/helpers/auth.ts for login helper:
   export async function loginAs(page, email, password) {
     await page.goto('/login')
     await page.fill('[name=email]', email)
     await page.fill('[name=password]', password)
     await page.click('[type=submit]')
     await page.waitForURL('**/signal-library')
   }

4. Use test fixtures from .env.test for credentials
5. Mock external APIs (Oracle, AI) in test mode using route interception

6. Add to bitbucket-pipelines.yml:
   - step:
       name: E2E Tests
       script:
         - pnpm test:e2e --reporter=list
```

## Dependencies
- TODO-314 (signal execution) should be done first for full flow tests
- Test credentials must be in Railway staging env

## Notes
AUDIT.md TEST-001, PLAN.md Sprint 3
