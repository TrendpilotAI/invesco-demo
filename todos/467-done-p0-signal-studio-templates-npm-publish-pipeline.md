# TODO-467: Publish @forwardlane/signal-studio-templates to npm Registry

**Repo:** signal-studio-templates
**Priority:** P0
**Effort:** S (2h)
**Status:** pending
**Source:** judge-agent-v2 / BRAINSTORM.md

## Description

The library is complete but never published. ForwardLane Signal Studio frontend and backend cannot consume it via npm install. This blocks integration.

## Acceptance Criteria

- [ ] `publishConfig` added to `package.json` pointing to ForwardLane private registry
- [ ] `.npmrc` configured with registry URL (token via env var `NPM_TOKEN`)
- [ ] `pnpm build && pnpm publish` works end-to-end
- [ ] `.github/workflows/ci.yml` publishes on `v*` tag push
- [ ] Package importable as `import { TemplateEngine } from '@forwardlane/signal-studio-templates'`

## Agent Prompt

```
In /data/workspace/projects/signal-studio-templates/:

1. Update package.json — add:
   "publishConfig": {
     "registry": "https://npm.forwardlane.com",
     "access": "restricted"
   }

2. Create .npmrc:
   //npm.forwardlane.com/:_authToken=${NPM_TOKEN}
   @forwardlane:registry=https://npm.forwardlane.com

3. If .github/workflows/ci.yml doesn't exist, create it:
   - Trigger: push to main + pull_request + tags matching v*
   - Steps: checkout, pnpm install, typecheck, lint, test, build
   - On tag push only: pnpm publish --no-git-checks
   - Secrets: NPM_TOKEN

4. Run: pnpm build && verify dist/ is populated correctly

5. Update README with: npm install @forwardlane/signal-studio-templates
```

## Dependencies

- TODO-428 (CI/CD) — can be merged into same PR
