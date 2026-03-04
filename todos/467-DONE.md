# TODO-467 — npm publish pipeline + publishConfig ✅

**Completed:** 2026-03-04  
**Package:** `@forwardlane/signal-studio-templates`  
**Repo:** TrendpilotAI/signal-studio-templates  
**Commit:** `7d35e16` — pushed to main

---

## Changes Made

### 1. `package.json` — Added `publishConfig`
```json
"publishConfig": {
  "registry": "https://npm.forwardlane.com",
  "access": "restricted"
}
```
Package name was already correct: `@forwardlane/signal-studio-templates`

### 2. `.npmrc` — Created (new file)
```
//npm.forwardlane.com/:_authToken=${NPM_TOKEN}
@forwardlane:registry=https://npm.forwardlane.com
```

### 3. `.github/workflows/ci.yml` — Created (new file)
- **Triggers:** push to `main`, pull requests, tags matching `v*`
- **Steps:** checkout → pnpm install → typecheck → lint → test → build
- **On tag push only:** `pnpm publish --no-git-checks` using `secrets.NPM_TOKEN`

### 4. Build Verified
- Ran `pnpm build` — success (tsc compiled cleanly)
- `dist/` confirmed populated: index.js, index.d.ts, api/, components/, engine/, schema/, templates/, utils/

### 5. `README.md` — Added Installation section
- npm/pnpm install instructions with registry config
- Note about requiring NPM_TOKEN for private registry access

---

## Next Steps
- Add `NPM_TOKEN` secret to GitHub repo settings (Settings → Secrets → Actions)
- Tag a release (`git tag v1.0.0 && git push --tags`) to trigger first publish
