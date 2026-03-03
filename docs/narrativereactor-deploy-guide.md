# NarrativeReactor Railway Deployment Guide

## Current Status ✅ Prepared, ❌ Deployment Failed

The project is properly configured for Railway deployment but the latest deployment attempt failed.

### ✅ What's Working

1. **Build System**: The project builds successfully locally
   - `yarn install` and `yarn build` completed without errors
   - TypeScript compilation works (7.87s build time)

2. **Railway Configuration**: Properly configured
   - ✅ `railway.json` exists with correct Dockerfile configuration
   - ✅ `Dockerfile` is properly structured (multi-stage build, security hardened)
   - ✅ `.env.example` contains all required environment variables
   - ✅ Connected to Railway project "OpenClaw AI + n8n + Tailscale"

3. **Environment Setup**: Complete environment variable documentation
   - Required: `API_KEY`, `GOOGLE_GENAI_API_KEY`, `ANTHROPIC_API_KEY`, `FAL_KEY`, `WEBHOOK_SECRET`
   - Production: `CORS_ALLOWED_ORIGINS`, `TOKEN_ENCRYPTION_KEY`, `DASHBOARD_PASSWORD`
   - Optional: Model overrides, cost tracking, Sentry integration

### ❌ Current Issue: Deployment Failed

**Last Deployment**: `201f833d-43af-46f1-835f-94735d050ecf` - FAILED (2026-03-03 10:49:49 UTC)
**Service**: `openclaw-railway-template` (existing service being reused)

**Previous Success**: `8f85cd24-5342-4b38-bae5-c7b4ba590e12` - SUCCESS (2026-03-03 05:03:54 UTC)

## Project Architecture

```
NarrativeReactor/
├── src/                    # TypeScript source
├── dist/                   # Built output
├── public/                 # Static dashboard assets
├── prompts/                # AI prompt templates
├── Dockerfile              # Multi-stage production build
├── railway.json            # Railway deployment config
├── .env.example            # Environment template
├── package.json            # Dependencies & scripts
└── genkit.config.js        # Genkit flow configuration
```

## Deployment Architecture

**Target**: Railway Cloud Platform
- **Service**: openclaw-railway-template (reusing existing service)
- **Build**: Dockerfile (multi-stage Node.js 22)
- **Port**: 8080 (Railway default)
- **Health Check**: `/health` endpoint

## Environment Variables Required for Production

### Core API Keys (Required)
```bash
API_KEY=your-api-key-here                    # Authentication for /api/* routes
GOOGLE_GENAI_API_KEY=your-gemini-key        # Gemini AI provider
ANTHROPIC_API_KEY=your-claude-key           # Claude AI provider  
FAL_KEY=your-fal-ai-key                     # Fal.ai for video/image generation
WEBHOOK_SECRET=your-webhook-secret          # Webhook signature verification
```

### Production Security (Required in Production)
```bash
CORS_ALLOWED_ORIGINS=https://app.example.com,https://dashboard.example.com
TOKEN_ENCRYPTION_KEY=64-char-hex-string     # Generate: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
DASHBOARD_PASSWORD=your-dashboard-password   # Dashboard authentication
```

### Optional Configuration
```bash
NR_PORT=3401                                # API server port (Railway uses PORT=8080)
GENKIT_PORT=3402                            # Genkit dev UI port
JWT_SECRET=your-jwt-secret                  # Falls back to API_KEY
FAL_IMAGE_MODEL=fal-ai/hunyuan-image/v3/instruct/text-to-image
FAL_VIDEO_MODEL=fal-ai/bytedance/seedance/v1.5/pro/text-to-video
SENTRY_DSN=https://...                      # Error reporting
COST_FAL_IMAGE=0.01                         # Cost tracking overrides
COST_FAL_VIDEO=0.10
COST_CLAUDE_CALL=0.03
```

## Docker Configuration

**Multi-stage build optimized for Railway:**
- **Stage 1**: Build dependencies, TypeScript compilation
- **Stage 2**: Production runtime, non-root user, health checks
- **Port**: 8080 (Railway standard)
- **Health**: `/health` endpoint with 30s interval
- **Security**: Runs as `appuser` (non-root)

## Next Steps to Fix Deployment

### 1. Check Environment Variables
Verify all required environment variables are set in Railway dashboard:
```bash
railway variables --service openclaw-railway-template
```

### 2. Check Build Logs
Get detailed build failure information:
```bash
railway logs --service openclaw-railway-template --deployment 201f833d-43af-46f1-835f-94735d050ecf
```

### 3. Retry Deployment
```bash
cd /data/workspace/projects/NarrativeReactor
RAILWAY_TOKEN=d34fc01b-7d8d-440b-9be9-5270d2e40230 railway up --service openclaw-railway-template --message "Fixed deployment attempt"
```

### 4. Alternative: Create New Service
If the existing service has issues, create a dedicated service:
```bash
RAILWAY_TOKEN=d34fc01b-7d8d-440b-9be9-5270d2e40230 railway add --service narrativereactor
```

## API Endpoints (Once Deployed)

### Core Features
- `POST /api/generate` - Content generation via Genkit flows
- `POST /api/compliance` - Brand compliance checking
- `GET/POST /api/campaigns` - Campaign management
- `POST /api/video` - Video generation pipeline
- `POST /api/audio/tts` - Text-to-speech
- `GET /health` - Health check (no auth required)

### Dashboard
- **URL**: `https://<railway-domain>.up.railway.app`
- **Login**: Requires `DASHBOARD_PASSWORD`
- **Features**: Content management, campaign tracking, cost monitoring

## Security Features ✅

- **CORS Protection**: `CORS_ALLOWED_ORIGINS` enforced in production
- **API Authentication**: All `/api/*` routes require `X-API-Key` header
- **Rate Limiting**: 100 requests/15min/IP on API routes
- **Token Encryption**: Production-grade token encryption
- **Dashboard Auth**: Password-protected with JWT sessions
- **Container Security**: Non-root execution, multi-stage builds

## Performance Notes

- **Build Time**: ~8 seconds (TypeScript compilation)
- **Dependencies**: 371 node_modules packages
- **Tests**: 274 tests across 24 files
- **Health Check**: 30s interval, 5s timeout, 3 retries

## Troubleshooting Checklist

1. **Environment Variables**: All required keys present?
2. **Token Encryption Key**: 64-char hex string generated correctly?
3. **CORS Origins**: Properly formatted comma-separated list?
4. **Railway Service**: Has sufficient resources allocated?
5. **Build Context**: All files (src/, public/, prompts/) included?

## Manual Verification Steps

```bash
# Test local build
cd /data/workspace/projects/NarrativeReactor
yarn install && yarn build

# Check Docker build
docker build -t narrativereactor-test .
docker run -p 8080:8080 --env-file .env narrativereactor-test

# Health check
curl http://localhost:8080/health
```

---

**Next Action**: Debug the deployment failure by checking Railway dashboard logs and environment variable configuration.