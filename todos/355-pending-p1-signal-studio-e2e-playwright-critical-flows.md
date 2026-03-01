# TODO-355: Add E2E Playwright Tests for Critical User Flows

**Priority:** P1
**Effort:** L
**Repo:** signal-studio
**Status:** pending

## Description
Playwright config exists but only smoke tests present. Critical flows untested: auth login, signal library CRUD, AI chat, visual builder, Oracle connection.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Review existing tests: ls __tests__/ and cat playwright.config.ts

2. Create e2e/auth.spec.ts:
   - Test: user can login with valid credentials
   - Test: invalid credentials shows error
   - Test: unauthenticated user redirected to login
   - Test: logout works

3. Create e2e/signal-library.spec.ts:
   - Test: authenticated user can view signal library
   - Test: user can filter signals by category
   - Test: user can search signals
   - Test: user can view signal details

4. Create e2e/ai-chat.spec.ts:
   - Test: AI chat panel opens
   - Test: user can send message, receives response
   - Test: streaming response displays correctly
   - Test: Oracle query via chat returns results

5. Create e2e/visual-builder.spec.ts:
   - Test: visual builder page loads
   - Test: can drag node from sidebar to canvas
   - Test: can connect two nodes
   - Test: properties panel shows for selected node

6. Create e2e/templates.spec.ts:
   - Test: templates gallery loads (20 templates visible)
   - Test: search/filter works
   - Test: template can be viewed/cloned

7. Add to package.json scripts if not present:
   "test:e2e:critical": "playwright test e2e/"

8. Commit: "test(e2e): add Playwright tests for 5 critical user flows"
```

## Dependencies
None (can run against local dev server)

## Acceptance Criteria
- 5 E2E test files in e2e/
- All tests pass against local dev server
- CI pipeline runs E2E tests
- Auth, signal library, AI chat, visual builder, templates all covered
