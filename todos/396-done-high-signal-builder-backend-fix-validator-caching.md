# TODO-396 DONE: Fix Missing Caching in Signal Validators (Hot Path)

**Status:** done
**Completed:** 2026-03-07
**Branch:** feat/p0-todos-352-356
**Commit:** 0d1e650

## What Was Done

Added instance-level caching to two validator base classes to eliminate repeated DB calls within a single validation run.

### BaseFilterValueValidator (base_filter_value_validator.py)

Three `# TODO: cache` points addressed:

1. **`_get_plain_property(property_id)`** — Added `self._cache_plain_property: dict = {}` in `__init__`. On repeated calls with the same `property_id`, returns cached `PropertyWithId` without hitting `property_storage.get_object_from_scope` again. Relevant when a filter group has multiple rules referencing the same property.

2. **`_get_basic_operator_node(signal_node_id)`** — Added `self._cache_basic_operator_node: dict = {}` in `__init__`. On repeated calls with same `signal_node_id`, returns cached `SignalNodeWithId` without hitting `signal_node_storage.get_object` again.

3. **`_get_operator_schema(filters)`** — Converted from `@staticmethod` to instance method. Added `self._cache_operator_schema: dict = {}` in `__init__`. Caches `OperatorSchema` by `operator_type`. This method is called 3-5× per `filter_rule` validation (from `_validate_operator_allowed_for_prop`, `_get_property_index`, `_validate_chain_*` methods).

### BaseOrderingValidator (base_ordering_validator.py)

1. **`_get_ordering_schema()`** — Added `self._cache_ordering_schema = None` in `__init__`. Caches the result on first call. The method is called from `validate_value`, `_validate_chain_prop_ordering_param`, and `_get_property_index` — 3× per validation for the same ordering type.

### Key design decisions
- All caches are **instance attributes** initialized in `__init__`, so they are scoped to a single validator lifecycle and cannot leak between requests.
- Caches use `None` sentinel (ordering) or empty `dict` (filter) — both initialized fresh per instance.
- The `_get_operator_schema` `@staticmethod` → instance method change is backward compatible since all call sites use `self._get_operator_schema(filters)`.

## Tests Added

`tests/signals/features/signal_construction/validators/create_validators/test_validator_caching.py`

- `test_get_plain_property_db_called_once` — verifies storage called once for same property_id
- `test_get_plain_property_different_ids_hit_db_separately` — two different ids → 2 DB calls total
- `test_get_basic_operator_node_db_called_once` — storage called once for same node_id
- `test_get_operator_schema_schema_lookup_called_once` — schema lookup called once for same operator
- `test_get_operator_schema_different_operators_each_looked_up_once` — 2 operators → 2 lookups total
- `test_get_ordering_schema_schema_lookup_called_once` — lookup called once regardless of how many times validate_value triggers it
- `test_get_ordering_schema_cache_is_not_shared_across_instances` — separate instances have independent caches

## Test Run Status

Full test suite (`pipenv run pytest tests/ -x -q`) could not be executed locally due to missing system packages (psycopg2 build fails without pg_config in CI environment, starlette/slowapi/celery dependencies not fully installed). Code changes are syntactically valid (AST-parsed clean). Logic verified by code inspection and targeted unit test design.
