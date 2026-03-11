#!/usr/bin/env python3
"""
Otter.ai Bulk Export Parser
Parses the ZIP file from Otter.ai's bulk export feature into our standard format.

Usage:
    python3 parse_otter_export.py /path/to/otter-export.zip
    
    Or for a directory of .txt files:
    python3 parse_otter_export.py /path/to/otter-exports/
"""
import os, json, sys, re, zipfile
from datetime import datetime
from pathlib import Path

PARSED_DIR = Path("/data/workspace/transcripts/otter/parsed")

def parse_otter_txt(text, filename=""):
    """Parse an Otter.ai TXT transcript into structured format."""
    lines = text.strip().split('\n')
    
    parsed = {
        "source": "otter",
        "source_id": filename.replace('.txt', '').replace('.docx', ''),
        "title": "",
        "meeting_date": None,
        "duration_mins": None,
        "participants": [],
        "transcript_raw": text,
        "transcript_json": [],
        "summary": "",
        "action_items": [],
        "key_topics": [],
        "sentiment": {},
        "raw_text": text,
    }
    
    # Try to extract title from filename or first line
    if lines:
        parsed["title"] = lines[0].strip() if lines[0].strip() else filename
    
    # Parse date from filename pattern like "Meeting 2024-01-15"
    date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', filename)
    if date_match:
        try:
            parsed["meeting_date"] = datetime.strptime(date_match.group(1), "%Y-%m-%d").isoformat()
        except:
            pass
    
    # Parse transcript lines - Otter format is typically:
    # Speaker Name  HH:MM
    # Text content here
    speakers = set()
    current_speaker = ""
    current_text = []
    
    speaker_pattern = re.compile(r'^(.+?)\s+(\d{1,2}:\d{2})\s*$')
    timestamp_pattern = re.compile(r'^(\d{1,2}:\d{2})\s*$')
    
    for line in lines[1:]:  # Skip title line
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check if this is a speaker line
        match = speaker_pattern.match(stripped)
        if match:
            # Save previous segment
            if current_speaker and current_text:
                text_block = ' '.join(current_text)
                parsed["transcript_json"].append({
                    "speaker": current_speaker,
                    "text": text_block,
                    "timestamp": "",
                })
            
            current_speaker = match.group(1).strip()
            speakers.add(current_speaker)
            current_text = []
        else:
            current_text.append(stripped)
    
    # Don't forget last segment
    if current_speaker and current_text:
        text_block = ' '.join(current_text)
        parsed["transcript_json"].append({
            "speaker": current_speaker,
            "text": text_block,
            "timestamp": "",
        })
    
    # Build participants
    parsed["participants"] = [{"name": s, "email": "", "role": "participant"} for s in sorted(speakers)]
    
    # Rebuild clean transcript
    if parsed["transcript_json"]:
        parsed["transcript_raw"] = "\n".join(
            f"[{seg['speaker']}]: {seg['text']}" 
            for seg in parsed["transcript_json"]
        )
    
    return parsed

def parse_otter_docx(filepath):
    """Parse DOCX export from Otter."""
    try:
        from docx import Document
        doc = Document(filepath)
        text = '\n'.join(p.text for p in doc.paragraphs)
        return parse_otter_txt(text, filepath.name)
    except ImportError:
        print("  ⚠️ python-docx not installed, falling back to text extraction")
        # Try basic text extraction
        import subprocess
        result = subprocess.run(['strings', str(filepath)], capture_output=True, text=True)
        return parse_otter_txt(result.stdout, filepath.name)

def process_zip(zip_path):
    """Extract and parse all transcripts from Otter ZIP export."""
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 Extracting: {zip_path}")
    extract_dir = Path("/data/workspace/transcripts/otter/raw")
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_dir)
        files = z.namelist()
    
    print(f"  Found {len(files)} files in ZIP")
    
    parsed_count = 0
    for filepath in sorted(extract_dir.rglob("*")):
        if filepath.suffix.lower() == '.txt':
            print(f"  Parsing: {filepath.name}...", end=" ")
            with open(filepath, 'r', errors='replace') as f:
                text = f.read()
            parsed = parse_otter_txt(text, filepath.name)
            
        elif filepath.suffix.lower() == '.docx':
            print(f"  Parsing: {filepath.name}...", end=" ")
            parsed = parse_otter_docx(filepath)
            
        else:
            continue
        
        # Save parsed
        out_name = re.sub(r'[^\w\-.]', '_', filepath.stem) + '.json'
        out_path = PARSED_DIR / out_name
        with open(out_path, 'w') as f:
            json.dump(parsed, f, indent=2, default=str)
        
        segments = len(parsed["transcript_json"])
        print(f"✅ ({segments} segments)")
        parsed_count += 1
    
    print(f"\n✅ Parsed {parsed_count} transcripts → {PARSED_DIR}")

def process_directory(dir_path):
    """Process a directory of exported transcript files."""
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    dir_path = Path(dir_path)
    
    files = list(dir_path.glob("*.txt")) + list(dir_path.glob("*.docx"))
    print(f"📂 Found {len(files)} transcript files in {dir_path}")
    
    for filepath in sorted(files):
        print(f"  Parsing: {filepath.name}...", end=" ")
        
        if filepath.suffix.lower() == '.txt':
            with open(filepath, 'r', errors='replace') as f:
                text = f.read()
            parsed = parse_otter_txt(text, filepath.name)
        else:
            parsed = parse_otter_docx(filepath)
        
        out_name = re.sub(r'[^\w\-.]', '_', filepath.stem) + '.json'
        out_path = PARSED_DIR / out_name
        with open(out_path, 'w') as f:
            json.dump(parsed, f, indent=2, default=str)
        
        print(f"✅")
    
    print(f"\n✅ Done! {len(files)} files → {PARSED_DIR}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 parse_otter_export.py /path/to/otter-export.zip")
        print("  python3 parse_otter_export.py /path/to/transcript-files/")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    
    if path.suffix.lower() == '.zip':
        process_zip(path)
    elif path.is_dir():
        process_directory(path)
    else:
        print(f"❌ Unsupported: {path}")
        print("Provide a .zip file or directory of .txt/.docx files")
        sys.exit(1)

if __name__ == "__main__":
    main()
