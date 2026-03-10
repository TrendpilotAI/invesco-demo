# TODO-881: Pin Wildcard Genkit Dependencies

**Repo**: NarrativeReactor  
**Priority**: P0 — Stability  
**Effort**: 30 minutes  
**Status**: Pending  

## Problem

6 packages in `package.json` use wildcard `*` versions:

```json
"genkit": "*",
"@genkit-ai/dotprompt": "*",
"@genkit-ai/express": "^1.27.0",
"@genkit-ai/firebase": "*",
"@genkit-ai/google-genai": "*",
"@genkit-ai/vertexai": "*",
"genkitx-anthropic": "*",
```

Any `npm install` (or CI cache miss) could pull in breaking major versions.

## Solution

```bash
# Run in /data/workspace/projects/NarrativeReactor/
cd /data/workspace/projects/NarrativeReactor
node -e "
const deps = require('./node_modules/genkit/package.json');
console.log('genkit:', deps.version);
"
# Repeat for each package, then pin to exact versions in package.json
```

Or simply:
```bash
npm ls genkit @genkit-ai/dotprompt @genkit-ai/firebase @genkit-ai/google-genai @genkit-ai/vertexai genkitx-anthropic 2>&1 | grep -v "^npm" | head -20
```

Then update package.json to use `^X.Y.Z` (minor-safe) instead of `*`.

## Files to Change

- `package.json` — pin all 6 wildcard genkit deps to current installed versions

## Acceptance Criteria

- [ ] No `*` wildcard versions in package.json
- [ ] All genkit deps use `^X.Y.Z` semver ranges
- [ ] `npm ci` still succeeds in CI
- [ ] Tests still passing
