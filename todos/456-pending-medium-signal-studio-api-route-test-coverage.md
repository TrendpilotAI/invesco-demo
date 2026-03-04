# TODO-456: Add test coverage for uncovered API routes in Signal Studio

**Repo:** signal-studio  
**Priority:** medium  
**Effort:** M  
**Date:** 2026-03-04  

## Problem

`/app/api/` has 17 route groups. Jest tests cover only ~6. Critical uncovered routes:
- `/api/visual-builder/chat/route.ts` — LLM call, no test
- `/api/data-pipeline/` — new, no test  
- `/api/agent-history/` — new, no test
- `/api/oml/` — Oracle ML routes, no test
- `/api/semantic/` — vector search, no test

## Task

Add Jest unit tests for the top 5 highest-risk uncovered API routes.

## Coding Prompt

```
In /data/workspace/projects/signal-studio/__tests__/api/, create test files for:
1. visual-builder-chat.test.ts — mock LLM call, assert streaming response format
2. data-pipeline.test.ts — mock DB, test CRUD operations
3. agent-history.test.ts — test list/get agent run history
4. semantic-search.test.ts — mock Oracle vector store, test embedding call
5. oml.test.ts — mock Oracle ML, test model inference route

Use existing patterns from __tests__/lib/oracle-services.test.ts for Oracle mocks.
Use existing patterns from __tests__/lib/chat-service.test.ts for LLM mocks.
Each test file should:
- Mock all external dependencies (Oracle, OpenAI, Anthropic)
- Test happy path + error cases
- Assert correct HTTP status codes and response shapes
- Use existing test-helpers from __tests__/utils/
```

## Acceptance Criteria
- [ ] 5 new test files created
- [ ] All tests pass in CI (`pnpm test:api`)
- [ ] Coverage for targeted routes ≥80%
