# 228 · NarrativeReactor · Test Coverage Expansion

**Status:** pending  
**Priority:** high  
**Project:** NarrativeReactor  
**Created:** 2026-02-27

---

## Task Description

Current tests cover 4 flows and 2 services. 26+ services are untested. Expand vitest coverage to hit 70%+ overall, focusing on high-risk services: contentPipeline, tts, videoStitcher, captionGenerator, costTracker, and the approval workflow.

---

## Coding Prompt (agent-executable)

```
Working in /data/workspace/projects/NarrativeReactor/src/__tests__/services/:

0. First run: npm run test:coverage to see current baseline coverage report.

1. Create comprehensive test files for each service using vitest + vi.mock():

a. contentPipeline.test.ts (if not exists/incomplete):
   - Mock LLM calls (vi.mock Genkit flows)
   - Test: pipeline creation, step execution, error handling, retry logic
   - Test: pipeline state persistence

b. tts.test.ts:
   - Mock ElevenLabs/Fish Audio API (vi.mock fetch)
   - Test: text-to-speech generation, voice selection, audio format output
   - Test: long text chunking behavior

c. videoStitcher.test.ts:
   - Mock ffmpeg subprocess
   - Test: clip ordering, transition application, output path generation
   - Test: error on missing input files

d. captionGenerator.test.ts:
   - Mock LLM response
   - Test: caption length limits, hashtag injection, emoji mode
   - Test: platform-specific formatting (Twitter vs Instagram vs LinkedIn)

e. costTracker.test.ts:
   - Test: token counting accuracy
   - Test: cost accumulation across multiple calls
   - Test: getCostSummary() returns correct totals
   - Test: cost limits trigger warnings

f. approvalWorkflow.test.ts:
   - Test: workflow state transitions (pending → approved → published)
   - Test: rejection flow
   - Test: timeout handling

2. Update vitest.config.ts coverage thresholds:
   coverage: { thresholds: { lines: 70, functions: 70, branches: 65 } }

3. Add test fixtures in src/__tests__/fixtures/:
   - mockBrandProfile.ts
   - mockLLMResponse.ts  
   - mockVideoClip.ts
```

---

## Dependencies

- 224 (auth improvements — auth tests needed first)

## Effort Estimate

8–10 hours

## Acceptance Criteria

- [ ] `npm run test:coverage` shows > 70% line coverage
- [ ] All 6 new service test files created and passing
- [ ] No flaky tests (run 3x in CI)
- [ ] Coverage thresholds enforced in vitest config
- [ ] Test run completes in < 2 minutes
