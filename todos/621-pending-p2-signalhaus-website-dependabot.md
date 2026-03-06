# TODO 621 — Dependabot Configuration

**Repo:** signalhaus-website
**Priority:** P2
**Effort:** XS (15 minutes)
**Status:** pending

## Task
Add `.github/dependabot.yml` for automated dependency updates.

## Coding Prompt
```
Create /data/workspace/projects/signalhaus-website/.github/dependabot.yml:

version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
    labels:
      - "dependencies"

Also add tsconfig.tsbuildinfo to .gitignore if not already present.

Run: npm audit
Fix any high/critical CVEs.
```

## Acceptance Criteria
- [ ] `.github/dependabot.yml` committed
- [ ] `tsconfig.tsbuildinfo` in `.gitignore`
- [ ] `npm audit` shows no high/critical issues
