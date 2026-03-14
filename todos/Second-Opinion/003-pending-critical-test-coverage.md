# TODO: Add Unit & Integration Tests (~15% → 70%+ Coverage)

- **Project:** Second-Opinion
- **Priority:** CRITICAL
- **Status:** pending
- **Category:** Testing
- **Effort:** L (1-2 weeks)
- **Created:** 2026-03-14

## Description
Current test coverage is estimated at ~10-15%. No unit tests exist for any of the 7 hooks or 43 components. Only E2E skeleton scripts exist (Puppeteer-based). Vitest is configured but unused.

## Action Items (Priority Order)
1. **`hooks/useAnalysisPipeline.test.ts`** — Core business logic, highest priority
2. **`hooks/useAuthLifecycle.test.ts`** — Auth state management
3. **`components/PatientChat.test.tsx`** — Main user interaction
4. **`components/AnalysisDashboard.test.tsx`** — Results display
5. **`components/FileUploader.test.tsx`** — File upload handling
6. **Firebase rules tests** — `firestore.rules.test.ts` (use emulator)
7. **Cloud Functions unit tests** — `functions/test/`
8. **Migrate E2E to Playwright** — Remove Puppeteer dependency
9. Add `--coverage` to CI with 70% threshold

## Current State
- Vitest configured in package.json with coverage support
- `@testing-library/react` and `@testing-library/jest-dom` installed
- `jsdom` installed for component testing
- Both Playwright and Puppeteer installed (consolidate to Playwright)
