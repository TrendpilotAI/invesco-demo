#!/usr/bin/env python3
"""Simple HTTP server for YouTube transcript extraction.
Listens on port 8082, accepts YouTube URLs, returns JSON with transcript + metadata.
"""

import json
import re
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

LANGUAGES = ["en", "fr", "de", "es", "it", "pt", "nl"]
PORT = 8082


def extract_video_id(url_or_id):
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$"
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    return url_or_id


def get_video_title(video_id):
    try:
        r = requests.get(f"https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_id}", timeout=10)
        d = r.json()
        return d.get("title", "Unknown"), d.get("author_name", "Unknown")
    except:
        return "Unknown", "Unknown"


def fetch_transcript(video_id):
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=LANGUAGES)
    entries = [{"text": e.text, "start": e.start, "duration": e.duration} for e in transcript]
    full_text = " ".join(e["text"] for e in entries)
    return entries, full_text


class Handler(BaseHTTPRequestHandler):
    def _handle(self, url_param=None):
        try:
            if not url_param:
                # Try query params
                parsed = urlparse(self.path)
                params = parse_qs(parsed.query)
                url_param = params.get("url", params.get("video_id", [None]))[0]

            if not url_param:
                # Try reading POST body
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length:
                    body = json.loads(self.rfile.read(content_length))
                    url_param = body.get("url") or body.get("video_id")

            if not url_param:
                self._respond(400, {"error": "Missing 'url' or 'video_id' parameter"})
                return

            video_id = extract_video_id(url_param)
            title, author = get_video_title(video_id)
            entries, full_text = fetch_transcript(video_id)

            self._respond(200, {
                "video_id": video_id,
                "title": title,
                "author": author,
                "entries_count": len(entries),
                "full_text": full_text,
                "transcript": entries
            })
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            self._respond(404, {"error": str(e)})
        except Exception as e:
            self._respond(500, {"error": str(e)})

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def do_GET(self):
        if self.path == "/health":
            self._respond(200, {"status": "ok"})
            return
        self._handle()

    def do_POST(self):
        self._handle()

    def log_message(self, format, *args):
        print(f"[transcript-server] {args[0]}" if args else "")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    print(f"YouTube Transcript Server listening on port {port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
