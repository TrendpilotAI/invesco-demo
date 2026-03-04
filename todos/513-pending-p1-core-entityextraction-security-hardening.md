# TODO-513: Security Hardening (Dependency Audit + Request Limits + Key Hashing)

**Repo:** core-entityextraction
**Priority:** P1
**Effort:** S (2-3h)
**Dependencies:** None
**Blocks:** None

## Description
Bundle of quick security wins: dependency audit, HTTP request size limits, and improved API key handling.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Pin exact versions in requirements.txt (no >= ranges)
2. Add pip-audit to CI pipeline, run and fix any CVEs
3. Add request body size limit middleware:
   - uvicorn --limit-concurrency 100
   - Add middleware to reject bodies > 1MB
4. Document API key rotation procedure in README.md
5. Add secrets scanning: check no hardcoded keys in docker/, .env files
6. Optional (if time): hash API keys with bcrypt in Postgres instead of plaintext comparison
```

## Acceptance Criteria
- [ ] All deps pinned to exact versions
- [ ] pip-audit passes clean
- [ ] Request body size limited at HTTP level
- [ ] Key rotation documented
- [ ] No hardcoded secrets in codebase
