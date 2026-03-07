# TODO-825: Expand Translator Unit Test Coverage

**Repo**: signal-builder-backend  
**Priority**: HIGH  
**Effort**: Medium (6-10 hours)

## Problem
`apps/translators/` contains the most complex logic (semantic SQL translation) but has sparse test coverage.

## Task
Add comprehensive unit tests for:

### `expression_translator.py` (352 lines)
- `test_sort_calculations_by_dependency_with_cycle` — should raise on circular deps
- `test_translate_chained_calculations` — nested calc references
- `test_translate_with_missing_property` — should raise TranslationError

### `dataset_query_generator.py` (266 lines)  
- `test_multi_table_join_resolution` — correct join columns identified
- `test_generate_query_with_filters` — WHERE clause construction
- `test_generate_query_with_ordering` — ORDER BY construction

### `group_filter_signal_data_translator.py`
- `test_get_dynamic_result_value_same_dataset` — same-dataset identifier format
- `test_get_dynamic_result_value_cross_dataset` — cross-dataset identifier format

## Acceptance Criteria
- Translator module test coverage > 80% (measure with `pytest --cov=apps/translators`)
- All new tests pass in tox
