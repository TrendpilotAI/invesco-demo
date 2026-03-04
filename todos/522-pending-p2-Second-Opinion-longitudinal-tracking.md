# TODO 522: Longitudinal Case Tracking
**Repo:** Second-Opinion  
**Priority:** P2 — Retention  
**Effort:** 2 days  
**Status:** pending

## Description
Let users upload follow-up medical files and track condition progression over time. "Upload your follow-up X-ray — see how your condition evolved." Massive retention hook — users return monthly.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/:

1. Add `caseGroupId` field to Firestore cases collection (links related cases)
2. Create components/PatientTimeline.tsx enhancement:
   - Timeline view of all cases for a patient grouped by condition
   - Each timeline entry shows: date, key finding, confidence score
   - "Compare" button between any two cases
3. Create components/DeltaAnalysis.tsx:
   - Side-by-side diff of two analysis outputs
   - Calls a new Cloud Function `compareAnalyses`
4. Add functions/src/comparison.ts:
   - compareAnalyses(caseId1, caseId2) Cloud Function
   - Uses Gemini to generate: "Changes since last analysis: ..."
   - Returns structured delta: { improved, worsened, unchanged, newFindings }
5. Add "Add to existing case" option in FileUploader.tsx
```

## Acceptance Criteria
- [ ] Users can link a new upload to an existing case
- [ ] Timeline view shows progression
- [ ] Delta analysis highlights changes
- [ ] Exportable progression report (PDF-ready HTML)

## Dependencies
None
