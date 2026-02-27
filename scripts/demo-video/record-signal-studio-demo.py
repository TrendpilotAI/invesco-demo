#!/usr/bin/env python3
"""
Signal Studio Demo Video Recorder

Records automated browser demos of Signal Studio features using Playwright.
Captures frames via CDP screencast and encodes to MP4/GIF with FFmpeg.

Usage:
    python3 record-signal-studio-demo.py [--demo DEMO_NAME] [--output DIR] [--format mp4|gif|webm]
    
    # Record the admin console demo
    python3 record-signal-studio-demo.py --demo admin
    
    # Record all demos
    python3 record-signal-studio-demo.py --demo all
    
    # List available demos
    python3 record-signal-studio-demo.py --list

Prerequisites:
    pip install playwright
    python3 -m playwright install chromium
    apt-get install ffmpeg
"""

import argparse
import asyncio
import base64
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ============== CONFIGURATION ==============

SIGNAL_STUDIO_URL = os.environ.get(
    "SIGNAL_STUDIO_URL",
    "https://signal-studio-production-a258.up.railway.app"
)

DJANGO_BACKEND_URL = os.environ.get(
    "DJANGO_BACKEND_URL", 
    "https://django-backend-production-3b94.up.railway.app"
)

OUTPUT_BASE = Path(os.environ.get("DEMO_OUTPUT_DIR", "/data/workspace/demo-videos"))
FRAME_RATE = 30
JPEG_QUALITY = 90
VIEWPORT_WIDTH = 1440
VIEWPORT_HEIGHT = 900

# Demo credentials
DEMO_EMAIL = "demo@forwardlane.com"
DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "demo123")


# ============== DEMO SEQUENCES ==============

async def demo_login(page):
    """Login to Signal Studio"""
    await page.goto(f"{SIGNAL_STUDIO_URL}/login", wait_until="networkidle")
    await page.wait_for_timeout(1000)
    
    # Check if we're already logged in (redirected to dashboard)
    if "/login" not in page.url:
        return
    
    # Fill login form
    email_input = page.locator('input[type="email"], input[name="email"], input[placeholder*="mail"]').first
    if await email_input.is_visible():
        await email_input.fill(DEMO_EMAIL)
        await page.wait_for_timeout(300)
    
    password_input = page.locator('input[type="password"]').first
    if await password_input.is_visible():
        await password_input.fill(DEMO_PASSWORD)
        await page.wait_for_timeout(300)
    
    submit_btn = page.locator('button[type="submit"], button:has-text("Sign in"), button:has-text("Log in")').first
    if await submit_btn.is_visible():
        await submit_btn.click()
        await page.wait_for_timeout(2000)


async def demo_admin_console(page, frames_collector):
    """Demo: Operations Center / Admin Console"""
    print("  📍 Navigating to Operations Center...")
    await page.goto(f"{SIGNAL_STUDIO_URL}/admin", wait_until="networkidle")
    await page.wait_for_timeout(3000)  # Let data load
    
    # Capture the full dashboard
    print("  📸 Capturing dashboard overview...")
    await page.wait_for_timeout(2000)
    
    # Hover over service health cards
    print("  🖱️  Hovering over system health...")
    cards = page.locator('[class*="card"], [class*="Card"]')
    count = await cards.count()
    for i in range(min(count, 4)):
        card = cards.nth(i)
        if await card.is_visible():
            await card.hover()
            await page.wait_for_timeout(800)
    
    # Scroll down to see more sections
    print("  📜 Scrolling through sections...")
    await page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
    await page.wait_for_timeout(2000)
    
    await page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
    await page.wait_for_timeout(2000)
    
    # Scroll back to top
    await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
    await page.wait_for_timeout(1500)


async def demo_easy_button(page, frames_collector):
    """Demo: Easy Button Dashboard"""
    print("  📍 Navigating to Easy Button...")
    await page.goto(f"{SIGNAL_STUDIO_URL}/easy-button", wait_until="networkidle")
    await page.wait_for_timeout(3000)
    
    # Show the dashboard metrics
    print("  📸 Capturing dashboard metrics...")
    await page.wait_for_timeout(2000)
    
    # Hover over stat cards
    stats = page.locator('.ant-statistic, [class*="statistic"], [class*="Statistic"]')
    stat_count = await stats.count()
    for i in range(min(stat_count, 4)):
        stat = stats.nth(i)
        if await stat.is_visible():
            await stat.hover()
            await page.wait_for_timeout(600)
    
    # Scroll through advisor list
    print("  📜 Scrolling through advisors...")
    await page.evaluate("window.scrollBy({ top: 300, behavior: 'smooth' })")
    await page.wait_for_timeout(2000)
    
    await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
    await page.wait_for_timeout(1500)


async def demo_signal_library(page, frames_collector):
    """Demo: Signal Library with Collections"""
    print("  📍 Navigating to Signal Library...")
    await page.goto(f"{SIGNAL_STUDIO_URL}/signal-library", wait_until="networkidle")
    await page.wait_for_timeout(3000)
    
    # Show the collections
    print("  📸 Capturing signal library...")
    await page.wait_for_timeout(2000)
    
    # Click on a collection if available
    collection = page.locator('[class*="collection"], [class*="Collection"]').first
    if await collection.is_visible():
        await collection.click()
        await page.wait_for_timeout(2000)
    
    # Scroll to see signals
    await page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
    await page.wait_for_timeout(2000)
    
    await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
    await page.wait_for_timeout(1500)


async def demo_visual_builder(page, frames_collector):
    """Demo: Visual Signal Builder (React Flow)"""
    print("  📍 Navigating to Visual Builder...")
    await page.goto(f"{SIGNAL_STUDIO_URL}/visual-builder/builder", wait_until="networkidle")
    await page.wait_for_timeout(3000)
    
    # Show the React Flow canvas
    print("  📸 Capturing visual builder...")
    await page.wait_for_timeout(2000)
    
    # Try to interact with nodes
    nodes = page.locator('[class*="react-flow__node"], .react-flow__node')
    node_count = await nodes.count()
    print(f"  🔗 Found {node_count} nodes")
    
    for i in range(min(node_count, 3)):
        node = nodes.nth(i)
        if await node.is_visible():
            await node.hover()
            await page.wait_for_timeout(1000)
            await node.click()
            await page.wait_for_timeout(1000)
    
    # Show the full canvas
    await page.wait_for_timeout(2000)


async def demo_chat(page, frames_collector):
    """Demo: AI Chat Interface"""
    print("  📍 Navigating to AI Chat...")
    await page.goto(f"{SIGNAL_STUDIO_URL}/chat", wait_until="networkidle")
    await page.wait_for_timeout(2000)
    
    # Type a sample query
    chat_input = page.locator('textarea, input[placeholder*="message"], input[placeholder*="chat"], input[placeholder*="Ask"]').first
    if await chat_input.is_visible():
        print("  ⌨️  Typing sample query...")
        await chat_input.click()
        await page.wait_for_timeout(500)
        
        # Type slowly for effect
        query = "Show me advisors with high TCX scores"
        for char in query:
            await chat_input.type(char, delay=80)
        
        await page.wait_for_timeout(1000)
        
        # Don't actually submit — just show the typing
        await page.wait_for_timeout(2000)
    
    await page.wait_for_timeout(1500)


async def demo_full_walkthrough(page, frames_collector):
    """Full product walkthrough — all features"""
    await demo_easy_button(page, frames_collector)
    await demo_signal_library(page, frames_collector)
    await demo_visual_builder(page, frames_collector)
    await demo_admin_console(page, frames_collector)
    await demo_chat(page, frames_collector)


# ============== DEMO REGISTRY ==============

DEMOS = {
    "admin": {
        "name": "Operations Center",
        "description": "Admin console — system health, jobs, pipelines, signals",
        "func": demo_admin_console,
        "duration_est": "30s",
    },
    "easy-button": {
        "name": "Easy Button Dashboard",
        "description": "Advisor dashboard with AUM, signals, and client priorities",
        "func": demo_easy_button,
        "duration_est": "25s",
    },
    "signal-library": {
        "name": "Signal Library",
        "description": "Signal collections, browsing, and management",
        "func": demo_signal_library,
        "duration_est": "25s",
    },
    "visual-builder": {
        "name": "Visual Signal Builder",
        "description": "React Flow canvas for building signals visually",
        "func": demo_visual_builder,
        "duration_est": "30s",
    },
    "chat": {
        "name": "AI Chat",
        "description": "Natural language signal queries",
        "func": demo_chat,
        "duration_est": "20s",
    },
    "full": {
        "name": "Full Walkthrough",
        "description": "Complete product demo — all features",
        "func": demo_full_walkthrough,
        "duration_est": "2m",
    },
}


# ============== RECORDING ENGINE ==============

class FrameCollector:
    """Collects screencast frames from CDP"""
    
    def __init__(self):
        self.frames = []
        self._collecting = False
    
    def on_frame(self, data: bytes):
        if self._collecting:
            self.frames.append(data)
    
    def start(self):
        self._collecting = True
    
    def stop(self):
        self._collecting = False
    
    def save(self, output_dir: Path, frame_skip: int = 3):
        """Save frames to disk, keeping every Nth frame"""
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved = 0
        for i in range(0, len(self.frames), frame_skip):
            filename = f"frame_{saved:05d}.jpg"
            (output_dir / filename).write_bytes(self.frames[i])
            saved += 1
        
        return saved


async def record_demo(demo_key: str, output_dir: Path, video_format: str = "mp4"):
    """Record a demo video"""
    from playwright.async_api import async_playwright
    
    demo = DEMOS[demo_key]
    print(f"\n🎬 Recording: {demo['name']}")
    print(f"   {demo['description']}")
    print(f"   Estimated duration: {demo['duration_est']}")
    print()
    
    frames_dir = output_dir / f"{demo_key}-frames"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--window-size=1440,900",
            ]
        )
        
        context = await browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            device_scale_factor=2,  # Retina quality
            ignore_https_errors=True,
        )
        
        page = await context.new_page()
        
        # Start CDP screencast
        client = await context.new_cdp_session(page)
        
        collector = FrameCollector()
        
        async def handle_frame(params):
            frame_data = base64.b64decode(params["data"])
            collector.on_frame(frame_data)
            await client.send("Page.screencastFrameAck", {"sessionId": params["sessionId"]})
        
        client.on("Page.screencastFrame", handle_frame)
        
        await client.send("Page.startScreencast", {
            "format": "jpeg",
            "quality": JPEG_QUALITY,
            "maxWidth": VIEWPORT_WIDTH * 2,
            "maxHeight": VIEWPORT_HEIGHT * 2,
            "everyNthFrame": 1,
        })
        
        collector.start()
        
        # Login first if needed
        try:
            print("  🔑 Logging in...")
            await demo_login(page)
        except Exception as e:
            print(f"  ⚠️  Login skipped: {e}")
        
        # Run the demo sequence
        start_time = time.time()
        try:
            await demo["func"](page, collector)
        except Exception as e:
            print(f"  ❌ Demo error: {e}")
        
        elapsed = time.time() - start_time
        print(f"\n  ⏱️  Recording duration: {elapsed:.1f}s")
        
        # Stop recording
        collector.stop()
        await client.send("Page.stopScreencast")
        
        print(f"  📸 Captured {len(collector.frames)} raw frames")
        
        # Save frames
        frame_skip = 2  # Keep every 2nd frame for 15fps effective at 30fps encode
        saved = collector.save(frames_dir, frame_skip=frame_skip)
        print(f"  💾 Saved {saved} frames to {frames_dir}")
        
        await browser.close()
    
    # Encode to video
    if saved > 0:
        output_file = output_dir / f"{demo_key}-demo.{video_format}"
        encode_video(frames_dir, output_file, video_format)
        
        # Also create a GIF version for easy sharing
        if video_format == "mp4":
            gif_file = output_dir / f"{demo_key}-demo.gif"
            encode_video(frames_dir, gif_file, "gif")
        
        return output_file
    else:
        print("  ⚠️  No frames captured — skipping encode")
        return None


def encode_video(frames_dir: Path, output_file: Path, video_format: str):
    """Encode frames to video using FFmpeg"""
    print(f"\n  🎥 Encoding {video_format}...")
    
    input_pattern = str(frames_dir / "frame_%05d.jpg")
    
    if video_format == "mp4":
        cmd = [
            "ffmpeg", "-y",
            "-framerate", "30",
            "-i", input_pattern,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(output_file),
        ]
    elif video_format == "gif":
        cmd = [
            "ffmpeg", "-y",
            "-framerate", "15",
            "-i", input_pattern,
            "-vf", "fps=12,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3",
            str(output_file),
        ]
    elif video_format == "webm":
        cmd = [
            "ffmpeg", "-y",
            "-framerate", "30",
            "-i", input_pattern,
            "-c:v", "libvpx-vp9",
            "-crf", "28",
            "-b:v", "0",
            "-pix_fmt", "yuv420p",
            str(output_file),
        ]
    else:
        print(f"  ❌ Unknown format: {video_format}")
        return
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        size = output_file.stat().st_size
        size_str = f"{size / 1024:.0f}KB" if size < 1024 * 1024 else f"{size / (1024*1024):.1f}MB"
        print(f"  ✅ Created {output_file.name} ({size_str})")
    else:
        print(f"  ❌ FFmpeg error: {result.stderr[:200]}")


# ============== CLI ==============

def main():
    parser = argparse.ArgumentParser(description="Signal Studio Demo Video Recorder")
    parser.add_argument("--demo", type=str, default="admin", help="Demo to record (or 'all')")
    parser.add_argument("--output", type=str, default=str(OUTPUT_BASE), help="Output directory")
    parser.add_argument("--format", type=str, default="mp4", choices=["mp4", "gif", "webm"])
    parser.add_argument("--list", action="store_true", help="List available demos")
    
    args = parser.parse_args()
    
    if args.list:
        print("\n📋 Available demos:\n")
        for key, demo in DEMOS.items():
            print(f"  {key:20s} {demo['name']} ({demo['duration_est']})")
            print(f"  {'':20s} {demo['description']}")
            print()
        return
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.demo == "all":
        demos_to_run = [k for k in DEMOS.keys() if k != "full"]
    elif args.demo in DEMOS:
        demos_to_run = [args.demo]
    else:
        print(f"❌ Unknown demo: {args.demo}")
        print(f"   Available: {', '.join(DEMOS.keys())}")
        sys.exit(1)
    
    print(f"🎬 Signal Studio Demo Recorder")
    print(f"   Target: {SIGNAL_STUDIO_URL}")
    print(f"   Output: {output_dir}")
    print(f"   Format: {args.format}")
    
    results = []
    for demo_key in demos_to_run:
        result = asyncio.run(record_demo(demo_key, output_dir, args.format))
        results.append((demo_key, result))
    
    print("\n" + "=" * 60)
    print("📼 Recording Summary")
    print("=" * 60)
    for key, path in results:
        status = f"✅ {path}" if path else "❌ Failed"
        print(f"  {key:20s} {status}")
    
    print(f"\n📁 Videos saved to: {output_dir}")


if __name__ == "__main__":
    main()
