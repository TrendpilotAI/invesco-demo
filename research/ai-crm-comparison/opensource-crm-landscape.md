# Open-Source & Self-Hosted CRM Landscape
*Research date: March 2026 | Compiled by Freya (GTM & Analysis)*

---

## Overview

Open-source CRMs have experienced a renaissance driven by three trends:
1. **Privacy/data sovereignty concerns** — companies want to own their data
2. **Railway/Docker deployment** — self-hosting is now genuinely easy
3. **AI integration** — open-source tools can plug into OpenAI/Anthropic APIs

The key question for Nathan's stack: **can we deploy on Railway, connect to our Data Waterfall, and not spend engineering time maintaining it?**

---

## 1. Twenty CRM (⭐ Top Recommendation)

**GitHub:** github.com/twentyhq/twenty | **Stars:** ~40,340 (Feb 2026) | **License:** AGPL-3.0

### What It Is
Twenty is the open-source alternative to Salesforce — built modern (TypeScript/React/NestJS), API-first, with a beautiful UI inspired by Notion. Founded 2023 by Charles Bochet's team. Growing extremely fast (20K stars in Nov 2024 → 40K stars by Feb 2026).

### Features
- Contact and company management with custom fields
- Pipeline visualization (Kanban and Table views)
- Custom objects for any data structure
- Email and calendar synchronization (IMAP + CalDAV support)
- Role-based and field-level permissions
- Two-factor authentication
- Workflow automation engine
- GraphQL + REST APIs (excellent API quality)
- CSV import/export
- Notes and tasks linked to records
- Data migration tools
- Duplicate record merging

### AI Capabilities
- No native AI features built in (as of early 2026)
- **BUT** the API-first architecture means AI can be bolted on via n8n workflows
- Can connect to OpenAI, Anthropic, or local models via custom integrations
- Community is actively building AI extensions

### Railway Deployment
- **Official Railway template** exists (created Feb 21, 2025)
- Template includes: Twenty app + Twenty Worker + PostgreSQL + Redis + Storage bucket
- Uses `twentycrm/twenty:v1.17.0` image
- **Requires Railway Hobby or Pro plan** (free tier doesn't have enough memory)
- Railway Pro plan: ~$20/mo + resource usage (~$35-60/mo total estimated)
- Setup is straightforward with the template

### Self-Hosting Requirements
- PostgreSQL database
- Redis cache
- Object storage (S3-compatible or local)
- Two Docker containers (app + worker)
- ~1-2GB RAM minimum

### Customization Potential
- **Very high** — custom objects, custom fields, custom workflows
- TypeScript/React frontend is hackable
- NestJS backend is extensible
- Plugin/extension architecture in development

### Community Size
- 40K+ GitHub stars (fastest-growing CRM on GitHub)
- Active Discord community
- Regular releases (v1.17+)
- Well-funded project (VC-backed)

### Pricing (Self-Hosted)
- Software: **Free**
- Railway hosting: **~$35-60/mo** (PostgreSQL + Redis + app)
- Total: **~$35-60/mo** for unlimited users

### Integrations
- Email (IMAP/SMTP)
- Calendar (CalDAV)
- REST API + GraphQL
- Webhooks
- Zapier/n8n via API

### Strengths
- Best UI/UX of any open-source CRM by far
- Modern tech stack (maintainable by Nathan's team)
- Official Railway template (5-minute deploy)
- Fastest-growing open-source CRM
- API-first means everything is connectable
- No user limits
- Full data ownership

### Weaknesses
- No native AI features (must build your own)
- Not as feature-rich as Salesforce/HubSpot out-of-the-box
- Self-hosting requires some ongoing maintenance
- Still maturing (some features in progress)

### Verdict for Nathan: 9/10
Twenty is the clear winner for self-hosted. Modern stack, easy Railway deploy, API-first, and Nathan's team can literally build AI features on top of it using n8n + OpenClaw. The 40K stars and active development indicate this isn't a dead project.

---

## 2. ERPNext / Frappe CRM

**GitHub:** github.com/frappe/erpnext | **Stars:** ~23K | **License:** GPL-3.0

### What It Is
ERPNext is a comprehensive open-source ERP (finance, HR, inventory, manufacturing) with a CRM module. Frappe CRM is the standalone CRM from the same team. Frappe Framework is the underlying platform.

### CRM Features
- Lead and opportunity management
- Contact and customer management
- Email campaigns and marketing
- Customer portal
- Analytics and reports
- Territory and sales team management
- Integration with ERPNext modules (invoicing, quotations, etc.)

### AI Capabilities
- No native AI in base product
- Can integrate via Frappe's extensibility framework
- Community plugins exist for AI features
- OpenAI integration possible via custom development

### Railway Deployment
- **Official Railway template** exists
- Docker-based deployment
- Somewhat complex setup (MariaDB + Redis + Frappe/ERPNext containers)
- Single-container mode available using Supervisor
- **Has deployment challenges** — more complex than Twenty
- Memory-intensive

### Self-Hosting Requirements
- MariaDB (not PostgreSQL — different from most modern tools)
- Redis
- Multiple workers (scheduler, queue workers)
- Minimum ~2-4GB RAM for stable operation

### Customization Potential
- **Very high** — Frappe Framework is a Python low-code platform
- Custom DocTypes (like custom objects)
- Extensive hooks and overrides
- Large partner/consultant ecosystem

### Community Size
- ERPNext: 23K stars
- Frappe CRM: ~3.5K stars separately
- Large community, especially in South Asia and Middle East
- Active forums (discuss.frappe.io)

### Pricing (Self-Hosted)
- Software: **Free**
- Railway hosting: **~$50-80/mo** (more resources needed than Twenty)
- Frappe Cloud managed hosting: $25-100/mo per site

### Integrations
- REST API
- Webhooks
- Email/calendar
- WhatsApp (Twilio)
- Payment gateways
- ERPNext modules (if using full ERP)

### Strengths
- Full ERP if you grow into needing invoicing, HR, etc.
- Very customizable Python platform
- Strong professional services ecosystem

### Weaknesses
- Complex to deploy and maintain
- Uses MariaDB (not PostgreSQL — incompatible with Nathan's existing Postgres setup)
- UI is dated compared to Twenty
- CRM module is secondary to ERPNext's ERP focus
- Overkill for a 2-5 person team

### Verdict for Nathan: 5/10
Too complex. The MariaDB dependency is a friction point given Nathan's PostgreSQL-first stack. ERPNext's strength is as a full ERP — using it just for CRM is like buying a truck to carry groceries.

---

## 3. SuiteCRM

**GitHub:** github.com/SuiteCRM/SuiteCRM | **Stars:** ~5,300 | **License:** AGPL-3.0

### What It Is
SuiteCRM is the most mature open-source CRM — a community fork of SugarCRM Open Source. Often called the "open-source Salesforce alternative." Very feature-rich but shows its age (originally built in 2004 as SugarCRM).

### Features
- Full sales pipeline management
- Marketing automation (campaigns, email marketing)
- Customer service module
- Reporting and analytics
- Workflow automation
- Custom modules
- Multi-currency and multi-language
- REST API

### AI Capabilities
- No native AI features
- SuiteCRM Store has community add-ons
- AI integration would require custom development
- Architecture is PHP/Symfony — less modern for AI integration

### Railway Deployment
- Docker images available
- Not an official Railway template
- PHP + MySQL stack — more complex for modern deployment
- Older architecture makes containerization trickier

### Self-Hosting Requirements
- MySQL/MariaDB
- PHP 8.x
- Web server (Apache/Nginx)
- Minimum 2GB RAM

### Customization Potential
- High — long history of customization
- Many third-party modules available
- But architecture is dated PHP monolith

### Community Size
- 5.3K GitHub stars
- Long-established community
- Regular maintenance releases (SuiteCRM 7.15, Dec 2025; SuiteCRM 8.9.2, Jan 2026)
- SuiteCRM 8 is a rewrite with better modern architecture

### Pricing (Self-Hosted)
- Software: **Free**
- Railway hosting: **~$40-60/mo**

### Strengths
- Most feature-complete open-source CRM
- 20+ years of feature development
- Strong partner ecosystem
- SuiteCRM 8 is significantly modernized

### Weaknesses
- PHP legacy architecture
- UI is dated (improving with SuiteCRM 8)
- No AI capabilities
- Lower GitHub star growth (less momentum than Twenty)
- More complex setup than Twenty

### Verdict for Nathan: 3/10
Too dated and complex. No AI capabilities. Twenty provides a better modern alternative.

---

## 4. Odoo CRM

**GitHub:** github.com/odoo/odoo | **Stars:** ~40K | **License:** LGPL-3.0 (Community) / Proprietary (Enterprise)

### What It Is
Odoo is a modular ERP/CRM platform. The Community edition is open-source (but limited). The Enterprise edition is proprietary ($). Odoo CRM is a module within the larger Odoo suite (30+ modules including accounting, HR, manufacturing, etc.).

### CRM Features
- Pipeline management with Kanban view
- Lead mining and scoring
- Email marketing campaigns
- Activity scheduling
- Customer portal
- Sales quotations
- Advanced reporting
- Territory management

### AI Capabilities
- **Odoo 18+ has AI features** (announced 2024-2025)
- AI in email writing (Enterprise edition)
- AI for translation
- AI assistance in Studio (low-code builder)
- More AI features in Enterprise vs. Community
- Odoo.ai is building deeper AI agents (timeline unclear)

### Railway Deployment
- **Official Railway template** for Odoo 19 with PostgreSQL
- Uses Railway's managed PostgreSQL
- Estimated cost: **~$35-50/mo** on Railway
- Simpler than ERPNext deployment

### Self-Hosting Requirements
- PostgreSQL (good — matches Nathan's stack)
- Python 3.10+
- Minimum 2GB RAM (4GB recommended)

### Customization Potential
- Very high — Python-based, modular architecture
- Odoo Studio (low-code builder) in Enterprise
- Large global partner ecosystem
- Custom modules can be built

### Community Size
- 40K GitHub stars
- Massive global community
- 12M+ users worldwide
- Annual Odoo Experience conference

### Pricing
| Version | Price |
|---------|-------|
| Community (self-hosted) | Free |
| Enterprise (hosted) | ~$19.90-38.90/user/mo |
| Railway self-hosting | ~$35-50/mo (infra only) |

### Strengths
- PostgreSQL-compatible (matches Nathan's stack)
- Grow into full ERP if needed
- Odoo 19 Railway template
- Strong community and ecosystem
- AI features coming in Enterprise

### Weaknesses
- Community edition is significantly limited vs. Enterprise
- Best features require Enterprise license (per-user cost)
- Complex — not for 2-5 person teams without an admin
- CRM module quality is mixed reviews for pure sales use

### Verdict for Nathan: 5/10
The PostgreSQL compatibility is nice and Railway template exists. But for CRM-only use, it's overkill. If Nathan ever needs ERP features (invoicing, HR, project management all in one), Odoo becomes more compelling.

---

## 5. EspoCRM

**GitHub:** github.com/espocrm/espocrm | **Stars:** ~2,800 | **License:** AGPL-3.0

### What It Is
EspoCRM is a lightweight, modern-feeling open-source CRM. Clean UI, not trying to be an ERP. Actively maintained (EspoCRM 9.3.2 released March 6, 2026).

### Features
- Contact and account management
- Sales pipeline (leads, opportunities)
- Email campaigns
- Activity tracking
- VoIP calling integration
- Custom fields and entities
- Reports and dashboards
- REST API
- Calendar integration
- Portal for customer access

### AI Capabilities
- No native AI
- Can integrate via API
- Community extensions available

### Railway Deployment
- Docker images available
- PHP-based, similar complexity to SuiteCRM
- No official Railway template
- MySQL/MariaDB + PHP stack

### Self-Hosting Requirements
- MySQL or MariaDB (not PostgreSQL natively, though extensions exist)
- PHP 8.1+
- Web server
- Minimum 1GB RAM (lighter than alternatives)

### Customization Potential
- Medium-high — entity framework for custom objects
- Extension system
- PHP-based (accessible)

### Community Size
- 2.8K GitHub stars (smaller but active)
- Active forum and issue tracker
- Regular releases

### Pricing (Self-Hosted)
- Software: **Free**
- Railway hosting: **~$30-40/mo** (lighter resource needs)

### Strengths
- Lightweight and fast
- Clean, modern UI for an open-source CRM
- Active development (recent March 2026 release)
- Lower hosting costs

### Weaknesses
- Small community vs. Twenty/Odoo
- MySQL dependency (not PostgreSQL native)
- No AI features
- Limited ecosystem

### Verdict for Nathan: 4/10
Decent lightweight option but smaller community and no PostgreSQL native support. Twenty is better.

---

## 6. Monica CRM

**GitHub:** github.com/monicahq/monica | **Stars:** ~22K | **License:** AGPL-3.0

### What It Is
Monica is a **Personal Relationship Manager (PRM)** — NOT a B2B sales CRM. It's designed for individuals to track personal relationships (friends, family, acquaintances). Beautiful UI, privacy-focused, Docker-deployable.

### Features
- Contact management with detailed profiles
- Interaction logging
- Reminder system (birthdays, anniversaries)
- Task management
- Notes and journals
- Gift tracking
- Relationship mapping
- Multi-user (share with partner/family)

### AI Capabilities
- Monica.im (the hosted version) has AI features as of 2025
- Self-hosted version: no native AI
- AI assistant mode for personal context

### Self-Hosting
- Docker-based, straightforward
- PostgreSQL or MySQL
- Very lightweight (~512MB RAM)

### Verdict for Nathan: 1/10
Wrong tool entirely — personal CRM, not B2B sales. Not relevant for ForwardLane/SignalHaus GTM.

---

## 7. Huly — Open-Source All-in-One

**GitHub:** github.com/hcengineering/platform | **Stars:** ~18K+ | **License:** EPL-2.0

### What It Is
Huly is an open-source alternative to Linear + Jira + Slack + Notion + CRM in one platform. The CRM module is one part of a larger "all-in-one workspace" play.

### Features
- Project and task management (Linear alternative)
- CRM (contacts, deals, pipeline)
- HRM and ATS (hiring)
- Team chat and virtual office
- Document editing
- GitHub bidirectional sync (issues, projects, milestones)
- AI transcription (Hulia assistant) for meetings

### AI Capabilities
- **Hulia AI assistant** for meeting transcription (real-time, Dec 2025)
- AI summarization of conversations
- More AI features in development

### Railway/Docker Deployment
- Docker Compose support (official)
- Available on Elest.io as managed service
- Complex multi-service deployment (chat, collaboration, CRM, etc.)

### Self-Hosting Requirements
- Multiple services (complex Docker Compose setup)
- MongoDB + Elastic + MinIO + multiple service containers
- High resource requirements (~4-8GB RAM for full suite)

### Community Size
- 18K+ GitHub stars
- Active community
- Backed by HardCode Labs

### Pricing (Self-Hosted)
- Software: Free
- Infrastructure: Moderate-high due to multi-service complexity

### Verdict for Nathan: 6/10
Very interesting if you want to **replace Motion + Asana + Slack + CRM** with one self-hosted tool. The CRM module is less mature than Twenty but the project management is excellent. The AI meeting transcription is relevant. Worth watching as a potential future consolidation play.

---

## 8. Chatwoot — Customer Engagement Platform

**GitHub:** github.com/chatwoot/chatwoot | **Stars:** ~22K | **License:** MIT / Enterprise**

### What It Is
Chatwoot is a customer support and engagement platform — NOT a B2B sales CRM. It's the open-source alternative to Intercom, Zendesk, Freshdesk. Live chat, email, social media, and WhatsApp support in one inbox.

### Features
- Multi-channel inbox (email, chat, social, WhatsApp, SMS)
- Contact management
- Team collaboration
- Automation workflows
- CRM-adjacent contact history
- Reports and analytics
- Self-service knowledge base

### AI Capabilities
- AI-powered suggestions and responses (via integration)
- GPT-powered reply suggestions
- Auto-labeling and categorization

### Railway Deployment
- Official Railway template available
- PostgreSQL + Redis + Rails app
- Well-documented deployment
- ~$30-50/mo on Railway

### Verdict for Nathan: 4/10
Relevant if SignalHaus has inbound customer support needs. Not a sales CRM. Could be useful if they build a product with support requirements.

---

## 9. Cal.com — Open-Source Scheduling

**GitHub:** github.com/calcom/cal.com | **Stars:** ~34K | **License:** AGPL-3.0

### What It Is
Cal.com is the open-source Calendly alternative. CRM-adjacent in that it tracks meeting requests, scheduling, and can be integrated into sales flows. Not a CRM.

### Features
- Meeting scheduling with calendar integration
- Team scheduling
- Workflows (automated emails/SMS)
- Analytics on booking patterns
- Embeddable booking widget
- Custom questions
- Zapier/webhook integration

### AI Capabilities
- AI-powered scheduling assistant (in development)
- Meeting prep summaries (roadmap)

### Railway Deployment
- Docker/Kubernetes deployment
- PostgreSQL
- Well-documented

### Verdict for Nathan: 5/10 as a scheduling tool
Relevant as a standalone tool to replace Calendly. Not a CRM but useful in the sales stack. The open-source version can be self-hosted for near-zero cost.

---

## GitHub Stars Summary (March 2026)

| CRM | Stars | Activity | Railway Template |
|-----|-------|----------|-----------------|
| Twenty CRM | ~40K | ⭐⭐⭐⭐⭐ (hot) | ✅ Official |
| Odoo | ~40K | ⭐⭐⭐⭐⭐ (mature) | ✅ Official |
| Cal.com | ~34K | ⭐⭐⭐⭐⭐ | ✅ |
| Chatwoot | ~22K | ⭐⭐⭐⭐ | ✅ Official |
| Monica | ~22K | ⭐⭐⭐⭐ | Via Docker |
| ERPNext | ~23K | ⭐⭐⭐⭐ | ✅ Official |
| Huly | ~18K | ⭐⭐⭐⭐ | Via Docker |
| SuiteCRM | ~5.3K | ⭐⭐⭐ | Via Docker |
| EspoCRM | ~2.8K | ⭐⭐⭐ | Via Docker |

---

## Self-Hosted Cost Comparison (Railway, Monthly)

| Tool | Software Cost | Railway Infra | Total/mo | Users |
|------|--------------|---------------|----------|-------|
| Twenty CRM | $0 | ~$35-60 | **$35-60** | Unlimited |
| Odoo Community | $0 | ~$35-50 | **$35-50** | Unlimited |
| ERPNext | $0 | ~$50-80 | **$50-80** | Unlimited |
| EspoCRM | $0 | ~$30-40 | **$30-40** | Unlimited |
| SuiteCRM | $0 | ~$40-60 | **$40-60** | Unlimited |
| Huly | $0 | ~$60-100 | **$60-100** | Unlimited |
| Chatwoot | $0 | ~$30-50 | **$30-50** | Unlimited |

Compare to SaaS: HubSpot Professional for 5 users = $500/mo. **Self-hosting savings: $440-465/mo.**
