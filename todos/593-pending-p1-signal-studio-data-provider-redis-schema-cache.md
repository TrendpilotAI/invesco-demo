# TODO 593 — Redis-backed SchemaRegistry cache

**Repo:** signal-studio-data-provider  
**Priority:** P1 (Scalability)  
**Effort:** M (1-2 days)  
**Dependencies:** 590

## Task Description
`SchemaRegistry` uses an in-process dict cache — useless in multi-worker deployments. Add optional Redis backend so all workers share schema cache. Fall back to in-memory if Redis not configured.

## Changes Required
- Add optional `redis_url: str | None` to `OrgConfig`  
- Create `utils/cache.py` with `SchemaCache` abstract base + `MemorySchemaCache` + `RedisSchemaCache` implementations
- `SchemaRegistry.__init__` accepts optional `cache: SchemaCache` (defaults to memory)
- Serialize/deserialize `SchemaInfo` via `model_dump()`/pydantic reconstruction
- TTL managed by Redis `SETEX`

## Autonomous Agent Prompt
```
In /data/workspace/projects/signal-studio-data-provider/:

1. Create utils/cache.py with:
   - Abstract `SchemaCache` protocol with `get(org_id) -> SchemaInfo | None`, `set(org_id, schema, ttl)`, `invalidate(org_id)`
   - `MemorySchemaCache` using dict + time.time() TTL
   - `RedisSchemaCache` using `redis.asyncio.Redis` — serialize SchemaInfo with `dataclasses.asdict()`, store as JSON with SETEX

2. Update schema/registry.py:
   - Accept optional `cache: SchemaCache | None` in __init__; default to MemorySchemaCache
   - Replace `self._schema_cache` dict operations with `cache.get/set/invalidate` calls

3. Update config.py OrgConfig to add `redis_url: str | None = None`

4. Update factory.py to instantiate RedisSchemaCache if `org_config.redis_url` is set

5. Add tests/test_schema_cache.py testing both memory and Redis backends (mock redis for Redis tests)

Run pytest tests/ to verify.
```

## Acceptance Criteria
- [ ] Redis cache backend implemented and optional
- [ ] Falls back to in-memory when `redis_url` not set
- [ ] SchemaRegistry tests pass with both backends
- [ ] Serialization round-trips correctly for all dataclass types
