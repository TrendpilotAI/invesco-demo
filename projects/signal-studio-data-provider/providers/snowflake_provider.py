"""Snowflake DataProvider — enterprise tier."""

from __future__ import annotations

import asyncio
import re
import time
from functools import lru_cache
from typing import Any

_SAFE_IDENTIFIER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def _validate_identifier(name: str) -> str:
    """Raise ValueError if *name* is not a safe SQL identifier."""
    if not _SAFE_IDENTIFIER_RE.match(name):
        raise ValueError(f"Unsafe SQL identifier: {name!r}")
    return name

import pandas as pd

from ..config import OrgConfig

from .base import (
    ColumnInfo, DataProvider, QueryResult, SchemaInfo, SignalDefinition, TableInfo,
)


class _TTLCache:
    """Simple TTL cache for query results."""

    def __init__(self, ttl: int = 300):
        self._ttl = ttl
        self._store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry and (time.time() - entry[0]) < self._ttl:
            return entry[1]
        self._store.pop(key, None)
        return None

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (time.time(), value)

    def clear(self) -> None:
        self._store.clear()


class SnowflakeProvider:
    """Snowflake-backed DataProvider with connection pooling, caching, and cost tracking."""

    def __init__(self, config: OrgConfig) -> None:
        self._config = config
        sf = config.snowflake
        if sf is None:
            raise ValueError("SnowflakeConfig required for enterprise tier")
        self._sf = sf
        self._cache = _TTLCache(ttl=config.cache_ttl)
        self._total_credits: float = 0.0
        self._conn: Any = None  # lazy

    # -- internal helpers --------------------------------------------------

    def _get_connection(self):
        if self._conn is None:
            import snowflake.connector  # type: ignore
            self._conn = snowflake.connector.connect(
                account=self._sf.account,
                user=self._sf.user,
                password=self._sf.password,
                warehouse=self._sf.warehouse,
                database=self._sf.database,
                schema=self._sf.schema_name,
                role=self._sf.role,
            )
        return self._conn

    def _cursor(self):
        return self._get_connection().cursor()

    # -- DataProvider implementation ---------------------------------------

    def _execute_query_sync(self, sql: str, params: list[Any] | None = None) -> QueryResult:
        """Blocking Snowflake query — must be called via run_in_executor, never directly from the event loop."""
        cur = self._cursor()
        t0 = time.time()
        try:
            cur.execute(sql, params or [])
            columns = [desc[0] for desc in cur.description] if cur.description else []
            rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        finally:
            elapsed = (time.time() - t0) * 1000
            cur.close()

        # Rough cost estimate: 1 credit ≈ 1 minute of XS warehouse
        cost = elapsed / 60_000  # very rough
        return QueryResult(rows=rows, columns=columns, row_count=len(rows), execution_time_ms=elapsed, cost=cost)

    async def execute_query(self, sql: str, params: list[Any] | None = None) -> QueryResult:
        cache_key = f"{sql}|{params}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        # TODO-312: Offload blocking Snowflake I/O to a thread pool so we don't block the asyncio event loop
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._execute_query_sync, sql, params)

        self._total_credits += result.cost or 0.0
        self._cache.set(cache_key, result)
        return result

    async def get_schema(self, org_id: str) -> SchemaInfo:
        tables = await self.get_tables(org_id)
        return SchemaInfo(org_id=org_id, tables=tables)

    def _test_connection_sync(self) -> bool:
        cur = self._cursor()
        cur.execute("SELECT 1")
        cur.close()
        return True

    async def test_connection(self) -> bool:
        # TODO-312: Offload blocking call to thread pool
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._test_connection_sync)
        except Exception:
            return False

    async def get_tables(self, org_id: str) -> list[TableInfo]:
        result = await self.execute_query(
            "SELECT TABLE_NAME, ROW_COUNT, COMMENT "
            "FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s",
            [self._sf.schema_name],  # TODO-434: Snowflake execute() requires positional list, not dict
        )
        return [
            TableInfo(
                name=r["TABLE_NAME"],
                schema_name=self._sf.schema_name,
                row_count=r.get("ROW_COUNT"),
                description=r.get("COMMENT", ""),
            )
            for r in result.rows
        ]

    async def get_columns(self, table: str, org_id: str) -> list[ColumnInfo]:
        result = await self.execute_query(
            "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COMMENT "
            "FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s AND TABLE_SCHEMA = %s",
            [table, self._sf.schema_name],  # TODO-434: Snowflake execute() requires positional list, not dict
        )
        return [
            ColumnInfo(
                name=r["COLUMN_NAME"],
                data_type=r["DATA_TYPE"],
                nullable=r.get("IS_NULLABLE", "YES") == "YES",
                description=r.get("COMMENT", ""),
            )
            for r in result.rows
        ]

    async def execute_signal(self, signal: SignalDefinition, params: dict[str, Any] | None = None) -> pd.DataFrame:
        merged = {**signal.parameters, **(params or {})}
        result = await self.execute_query(signal.sql, merged)
        return pd.DataFrame(result.rows, columns=result.columns)

    def _write_back_sync(self, table: str, data: list[dict[str, Any]]) -> int:
        columns = list(data[0].keys())
        # TODO-313: Validate identifiers to prevent SQL injection via table/column names
        _validate_identifier(table)
        for col in columns:
            _validate_identifier(col)
        placeholders = ", ".join(["%s"] * len(columns))
        col_str = ", ".join(columns)
        sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
        cur = self._cursor()
        try:
            cur.executemany(sql, [tuple(row[c] for c in columns) for row in data])
            self._get_connection().commit()
        finally:
            cur.close()
        return len(data)

    async def write_back(self, table: str, data: list[dict[str, Any]], org_id: str) -> int:
        if not data:
            return 0
        # TODO-312: Offload blocking Snowflake I/O to thread pool
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._write_back_sync, table, data)

    async def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # -- Cortex AI helpers -------------------------------------------------

    # SS-3: Allowlist of valid Snowflake Cortex model names.
    # Only these exact strings may be passed to Cortex SQL functions.
    # Update this set when Snowflake adds new Cortex models.
    CORTEX_COMPLETE_MODELS: frozenset[str] = frozenset([
        # Snowflake proprietary
        "snowflake-arctic",
        "snowflake-arctic-instruct",
        # Meta Llama family
        "llama2-70b-chat",
        "llama3-8b",
        "llama3-70b",
        "llama3.1-8b",
        "llama3.1-70b",
        "llama3.1-405b",
        "llama3.2-1b",
        "llama3.2-3b",
        # Mistral family
        "mistral-7b",
        "mistral-large",
        "mistral-large2",
        "mixtral-8x7b",
        # Reka
        "reka-core",
        "reka-flash",
        # AI21
        "jamba-instruct",
        "jamba-1.5-mini",
        "jamba-1.5-large",
        # Google
        "gemma-7b",
    ])

    CORTEX_EMBED_MODELS: frozenset[str] = frozenset([
        "snowflake-arctic-embed-m",
        "snowflake-arctic-embed-l",
        "e5-base-v2",
        "multilingual-e5-large",
        "nv-embed-qa-4",
        "voyage-multilingual-2",
    ])

    @classmethod
    def _validate_cortex_model(cls, model: str, *, kind: str = "complete") -> str:
        """Validate model name against the appropriate Cortex allowlist.

        Args:
            model: Model name to validate.
            kind: ``"complete"`` or ``"embed"`` — selects which allowlist to check.

        Raises:
            ValueError: If *model* is ``None``, empty, or not in the allowlist.
        """
        if not model or not isinstance(model, str):
            raise ValueError("Model name must be a non-empty string")

        allowlist = (
            cls.CORTEX_COMPLETE_MODELS if kind == "complete"
            else cls.CORTEX_EMBED_MODELS
        )

        if model not in allowlist:
            raise ValueError(
                f"Invalid Cortex {kind} model {model!r}. "
                f"Allowed models: {sorted(allowlist)}"
            )
        return model

    async def cortex_complete(self, model: str, prompt: str) -> str:
        """Call Snowflake Cortex COMPLETE function.

        The model name is validated against an allowlist before being
        placed into SQL.  The prompt is always parameterized.
        """
        self._validate_cortex_model(model, kind="complete")
        # SS-3 FIX: model is allowlist-validated above so it is safe to
        # interpolate.  The prompt is bound via %s parameterization.
        result = await self.execute_query(
            f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', %s) AS response",
            [prompt],
        )
        return result.rows[0]["RESPONSE"] if result.rows else ""

    async def cortex_embed(self, model: str, text: str) -> list[float]:
        """Call Snowflake Cortex EMBED_TEXT function.

        The model name is validated against an allowlist before being
        placed into SQL.  The text is always parameterized.
        """
        self._validate_cortex_model(model, kind="embed")
        # SS-3 FIX: model is allowlist-validated above so it is safe to
        # interpolate.  The text is bound via %s parameterization.
        result = await self.execute_query(
            f"SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('{model}', %s) AS embedding",
            [text],
        )
        return result.rows[0]["EMBEDDING"] if result.rows else []

    @property
    def total_credits(self) -> float:
        return self._total_credits
