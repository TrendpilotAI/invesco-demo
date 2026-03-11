# Transcript Extraction Plan: Read.ai + Otter.ai + Motion

> Goal: Extract ALL historic transcripts from 3 locked-up silos → unified PostgreSQL database
> Status: Ready to execute once Nathan provides credentials

---

## Summary of Extraction Methods

| Tool | Method | Difficulty | Data Format | Auth Needed |
|------|--------|-----------|-------------|-------------|
| **Read.ai** | REST API (open beta) | ✅ Easy | JSON (transcript + summary + action items) | API Bearer token |
| **Otter.ai** | Bulk export UI + API (enterprise) | ⚠️ Medium | TXT/DOCX/PDF (manual) or JSON (API) | Login for manual; OAuth2 for API |
| **Motion** | Full data export + API | ⚠️ Medium | ZIP of JSON files | Settings export + API key |

---

## Tool 1: Read.ai — API Extraction (Easiest)

### What We Get
- Full meeting transcripts with speaker labels
- AI-generated summaries
- Action items
- Key questions
- Topics discussed
- Participant reactions & sentiments
- Meeting metadata (date, duration, participants)

### API Details
- **Base URL:** `https://api.read.ai/`
- **Auth:** Bearer token in `Authorization` header
- **Rate Limits:** Not documented (beta), assume conservative

### Endpoints
```
GET /v1/meetings                    → List all meetings (paginated, reverse chronological)
GET /v1/meetings/{id}?expand[]=transcript&expand[]=summary&expand[]=action_items
                                    → Get full meeting with transcript
```

### Steps for Nathan
1. Go to Read.ai → Settings → API (or Developer section)
2. Generate an API key / Bearer token
3. Share it with Honey (save as env var)

### Script Will Do
1. Paginate through ALL meetings via `/v1/meetings`
2. For each meeting, fetch full details with `expand[]=transcript`
3. Store raw JSON in `/data/workspace/transcripts/read-ai/raw/`
4. Parse and load into PostgreSQL

---

## Tool 2: Otter.ai — Dual Extraction (Manual + API)

### Path A: Bulk Export (Immediate, No API Needed)

#### What We Get
- Transcripts in TXT/DOCX/PDF format
- Audio files (optional)
- "Takeaways" (summaries + action items)

#### Steps for Nathan
1. Go to https://otter.ai/home
2. Click "My Conversations"
3. Select ALL conversations (checkbox at top)
4. Click "Export" → Choose format (TXT is most parseable, DOCX for formatting)
5. Wait for email with ZIP download link
6. Download ZIP and upload to Google Drive or share with Honey

### Path B: API (Enterprise Only)

#### API Details
- **Docs:** https://developer-guides.tryotter.com/api-reference/
- **Auth:** OAuth 2.0 (client_id + client_secret from account manager)
- **Availability:** Enterprise plans only

#### If Enterprise Access Available
```
POST /oauth/token                   → Get access token
GET /v2/meetings                    → List meetings
GET /v2/meetings/{id}/transcript    → Full transcript with speaker labels + timestamps
GET /v2/meetings/{id}/summary      → AI summary
GET /v2/meetings/{id}/action-items  → Action items
```

### Recommendation
**Start with Path A (manual bulk export)** — it's available RIGHT NOW on any plan. I'll build a parser to convert the TXT/DOCX files into structured JSON for our database.

---

## Tool 3: Motion — Full Data Export

### What We Get
- Tasks, projects, notes (JSON format)
- AI Notetaker transcripts (if stored as Motion docs)
- Meeting summaries and action items

### Path A: Settings Export (Immediate)

#### Steps for Nathan
1. Go to https://app.usemotion.com
2. Settings → scroll to bottom → "Export all data"
3. Click export → wait for processing
4. Download ZIP file (contains folders + JSON files)

### Path B: API (Limited)

#### API Details
- **Base URL:** `https://api.usemotion.com/v1`
- **Auth:** `X-API-Key` header
- **Docs:** https://docs.usemotion.com/api-reference/

#### Relevant Endpoints
```
GET /v1/projects                    → List projects
GET /v1/projects/{id}               → Project details
POST /v1/notes/query                → Search notes (beta)
GET /v1/notes/{id}                  → Get note by ID
```

### Notes
- Motion's API is more task/project-focused
- Transcript data likely lives in "Notes" or "Docs"
- Full data export is the safest bet for getting everything

---

## Database Schema (Target)

```sql
CREATE TABLE meeting_transcripts (
    id              SERIAL PRIMARY KEY,
    source          VARCHAR(20) NOT NULL,  -- 'read_ai', 'otter', 'motion'
    source_id       VARCHAR(255),          -- Original ID from source platform
    title           TEXT,
    meeting_date    TIMESTAMP,
    duration_mins   INTEGER,
    participants    JSONB,                 -- [{name, email, role}]
    
    -- Content
    transcript_raw  TEXT,                  -- Full transcript text
    transcript_json JSONB,                 -- Structured: [{speaker, text, timestamp}]
    summary         TEXT,                  -- AI-generated summary
    action_items    JSONB,                 -- [{item, assignee, due_date}]
    key_topics      JSONB,                 -- [topic1, topic2, ...]
    sentiment       JSONB,                 -- {overall, by_participant}
    
    -- Metadata
    recording_url   TEXT,
    source_url      TEXT,                  -- Link back to original
    raw_json        JSONB,                 -- Complete raw response
    
    -- Our enrichment
    hubspot_deal_id VARCHAR(255),          -- Linked HubSpot deal
    hubspot_contact_ids JSONB,             -- Linked contacts
    follow_up_status VARCHAR(50),          -- 'pending', 'done', 'overdue'
    ai_insights     JSONB,                 -- Honey's analysis
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX idx_transcripts_source ON meeting_transcripts(source);
CREATE INDEX idx_transcripts_date ON meeting_transcripts(meeting_date);
CREATE INDEX idx_transcripts_hubspot ON meeting_transcripts(hubspot_deal_id);

-- Full-text search on transcripts
CREATE INDEX idx_transcripts_fts ON meeting_transcripts 
    USING gin(to_tsvector('english', transcript_raw));
```

---

## What Nathan Needs To Do (Action Items)

### Immediate (5 minutes each)
1. **Read.ai** → Generate API key → Share with Honey
2. **Otter.ai** → Bulk export ALL conversations → Download ZIP → Upload
3. **Motion** → Settings → Export all data → Download ZIP → Upload

### After Export
- Honey runs extraction scripts automatically
- All transcripts loaded into PostgreSQL
- AI enrichment layer adds: deal linkage, follow-up tracking, insight extraction
- HubSpot sync connects transcripts to contacts/deals

---

## Post-Extraction: The Leverage Play

Once all transcripts are in our database, Honey can:

1. **Cross-reference with HubSpot** — Link transcripts to deals/contacts automatically by matching participant emails
2. **Extract missed follow-ups** — Find every "I'll send you X" or "Let's schedule Y" that never happened
3. **Identify buying signals** — NL→SQL query: "Show me all meetings where budget was discussed but no proposal followed"
4. **Build client intelligence profiles** — Aggregate all conversations per client into a living brief
5. **Generate proactive outreach** — "You met with Craig 3 weeks ago, discussed X, no follow-up yet"
6. **Train Signal Studio** — Real conversation data to improve our NL→SQL models
