# TODO-506: Add CORS Middleware

**Repo:** core-entityextraction
**Priority:** P1
**Effort:** S (30min)
**Dependencies:** None
**Blocks:** None

## Description
No CORS headers currently. Add CORSMiddleware with configurable allowed origins.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. from fastapi.middleware.cors import CORSMiddleware
2. Add ALLOWED_ORIGINS env var (comma-separated, default: empty = deny all)
3. app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])
4. Document in README.md
```

## Acceptance Criteria
- [ ] CORS middleware added with env-configurable origins
- [ ] Default is deny-all (secure by default)
- [ ] README updated
