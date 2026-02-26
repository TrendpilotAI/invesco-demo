# Demo Video Production Guide — Second-Opinion (MedGemma Impact Challenge)

**Goal:** 3-minute polished demo video | **Deadline:** Feb 24, 2026 | **Prize Pool:** $100K

---

## Table of Contents
1. [Recording Setup & Settings](#1-recording-setup--settings)
2. [Screen Recording Tools](#2-screen-recording-tools)
3. [Voiceover & Audio](#3-voiceover--audio)
4. [Music & Sound Design](#4-music--sound-design)
5. [Editing Workflow](#5-editing-workflow)
6. [Storytelling & Pacing](#6-storytelling--pacing)
7. [What Judges Want](#7-what-judges-want)
8. [AI-Assisted Production](#8-ai-assisted-production)
9. [Video Compression & Export](#9-video-compression--export)
10. [Common Mistakes](#10-common-mistakes)
11. [Pre-Submission Checklist](#11-pre-submission-checklist)

---

## 1. Recording Setup & Settings

### Resolution & Frame Rate
- **Resolution:** 1920×1080 (1080p) — standard for Kaggle/YouTube. 4K is overkill and harder to compress.
- **Frame Rate:** 30fps for screen recordings, 24fps if you want a more cinematic feel for title cards.
- **Aspect Ratio:** 16:9 (never record vertical)

### Browser Setup (for live demo segments)
- Chrome, **clean profile** — no bookmarks bar, no extensions visible
- Dark mode **OFF** (better readability on compressed video)
- Zoom browser to **125-150%** so UI elements are clearly readable
- Close all other tabs
- Turn off all notifications (macOS: Focus mode → Do Not Disturb)
- Use a clean wallpaper (solid dark color) if desktop is ever visible
- Hide the macOS dock (`Cmd+Option+D`)

### Screen Prep
- Set display to **1920×1080 native** (System Settings → Displays → Scaled → 1920×1080)
- If Retina, use a tool that records at logical resolution (not 2x physical)
- Close Spotlight, menu bar extras — anything that could pop up

---

## 2. Screen Recording Tools

### Recommended: **OBS Studio** (Free) + **CleanShot X** (for polish)

| Tool | Best For | Price | Link |
|------|----------|-------|------|
| **OBS Studio** | Full recording + audio mixing | Free | [obsproject.com](https://obsproject.com) |
| **ScreenFlow** | Recording + built-in editor | $169 | [telestream.net/screenflow](https://www.telestream.net/screenflow/) |
| **CleanShot X** | Quick clips, annotations, GIFs | $29 | [cleanshot.com](https://cleanshot.com) |
| **Loom** | Quick & easy, auto-upload | Free tier | [loom.com](https://loom.com) |
| **QuickTime** | Simple, built-in, no install | Free | Built into macOS |

### OBS Settings for This Video
```
Output:
  Recording Format: MKV (remux to MP4 after — crash-safe)
  Encoder: Apple VT H265 (or x264 if no Apple Silicon)
  Rate Control: CRF 18-20
  
Audio:
  Sample Rate: 48kHz
  Channels: Mono (voiceover) or Stereo (if adding music)
  
Video:
  Base Resolution: 1920x1080
  Output Resolution: 1920x1080
  FPS: 30
```

### Recording Strategy for Your Script
Record each segment separately (don't try for one take):
1. **Segment 1 (Hook):** Create title cards in Canva/Figma, export as video or images
2. **Segment 2 (Problem):** Slides or stock footage with text overlays
3. **Segment 3-4 (Solution + Demo):** Screen recording of the actual app
4. **Segment 5 (Architecture):** Animated diagram or clean slide + brief code scroll
5. **Segment 6 (Impact):** Comparison slide
6. **Segment 7 (Close):** Logo + links slide

Record voiceover as a **separate audio track** and sync in editing. This gives you way more flexibility.

---

## 3. Voiceover & Audio

### Equipment (Budget-Friendly)
- **Best:** Any USB condenser mic (Blue Yeti, Audio-Technica AT2020USB+, Rode NT-USB Mini ~$99)
- **Good enough:** AirPods Pro / wired Apple EarPods — surprisingly decent for voice
- **Last resort:** MacBook built-in mic — record in a closet with clothes around you (deadens echo)

### Recording Tips
- **Record in a small, soft room** — closet > open living room. Blankets/pillows kill echo.
- **Mic 4-6 inches from mouth**, slightly off-axis (not directly in front — reduces plosives)
- **Pop filter** or just put a sock over the mic
- **Record 10 seconds of silence** at the start — use this as a noise profile for cleanup
- **Stand up** while recording — your voice sounds more energetic
- **Smile** while talking — it literally changes your vocal tone
- **Pace:** ~130 words/min for clarity. Your script is ~650 words = 5 min at slow pace, 3 min at ~215 wpm. **Practice to hit natural 200-215 wpm** — this is "confident and energetic" speed.
- **Record each segment separately** — easier to get clean takes
- **Do 3 takes of each segment** — pick the best, comp if needed

### Audio Post-Processing (Free)
Use **Audacity** (free) or **GarageBand** (free on Mac):
1. Noise reduction (use that silent intro as noise profile)
2. Normalize to -3dB
3. Light compression (ratio 2:1, threshold -20dB) — evens out volume
4. High-pass filter at 80Hz — removes room rumble
5. Export as WAV 48kHz 16-bit

### AI Voiceover Alternatives
If time is tight or you want a polished backup:
- **ElevenLabs** — best quality AI voices, $5/mo starter. Can clone your voice with 1 min of audio. [elevenlabs.io](https://elevenlabs.io)
- **HeyGen** — AI avatar + voice. Could work for intro/outro but feels less authentic for a hackathon. [heygen.com](https://heygen.com)
- **Google Cloud TTS** — free tier, decent quality, fits the Google ecosystem narrative

**Recommendation:** Use your real voice. Judges value authenticity. AI voice = obvious and slightly off-putting for a medical AI product (ironic). Use ElevenLabs only as backup if your recording environment is terrible.

---

## 4. Music & Sound Design

### Royalty-Free Music Sources

| Source | Price | Best For | Link |
|--------|-------|----------|------|
| **Uppbeat** | Free tier (with credit) | Tech/startup vibes | [uppbeat.io](https://uppbeat.io) |
| **Artlist** | $10/mo | High-quality, no attribution | [artlist.io](https://artlist.io) |
| **Epidemic Sound** | $15/mo | Huge library | [epidemicsound.com](https://epidemicsound.com) |
| **YouTube Audio Library** | Free | Basic but legal | [studio.youtube.com](https://studio.youtube.com) |
| **Pixabay Music** | Free | Simple background tracks | [pixabay.com/music](https://pixabay.com/music/) |
| **Mixkit** | Free | Clean, modern tracks | [mixkit.co/free-stock-music](https://mixkit.co/free-stock-music/) |

### Music Selection Tips
- **Genre:** Ambient/electronic, light piano, or soft tech-corporate. NOT epic trailer music.
- **Energy curve:** Start subtle (hook), slightly more energy during demo, swell during impact, resolve at close
- **Volume:** Music at **-20 to -25dB** below voiceover. If you can consciously hear the music, it's too loud.
- **Key moment:** A subtle music swell at "Medical AI shouldn't be a luxury" (2:40) adds emotional punch
- **No lyrics.** Ever.

### Sound Effects (Optional but Polished)
- Subtle "whoosh" on slide transitions
- Soft click/chime when pipeline steps complete
- Keep it minimal — 2-3 sound effects max in the whole video
- Source: [freesound.org](https://freesound.org), [mixkit.co/free-sound-effects](https://mixkit.co/free-sound-effects/)

---

## 5. Editing Workflow

### Recommended Editors

| Tool | Price | Skill Level | Link |
|------|-------|-------------|------|
| **DaVinci Resolve** | Free | Pro-level, steep learning curve | [blackmagicdesign.com](https://www.blackmagicdesign.com/products/davinciresolve/) |
| **CapCut Desktop** | Free | Easy, great captions/effects | [capcut.com](https://www.capcut.com) |
| **iMovie** | Free (Mac) | Simple, gets the job done | Built into macOS |
| **Final Cut Pro** | $300 / Free trial | Pro, fast on Apple Silicon | Mac App Store |
| **Descript** | $24/mo | Edit video by editing text | [descript.com](https://descript.com) |

### **Recommended for You: CapCut Desktop or DaVinci Resolve**
- CapCut: fastest path to polished output, great auto-captions, easy text overlays
- DaVinci: more control, better color/audio, but steeper curve

### Editing Steps (In Order)
1. **Rough cut:** Lay down voiceover on timeline. Trim dead air and flubs.
2. **Visual sync:** Add screen recordings, slides, and title cards synced to voiceover.
3. **Text overlays:** Add key stats as text on screen (the $200-$2000, 12%, etc.)
4. **Transitions:** Simple cuts or cross-dissolves only. No star wipes. No spinning transitions.
5. **Music:** Add background track, adjust volume curve.
6. **Captions/subtitles:** Auto-generate (CapCut/Descript do this well), then proofread. **This is critical — judges may watch on mute.**
7. **Color/brightness:** Ensure screen recordings are bright and readable.
8. **Final review:** Watch at 1x speed, check audio levels, timing.

### Text Overlay Style
- Font: Clean sans-serif (Inter, SF Pro, Montserrat)
- Color: White text with subtle drop shadow or dark semi-transparent background
- Animation: Simple fade in/out (0.3s). No bouncing, no spinning.
- Position: Lower third or center screen on dark backgrounds

### Transitions Between Segments
- **Hook → Problem:** Fade to black (0.5s)
- **Problem → Solution:** Cut (direct)
- **Solution → Demo:** Cut (direct)
- **Demo → Architecture:** Brief fade or cut
- **Architecture → Impact:** Cut
- **Impact → Close:** Fade to black (0.5s), then fade in logo

---

## 6. Storytelling & Pacing (What Winners Do)

### The YC Demo Day Formula (Adapted)
YC's format works perfectly for 3-minute competition videos:
1. **Problem** (15-20% of time) — Make it visceral, use a specific number
2. **Solution** (10% of time) — One sentence, crystal clear
3. **Demo** (35-40% of time) — Show, don't tell. Let the product speak.
4. **How it works** (15-20% of time) — Technical credibility without jargon overload
5. **Impact/Traction** (10-15% of time) — Numbers, comparison, future
6. **Ask/Close** (5% of time) — Clean ending

Your script already follows this perfectly. The pacing is strong.

### What Makes Winning Demo Videos Stand Out

**From Kaggle competition analysis:**
- **Live demos over slides** — judges can tell when something actually works vs. vaporware
- **Showing real output** — not mockups, real model predictions on real data
- **Honest about limitations** — brief mention of what it doesn't do builds trust
- **Technical depth** — Kaggle judges are technical. Don't dumb it down too much.
- **Pipeline visualization** — showing data flow (which you have!) is hugely impressive

**From Product Hunt top launches:**
- **First 5 seconds determine everything** — your "68 million Americans" hook is strong
- **Show the UI early** — don't make people wait 90 seconds to see the product
- **Speed up repetitive actions** (2x-4x) but slow down on key moments (results appearing)
- **End with a clear CTA** — your live link + GitHub is perfect

**From YC Demo Day:**
- **Confidence in delivery** — not reading, not hesitant
- **Specific numbers** over vague claims ("two cents" > "affordable")
- **Comparison tables** — your traditional vs. Second-Opinion table is exactly right
- **Brevity** — say less, show more

### Pacing Tips for Your Script
- **0:00-0:15 (Hook):** Slow, dramatic. Let the stats breathe. Silence is powerful here.
- **0:15-0:40 (Problem):** Moderate pace, building urgency
- **0:40-0:55 (Solution):** Confident, slightly faster — you're excited about this
- **0:55-1:50 (Demo):** Slowest section. Let the viewer see what's happening. Don't rush the pipeline animation.
- **1:50-2:25 (Architecture):** Technical but clear. Medium pace.
- **2:25-2:50 (Impact):** Build energy — this is your "wow" moment
- **2:50-3:00 (Close):** Slow down, land it cleanly

---

## 7. What Judges Want (Google Health AI / Kaggle)

### Google's Health AI Team Values
Based on Google Health AI publications, HAI-DEF model documentation, and MedGemma challenge criteria:

1. **Responsible AI** — Show awareness of limitations, disclaimers, not replacing doctors
   - Your "Questions for Your Doctor" feature is *perfect* for this
   - The "we don't replace your doctor" line is essential — keep it
2. **Health Equity** — Access for underserved populations is a HUGE theme for Google Health
   - Your cost comparison ($0.02 vs $2,000) and global accessibility angle nail this
3. **Open Weights / Open Source** — Google released MedGemma as open weights for a reason. Emphasize this.
   - "No patient data leaves our servers" — this resonates deeply
4. **Technical Rigor** — Multi-model pipeline, proper triage, fallbacks — show engineering quality
5. **Real-World Deployability** — Not just a notebook. You have a live app. This is a massive differentiator.
   - Most Kaggle teams submit notebooks. You built a deployable product. EMPHASIZE THIS.
6. **Privacy** — On-prem/serverless GPU means data stays private. Google cares about this.

### Kaggle Competition Video Norms
- Kaggle doesn't have a standard video format — many submissions are rough screen recordings
- **This means a polished video stands out enormously.** Even basic production value puts you in top 10%.
- Judges watch dozens of videos — **respect their time**. Stay at or under 3 minutes.
- Include your team name and project name in the first 5 seconds
- Show the code running, not just slides

### Scoring Priorities (Typical for Google-sponsored challenges)
1. Impact & usefulness (30-40%)
2. Technical implementation & use of specified models (30-40%)
3. Creativity & innovation (15-20%)
4. Presentation quality (10-15%)

Presentation quality is "only" 10-15% but it colors perception of everything else. A polished video makes your technical work seem more rigorous.

---

## 8. AI-Assisted Production Tools

### HeyGen (AI Avatar)
- [heygen.com](https://heygen.com) — $24/mo Creator plan
- Can generate a talking-head avatar for intro/outro
- **Verdict:** Skip for this video. Authentic voiceover over screen recording is more credible for a medical AI product. An AI avatar presenting a medical tool feels ironic and potentially off-putting to health AI judges.

### Remotion (Programmatic Video)
- [remotion.dev](https://remotion.dev) — React-based video generation
- Could generate your architecture diagram animation programmatically
- **Verdict:** Overkill for one diagram. Use Canva/Figma animation or a simple animated GIF instead. Time investment not worth it for one 15-second segment.
- **Alternative:** Use [Excalidraw](https://excalidraw.com) for the architecture diagram → export as SVG → animate in CapCut with simple fade-ins for each step

### Descript
- [descript.com](https://descript.com) — Edit video by editing a text transcript
- Great for removing filler words ("um", "uh") automatically
- Can generate captions instantly
- **Verdict:** Good option if voiceover needs heavy editing

### Canva
- [canva.com](https://canva.com) — Free tier works
- Create title cards, comparison slides, logo screens
- Has video export for animated slides
- **Verdict:** Use this for Segments 1, 2, 6, and 7 (the non-screen-recording segments)

---

## 9. Video Compression & Export

### Export Settings
```
Format: MP4 (H.264)
Resolution: 1920x1080
Frame Rate: 30fps
Video Bitrate: 8-12 Mbps (CBR or VBR 2-pass)
Audio: AAC, 192kbps, 48kHz
Total file size for 3 min: ~180-270 MB
```

### If Kaggle Has a File Size Limit
- Drop bitrate to 5-6 Mbps (still looks great for screen recordings)
- Use H.265/HEVC if the platform supports it (50% smaller, same quality)
- Use HandBrake (free) for final compression: [handbrake.fr](https://handbrake.fr)
  - Preset: "Fast 1080p30" → adjust RF to 20-22

### HandBrake Settings (if needed)
```
Preset: Fast 1080p30
Encoder: H.264 (x264)
Quality: RF 20 (lower = bigger/better, 18-22 is sweet spot)
Audio: AAC 192kbps
```

### Upload Considerations
- Upload to **YouTube as Unlisted** first — test that it looks/sounds right after compression
- Keep a high-quality master file (ProRes or CRF 15) before compressing
- Kaggle may accept YouTube links — check submission requirements

---

## 10. Common Mistakes to Avoid

### Video
- ❌ Recording at wrong resolution (blurry text)
- ❌ Notification popup during screen recording
- ❌ Visible bookmarks bar with personal sites
- ❌ Mouse cursor moving erratically/nervously — move deliberately
- ❌ Too many transitions/effects — screams amateur
- ❌ Tiny text on screen that's unreadable

### Audio
- ❌ Echo/reverb from recording in a large room
- ❌ Inconsistent volume between segments
- ❌ Background music too loud — competing with voice
- ❌ Mouth clicks, breathing, AC hum
- ❌ Reading the script in a flat monotone

### Content
- ❌ Spending too long on the problem (judges get it — move to demo fast)
- ❌ Not showing a live demo (slides-only = death)
- ❌ Demo crashes on camera with no backup
- ❌ Going over 3 minutes
- ❌ No captions (judges watch on mute!)
- ❌ Forgetting to mention the competition's required models by name

### Production
- ❌ Trying to do it in one take (record segments separately!)
- ❌ Spending 3 days perfecting the video instead of the product
- ❌ Not doing a test recording first to check audio/video quality

---

## 11. Pre-Submission Checklist

### Before Recording
- [ ] App is deployed and working — test the full pipeline 3 times
- [ ] Pre-record a backup demo (in case live demo fails during recording)
- [ ] Browser: clean Chrome profile, 125%+ zoom, no extensions, no bookmarks bar
- [ ] macOS: Do Not Disturb ON, Dock hidden, clean wallpaper
- [ ] Mic tested — record 10 seconds and play back to check quality
- [ ] Script printed or on second screen — practice reading it aloud 3 times
- [ ] All slides/title cards created in Canva/Figma

### During Recording
- [ ] Record voiceover separately from screen capture
- [ ] Record 3 takes of each segment
- [ ] Move mouse deliberately and slowly
- [ ] Pause after key statements (let the stats land)
- [ ] Speed up loading/waiting parts in post

### During Editing
- [ ] Voiceover synced to visuals
- [ ] Background music added at -20 to -25dB
- [ ] Text overlays for all key stats
- [ ] Captions/subtitles added and proofread
- [ ] All model names correct: MedGemma 4B, MedGemma 27B, MedSigLIP, Gemini
- [ ] Total runtime: 2:50-3:00 (don't go over)
- [ ] Transitions are simple (cuts and fades only)

### Before Export
- [ ] Watch the full video at 1x speed with fresh eyes
- [ ] Check audio levels — consistent throughout, no clipping
- [ ] Verify text is readable at 1080p on a laptop screen
- [ ] Logo and links visible in closing frame for at least 5 seconds
- [ ] Export at 1080p30, H.264, 8-12 Mbps

### Before Submission
- [ ] Upload to YouTube (unlisted) — verify quality after YouTube processing
- [ ] Watch on phone — still readable?
- [ ] Check Kaggle submission requirements for format/size limits
- [ ] File named clearly: `Second-Opinion-Demo-MedGemma-Challenge.mp4`
- [ ] Share with one person for feedback before submitting

---

## Quick-Start Production Plan (2-Day Schedule)

### Day 1: Record Everything (4-6 hours)
1. **Hour 1:** Create all slides/title cards in Canva (Segments 1, 2, 6, 7)
2. **Hour 2:** Set up recording environment, test mic, test screen capture
3. **Hour 3:** Record all screen recordings (Segments 3, 4, 5)
4. **Hour 4:** Record voiceover for all segments (3 takes each)
5. **Hour 5-6:** Buffer / re-record anything that didn't work

### Day 2: Edit & Polish (4-6 hours)
1. **Hour 1-2:** Rough cut — lay voiceover on timeline, sync visuals
2. **Hour 2-3:** Add text overlays, transitions, music
3. **Hour 3-4:** Generate and proofread captions
4. **Hour 4-5:** Final review, export, compression
5. **Hour 5-6:** Upload, test, submit

---

## Summary: The 80/20 of a Polished Demo Video

If you only do 5 things:
1. **Clean audio** — record voiceover in a quiet/soft room with a decent mic
2. **Add captions** — judges watch on mute
3. **Show a live demo** — not slides, the real app working
4. **Keep it under 3 minutes** — respect the judges' time
5. **Nail the first 10 seconds** — your "68 million Americans" hook is strong, deliver it with conviction

Everything else is bonus. A clean recording with good audio beats a flashy production with bad sound every time.

---

*Guide prepared for Nathan / TrendpilotAI — Second-Opinion MedGemma Impact Challenge, Feb 2026*
