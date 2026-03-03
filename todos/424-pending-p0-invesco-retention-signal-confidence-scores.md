# TODO #424: Add Signal Confidence Scores to Signal Cards

**Priority:** P0 (pre-demo)
**Effort:** XS (1 hour)
**Repo:** invesco-retention
**Source:** BRAINSTORM.md v3, Category 1.8

## Description

Add a confidence percentage + data source count to each signal card. Addresses the enterprise "how do you know this?" objection before it's raised.

Example: "87% confidence — based on 14 data points across 4 sources"

## Acceptance Criteria
- [ ] Each signal card shows a confidence score (%)
- [ ] Score is accompanied by "N data points across M sources" text
- [ ] Scores feel realistic and vary by signal type/severity
- [ ] Visual styling is subtle — doesn't overwhelm the signal headline

## Implementation Prompt

```
In /data/workspace/projects/invesco-retention/demo-app/src/lib/mock-data.ts:

1. Add `confidence: number` and `dataPointCount: number` and `sourceCount: number` to the Signal type
2. Assign realistic values:
   - urgent signals: 85-95% confidence, 12-18 data points, 4-5 sources
   - attention signals: 70-84% confidence, 8-12 data points, 3-4 sources
   - positive signals: 75-90% confidence, 10-15 data points, 3-5 sources
   - info signals: 60-75% confidence, 5-9 data points, 2-3 sources
3. In salesforce/page.tsx signal card rendering, add a small confidence badge:
   <span className="text-xs text-gray-400">{confidence}% confidence · {dataPointCount} data points</span>
4. Place below the signal description, above the action buttons
```

## Dependencies
- None

## Demo Impact
HIGH — Directly addresses enterprise AI explainability concern.
