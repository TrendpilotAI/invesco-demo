#!/usr/bin/env python3
"""
Read.ai Transcript Extractor
Pulls ALL meeting transcripts via Read.ai REST API.

Usage:
    export READ_AI_API_KEY="your_bearer_token"
    python3 extract_read_ai.py
"""
import os, json, time, sys
from datetime import datetime
from pathlib import Path
import requests

API_BASE = "https://api.read.ai"
API_KEY = os.environ.get("READ_AI_API_KEY")
OUTPUT_DIR = Path("/data/workspace/transcripts/read-ai/raw")
PARSED_DIR = Path("/data/workspace/transcripts/read-ai/parsed")

def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

def list_meetings(cursor=None):
    """List meetings with pagination."""
    url = f"{API_BASE}/v1/meetings"
    params = {}
    if cursor:
        params["cursor"] = cursor
    
    resp = requests.get(url, headers=get_headers(), params=params)
    resp.raise_for_status()
    return resp.json()

def get_meeting(meeting_id):
    """Get full meeting details with transcript expanded."""
    url = f"{API_BASE}/v1/meetings/{meeting_id}"
    params = {
        "expand[]": ["transcript", "summary", "action_items", "key_questions", "topics"]
    }
    
    resp = requests.get(url, headers=get_headers(), params=params)
    resp.raise_for_status()
    return resp.json()

def parse_meeting(raw):
    """Parse raw Read.ai meeting into our standard format."""
    parsed = {
        "source": "read_ai",
        "source_id": raw.get("id"),
        "title": raw.get("title") or raw.get("subject") or "Untitled Meeting",
        "meeting_date": raw.get("start_time") or raw.get("created_at"),
        "duration_mins": None,
        "participants": [],
        "transcript_raw": "",
        "transcript_json": [],
        "summary": "",
        "action_items": [],
        "key_topics": [],
        "sentiment": {},
        "raw_json": raw,
    }
    
    # Duration
    start = raw.get("start_time")
    end = raw.get("end_time")
    if start and end:
        try:
            s = datetime.fromisoformat(start.replace("Z", "+00:00"))
            e = datetime.fromisoformat(end.replace("Z", "+00:00"))
            parsed["duration_mins"] = int((e - s).total_seconds() / 60)
        except:
            pass
    
    # Participants
    for p in raw.get("participants", []):
        parsed["participants"].append({
            "name": p.get("name", ""),
            "email": p.get("email", ""),
            "role": p.get("role", "participant"),
        })
    
    # Transcript
    transcript = raw.get("transcript", {})
    if isinstance(transcript, dict):
        entries = transcript.get("entries", []) or transcript.get("segments", [])
    elif isinstance(transcript, list):
        entries = transcript
    else:
        entries = []
    
    lines = []
    for entry in entries:
        speaker = entry.get("speaker", entry.get("speaker_name", "Unknown"))
        text = entry.get("text", entry.get("content", ""))
        ts = entry.get("start_time", entry.get("timestamp", ""))
        lines.append(f"[{speaker}]: {text}")
        parsed["transcript_json"].append({
            "speaker": speaker,
            "text": text,
            "timestamp": ts,
        })
    parsed["transcript_raw"] = "\n".join(lines)
    
    # Summary
    summary = raw.get("summary", "")
    if isinstance(summary, dict):
        summary = summary.get("text", summary.get("content", str(summary)))
    parsed["summary"] = summary
    
    # Action items
    actions = raw.get("action_items", [])
    if isinstance(actions, list):
        for a in actions:
            if isinstance(a, dict):
                parsed["action_items"].append({
                    "item": a.get("text", a.get("content", str(a))),
                    "assignee": a.get("assignee", ""),
                    "due_date": a.get("due_date", ""),
                })
            else:
                parsed["action_items"].append({"item": str(a), "assignee": "", "due_date": ""})
    
    # Topics
    topics = raw.get("topics", raw.get("key_topics", []))
    if isinstance(topics, list):
        parsed["key_topics"] = [t.get("name", str(t)) if isinstance(t, dict) else str(t) for t in topics]
    
    return parsed

def main():
    if not API_KEY:
        print("ERROR: Set READ_AI_API_KEY environment variable")
        print("  Go to Read.ai → Settings → API → Generate key")
        sys.exit(1)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    
    print("🔍 Fetching Read.ai meetings...")
    
    all_meetings = []
    cursor = None
    page = 0
    
    while True:
        page += 1
        print(f"  Page {page}...", end=" ")
        
        try:
            result = list_meetings(cursor)
        except requests.exceptions.HTTPError as e:
            print(f"API Error: {e}")
            break
        
        meetings = result.get("data", result.get("meetings", []))
        if not meetings:
            print("no more meetings.")
            break
        
        print(f"{len(meetings)} meetings found")
        all_meetings.extend(meetings)
        
        # Check for next page
        cursor = result.get("next_cursor", result.get("pagination", {}).get("next_cursor"))
        if not cursor:
            break
        
        time.sleep(0.5)  # Rate limiting
    
    print(f"\n📥 Total meetings: {len(all_meetings)}")
    print("📝 Fetching full transcripts...")
    
    for i, meeting in enumerate(all_meetings):
        mid = meeting.get("id")
        title = meeting.get("title", "untitled")[:50]
        print(f"  [{i+1}/{len(all_meetings)}] {title}...", end=" ")
        
        try:
            full = get_meeting(mid)
            
            # Save raw
            raw_path = OUTPUT_DIR / f"{mid}.json"
            with open(raw_path, "w") as f:
                json.dump(full, f, indent=2, default=str)
            
            # Parse and save
            parsed = parse_meeting(full)
            parsed_path = PARSED_DIR / f"{mid}.json"
            with open(parsed_path, "w") as f:
                json.dump(parsed, f, indent=2, default=str)
            
            transcript_len = len(parsed["transcript_raw"])
            print(f"✅ ({transcript_len} chars)")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(0.3)
    
    print(f"\n✅ Done! Raw files: {OUTPUT_DIR}")
    print(f"✅ Parsed files: {PARSED_DIR}")
    
    # Summary
    parsed_files = list(PARSED_DIR.glob("*.json"))
    total_chars = 0
    for pf in parsed_files:
        with open(pf) as f:
            d = json.load(f)
            total_chars += len(d.get("transcript_raw", ""))
    
    print(f"\n📊 Summary:")
    print(f"   Meetings extracted: {len(parsed_files)}")
    print(f"   Total transcript chars: {total_chars:,}")
    print(f"   Avg per meeting: {total_chars // max(len(parsed_files), 1):,}")

if __name__ == "__main__":
    main()
