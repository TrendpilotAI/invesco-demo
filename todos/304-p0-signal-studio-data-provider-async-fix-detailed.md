Title: 304 — Signal Studio Data Provider: Fix async-blocking Snowflake/Oracle connectors (Critical)
Repo: signal-studio-data-provider
Priority: P0 (Critical)
Owner: Data provider engineer
Estimated effort: 1-2 days

Description:
Eliminate blocking calls in Snowflake and Oracle providers so FastAPI event loop is not blocked. Replace sync connectors with async drivers or run blocking calls in threadpool executors. Fix SQL parameter binding vulnerabilities (no f-strings).

Acceptance criteria:
- No blocking calls on FastAPI event loop (verified via local async profiler or load test)
- All SQL executions use parameterized queries; JWT-derived params are sanitized
- Integration tests for Snowflake/Oracle provider run and pass (mocked connectors allowed)

Execution steps / Agent-executable prompt:
1. Audit providers for sync connector usage (snowflake-connector-python sync calls, cx_Oracle, etc.)
2. If async drivers exist, migrate; otherwise wrap calls in run_in_executor with proper connection pooling
3. Replace any f-string SQL assembly with parameterized queries
4. Add unit/integration tests that assert parameterization and non-blocking behavior

Verification tests:
- Async linter/profiler shows no blocking handlers
- Integration test suite passes for providers

Notes:
- Ensure connection pooling is configured (max connections, timeout)
- If Snowflake async driver unavailable, document and use thread executor pattern with careful backpressure
