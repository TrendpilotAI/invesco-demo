---
id: "475"
status: pending
priority: medium
repo: signal-studio-data-provider
title: "Add DatabricksProvider for enterprise market coverage"
effort: L
dependencies: ["472"]
created: "2026-03-04"
---

## Task Description

Databricks Unity Catalog is the fastest-growing enterprise data warehouse, now competing directly with Snowflake. Signal Studio needs a DatabricksProvider to close deals with Databricks-native customers. This is a tier-4 enterprise offering.

## Coding Prompt

1. Add to `pyproject.toml`:
```toml
[project.optional-dependencies]
databricks = ["databricks-sql-connector>=3.0"]
all = ["signal-studio-data-provider[snowflake,supabase,oracle,databricks]"]
```

2. Add `DatabricksConfig` to `config.py`:
```python
class DatabricksConfig(BaseModel):
    server_hostname: str
    http_path: str  # /sql/1.0/warehouses/xxx
    access_token: str
    catalog: str = "hive_metastore"
    schema_name: str = "default"
```

3. Create `providers/databricks_provider.py`:
```python
"""Databricks DataProvider — enterprise tier (Unity Catalog)."""
from __future__ import annotations

import asyncio
import time
from typing import Any

import pandas as pd

from ._utils import validate_identifier
from ..config import OrgConfig
from .base import ColumnInfo, DataProvider, QueryResult, SchemaInfo, SignalDefinition, TableInfo


class DatabricksProvider:
    """Databricks-backed DataProvider using databricks-sql-connector."""

    def __init__(self, config: OrgConfig) -> None:
        self._config = config
        db = config.databricks
        if db is None:
            raise ValueError("DatabricksConfig required for databricks tier")
        self._db = db
        self._connection = None

    def _get_connection(self):
        if self._connection is None:
            from databricks import sql as dbsql
            self._connection = dbsql.connect(
                server_hostname=self._db.server_hostname,
                http_path=self._db.http_path,
                access_token=self._db.access_token,
            )
        return self._connection

    def _execute_sync(self, sql: str, params=None) -> QueryResult:
        t0 = time.time()
        conn = self._get_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql, parameters=list((params or {}).values()) or None)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
        elapsed = (time.time() - t0) * 1000
        result_rows = [dict(zip(columns, row)) for row in rows]
        return QueryResult(rows=result_rows, columns=columns, row_count=len(result_rows), execution_time_ms=elapsed)

    async def execute_query(self, sql: str, params=None) -> QueryResult:
        return await asyncio.to_thread(self._execute_sync, sql, params)

    async def get_schema(self, org_id: str) -> SchemaInfo:
        tables = await self.get_tables(org_id)
        return SchemaInfo(org_id=org_id, tables=tables)

    async def test_connection(self) -> bool:
        try:
            await self.execute_query("SELECT 1")
            return True
        except Exception:
            return False

    async def get_tables(self, org_id: str) -> list[TableInfo]:
        result = await self.execute_query(
            f"SHOW TABLES IN {self._db.catalog}.{self._db.schema_name}"
        )
        return [TableInfo(name=r["tableName"], schema_name=self._db.schema_name) for r in result.rows]

    async def get_columns(self, table: str, org_id: str) -> list[ColumnInfo]:
        validate_identifier(table)
        result = await self.execute_query(f"DESCRIBE TABLE {self._db.catalog}.{self._db.schema_name}.{table}")
        return [
            ColumnInfo(name=r["col_name"], data_type=r["data_type"], nullable=True)
            for r in result.rows if not r["col_name"].startswith("#")
        ]

    async def execute_signal(self, signal: SignalDefinition, params=None) -> pd.DataFrame:
        merged = {**signal.parameters, **(params or {})}
        result = await self.execute_query(signal.sql, merged)
        return pd.DataFrame(result.rows, columns=result.columns)

    async def write_back(self, table: str, data: list[dict[str, Any]], org_id: str) -> int:
        if not data:
            return 0
        validate_identifier(table)
        # Use Databricks MERGE or bulk INSERT
        def _write_sync():
            conn = self._get_connection()
            columns = list(data[0].keys())
            for col in columns:
                validate_identifier(col)
            placeholders = ", ".join(["?"] * len(columns))
            col_str = ", ".join(columns)
            sql = f"INSERT INTO {self._db.catalog}.{self._db.schema_name}.{table} ({col_str}) VALUES ({placeholders})"
            with conn.cursor() as cursor:
                for row in data:
                    cursor.execute(sql, [row[c] for c in columns])
            return len(data)
        return await asyncio.to_thread(_write_sync)

    async def close(self) -> None:
        if self._connection:
            self._connection.close()
            self._connection = None
```

4. Register in `factory.py`:
```python
case "databricks":
    from .providers.databricks_provider import DatabricksProvider
    provider = DatabricksProvider(org_config)
```

5. Add mock tests in `tests/test_providers.py` for DatabricksProvider.

## Acceptance Criteria
- [ ] `DatabricksConfig` in `config.py`
- [ ] `DatabricksProvider` implements full `DataProvider` Protocol
- [ ] All methods use `asyncio.to_thread()` (sync connector)
- [ ] Factory routes `"databricks"` tier correctly
- [ ] Mock tests cover execute_query, get_schema, write_back
- [ ] pyproject.toml `databricks` extra added
