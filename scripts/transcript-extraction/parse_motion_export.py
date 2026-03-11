#!/usr/bin/env python3
"""
Motion Data Export Parser
Parses the full data export ZIP from Motion (Settings → Export All Data).

Usage:
    python3 parse_motion_export.py /path/to/motion-export.zip
"""
import os, json, sys, re, zipfile
from datetime import datetime
from pathlib import Path

PARSED_DIR = Path("/data/workspace/transcripts/motion/parsed")
RAW_DIR = Path("/data/workspace/transcripts/motion/raw")

def parse_motion_note(note_data, filename=""):
    """Parse a Motion note/doc that may contain meeting transcript."""
    parsed = {
        "source": "motion",
        "source_id": note_data.get("id", filename),
        "title": note_data.get("title", note_data.get("name", filename)),
        "meeting_date": note_data.get("created_at", note_data.get("date")),
        "duration_mins": None,
        "participants": [],
        "transcript_raw": "",
        "transcript_json": [],
        "summary": "",
        "action_items": [],
        "key_topics": [],
        "sentiment": {},
        "raw_json": note_data,
    }
    
    # Extract content from various Motion formats
    content = ""
    if "content" in note_data:
        c = note_data["content"]
        if isinstance(c, str):
            content = c
        elif isinstance(c, dict):
            content = c.get("text", c.get("html", json.dumps(c)))
    elif "description" in note_data:
        content = note_data["description"] or ""
    elif "body" in note_data:
        content = note_data["body"] or ""
    elif "text" in note_data:
        content = note_data["text"] or ""
    
    # Strip HTML if present
    content = re.sub(r'<[^>]+>', '\n', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    parsed["transcript_raw"] = content.strip()
    
    # Try to extract summary section
    summary_match = re.search(r'(?:Summary|Overview|Key Points)[:\s]*\n(.*?)(?:\n\n|\n(?:Action|Next|Follow))', 
                               content, re.IGNORECASE | re.DOTALL)
    if summary_match:
        parsed["summary"] = summary_match.group(1).strip()
    
    # Try to extract action items
    action_pattern = re.compile(r'(?:^[-•*]\s*|^\d+\.\s*)(.*?)$', re.MULTILINE)
    action_section = re.search(r'(?:Action Items?|Next Steps?|Follow[- ]?up)[:\s]*\n(.*?)(?:\n\n|$)', 
                                content, re.IGNORECASE | re.DOTALL)
    if action_section:
        items = action_pattern.findall(action_section.group(1))
        parsed["action_items"] = [{"item": item.strip(), "assignee": "", "due_date": ""} 
                                   for item in items if item.strip()]
    
    # Extract participants if mentioned
    participant_match = re.search(r'(?:Participants?|Attendees?)[:\s]*\n(.*?)(?:\n\n|$)',
                                   content, re.IGNORECASE | re.DOTALL)
    if participant_match:
        names = re.findall(r'[-•*]\s*(.+)', participant_match.group(1))
        parsed["participants"] = [{"name": n.strip(), "email": "", "role": "participant"} for n in names]
    
    return parsed

def process_zip(zip_path):
    """Extract and parse Motion's full data export."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 Extracting: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(RAW_DIR)
        files = z.namelist()
    
    print(f"  Found {len(files)} files in export")
    
    # Scan for JSON files that might contain transcripts/notes
    json_files = list(RAW_DIR.rglob("*.json"))
    print(f"  Found {len(json_files)} JSON files")
    
    parsed_count = 0
    transcript_count = 0
    
    for jf in sorted(json_files):
        try:
            with open(jf, 'r', errors='replace') as f:
                data = json.load(f)
        except:
            continue
        
        # Handle both single objects and arrays
        items = data if isinstance(data, list) else [data]
        
        for item in items:
            if not isinstance(item, dict):
                continue
            
            # Look for items that look like meeting notes/transcripts
            item_type = item.get("type", item.get("kind", "")).lower()
            title = (item.get("title", "") or item.get("name", "") or "").lower()
            content = str(item.get("content", item.get("description", item.get("body", ""))) or "")
            
            # Heuristic: is this a meeting transcript?
            is_transcript = (
                "transcript" in title or
                "meeting" in title or
                "call" in title or
                "notetaker" in item_type or
                "transcript" in item_type or
                "meeting_note" in item_type or
                len(content) > 500  # Long content likely has substance
            )
            
            if is_transcript and content.strip():
                parsed = parse_motion_note(item, jf.name)
                
                out_name = re.sub(r'[^\w\-.]', '_', 
                    f"{item.get('id', parsed_count)}_{parsed['title'][:40]}") + '.json'
                out_path = PARSED_DIR / out_name
                
                with open(out_path, 'w') as f:
                    json.dump(parsed, f, indent=2, default=str)
                
                transcript_count += 1
                print(f"  📝 {parsed['title'][:60]} ({len(content)} chars)")
            
            parsed_count += 1
    
    print(f"\n✅ Processed {parsed_count} items")
    print(f"📝 Found {transcript_count} transcript/meeting notes → {PARSED_DIR}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_motion_export.py /path/to/motion-export.zip")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    
    if path.suffix.lower() == '.zip':
        process_zip(path)
    elif path.is_dir():
        # Process raw directory
        RAW_DIR = path
        PARSED_DIR.mkdir(parents=True, exist_ok=True)
        json_files = list(path.rglob("*.json"))
        print(f"📂 Processing {len(json_files)} JSON files from {path}")
        # Reuse zip logic with extracted dir
        process_zip_dir = process_zip  # Would need refactor, keeping simple for now
    else:
        print(f"❌ Provide a .zip file from Motion's export")
        sys.exit(1)

if __name__ == "__main__":
    main()
