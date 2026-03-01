# 369 — Add GitHub Actions CI Pipeline

## Task Description
Create a `.github/workflows/ci.yml` pipeline that runs on every PR and push to main. The pipeline should typecheck, lint, run tests with coverage, and validate the Docker build. Currently nothing prevents broken code from merging.

## Coding Prompt
You are working on the NarrativeReactor repo at `/data/workspace/projects/NarrativeReactor/`.

Create `.github/workflows/ci.yml` with the following jobs:

1. **typecheck** — `npx tsc --noEmit`
2. **lint** — `npm run lint` (if lint script exists; if not, add ESLint config first)
3. **test** — `npm run test:ci` with coverage; fail if coverage < 70% lines
4. **docker-build** — `docker build .` (no push, just validate build succeeds)

Requirements:
- Trigger on: `push` to `main`, `pull_request` to `main`
- Use Node.js 20 (match Dockerfile)
- Cache `node_modules` via `actions/cache` keyed on `package-lock.json` hash
- Use `actions/checkout@v4` and `actions/setup-node@v4`
- Jobs should run in parallel where possible (typecheck + lint + test independent; docker-build after test passes)
- Add status badge to `README.md`

Check `package.json` for existing scripts and match them. Inspect `vitest.config.ts` for coverage config.

Also verify `vitest.config.ts` has coverage thresholds set:
```ts
coverage: {
  thresholds: { lines: 70, functions: 70, branches: 60 }
}
```
Add them if missing.

## Dependencies
None

## Estimated Effort
S

## Acceptance Criteria
- [ ] `.github/workflows/ci.yml` exists and is valid YAML
- [ ] `tsc --noEmit` runs in CI
- [ ] Tests run with coverage in CI
- [ ] Pipeline fails if coverage drops below 70% lines
- [ ] Docker build is validated
- [ ] README has CI status badge
- [ ] Branch protection can be configured to require this check
