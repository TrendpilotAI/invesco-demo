# YouTube Transcript Automation Setup

## What Was Built

### 1. n8n Workflow (`projects/n8n-workflows/youtube-transcript-automation.json`)
Importable n8n workflow with these nodes:
- **Webhook Trigger** — POST to `/webhook/youtube-summarize` with `{"url": "https://youtube.com/watch?v=..."}`
- **Extract Video ID** — Code node parses YouTube URLs
- **Get Video Title** — HTTP request to noembed API
- **Fetch Transcript** — Code node scrapes YouTube's innertube captions API (no auth needed)
- **Summarize with Claude** — HTTP request to Anthropic API (needs `ANTHROPIC_API_KEY` env var in n8n)
- **Send to Telegram** — Sends formatted summary to chat ID 8003607839 (needs Telegram bot credential)
- **Respond to Webhook** — Returns JSON response

**To import:** n8n Settings → Import from File → select the JSON

**Prerequisites in n8n:**
- Set `ANTHROPIC_API_KEY` environment variable
- Configure Telegram Bot API credential

### 2. Standalone Script (`scripts/youtube-monitor.sh`)
Bash script that fetches transcripts and summarizes via Claude API.

```bash
# Full summary
./scripts/youtube-monitor.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# Raw transcript only
./scripts/youtube-monitor.sh "https://www.youtube.com/watch?v=VIDEO_ID" --raw
```

**Tested successfully** with `rWUWfj_PqmM` — a video about "20X Companies" using AI automation.

### 3. Python Transcript Server (`scripts/youtube-transcript-server.py`)
HTTP server on port 8082 for transcript extraction.

```bash
# Start server
python3 scripts/youtube-transcript-server.py

# Query it
curl "http://localhost:8082/?url=https://www.youtube.com/watch?v=VIDEO_ID"
curl -X POST http://localhost:8082/ -H "Content-Type: application/json" -d '{"url":"VIDEO_ID"}'
```

Returns JSON with `video_id`, `title`, `author`, `full_text`, `transcript` (timestamped segments).

Can be called by n8n's HTTP Request node if deployed alongside the n8n instance.

## Architecture

```
User → Webhook/CLI → Extract Video ID → Fetch Transcript → Claude Summarize → Telegram/Output
```

## Notes
- Transcript fetching works directly (no VPN needed) using `youtube-transcript-api` Python library
- The n8n Code node uses YouTube's innertube captions API directly via JavaScript (no Python dependency)
- Claude Sonnet is used for summarization (good balance of speed/quality)
