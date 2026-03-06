# 806 — Pin Dependencies and Add Security Scanning

**Repo:** signal-studio-auth  
**Priority:** P1 (security)  
**Effort:** S (1 hour)  
**Dependencies:** none

## Acceptance Criteria

- [ ] `requirements.lock` generated via `pip-compile`
- [ ] CI uses `requirements.lock` for reproducible installs
- [ ] `pip audit` step added to CI to catch known CVEs
- [ ] `requirements.txt` retains loose bounds for flexibility; lock file used in prod/CI

## Coding Prompt

```
In /data/workspace/projects/signal-studio-auth/:

1. Install pip-tools: pip install pip-tools
2. Run: pip-compile requirements.txt -o requirements.lock
3. Commit requirements.lock

4. In .github/workflows/ci.yml, change:
   - run: pip install -r requirements.txt
   to:
   - run: pip install -r requirements.lock

5. Add pip audit step:
   - run: pip install pip-audit && pip-audit -r requirements.lock

6. Add a Makefile target for updating the lock file:
   update-deps:
       pip-compile requirements.txt -o requirements.lock
```
