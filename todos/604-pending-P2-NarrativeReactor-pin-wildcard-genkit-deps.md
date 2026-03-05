# TODO-604: Pin Wildcard Genkit Dependencies — NarrativeReactor

**Priority:** P2 (Reliability)
**Repo:** NarrativeReactor
**Effort:** 30 minutes
**Dependencies:** None

## Problem
Multiple genkit packages use `*` (wildcard) version in package.json. This means any install could pull breaking changes without warning.

## Task
Pin all wildcard genkit dependencies to their current installed versions.

## Acceptance Criteria
- [ ] No `*` versions in package.json dependencies
- [ ] All genkit packages pinned to exact or caret versions
- [ ] `npm install` produces no version changes
- [ ] All tests still pass

## Agent Prompt
```
In /data/workspace/projects/NarrativeReactor:
1. Run: cat node_modules/genkit/package.json | grep '"version"'
2. Run same for: @genkit-ai/dotprompt, @genkit-ai/firebase, @genkit-ai/google-genai, @genkit-ai/vertexai, genkitx-anthropic
3. Update package.json replacing * with ^{actual_version} for each
4. Run: npm install to lock versions
5. Run: npm test to verify all pass
6. Commit: "chore: pin wildcard genkit deps to current versions"
```
