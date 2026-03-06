# 803 — Add Docker + docker-compose for Local Dev

**Repo:** signal-studio-auth  
**Priority:** P1  
**Effort:** S (2 hours)  
**Dependencies:** none

## Acceptance Criteria

- [ ] `Dockerfile` with multi-stage build (builder + runtime)
- [ ] `docker-compose.yml` with FastAPI + Redis services
- [ ] `.env.example` with all required environment variables
- [ ] `README.md` updated with local dev instructions

## Coding Prompt

```
Create /data/workspace/projects/signal-studio-auth/Dockerfile:

FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

Create docker-compose.yml:
services:
  auth:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [redis]
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

Create .env.example with:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_JWT_SECRET=your-jwt-secret
SUPABASE_JWT_ALGORITHM=HS256
SUPABASE_JWT_AUDIENCE=authenticated
AUTH_MODE=supabase
REDIS_URL=redis://redis:6379
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```
