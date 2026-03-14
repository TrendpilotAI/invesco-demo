# 🔴 CRITICAL ISSUES — signal-studio-data-provider

**Flagged:** 2026-03-14

---

## 1. RUNTIME BREAKAGE: SecretStr fields accessed without `.get_secret_value()`

**Impact:** All provider connections will CRASH at runtime  
**Root cause:** `config.py` was updated to use `pydantic.SecretStr` for passwords/keys, but provider code still accesses them as plain `str`.

**Affected files:**
| File | Line | Code | Fix |
|------|------|------|-----|
| `providers/snowflake_provider.py` | 71 | `password=self._sf.password` | `password=self._sf.password.get_secret_value()` |
| `providers/oracle_provider.py` | 49 | `password=self._ora.password` | `password=self._ora.password.get_secret_value()` |
| `providers/supabase_provider.py` | 43 | `self._sb.database_url` | `self._sb.database_url.get_secret_value()` |

**Also check:** Any usage of `anon_key` or `service_role_key` in supabase_provider.py.

**Effort:** 15 minutes  
**Risk:** Zero — purely mechanical fix

---

## 2. TEST RUNNER BROKEN: Zero Tests Executing

**Impact:** No test coverage verification possible  
**Error:** `ValueError: numpy.dtype size changed, may indicate binary incompatibility`  
**Fix:** `pip install --upgrade numpy pandas` or pin compatible versions in `pyproject.toml`  
**Effort:** 10 minutes

---

## Resolution Priority

Fix #1 FIRST — it's a regression from the SecretStr security improvement that creates a worse problem (nothing works) than the original issue (credentials could leak in logs).
