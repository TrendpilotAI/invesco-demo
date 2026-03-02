# TODO-406: Dockerfile + GitHub Actions CI Pipeline

**Repo:** signal-studio-auth  
**Priority:** HIGH  
**Effort:** S (2-3 hours)  
**Dependencies:** None

## Problem
No deployment artifacts or CI pipeline. Manual deploys are error-prone. No automated test/lint/security checks on PRs.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-auth/:

1. Create Dockerfile:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 8080
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```

2. Create .github/workflows/ci.yml:
   - Trigger: push to main, PRs to main
   - Jobs:
     a. test: `pip install -r requirements.txt && pytest --tb=short`
     b. lint: `pip install ruff && ruff check .`
     c. security: `pip install bandit safety && bandit -r . -x tests && safety check`
   - Use python:3.11, cache pip dependencies

3. Create railway.json:
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": { "builder": "DOCKERFILE" },
     "deploy": {
       "healthcheckPath": "/health",
       "healthcheckTimeout": 30,
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```

4. Add GET /health endpoint to main.py:
   ```python
   @app.get("/health")
   def health(): return {"status": "ok"}
   ```

5. Create .ruff.toml with sensible defaults for Python 3.11
```

## Acceptance Criteria
- [ ] Docker builds successfully: `docker build -t signal-studio-auth .`
- [ ] CI runs on every PR
- [ ] CI catches: test failures, lint errors, security issues
- [ ] Railway deploy config present
- [ ] /health endpoint returns 200
