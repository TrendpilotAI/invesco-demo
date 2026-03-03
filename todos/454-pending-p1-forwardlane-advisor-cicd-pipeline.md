# TODO 454 — forwardlane_advisor: CI/CD Pipeline

**Priority:** P1 | **Effort:** M | **Repo:** forwardlane_advisor

## Description
No CI/CD configuration exists. Add GitHub Actions for automated testing and deployment.

## Full Coding Prompt
```
Add CI/CD pipeline for forwardlane_advisor using GitHub Actions.

Create .github/workflows/ci.yml:
- Trigger: push to main, PR to main
- Jobs:
  1. lint: npm run lint (add ESLint config first)
  2. test: npm test (existing mocha tests)
  3. security: npm audit --audit-level=high
  4. docker: build Docker image, push to registry

Create .github/workflows/deploy.yml:
- Trigger: push to main (after CI passes)
- Deploy to staging environment
- Add manual approval for production deploy

Also add:
1. .eslintrc.js with sensible Node.js rules
2. .prettierrc for code formatting
3. Update package.json scripts:
   - "lint": "eslint . --ext .js"
   - "lint:fix": "eslint . --ext .js --fix"
4. Add docker-compose.yml for local development:
   - Services: app, mysql, rabbitmq
   - Use environment variables from .env

Document setup in DEVELOPMENT.md
```

## Acceptance Criteria
- [ ] GitHub Actions CI runs on every PR
- [ ] Tests must pass before merge
- [ ] Docker image builds successfully in CI
- [ ] docker-compose up works for local dev
- [ ] ESLint passes with no errors

## Dependencies
- TODO 451

## Estimated Effort
2-3 days
