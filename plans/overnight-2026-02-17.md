# Overnight Sprint Plan — Feb 17, 2026

## Batch 1 (Launch immediately — no dependencies)

### 🏥 Agent 1: Second-Opinion — FHIR Export + Uncertainty Detection
Build two competition-critical features Google specifically wants to see:
- FHIR R4 Bundle export from analysis results (Patient, Condition, DiagnosticReport resources)
- Model disagreement/uncertainty detection — when models disagree, flag it as a safety feature
- Wire both into AnalysisDashboard UI

### 🏥 Agent 2: Second-Opinion — Proper Build Pipeline
- Replace CDN Tailwind with PostCSS/Tailwind build (install tailwindcss, postcss, autoprefixer)
- Configure tailwind.config.js scanning all component files
- Create proper index.css with @tailwind directives
- Add Firebase Hosting deploy config (firebase.json, .firebaserc)
- Verify `npm run build` still works clean

### 🏥 Agent 3: Second-Opinion — Demo Mode UI + Self-Evaluation
- Add a visible demo mode toggle button in the app header
- Wire demo-mode.ts sample cases into a case selector dropdown
- Build model self-evaluation scoring (confidence calibration per model)
- Add "AI Uncertainty" badge when models disagree >30%

### 🎵 Agent 4: FlipMyEra — SEO + Loading UX + Error Boundaries
- Add SEO meta tags + Open Graph tags to index.html
- Add React Helmet for per-page dynamic meta
- Build loading skeleton components for main pages
- Wrap all route-level components with error boundaries
- Run tests to verify nothing breaks

### 🎵 Agent 5: FlipMyEra — Free Trial Credits + Stripe Webhooks
- Implement free credits on signup (grant X credits after profile creation)
- Add credit balance display in header/dashboard
- Write integration tests for Stripe webhook handlers
- Add rate limiting middleware on API-facing routes

### 📖 Agent 6: NarrativeReactor — Dotprompts + Express Routes
- Verify/create all 5 dotprompt templates (scene-gen, narrative-assembly, score-gen, previs-image, episode-copy)
- Build Express REST API routes for all flows (POST /api/generate, /api/compliance, /api/video, /api/chat, /api/social/*)
- Add basic auth middleware (API key-based)
- Add CORS and rate limiting
- Verify server starts and routes respond

### 📈 Agent 7: Trendpilot — Phase 2 Build (Scheduler + API)
- Build scheduler service (cron-triggered aggregation runs)
- Build REST API layer (GET /trends, GET /topics/:id, POST /subscribe)
- Add historical trend storage with timestamps
- Build email digest template generation
- Write Phase 2 tests for all new code

## Batch 2 (Launch after Batch 1 completes)

### 🏥 Agent 8: Second-Opinion — Full Test Suite + Polish
- Run all existing tests, fix any failures
- Write missing tests for new FHIR, uncertainty, demo mode features
- Polish landing page copy (compelling CTAs, competition-ready)
- Update README with architecture diagram (Mermaid)
- Final `npm run build` verification

### 🎵 Agent 9: FlipMyEra — Production Hardening
- Verify Sentry is reporting errors correctly
- Add Content Security Policy headers
- Review and harden Supabase RLS policies
- Performance audit (bundle size, lazy loading)
- Push all changes to main

### 📖 Agent 10: NarrativeReactor — Dashboard UI + n8n Webhooks  
- Build simple web dashboard (React or static HTML) for managing flows
- Add webhook endpoints for n8n integration (trigger flows via HTTP)
- Wire up real fal.ai credentials for image generation
- Add cost tracking per generation
- Deploy to Railway

## Batch 3 (Launch after Batch 2 completes)

### 🏥 Agent 11: Second-Opinion — Agentic Planning + Visual Grounding
Google wants agentic workflows. Build:
- Multi-step reasoning chain: triage → specialist routing → model selection → synthesis
- Visual grounding: when images are uploaded, annotate which regions each model focused on
- Add planning trace to the ProcessingLogWindow (show the agent's decision tree)
- Write tests for the planning logic

### 🏥 Agent 12: Second-Opinion — Accessibility + i18n Foundation
- Full WCAG 2.1 AA audit and fixes (aria labels, keyboard nav, focus management, contrast)
- Add screen reader announcements for pipeline status updates
- Set up i18n framework (react-i18next) with English base strings extracted
- Add Spanish translation file (medical AI = huge LatAm market)
- Test with axe-core automated accessibility checker

### 🎵 Agent 13: FlipMyEra — Analytics + A/B Testing + Conversion Funnel
- Wire PostHog (already in codebase) with proper event tracking
- Add funnel events: landing → signup → create_ebook → preview → purchase
- Build A/B test framework for pricing page (test $9.99 vs $14.99 vs $19.99)
- Add conversion dashboard page for admin
- Write tests for analytics events

### 🎵 Agent 14: FlipMyEra — Email Flows + Onboarding
- Build transactional email templates (welcome, purchase confirmation, ebook ready)
- Add onboarding wizard for first-time users (3-step: pick era → customize → preview)
- Implement email service integration (Resend or SendGrid via Supabase Edge Function)
- Add drip campaign triggers (abandoned cart, inactive user)
- Write tests for email template rendering

### 📖 Agent 15: NarrativeReactor — Social OAuth + Content Calendar
- Build real X/Twitter OAuth 2.0 PKCE flow (not just stubs)
- Add LinkedIn OAuth flow
- Build content calendar UI (weekly grid, drag-to-schedule)
- Implement scheduled post queue with timestamps
- Add post preview with platform-specific formatting (char limits, media)

### 📈 Agent 16: Trendpilot — Phase 3 (Alerting + User Profiles)
- Build user preference profiles (topics, keywords, industries to track)
- Implement threshold-based alerting (spike detection, velocity alerts)
- Add notification channels (email digest, webhook, Slack)
- Build trend comparison view (this week vs last week)
- Write Phase 3 tests

## Batch 4 (Launch after Batch 3 completes)

### 🏥 Agent 17: Second-Opinion — Performance + Offline + PWA Polish
- Lighthouse audit and optimize (target 90+ on all categories)
- Implement service worker caching strategies (stale-while-revalidate for API, cache-first for assets)
- Add offline analysis queue (store requests, sync when back online)
- Optimize bundle size (code splitting per route, tree shaking)
- Add app install prompt for mobile

### 🏥 Agent 18: Second-Opinion — Medical Knowledge Graph + Citations
- Build a medical knowledge graph linking conditions → symptoms → treatments → drugs
- Add citation system: every AI claim links back to source (PubMed, FDA, clinical guidelines)
- Implement "Evidence Strength" indicators (meta-analysis > RCT > case study)
- Wire into AnalysisDashboard as expandable citation cards
- Write tests for knowledge graph queries

### 🎵 Agent 19: FlipMyEra — Social Sharing + Referral System
- Build shareable ebook preview pages (public URLs with OG images)
- Add social share buttons (Twitter, Instagram Stories, TikTok link)
- Implement referral system (share link → friend signs up → both get credits)
- Build referral tracking dashboard for admin
- Add viral loop: finished ebook → "Share & earn credits" CTA

### 📖 Agent 20: NarrativeReactor — Multi-Channel Publishing + Analytics
- Build cross-platform publish pipeline (X + LinkedIn + Threads in one click)
- Add post performance tracking (pull engagement metrics after 24h/48h/7d)
- Build content performance dashboard (best times, top formats, engagement trends)
- Implement A/B copy testing (publish variant A to subset, measure, then full publish)
- Add content library (searchable archive of all generated content)

### 📈 Agent 21: Trendpilot — Phase 4 (Dashboard UI + Deploy)
- Build full web dashboard (React + Vite, simple and clean)
- Trend cards with sparkline charts
- Source attribution (which feeds spotted it first)
- Historical timeline view
- Deploy to Railway with proper env config

## Batch 5 (Launch after Batch 4 completes — stretch goals)

### 🏥 Agent 22: Second-Opinion — Competition Submission Package
- Final Kaggle writeup polish (all sections, citations, architecture diagram)
- Generate screenshots for writeup (landing, analysis, pipeline, results)
- Create deployment documentation (one-command setup)
- Final security audit (no API keys in code, proper .gitignore)
- Make repo public-ready (clean git history, LICENSE, CONTRIBUTING.md)

### 🎵 Agent 23: FlipMyEra — Launch Readiness Audit
- Full pre-launch checklist (DNS, SSL, error tracking, monitoring, backups)
- Load testing (simulate 100 concurrent users)
- Legal pages (Terms of Service, Privacy Policy templates)
- Build marketing landing page variant (focused on conversion)
- Create launch announcement content (tweet thread, Product Hunt draft)

### 📖 Agent 24: NarrativeReactor — AI Agent Collaboration
- Build agent-to-agent communication protocol (NarrativeReactor ↔ Trendpilot)
- Auto-generate content briefs from trending topics (Trendpilot feeds NarrativeReactor)
- Add feedback loop: social performance data → adjust content strategy
- Build "campaign mode" (multi-post narrative arc across days)
- Document the full AI mesh architecture

### 📈 Agent 25: Trendpilot — Phase 5 (Monetization + API Keys)
- Build API key management (generate, revoke, rate limit per key)
- Implement 4-tier pricing (Free/Starter/Pro/Enterprise)
- Add usage metering and billing integration (Stripe)
- Build public API documentation (OpenAPI spec)
- Create developer onboarding flow

### 🤖 Agent 26: Infrastructure — Full Mesh Wiring
- Verify all Railway services healthy (n8n, Postiz, NarrativeReactor, Trendpilot)
- Wire n8n viral video workflow (import + configure triggers)
- Connect Postiz to social accounts
- Build status dashboard that monitors all services
- Document the complete Railway architecture

## Batch 6 (Cross-Project Integration)

### 🏥 Agent 27: Second-Opinion — Patient Data Export + Interoperability
- Build PDF report generation (full analysis → downloadable medical report)
- Add HL7v2 message export (for hospital system integration)
- Build patient timeline view (all analyses chronologically)
- Implement data retention policies (auto-delete after X days, user-configurable)
- Add HIPAA compliance checklist component (visible trust signals)

### 🏥 Agent 28: Second-Opinion — Advanced AI Pipeline
- Add model ensemble voting (weighted consensus based on confidence + specialty match)
- Build specialist routing: dermatology images → skin-focused models, radiology → chest-focused
- Implement chain-of-thought display (show reasoning steps, not just conclusions)
- Add model performance benchmarking (track accuracy over time per model)
- Build A/B model testing framework (swap models without code changes)

### 🎵 Agent 29: FlipMyEra — Content Expansion + Templates
- Add new era templates beyond Taylor Swift (Beyoncé, Harry Styles, BTS, custom artist)
- Build template marketplace (users can create + share custom templates)
- Add collaborative ebook creation (invite friends to co-author)
- Implement ebook versioning (edit after creation, track changes)
- Build ebook gallery/showcase (public page of best creations)

### 🎵 Agent 30: FlipMyEra — Mobile Optimization + Native Feel
- Full responsive audit (every page looks great on mobile)
- Add touch gestures (swipe between ebook pages, pinch to zoom)
- Implement pull-to-refresh on dashboard
- Add haptic feedback triggers (on purchase, on ebook complete)
- Build app-like navigation (bottom tab bar on mobile, sidebar on desktop)

### 📖 Agent 31: NarrativeReactor — Voice + Audio Content
- Integrate Fish Audio TTS for audio content generation
- Build podcast script generator (from blog post → podcast episode)
- Add voiceover for video content (scene narration)
- Implement multi-voice dialogue (character A + character B voices)
- Build audio content library with playback UI

### 📈 Agent 32: Trendpilot — ML Trend Prediction
- Build trend velocity model (predict which topics will peak in 24/48/72h)
- Implement sentiment analysis on aggregated content
- Add geographic trend mapping (trending where?)
- Build "trend lifecycle" classifier (emerging → growing → peaking → declining)
- Create prediction accuracy tracking dashboard

## Batch 7 (Growth + Monetization)

### 🏥 Agent 33: Second-Opinion — Telemedicine Integration
- Build video consultation booking UI (connect with real doctors for follow-up)
- Add specialist directory with filtering (location, specialty, insurance)
- Implement consultation notes template (pre-filled from AI analysis)
- Build insurance pre-authorization document generator
- Add appointment reminder system (email + push)

### 🏥 Agent 34: Second-Opinion — Research Mode
- Build research paper search integration (PubMed API)
- Add clinical trial matching (ClinicalTrials.gov API)
- Implement drug interaction checker (OpenFDA API)
- Build research summary generator (AI summarizes relevant papers)
- Add "Similar Cases" feature (anonymized case matching)

### 🎵 Agent 35: FlipMyEra — Monetization Engine
- Build subscription tiers (Basic: 3 ebooks/mo, Pro: unlimited, Enterprise: API)
- Implement usage-based billing with Stripe metered pricing
- Add gift cards / gift ebook feature
- Build affiliate program (creators earn commission on referrals)
- Create revenue dashboard with MRR tracking, churn, LTV

### 🎵 Agent 36: FlipMyEra — AI Image Enhancement
- Integrate DALL-E / Stable Diffusion for custom ebook cover art
- Build image style transfer (apply era-specific visual themes)
- Add AI-generated illustrations for ebook chapters
- Implement image editor (crop, filter, text overlay)
- Build image asset library (pre-made stickers, borders, frames)

### 📖 Agent 37: NarrativeReactor — Campaign Intelligence
- Build competitor content tracker (monitor competitor social accounts)
- Add trending hashtag discovery + recommendation
- Implement optimal posting time calculator (per platform, per audience)
- Build audience persona builder (AI-generated from engagement data)
- Create weekly content strategy report (auto-generated)

### 📈 Agent 38: Trendpilot — White-Label + Multi-Tenant
- Build multi-tenant architecture (each customer gets isolated data)
- Add white-label theming (custom logo, colors, domain)
- Implement team management (invite members, role-based access)
- Build custom feed builder (customers pick their own sources)
- Add export API (CSV, JSON, webhook push)

## Batch 8 (Platform Maturity)

### 🏥 Agent 39: Second-Opinion — Multi-Language Medical AI
- Add medical terminology translation (EN → ES, FR, DE, ZH, PT)
- Implement language-aware prompts (adjust AI queries per language)
- Build medical glossary with plain-language explanations per locale
- Add right-to-left layout support (Arabic, Hebrew)
- Create locale-specific medical disclaimer templates

### 🎵 Agent 40: FlipMyEra — Creator Economy Features
- Build creator profiles (public pages with portfolio)
- Add tipping/support feature (fans can tip creators)
- Implement creator analytics (views, shares, earnings)
- Build featured creators section on homepage
- Add creator verification badges

### 📖 Agent 41: NarrativeReactor — Advanced Video Pipeline
- Build multi-scene video stitching (combine previs → transitions → final cut)
- Add subtitle/caption generation (auto from script)
- Implement video templates (product launch, case study, testimonial formats)
- Build video thumbnail generator (AI-selected best frame + text overlay)
- Add video performance prediction (estimate engagement before publishing)

### 📈 Agent 42: Trendpilot — Enterprise Features
- Build SSO integration (SAML, OAuth for enterprise customers)
- Add audit logging (who accessed what, when)
- Implement data retention + compliance controls (GDPR, SOC2 prep)
- Build admin console (user management, billing, usage)
- Add SLA monitoring dashboard

### 🤖 Agent 43: Infrastructure — Monitoring + Observability
- Set up centralized logging (aggregate logs from all Railway services)
- Build health check endpoints for every service
- Implement alerting (service down → Telegram notification)
- Add performance metrics collection (response times, error rates)
- Build Grafana-style metrics dashboard

### 🤖 Agent 44: Infrastructure — Backup + Disaster Recovery
- Implement automated Postgres backups (daily → S3/R2)
- Build Redis snapshot scheduling
- Create one-command restore scripts
- Document recovery procedures for each service
- Test backup/restore cycle end-to-end

## Batch 9 (Ecosystem + Network Effects)

### 🏥 Agent 45: Second-Opinion — Provider Portal
- Build doctor/provider dashboard (see patients who shared analyses)
- Add provider verification flow (NPI number lookup)
- Implement secure messaging (patient ↔ provider, encrypted)
- Build provider analytics (how many patients referred, outcomes)
- Add EHR integration stubs (Epic FHIR, Cerner)

### 🎵 Agent 46: FlipMyEra — Marketplace + UGC Platform
- Build ebook marketplace (browse + buy other creators' ebooks)
- Add ratings + reviews system
- Implement content moderation pipeline (AI + manual review)
- Build discovery algorithm (personalized recommendations)
- Add collections/playlists (curated ebook bundles)

### 📖 Agent 47: NarrativeReactor — Multi-Brand Management
- Build brand profiles (multiple brands per account, each with own guidelines)
- Add brand voice cloning (analyze existing content → replicate tone)
- Implement approval workflows (draft → review → approve → publish)
- Build brand consistency scorer (how on-brand is this content?)
- Add team collaboration (assign tasks, comments, revisions)

### 📈 Agent 48: Trendpilot — Data Partnerships + Enrichment
- Build data source marketplace (premium feeds: Bloomberg, Reuters stubs)
- Add social listening integration (track brand mentions)
- Implement influencer discovery (who's driving conversation on a topic)
- Build custom report generator (drag-and-drop report builder)
- Add API marketplace listing (publish to RapidAPI)

### 🤖 Agent 49: Infrastructure — CI/CD Pipeline Unification
- Build monorepo CI/CD (or unified pipeline across all project repos)
- Add automated dependency updates (Renovate/Dependabot)
- Implement staging environments per project (preview deploys)
- Build deployment status page (public status.forwardlane.com)
- Add rollback automation (one-click revert)

## Batch 10 (Vision — The AI Network)

### 🤖 Agent 50: AI Mesh — Agent Communication Protocol
- Design and implement agent-to-agent messaging (REST + events)
- Build shared context store (agents can read/write shared memory on Railway)
- Implement task delegation (Honey assigns work to specialist agents)
- Add agent health monitoring (heartbeat + capability registry)
- Document the protocol as an open spec

### 🤖 Agent 51: AI Mesh — Specialist Agent: Research Analyst
- Build a standalone research agent (separate Railway service)
- Capabilities: web search, paper analysis, competitive intelligence
- Expose via the agent communication protocol
- Auto-triggered by Trendpilot when new trends emerge
- Reports findings back to Honey for synthesis

### 🤖 Agent 52: AI Mesh — Specialist Agent: Content Creator
- Build a standalone content creation agent
- Capabilities: copy writing, image generation, video scripting
- Fed by NarrativeReactor briefs + Trendpilot trends
- Auto-publishes through Postiz
- Tracks performance and self-optimizes

### 🤖 Agent 53: AI Mesh — Specialist Agent: Customer Success
- Build a standalone customer support agent
- Capabilities: ticket triage, FAQ response, escalation routing
- Monitors FlipMyEra + Second-Opinion support channels
- Auto-responds to common questions, escalates complex issues to Nathan
- Learns from resolution patterns

### 🤖 Agent 54: AI Mesh — Orchestrator Dashboard
- Build the master control panel for the entire AI network
- Real-time view of all agents (status, current task, last output)
- Task queue management (assign, prioritize, cancel)
- Cost tracking per agent (API calls, compute, storage)
- Network topology visualization (who talks to whom)

### 🌐 Agent 55: ForwardLane.com — Website Rebuild
- Audit current ForwardLane.com
- Design modern landing page (hero, products, social proof, CTA)
- Build with Next.js + Tailwind (deploy to Vercel or Netlify)
- Wire in all products (Second-Opinion, FlipMyEra, Trendpilot, NarrativeReactor)
- SEO optimization + analytics setup

### 🌐 Agent 56: SignalHaus.ai — Website + Brand
- Audit current SignalHaus.ai
- Refresh brand identity (logo concepts, color palette, typography)
- Build modern website (product showcase, case studies, contact)
- Wire NarrativeReactor as the content engine
- Launch content calendar with initial 30 days of posts

## Execution Notes
- All agents work in isolation on their own project directory
- No cross-project dependencies within a batch
- Each agent runs tests before and after changes
- Each agent commits changes when done
- Batch N+1 launches automatically when Batch N reports complete
- Batches 1-3 are overnight priority; 4-5 are next day; 6-10 are the week ahead
- If any agent fails, log the error and continue — don't block the batch
