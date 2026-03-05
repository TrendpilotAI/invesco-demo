# TODO-617: Fix PostgreSQL Connection Leak in persistence.py

**Repo:** core-entityextraction  
**Priority:** P0 (Critical Bug)  
**Effort:** S (~30 min)  
**Status:** pending

## Problem
`load_all()`, `save_entities()`, and `delete_entities()` in `persistence.py` have `else: _put_conn(conn)` blocks that appear after `return` statements inside `try` blocks. In Python, `try/except/else` — the `else` runs only if no exception occurred, but the function already returned. The connection is borrowed from the pool but never returned on the success path, causing pool exhaustion under load.

## Task Description
Restructure all persistence functions to use `finally` blocks for connection return.

## Coding Prompt
```
Fix /data/workspace/projects/core-entityextraction/persistence.py:

In functions load_all(), save_entities(), delete_entities(), and init_db():
- Remove the `else: _put_conn(conn)` blocks (they're unreachable after return)
- Add `finally: _put_conn(conn)` blocks to guarantee connection return to pool
- Be careful: _put_conn(conn, close=True) should still be called in exception handlers when the connection may be broken

Pattern to use:
    conn = _get_conn()
    if conn is None:
        return <default>
    try:
        # ... do work ...
        return result
    except Exception as exc:
        LOGGER.error(...)
        _put_conn(conn, close=True)
        return <default>
    finally:
        # Only put back if not already closed
        pass  # handled above

Actually, cleaner pattern:
    conn = _get_conn()
    if conn is None:
        return <default>
    ok = True
    try:
        # ... do work ...
        return result
    except Exception as exc:
        LOGGER.error(...)
        ok = False
        return <default>
    finally:
        _put_conn(conn, close=not ok)
```

## Acceptance Criteria
- [ ] No unreachable `else: _put_conn` blocks remain
- [ ] All success paths return connection to pool
- [ ] All error paths close/discard connection
- [ ] Under load testing, pool doesn't exhaust after repeated calls

## Dependencies
None — standalone fix
