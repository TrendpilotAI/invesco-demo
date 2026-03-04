# TODO-571: GitHub Actions CI/CD Pipeline — forwardlane_advisor

**Repo:** forwardlane_advisor  
**Priority:** P1  
**Status:** pending

## Description
No CI/CD pipeline exists. Add GitHub Actions for automated testing and deployment.

## Steps
1. Create `.github/workflows/ci.yml`: run `npm run lint` + `npm test` on every PR
2. Create `.github/workflows/deploy.yml`: Docker build + push on merge to main
3. Add `dependabot.yml` for automated dependency updates
4. Add `.github/PULL_REQUEST_TEMPLATE.md`

## Acceptance Criteria
- PRs show green CI status check
- Failing tests block merge
- Merges to main trigger Docker build

## Dependencies
TODO-570 (unit tests must exist for CI to be useful)
