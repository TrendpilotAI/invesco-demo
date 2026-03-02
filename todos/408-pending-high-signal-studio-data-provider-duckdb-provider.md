# TODO 408 — DuckDB Provider for Local Dev/Testing

**Repo:** signal-studio-data-provider  
**Priority:** High (P1)  
**Effort:** Small-Medium (1 day)  
**Status:** pending

## Description
No way to run the library locally without real Snowflake/Supabase/Oracle credentials. DuckDB is in-process, zero-infra, and SQL-compatible. Enables fast local dev and CI integration tests without external services.

## Task
Create `providers/duckdb_provider.py` with `DuckDBProvider` implementing the full `DataProvider` protocol using duckdb's Python API.

### Coding Prompt
```
Create /data/workspace/projects/signal-studio-data-provider/providers/duckdb_provider.py

Implement DuckDBProvider that:
1. Takes OrgConfig with data_tier="local" 
2. Uses duckdb.connect(database=':memory:') or file path from config
3. Implements all DataProvider protocol methods:
   - execute_query: async wrapper around duckdb.execute() via asyncio.to_thread()
   - get_schema: introspect via INFORMATION_SCHEMA.TABLES + COLUMNS
   - get_tables / get_columns: same
   - test_connection: SELECT 1
   - execute_signal: run signal.sql and return DataFrame
   - write_back: INSERT INTO via duckdb
   - close: close connection

Add OrgConfig support:
- Add data_tier "local" to Literal type in config.py
- Add DuckDBConfig(db_path: str = ":memory:") to config.py

Add to factory.py:
  case "local":
      from .providers.duckdb_provider import DuckDBProvider
      provider = DuckDBProvider(org_config)

Add optional dep to pyproject.toml: duckdb = ["duckdb>=0.9"]

Add tests in tests/test_providers.py for DuckDBProvider (use real in-memory DB, no mocks needed).
```

## Acceptance Criteria
- [ ] DuckDBProvider implements full DataProvider protocol
- [ ] Works with in-memory DB by default
- [ ] Factory routes `data_tier="local"` to DuckDBProvider
- [ ] Real (non-mock) integration tests using in-memory DuckDB
- [ ] No production dependencies added (optional extra only)

## Dependencies
None
