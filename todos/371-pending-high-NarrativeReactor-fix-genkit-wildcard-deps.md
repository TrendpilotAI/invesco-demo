# 371 — Fix Wildcard Genkit Dependency Versions in package.json

## Task Description
`package.json` has multiple Genkit packages pinned to `"*"` (wildcard). This means `npm install` on a fresh machine or in CI may pull incompatible breaking versions. Pin to specific `^X.Y.Z` versions matching what's currently installed.

## Coding Prompt
You are working on the NarrativeReactor repo at `/data/workspace/projects/NarrativeReactor/`.

The following packages have wildcard versions in `package.json`:
- `genkit: "*"`
- `@genkit-ai/dotprompt: "*"`
- `@genkit-ai/firebase: "*"`
- `@genkit-ai/google-genai: "*"`
- `genkitx-anthropic: "*"`

Steps:
1. Run `cat package-lock.json | grep -A2 '"genkit"'` and similar for each package to find currently resolved versions
2. Or run `node -e "const l=require('./package-lock.json'); ['genkit','@genkit-ai/dotprompt','@genkit-ai/firebase','@genkit-ai/google-genai','genkitx-anthropic'].forEach(p => console.log(p, l.packages['node_modules/'+p]?.version))"` to extract all versions at once
3. Update `package.json` to replace `"*"` with `"^X.Y.Z"` for each (using caret range to allow patch updates)
4. Run `npm install` to regenerate lock file with pinned versions
5. Run `npm test` to confirm all tests still pass
6. Commit both `package.json` and the updated `package-lock.json`

Also check for any other `"*"` versions in dependencies/devDependencies and pin those too.

If `@genkit-ai/firebase` is not actually used in the codebase, remove it: `grep -rn "genkit-ai/firebase\|firebase-admin" src/` — if no results, remove from package.json.

## Dependencies
None

## Estimated Effort
S

## Acceptance Criteria
- [ ] No `"*"` versions remain in `package.json` dependencies or devDependencies
- [ ] All Genkit packages pinned to `^X.Y.Z` format
- [ ] `package-lock.json` committed with resolved versions
- [ ] `npm ci` succeeds in a clean environment
- [ ] All existing tests pass
- [ ] Unused dependencies removed (if any discovered)
