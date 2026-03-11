#!/usr/bin/env python3
"""
Unified Transcript Loader
Loads all parsed transcripts from Read.ai, Otter, and Motion into PostgreSQL.

Usage:
    export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
    python3 load_to_db.py
"""
import os, json, sys
from pathlib import Path
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import Json
except ImportError:
    print("Installing psycopg2...")
    os.system("pip install --break-system-packages psycopg2-binary")
    import psycopg2
    from psycopg2.extras import Json

DATABASE_URL = os.environ.get("DATABASE_URL")
TRANSCRIPT_DIRS = [
    Path("/data/workspace/transcripts/read-ai/parsed"),
    Path("/data/workspace/transcripts/otter/parsed"),
    Path("/data/workspace/transcripts/motion/parsed"),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS meeting_transcripts (
    id              SERIAL PRIMARY KEY,
    source          VARCHAR(20) NOT NULL,
    source_id       VARCHAR(255),
    title           TEXT,
    meeting_date    TIMESTAMP,
    duration_mins   INTEGER,
    participants    JSONB DEFAULT '[]',
    transcript_raw  TEXT,
    transcript_json JSONB DEFAULT '[]',
    summary         TEXT,
    action_items    JSONB DEFAULT '[]',
    key_topics      JSONB DEFAULT '[]',
    sentiment       JSONB DEFAULT '{}',
    recording_url   TEXT,
    source_url      TEXT,
    raw_json        JSONB,
    hubspot_deal_id VARCHAR(255),
    hubspot_contact_ids JSONB DEFAULT '[]',
    follow_up_status VARCHAR(50) DEFAULT 'pending',
    ai_insights     JSONB,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(source, source_id)
);

CREATE INDEX IF NOT EXISTS idx_transcripts_source ON meeting_transcripts(source);
CREATE INDEX IF NOT EXISTS idx_transcripts_date ON meeting_transcripts(meeting_date);
CREATE INDEX IF NOT EXISTS idx_transcripts_hubspot ON meeting_transcripts(hubspot_deal_id);
CREATE INDEX IF NOT EXISTS idx_transcripts_fts ON meeting_transcripts 
    USING gin(to_tsvector('english', COALESCE(transcript_raw, '')));
"""

INSERT = """
INSERT INTO meeting_transcripts 
    (source, source_id, title, meeting_date, duration_mins, participants,
     transcript_raw, transcript_json, summary, action_items, key_topics,
     sentiment, raw_json)
VALUES 
    (%(source)s, %(source_id)s, %(title)s, %(meeting_date)s, %(duration_mins)s, 
     %(participants)s, %(transcript_raw)s, %(transcript_json)s, %(summary)s,
     %(action_items)s, %(key_topics)s, %(sentiment)s, %(raw_json)s)
ON CONFLICT (source, source_id) DO UPDATE SET
    title = EXCLUDED.title,
    transcript_raw = EXCLUDED.transcript_raw,
    transcript_json = EXCLUDED.transcript_json,
    summary = EXCLUDED.summary,
    action_items = EXCLUDED.action_items,
    key_topics = EXCLUDED.key_topics,
    updated_at = NOW()
"""

def main():
    if not DATABASE_URL:
        print("ERROR: Set DATABASE_URL environment variable")
        print("  export DATABASE_URL='postgresql://user:pass@host:5432/dbname'")
        sys.exit(1)
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Create schema
    print("📦 Creating schema...")
    cur.execute(SCHEMA)
    conn.commit()
    print("  ✅ Schema ready")
    
    # Load all parsed transcripts
    total = 0
    for dir_path in TRANSCRIPT_DIRS:
        if not dir_path.exists():
            print(f"  ⏭️ Skipping {dir_path} (not found)")
            continue
        
        files = list(dir_path.glob("*.json"))
        print(f"\n📂 Loading {len(files)} files from {dir_path.parent.name}...")
        
        for filepath in sorted(files):
            try:
                with open(filepath) as f:
                    data = json.load(f)
                
                # Parse date
                meeting_date = data.get("meeting_date")
                if meeting_date and isinstance(meeting_date, str):
                    try:
                        meeting_date = datetime.fromisoformat(meeting_date.replace("Z", "+00:00"))
                    except:
                        meeting_date = None
                
                params = {
                    "source": data.get("source", "unknown"),
                    "source_id": str(data.get("source_id", filepath.stem)),
                    "title": data.get("title", "Untitled"),
                    "meeting_date": meeting_date,
                    "duration_mins": data.get("duration_mins"),
                    "participants": Json(data.get("participants", [])),
                    "transcript_raw": data.get("transcript_raw", ""),
                    "transcript_json": Json(data.get("transcript_json", [])),
                    "summary": data.get("summary", ""),
                    "action_items": Json(data.get("action_items", [])),
                    "key_topics": Json(data.get("key_topics", [])),
                    "sentiment": Json(data.get("sentiment", {})),
                    "raw_json": Json(data.get("raw_json", data.get("raw_text", ""))),
                }
                
                cur.execute(INSERT, params)
                total += 1
                
                title = data.get("title", "")[:50]
                print(f"  ✅ {data['source']}: {title}")
                
            except Exception as e:
                print(f"  ❌ {filepath.name}: {e}")
        
        conn.commit()
    
    # Summary
    cur.execute("SELECT source, COUNT(*), SUM(LENGTH(COALESCE(transcript_raw,''))) FROM meeting_transcripts GROUP BY source")
    print("\n📊 Database Summary:")
    print(f"{'Source':<15} {'Count':<10} {'Total Chars':<15}")
    print("-" * 40)
    for row in cur.fetchall():
        print(f"{row[0]:<15} {row[1]:<10} {row[2] or 0:<15,}")
    
    cur.execute("SELECT COUNT(*) FROM meeting_transcripts")
    print(f"\n✅ Total transcripts loaded: {cur.fetchone()[0]}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
