# Implement Redis Caching for Validator Hot Paths

**Repo:** signal-builder-backend  
**Priority:** medium  
**Effort:** M (2-3 days)  
**Phase:** 3

## Problem
Multiple validator methods have `# TODO: cache` comments, indicating repeated DB queries on hot validation paths. This slows down signal construction operations.

Key locations:
- `apps/signals/.../base_group_function_filter_value_validator.py:147`
- `apps/signals/.../base_ordering_validator.py:214`
- `apps/signals/.../base_filter_value_validator.py:245,339`

## Task
1. Create a `CacheService` wrapper around Redis
2. Implement TTL-based caching decorator for async methods
3. Apply caching to identified validator hot paths
4. Add cache invalidation on signal updates
5. Add cache hit/miss metrics to monitoring

## Acceptance Criteria
- Validator DB queries reduced by >50% on repeated calls
- Cache TTL configurable via environment variable
- Cache invalidated correctly on signal mutations
- No stale data bugs (test with freeze_gun)
