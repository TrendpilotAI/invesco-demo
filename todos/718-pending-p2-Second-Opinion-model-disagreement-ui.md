# TODO 718: Model Disagreement Alert UI for Second-Opinion

**Repo**: Second-Opinion  
**Priority**: P2  
**Effort**: 6 hours  
**Status**: pending

## Description
Surface the ensemble voting disagreement data from `services/ensembleVoting.ts` in the UI. Show a prominent banner when models disagree, flagging for human review. Key responsible AI differentiator for enterprise buyers.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/:
1. Read services/ensembleVoting.ts to understand the disagreement data structure
2. In components/AnalysisDashboard.tsx, add a ModelDisagreementBanner component
3. Banner should show: "⚠️ Models disagree on [finding] — flagging for expert review"
4. Include a confidence meter showing the split (e.g., "2 of 3 models agree")
5. Add a "Request Human Review" CTA button that triggers the consultation flow
6. Style with amber/yellow warning colors (not red — informational, not error)
7. Add unit test in tests/unit/components/ModelDisagreementBanner.test.tsx
```

## Acceptance Criteria
- [ ] Banner appears when ensembleVoting detects disagreement
- [ ] Shows which models disagree and confidence split
- [ ] CTA links to consultation/review flow
- [ ] Hidden when models agree
- [ ] Unit test passes

## Dependencies
- services/ensembleVoting.ts (exists)
- TODO 521 (Provider Dashboard — for human review routing)
