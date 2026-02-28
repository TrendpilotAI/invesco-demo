# SEO Analysis Automation Plan

## Overview

Automate Claude Cowork-style SEO analysis as an n8n workflow. Analyze websites, competitors, and Google Business Profiles to generate actionable SEO intelligence.

## Features to Build

### 1. Content Gap Finder
- **Input**: Target URL + competitor URLs
- **Process**: 
  - Scrape all page content from each site
  - Extract keywords, topics, headings
  - Compare to find gaps (topics target has that competitors don't)
- **Output**: List of 5+ topics to outrank competitors

### 2. Schema Auditor  
- **Input**: Target URL
- **Process**:
  - Scan all pages for existing JSON-LD schema
  - Identify missing schema types (Organization, Product, Article, FAQ, etc.)
  - Generate template JSON-LD for each missing type
- **Output**: Report of existing/missing schema + JSON-LD placeholders

### 3. Local Keyword Research
- **Input**: Business type, location
- **Process**:
  - Query local intent keywords
  - Analyze search volume + competition
- **Output**: Prioritized keyword list with metrics

### 4. Business Extractor
- **Input**: Business name or URL
- **Process**:
  - Extract NAP (Name, Address, Phone)
  - Fetch GBP data (reviews, posts, photos)
  - Find competitor businesses in area
- **Output**: Business profile + competitor intel

### 5. GBP Post Analyzer
- **Input**: GBP business ID or URL
- **Process**:
  - Fetch recent GBP posts
  - Analyze post frequency, content types, engagement
  - Identify posting gaps
- **Output**: GBP audit + posting recommendations

### 6. Competitor Gap Analysis
- **Input**: Target business + competitor list
- **Process**:
  - Compare web presence, content, keywords
  - Identify missing pages, keywords, backlinks
- **Output**: Actionable gap report

### 7. Keyword Research (Ahrefs-style)
- **Input**: Seed keywords
- **Process**:
  - Expand to related keywords
  - Extract volume, difficulty, CPC
  - Prioritize by intent + difficulty
- **Output**: Spreadsheet-ready keyword data

---

## n8n Workflow Architecture

```
┌─────────────┐
│   TRIGGER   │
│  (Webhook)  │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│              INPUT PARSER                     │
│  - target_url                                │
│  - competitors[]                             │
│  - keywords[]                                │
│  - location                                  │
│  - analysis_type (gap|schema|keywords|all)  │
└──────┬───────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│           SCRAPER COLLECTION                  │
├──────────────────────────────────────────────┤
│  • Website Scraper (target + competitors)     │
│  • GBP Fetcher (via Places API or scraping)   │
│  • Ahrefs API (keywords)                      │
│  • Google Search (local keywords)            │
└──────┬───────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│           ANALYSIS ENGINE                     │
├──────────────────────────────────────────────┤
│  • Content Gap Analyzer (LLM)                │
│  • Schema Detector (regex + LLM)             │
│  • Keyword Processor (dedupe + score)        │
│  • Competitor Comparator                     │
└──────┬───────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│           OUTPUT FORMATTING                   │
├──────────────────────────────────────────────┤
│  • Gap Report (markdown)                      │
│  • Schema JSON-LD (code blocks)               │
│  • Keyword Spreadsheet (CSV)                 │
│  • Posting Calendar (JSON)                   │
│  • PDF Report (optional)                     │
└──────┬───────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   RESPONSE  │
│  (Webhook)  │
└─────────────┘
```

---

## n8n Nodes Required

### Triggers
- **Webhook** — manual trigger
- **Schedule** — cron for recurring analysis

### HTTP & scraping
- **HTTP Request** — API calls
- **Puppeteer** or **Cheerio** — web scraping (via n8n-nodes-puppeteer)

### AI & Processing
- **OpenAI** — content analysis, gap detection
- **Code** node — data transformation
- **Merge** — combine multiple data sources

### Storage & Output
- **Google Sheets** — keyword spreadsheets
- **Slack/Discord** — notifications
- **Gmail** — email reports
- **S3/Storage** — save JSON/XML outputs

---

## Environment Variables

```env
# APIs
OPENAI_API_KEY=sk-...
AHREFS_API_KEY=xxxx
GOOGLE_PLACES_API_KEY=xxxx
SCRAPINGDOG_API_KEY=xxxx

# Scraping
PUPPETEER_SCREWS=...

# Storage
S3_BUCKET=...
S3_REGION=us-east-1
S3_ACCESS_KEY=...
S3_SECRET_KEY=...

# Notifications
SLACK_WEBHOOK_URL=...
DISCORD_WEBHOOK_URL=...
```

---

## Scheduled Runs

| Site/Business | Frequency | Analysis Types |
|---------------|-----------|----------------|
| SignalHaus | Weekly | gap, schema, keywords |
| FlipMyEra | Weekly | gap, keywords |
| ForwardLane | Weekly | gap, schema, keywords, gbp |
| New launches | Daily | all (first week) |

---

## Implementation Phases

### Phase 1: Core (Week 1)
- [ ] Webhook trigger + input parser
- [ ] Website scraper (target + 3 competitors)
- [ ] Basic gap analysis with OpenAI
- [ ] Markdown gap report output

### Phase 2: Schema (Week 2)
- [ ] Schema detector
- [ ] JSON-LD generator
- [ ] Combined audit report

### Phase 3: Local (Week 3)
- [ ] GBP post fetcher
- [ ] Local keyword research
- [ ] Posting recommendations

### Phase 4: Scale (Week 4)
- [ ] Multi-site support
- [ ] Scheduled runs
- [ ] Google Sheets output
- [ ] Slack notifications

---

## Quick Start

### Manual Run
```bash
curl -X POST https://n8n-production.up.railway.app/webhook/seo-analyze \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://example.com",
    "competitors": ["https://competitor1.com", "https://competitor2.com"],
    "analysis_type": "all"
  }'
```

### Schedule
Add Schedule Trigger node with cron: `0 9 * * 1` (Mondays 9am)

---

## Output Examples

### Gap Report
```markdown
## Content Gaps for example.com

### Topics to Outrank Competitors
1. **Local SEO Services** - competitor1 has, you don't
2. **Case Studies** - both competitors have rich case studies
3. **Video Testimonials** - only competitor2 has video content

### Recommendations
- Add "Local SEO" service page
- Create 3 case studies with measurable results
- Add video testimonials to homepage
```

### Schema Output
```json
{
  "missing": ["Product", "FAQPage"],
  "templates": {
    "Product": {
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "...",
      "description": "...",
      "offers": {
        "@type": "Offer",
        "price": "",
        "priceCurrency": "USD"
      }
    }
  }
}
```
