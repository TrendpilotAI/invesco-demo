# TODO 523: Comprehensive Test Suite
**Repo:** Second-Opinion  
**Priority:** P2 — Quality  
**Effort:** 2 days  
**Status:** pending

## Description
Second-Opinion has vitest + playwright configured but minimal test coverage. Services layer (AI calls, encryption, FHIR) and critical hooks are untested.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/tests/:

1. Unit tests (vitest):
   - services/geminiService.test.ts — mock Gemini API calls, test error handling
   - services/encryption.test.ts — test encrypt/decrypt roundtrip
   - services/fhir.test.ts — test FHIR JSON structure output
   - hooks/useAnalysisPipeline.test.ts — test state transitions
   - utils/validation.test.ts — test all validation functions

2. Integration tests (vitest + Firebase Emulator):
   - integration/pipeline.test.ts — full pipeline with emulated Firestore
   - integration/auth.test.ts — auth flow with emulated Firebase Auth

3. E2E tests (playwright):
   - e2e/auth-flow.spec.ts — sign up, sign in, sign out
   - e2e/upload-analyze.spec.ts — upload file → run analysis → see results
   - e2e/demo-mode.spec.ts — guided demo flow completes without errors

4. Update vitest.config.ts to include coverage thresholds (>60% for services/)
5. Update CI workflow to run tests on every PR
```

## Acceptance Criteria
- [ ] >60% coverage on services/ directory
- [ ] All hooks tested with React Testing Library
- [ ] E2E: auth + upload + analysis flows covered
- [ ] CI fails PR if coverage drops below threshold
- [ ] Tests run in <2 minutes

## Dependencies
None
