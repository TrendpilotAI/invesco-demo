# Trendpilot Railway Deployment Guide

Generated: March 3rd, 2026 — 11:36 AM UTC  
Project: /data/workspace/projects/Trendpilot

## 🎯 Overview

Trendpilot is an AI-powered newsletter platform that discovers trending topics and generates curated newsletters. This guide covers deploying it to Railway with Supabase as the database backend.

## 📋 Prerequisites

### Required Services
- [Railway](https://railway.app) account
- [Supabase](https://supabase.com) project
- [NewsAPI](https://newsapi.org) key
- [Resend](https://resend.com) API key (recommended for email)

### Local Tools
- Node.js 22+
- Yarn or npm
- Supabase CLI (for database setup)

## ⚙️ Environment Variables

Copy `/data/workspace/projects/Trendpilot/.env.example` to `.env` and configure:

### 🗄️ Database (Supabase)
```bash
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# For Next.js/browser compatibility (optional)
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

### 📧 Email Configuration
```bash
# Option 1: Resend (recommended)
RESEND_API_KEY=re_xxxxxxxxx
EMAIL_FROM=TrendPilot <digest@trendpilot.app>

# Option 2: Generic SMTP (alternative)
# SMTP_HOST=smtp.example.com
# SMTP_PORT=587
# SMTP_SECURE=false
# SMTP_USER=your-smtp-user
# SMTP_PASS=your-smtp-password
```

### 🔌 APIs
```bash
NEWS_API_KEY=your-newsapi-key-from-newsapi.org
```

### 🌐 Application
```bash
NODE_ENV=production
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
PUBLIC_BASE_URL=https://your-domain.com
```

## 🗃️ Database Setup

### 1. Create Supabase Project
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create new project
3. Note your project URL and keys

### 2. Run Migrations
```bash
cd /data/workspace/projects/Trendpilot

# Install Supabase CLI if needed
npm install -g @supabase/cli

# Login to Supabase
supabase login

# Link your project
supabase link --project-ref your-project-id

# Push the initial schema
supabase db push
```

### 3. Verify Schema
The migration creates these tables:
- `newsletters` - Newsletter content and metadata
- `topics` - Trending topics from various sources  
- `sections` - Newsletter sections
- `templates` - Email templates
- `subscribers` - Email subscribers with preferences
- `lists` - Subscriber segmentation
- `subscriber_lists` - Many-to-many subscriber/list junction
- `engagements` - Email analytics (opens, clicks, etc.)
- `click_events` - Click tracking events

All tables have Row Level Security (RLS) enabled for user isolation.

## 🚀 Railway Deployment

### 1. Connect Repository
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Connect your Git repository containing Trendpilot

### 2. Configure Build
Railway will automatically detect the Node.js project. The `railway.toml` file configures:
- Build command: `npm run build`
- Start command: `npm run start:prod`
- Health check: `/api/health`
- Auto-scaling settings

### 3. Set Environment Variables
In Railway dashboard, add all environment variables from your `.env` file:
1. Go to project → Variables tab
2. Add each variable from the list above
3. Railway automatically sets `PORT` - do not override

### 4. Deploy
1. Push code to your main branch
2. Railway auto-deploys on git push
3. Monitor logs in Railway dashboard

## 🔍 Verification Steps

### 1. Health Check
```bash
curl https://your-app.up.railway.app/api/health
# Should return: {"status":"ok","timestamp":"2026-03-03T..."}
```

### 2. API Endpoints
```bash
# List trends
curl https://your-app.up.railway.app/api/trends

# Check sources
curl https://your-app.up.railway.app/api/sources
```

### 3. Database Connection
Check Railway logs for successful database connections and any migration issues.

## ⚠️ Current Blockers

### 🛑 Critical Issues

#### 1. Build Failures
**Status**: ❌ **BLOCKING**
- TypeScript compilation fails with missing type definitions
- npm has a persistent error: "Class extends value undefined is not a constructor or null"
- Missing `@types/express`, `@types/nodemailer` in node_modules despite being in package.json

**Resolution Required**:
```bash
# Fix package manager issues
rm -rf node_modules yarn.lock package-lock.json
npm install
# OR
yarn install

# Ensure type definitions are installed
npm install --save-dev @types/express @types/nodemailer @types/supertest

# Fix TypeScript build command in package.json
# Change "tsc" to "npx tsc" in build scripts
```

#### 2. Package Manager Conflicts
**Status**: ❌ **BLOCKING**
- npm is corrupted/broken in current environment
- Yarn install succeeds but doesn't install all devDependencies
- Build scripts use `tsc` instead of `npx tsc`

#### 3. Environment Variable Validation
**Status**: ⚠️ **IMPORTANT**
- No runtime validation of required environment variables
- App may start but fail silently without proper config

### ⚡ Quick Wins

#### 1. Database Schema ✅
- Migration exists and is comprehensive
- RLS policies properly configured
- All required tables defined

#### 2. Dashboard Build ✅  
- Frontend builds successfully with Vite
- No critical dashboard issues found

#### 3. Railway Configuration ✅
- `railway.toml` properly configured
- Health check endpoint exists
- Scaling settings appropriate

## 📝 Next Steps

### Immediate (Fix Blockers)
1. **Fix build system**: Resolve npm/yarn/TypeScript issues
2. **Test local build**: Ensure `yarn build` works end-to-end  
3. **Validate environment**: Test with real Supabase credentials

### Pre-Deploy
1. **Environment validation**: Add startup checks for required env vars
2. **Database verification**: Test connection and migrations
3. **Email testing**: Verify Resend/SMTP configuration

### Post-Deploy
1. **Domain setup**: Configure custom domain in Railway
2. **Monitoring**: Set up health check alerts
3. **Performance**: Monitor app metrics and optimize

## 🔗 References

- **Project Repository**: `/data/workspace/projects/Trendpilot`
- **Railway Docs**: https://docs.railway.app
- **Supabase Docs**: https://supabase.com/docs
- **Environment Template**: `.env.example`
- **Build Configuration**: `railway.toml`

---

**Ready to deploy?** Fix the build blockers first, then follow the Railway deployment steps above. 🚀