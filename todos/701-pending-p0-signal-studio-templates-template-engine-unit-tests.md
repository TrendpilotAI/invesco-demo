---
id: 701
status: pending
repo: signal-studio-templates
priority: P0
effort: M
created: 2026-03-10
---

# TODO 701 — Template Engine Unit Tests (Core Path Untested)

**Repo:** signal-studio-templates  
**Priority:** P0 — Core execution path completely untested  
**Effort:** M (1 day)

## Problem

`engine/template-engine.ts` has ZERO unit tests. This is the critical execution path for the entire library. Tests pass because only peripheral code (SQL utils, mock data provider, API middleware) is tested. The most important code is untested.

Current coverage estimate: ~35%. Target: 70%+

## Solution

Add comprehensive unit tests for TemplateEngine using MockDataProvider and MockAIProvider.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates:

Create __tests__/engine/template-engine.test.ts with the following test suites:

1. getTemplates() tests:
   - Returns all 20 templates when no filters applied
   - Filters by category (meeting-prep, sales-intelligence, etc.)
   - Filters by id (single template lookup)
   - Returns empty array for unknown category
   - ALL_TEMPLATES matches TEMPLATES_BY_ID.size

2. validate() tests:
   - Valid template with required params → no errors
   - Missing required parameter → returns ValidationError with field name
   - Invalid parameter type → returns ValidationError
   - Missing required data source → returns ValidationError (mock availableDataSources to exclude a source)
   - All 20 templates validate with their own defaultConfig

3. execute() tests:
   - Basic execution returns ExecutionResult with expected shape
   - executionTimeMs is a positive number
   - rows matches mock data provider output
   - templateId and templateName in result match template
   - includeTalkingPoints: false skips aiProvider call
   - includeTalkingPoints: true calls aiProvider.generateTalkingPoints
   - Missing required parameter throws/rejects with descriptive error
   - Unknown templateId throws/rejects with "not found" error
   - sql field is NOT present in result (security requirement per TODO-636)

4. customize() tests:
   - Returns customized template with updated defaultConfig
   - Customization does not mutate original template
   - Invalid override field is rejected or ignored per schema

5. Error handling:
   - dataProvider.executeSQL() rejects → execute() propagates error
   - aiProvider.generateTalkingPoints() rejects → execute() still returns rows (talkingPoints undefined)

Use MockDataProvider and MockAIProvider from engine/ for all tests.
For data source tests, create a TestDataProvider that extends MockDataProvider with controllable availableDataSources().

Run pnpm test to verify all tests pass after implementation.
```

## Files

- `__tests__/engine/template-engine.test.ts` (new)

## Acceptance Criteria

- Coverage for engine/template-engine.ts: 80%+
- All 5 test suites pass
- No test imports from `dist/` — all imports from source TypeScript
- Tests run in under 5 seconds (no network calls)

## Dependencies

- Unblocks: test coverage threshold enforcement in CI
- See also: TODO-102 (original engine tests TODO)
