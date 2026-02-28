# 317 · NarrativeReactor — Railway + Docker Deployment Config

**Status:** pending  
**Priority:** high  
**Project:** NarrativeReactor  
**Effort:** ~4h  

---

## Task Description

NarrativeReactor has no deployment configuration. The platform needs production-ready Railway config and a multi-stage Dockerfile. This enables one-click deploys and consistent environments across dev/staging/prod.

## Full Coding Prompt

```
You are working in /data/workspace/projects/NarrativeReactor/.

## Step 1 — Multi-stage Dockerfile
Create `Dockerfile` at repo root:

```dockerfile
# ---- Build stage ----
FROM node:20-alpine AS builder
WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

# ---- Production stage ----
FROM node:20-alpine AS runner
WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

ENV NODE_ENV=production

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --prod

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/public ./public

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

## Step 2 — .dockerignore
Create `.dockerignore`:
```
node_modules
dist
.env
*.log
.git
web-ui/.next
web-ui/node_modules
```

## Step 3 — railway.json
Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "node dist/index.js",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

## Step 4 — Health endpoint
In `src/index.ts`, add before other routes:
```typescript
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', version: process.env.npm_package_version, ts: Date.now() });
});
```

## Step 5 — Web UI Dockerfile
Create `web-ui/Dockerfile`:
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 3001
CMD ["node", "server.js"]
```

## Step 6 — docker-compose.yml (local dev)
Create `docker-compose.yml`:
```yaml
version: '3.9'
services:
  api:
    build: .
    ports:
      - "3000:3000"
    env_file: .env
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  web-ui:
    build: ./web-ui
    ports:
      - "3001:3001"
    environment:
      - NEXT_PUBLIC_API_URL=http://api:3000
    depends_on:
      api:
        condition: service_healthy
```

## Step 7 — Update package.json scripts
Add:
```json
"docker:build": "docker build -t narrative-reactor .",
"docker:run": "docker-compose up",
"docker:push": "docker push narrative-reactor"
```

## Step 8 — Update README
Document the deployment section referencing this config.
```

## Dependencies
- 315 (README should document deployment)

## Acceptance Criteria
- [ ] `docker build .` succeeds from repo root
- [ ] `docker-compose up` starts both API and web-ui
- [ ] `GET /health` returns `{"status":"ok",...}`
- [ ] `railway.json` is valid JSON matching Railway's schema
- [ ] `.dockerignore` excludes node_modules and .env
- [ ] No secrets baked into Docker image
