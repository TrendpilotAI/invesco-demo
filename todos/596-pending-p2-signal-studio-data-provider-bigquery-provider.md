# TODO 596 — BigQuery DataProvider

**Repo:** signal-studio-data-provider  
**Priority:** P2 (Revenue Expansion)  
**Effort:** M (2-3 days)  
**Dependencies:** 590

## Task Description
Add a BigQuery-backed DataProvider for GCP-native enterprise clients. Many finance/analytics orgs run BigQuery as their primary warehouse. This expands TAM and aligns with the multi-cloud strategy.

## Changes Required
- `providers/bigquery_provider.py` implementing `DataProvider` protocol
- `BigQueryConfig` in `config.py` with `project_id`, `dataset`, `credentials_json` (SecretStr)
- New `data_tier = "bigquery"` in `OrgConfig.data_tier` Literal
- SQLAdapter dialect support for BigQuery (STRUCT access, ARRAY_AGG, backtick identifiers)
- Factory routing for `"bigquery"` tier

## Autonomous Agent Prompt
```
In /data/workspace/projects/signal-studio-data-provider/:

1. Add BigQueryConfig to config.py:
   class BigQueryConfig(BaseModel):
       project_id: str
       dataset: str
       credentials_json: SecretStr = Field(repr=False)  # JSON service account key

2. Update OrgConfig.data_tier Literal to include "bigquery"; add `bigquery: Optional[BigQueryConfig] = None`

3. Create providers/bigquery_provider.py using google-cloud-bigquery async client:
   - execute_query: use bigquery.Client.query() wrapped in asyncio.to_thread()
   - get_schema: use bigquery.Client.list_tables() + get_table() for column info
   - get_tables, get_columns: list from dataset
   - execute_signal: run signal.sql, return DataFrame
   - write_back: use bigquery.Client.insert_rows_json() or load_table_from_dataframe()
   - test_connection: run SELECT 1
   - close(): no-op (BQ client is stateless)

4. Add SQLAdapter dialect "bigquery" handling:
   - Backtick identifiers: `project.dataset.table`
   - ARRAY_AGG instead of STRING_AGG
   - TIMESTAMP_TRUNC instead of DATE_TRUNC
   - No FETCH FIRST — uses LIMIT

5. Update factory.py with case "bigquery": BigQueryProvider(org_config)

6. Add pyproject.toml optional: bigquery = ["google-cloud-bigquery>=3.0", "db-dtypes>=1.0"]

7. Add tests/test_bigquery_provider.py with mocked BigQuery client

Run pytest tests/ to verify.
```

## Acceptance Criteria
- [ ] BigQueryProvider implements full DataProvider protocol
- [ ] SQLAdapter handles BigQuery dialect
- [ ] Factory routes "bigquery" tier correctly
- [ ] Mock-based tests cover execute_query, get_schema, write_back
- [ ] README updated with BigQuery configuration example
