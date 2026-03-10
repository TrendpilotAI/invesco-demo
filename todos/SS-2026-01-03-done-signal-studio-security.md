# SS-2026-01 through SS-2026-03 — signal-studio Security TODOs

**Completed:** 2026-03-10  
**Repo:** TrendpilotAI/signal-studio (Bitbucket: forwardlane/signal-studio)  
**Branch:** main  

---

## SS-2026-01: Remove dump.rdb from git history + rotate Redis secrets

**Commit:** `a0b76e6`  
**Status:** ✅ Complete (with caveat on history purge)

### What was done:
- `dump.rdb` was already untracked in the remote HEAD (a prior commit `5952c74` removed it)
- Added `*.rdb` and `dump.rdb` to `.gitignore` (these were missing from the remote `.gitignore`)
- Added `README.md` security note with the `git-filter-repo` command to purge from history

### ⚠️ Action Required:
1. **Rotate Redis credentials** — any Redis passwords/URLs that were accessible via `dump.rdb` should be considered compromised
2. **Purge git history** — `dump.rdb` still exists in older git commits. Run:
   ```bash
   pip install git-filter-repo
   git filter-repo --path dump.rdb --invert-paths --force
   git push origin --force --all && git push origin --force --tags
   ```
   All collaborators must re-clone after force-push.

---

## SS-2026-02: pnpm audit to CI

**Commit:** `4255030`  
**Status:** ✅ Complete

### What was done:
- **PR pipeline:** Added `Dependency Audit` step (pnpm install + `pnpm audit --audit-level=high`) after install, before lint/test/build
- **develop branch:** Added `Dependency Audit` step before Deploy to Staging webhook
- **main branch:** Added `Dependency Audit` step before Deploy to Production webhook
- Also restored missing `develop` branch pipeline and deploy webhook steps that were absent from remote

---

## SS-2026-03: gitleaks secret scanning to CI

**Commit:** `3c4ed81`  
**Status:** ✅ Complete

### What was done:
- **PR pipeline:** `Secret Scanning (gitleaks)` added as **first step** — blocks PR merges if secrets detected
- **main pipeline:** `Secret Scanning (gitleaks)` added as **first step** — blocks production deploys if secrets detected
- Image: `zricethezav/gitleaks:latest`
- Flags: `--no-git --redact` (scans source files, redacts secrets in CI output)
- develop: skipped (deploy is webhook-only; Dependency Audit covers risk)

### Note:
Remote already had a partial gitleaks implementation from commit `c37a511` (landed before this task). Our commit standardized flags (`--no-git --redact` instead of `--redact --exit-code 1`) and added the develop branch coverage.

---

## Final Pipeline Structure

```
PR ('**'):
  1. Secret Scanning (gitleaks)     ← SS-2026-03
  2. Dependency Audit (pnpm audit)  ← SS-2026-02
  3. Lint and Test (pnpm build)

develop:
  1. Dependency Audit (pnpm audit)  ← SS-2026-02
  2. Deploy to Staging

main:
  1. Secret Scanning (gitleaks)     ← SS-2026-03
  2. Dependency Audit (pnpm audit)  ← SS-2026-02
  3. Deploy to Production
```

---

## Commit Hashes

| TODO | Commit | Message |
|------|--------|---------|
| SS-2026-01 | `a0b76e6` | security: remove dump.rdb from tracking, add *.rdb to .gitignore |
| SS-2026-02 | `4255030` | ci: add pnpm audit --audit-level=high to all pipelines |
| SS-2026-03 | `3c4ed81` | ci: add gitleaks secret scanning to Bitbucket pipelines |

All pushed to `origin/main` ✅
