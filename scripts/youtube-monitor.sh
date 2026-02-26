#!/usr/bin/env bash
# YouTube Video Transcript Summarizer
# Usage: youtube-monitor.sh <youtube_url> [--raw]
# Fetches transcript via Python, summarizes with Claude API

set -euo pipefail

URL="${1:?Usage: youtube-monitor.sh <youtube_url> [--raw]}"
RAW="${2:-}"

# Extract video ID
VIDEO_ID=$(echo "$URL" | grep -oP '(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})' | head -1 | sed 's/v=//;s/youtu\.be\///')
if [ -z "$VIDEO_ID" ]; then
    VIDEO_ID="$URL"  # Assume it's already a video ID
fi

echo "📺 Fetching transcript for video: $VIDEO_ID"

# Fetch transcript using Python
TRANSCRIPT_JSON=$(python3 -c "
import json, sys
from youtube_transcript_api import YouTubeTranscriptApi
import requests

video_id = '$VIDEO_ID'

# Get title
try:
    r = requests.get(f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_id}', timeout=10)
    d = r.json()
    title, author = d.get('title', 'Unknown'), d.get('author_name', 'Unknown')
except:
    title, author = 'Unknown', 'Unknown'

# Get transcript
api = YouTubeTranscriptApi()
transcript = api.fetch(video_id, languages=['en','fr','de','es','it','pt','nl'])
entries = [{'text': e.text, 'start': e.start} for e in transcript]
full_text = ' '.join(e['text'] for e in entries)

json.dump({'video_id': video_id, 'title': title, 'author': author, 'full_text': full_text, 'entries_count': len(entries)}, sys.stdout)
")

TITLE=$(echo "$TRANSCRIPT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['title'])")
AUTHOR=$(echo "$TRANSCRIPT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['author'])")
FULL_TEXT=$(echo "$TRANSCRIPT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['full_text'])")
ENTRIES=$(echo "$TRANSCRIPT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['entries_count'])")

echo "✅ Got transcript: \"$TITLE\" by $AUTHOR ($ENTRIES segments)"

if [ "$RAW" = "--raw" ]; then
    echo ""
    echo "--- RAW TRANSCRIPT ---"
    echo "$FULL_TEXT"
    exit 0
fi

# Truncate if too long for API (keep ~12k words)
TRUNCATED=$(echo "$FULL_TEXT" | head -c 50000)

echo "🤖 Summarizing with Claude..."

# Call Claude API
SUMMARY=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(python3 -c "
import json, sys
text = sys.stdin.read()
payload = {
    'model': 'claude-sonnet-4-20250514',
    'max_tokens': 1500,
    'messages': [{
        'role': 'user',
        'content': f'Summarize this YouTube video transcript concisely. Include key points, main arguments, and any notable quotes. Format with bullet points.\n\nVideo: $TITLE by $AUTHOR\n\nTranscript:\n{text}'
    }]
}
json.dump(payload, sys.stdout)
" <<< "$TRUNCATED")" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('content',[{}])[0].get('text','ERROR: '+json.dumps(r)))")

echo ""
echo "═══════════════════════════════════════"
echo "📺 $TITLE"
echo "👤 $AUTHOR"
echo "🔗 https://www.youtube.com/watch?v=$VIDEO_ID"
echo "═══════════════════════════════════════"
echo ""
echo "$SUMMARY"
