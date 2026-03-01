# 356 · NarrativeReactor — Lock Test Coverage at 70% Threshold

**Priority:** high  
**Effort:** S (< 1 day)  
**Repo:** /data/workspace/projects/NarrativeReactor/

---

## Task Description

Enforce a minimum 70% line/function coverage threshold in `vitest.config.ts` so CI fails if coverage regresses. Verify current coverage, identify gaps, and add targeted tests to reach the threshold.

---

## Coding Prompt (agent-executable)

```
In /data/workspace/projects/NarrativeReactor/:

1. Run current coverage to baseline:
   npm test -- --run --coverage 2>&1 | tail -30

2. Open vitest.config.ts. Add/update the coverage section:

   coverage: {
     provider: 'v8',
     reporter: ['text', 'lcov', 'html'],
     exclude: ['node_modules/**', 'dist/**', 'tests/**', '**/*.config.ts'],
     thresholds: {
       lines: 70,
       functions: 70,
       branches: 60,
       statements: 70
     }
   }

3. Run npm test -- --run --coverage again.

4. If thresholds fail, identify uncovered files from output. 
   For each file below threshold, add tests in tests/unit/{serviceName}.test.ts:
   - blotatoPublisher: mock fetch, test publish() success and retry
   - brandVoice: test scoreContent() with fixture input
   - campaigns: test createCampaign(), getCampaign(), listCampaigns()
   - costTracker: test recordCost(), getTotalCost()
   
   Focus on the highest-LOC services first.

5. Commit vitest.config.ts change first (threshold enforcement).
   Then commit test files separately.

6. Verify: npm test -- --run --coverage exits 0.
```

---

## Dependencies

- #355 (supertest E2E tests) — adds to coverage total
- Tests already at 287 (good baseline)

## Acceptance Criteria

- [ ] `vitest.config.ts` has `thresholds: { lines: 70, functions: 70 }`
- [ ] `npm test -- --run --coverage` exits 0
- [ ] Coverage report shows ≥ 70% lines and functions
- [ ] CI fails if new code drops coverage below threshold
