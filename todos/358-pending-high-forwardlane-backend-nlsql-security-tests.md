# TODO 358: NL→SQL Security & Edge Case Test Suite

**Repo:** forwardlane-backend  
**Priority:** HIGH  
**Effort:** M (3-5 hours)  
**Dependencies:** 355 (shared LLM client)

## Description

The `NLQueryView` and `_clean_sql()` method are security-critical — they accept user input, send it to an LLM, and execute the result as SQL against the analytical database. Coverage of edge cases and adversarial inputs is essential before wider Invesco rollout.

## Coding Prompt

```
You are working in /data/workspace/projects/forwardlane-backend/easy_button/tests/.

Task: Write comprehensive security and edge case tests for the NL→SQL pipeline.

Create file: easy_button/tests/test_nlsql_security.py

Test cases to cover:

1. _clean_sql() direct tests:
   - Valid SELECT passes through cleanly
   - SQL with markdown fences is stripped correctly  
   - Non-SELECT statement raises ValueError
   - UPDATE/INSERT/DELETE/DROP raises ValueError
   - Dangerous functions blocked: pg_read_file, pg_sleep, dblink, information_schema
   - Missing LIMIT gets one appended
   - Semicolons are stripped
   - Comments (--) are stripped
   - UNSUPPORTED returned as-is (not executed)

2. Prompt injection tests (mock LLM):
   - LLM returns "DROP TABLE advisors" → should be blocked by _clean_sql
   - LLM returns UPDATE statement → should be blocked
   - LLM returns SELECT with pg_sleep → should be blocked
   - LLM returns valid SELECT → should pass

3. Quick pattern matcher tests:
   - "show me at-risk advisors" → matches at-risk pattern
   - "growing advisors" → matches growth pattern  
   - "top AUM" → matches biggest pattern
   - "Invesco holdings" → matches invesco pattern
   - "completely unrelated query" → returns None (falls through to LLM)

4. API endpoint tests (use DRF APIClient):
   - Empty query returns 400
   - Valid question returns results dict with question/sql/columns/rows/count
   - Question that returns UNSUPPORTED returns helpful error message
   - Rate limiting: 11th request in 1 minute returns 429

Use pytest-django fixtures. Mock LLM calls with unittest.mock.patch.

Run: pytest easy_button/tests/test_nlsql_security.py -v
Commit: "test: NL→SQL security test suite — prompt injection, SQL blocking, patterns"
```

## Acceptance Criteria
- [ ] All _clean_sql() security cases tested
- [ ] Prompt injection scenarios covered
- [ ] Pattern matcher fully tested
- [ ] API endpoint integration tests included
- [ ] Rate limiting tested
- [ ] All tests pass
