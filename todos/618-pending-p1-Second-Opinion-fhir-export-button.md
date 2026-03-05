# TODO 618 — Second-Opinion: Wire FHIR Export Button
**Priority**: P1 | **Effort**: 4h | **Repo**: Second-Opinion

## Description
services/fhir.ts exists and produces valid FHIR R4 JSON. Wire it to a UI button in the analysis results view for one-click export. This is an enterprise signal for clinic partnerships.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/:

1. Read services/fhir.ts to understand the export function signature
2. Add "Export as FHIR R4" button to components/AnalysisDashboard.tsx
   - Button should call the FHIR service with the current case data
   - Trigger browser download of the FHIR JSON bundle
   - Show success toast "FHIR R4 bundle downloaded"
3. Add a FHIR badge/indicator to show the platform is FHIR-compliant
4. Ensure the export includes: Patient resource, DiagnosticReport, Observation, DocumentReference
5. Add unit test in tests/unit/services/fhir.test.ts verifying valid FHIR output structure

TypeScript only. No new dependencies.
```

## Acceptance Criteria
- [ ] FHIR export button visible in analysis results
- [ ] Downloads valid FHIR R4 JSON bundle
- [ ] Unit test passes validating bundle structure
- [ ] Works in production (Firebase deployed)

## Dependencies
- services/fhir.ts (already exists)
- TODO 519 (Stripe) not required — this is free tier feature
