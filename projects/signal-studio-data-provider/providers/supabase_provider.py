"""Supabase/PostgreSQL DataProvider — self-serve tier."""

from __future__ import annotations

import json
import re
import time
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


class SupabaseProvider:
    """Supabase-backed DataProvider using asyncpg for heavy queries."""

    def __init__(self, config: OrgConfig) -> None:
        self._config = config
        sb = config.supabase
        if sb is None:
            raise ValueError("SupabaseConfig required for self-serve tier")
        self._sb = sb
        self._pool: Any = None  # asyncpg pool, lazy

    # -- connection management ---------------------------------------------

    async def _get_pool(self):
        if self._pool is None:
            import asyncpg  # type: ignore
            self._pool = await asyncpg.create_pool(self._sb.database_url, min_size=2, max_size=20)
        return self._pool

    async def _set_jwt_on_conn(self, conn: Any, jwt: str | None) -> None:
        """Set request.jwt.claims per-connection for RLS. Scoped to this connection only."""
        if jwt:
            claims = json.dumps({"sub": jwt, "role": "authenticated"})
            await conn.execute(
                "SELECT set_config('request.jwt.claims', $1, true)",
                claims,
            )

    # -- DataProvider implementation ---------------------------------------

    async def execute_query(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        jwt: str | None = None,
    ) -> QueryResult:
        pool = await self._get_pool()
        t0 = time.time()
        async with pool.acquire() as conn:
            # Set RLS context per-connection — safe under concurrency
            await self._set_jwt_on_conn(conn, jwt)

            # asyncpg uses $1, $2 positional params
            param_values = list((params or {}).values())
            rows = await conn.fetch(sql, *param_values)
            elapsed = (time.time() - t0) * 1000

        if rows:
            columns = list(rows[0].keys())
            result_rows = [dict(r) for r in rows]
        else:
            columns, result_rows = [], []

        return QueryResult(rows=result_rows, columns=columns, row_count=len(result_rows), execution_time_ms=elapsed)

    async def get_schema(self, org_id: str) -> SchemaInfo:
        tables = await self.get_tables(org_id)
        return SchemaInfo(org_id=org_id, tables=tables)

    async def test_connection(self) -> bool:
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception:
            return False

    async def get_tables(self, org_id: str) -> list[TableInfo]:
        result = await self.execute_query(
            "SELECT table_name, obj_description((quote_ident(table_schema)||'.'||quote_ident(table_name))::regclass) as description "
            "FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"
        )
        return [
            TableInfo(name=r["table_name"], schema_name="public", description=r.get("description") or "")
            for r in result.rows
        ]

    async def get_columns(self, table: str, org_id: str) -> list[ColumnInfo]:
        result = await self.execute_query(
            "SELECT column_name, data_type, is_nullable, "
            "col_description((table_schema||'.'||table_name)::regclass, ordinal_position) as description "
            "FROM information_schema.columns WHERE table_name = $1 AND table_schema = 'public'",
            {"table": table},
        )
        return [
            ColumnInfo(
                name=r["column_name"],
                data_type=r["data_type"],
                nullable=r.get("is_nullable", "YES") == "YES",
                description=r.get("description") or "",
            )
            for r in result.rows
        ]

    async def execute_signal(
        self,
        signal: SignalDefinition,
        params: dict[str, Any] | None = None,
        jwt: str | None = None,
    ) -> pd.DataFrame:
        merged = {**signal.parameters, **(params or {})}
        result = await self.execute_query(signal.sql, merged, jwt=jwt)
        return pd.DataFrame(result.rows, columns=result.columns)

    async def write_back(
        self,
        table: str,
        data: list[dict[str, Any]],
        org_id: str,
        jwt: str | None = None,
    ) -> int:
        if not data:
            return 0
        pool = await self._get_pool()
        columns = list(data[0].keys())
        _validate_identifier(table)
        for col in columns:
            _validate_identifier(col)
        col_str = ", ".join(columns)
        placeholders = ", ".join(f"${i+1}" for i in range(len(columns)))
        sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
        async with pool.acquire() as conn:
            # Set RLS context per-connection — safe under concurrency
            await self._set_jwt_on_conn(conn, jwt)
            await conn.executemany(sql, [tuple(row[c] for c in columns) for row in data])
        return len(data)

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    # -- pgvector helpers --------------------------------------------------

    async def vector_search(self, table: str, embedding: list[float], column: str = "embedding", limit: int = 10, jwt: str | None = None) -> QueryResult:
        """Perform pgvector similarity search."""
        _validate_identifier(table)
        _validate_identifier(column)
        vec_str = "[" + ",".join(str(v) for v in embedding) + "]"
        sql = (
            f"SELECT *, ({column} <=> $1::vector) AS distance "
            f"FROM {table} ORDER BY {column} <=> $1::vector LIMIT $2"
        )
        return await self.execute_query(sql, {"vec": vec_str, "limit": limit}, jwt=jwt)

    # -- Realtime (placeholder for supabase-py realtime) -------------------

    async def subscribe(self, table: str, callback: Any) -> None:
        """Subscribe to realtime changes on a table. Requires supabase-py client."""
        raise NotImplementedError("Realtime subscriptions require supabase-py client setup")
