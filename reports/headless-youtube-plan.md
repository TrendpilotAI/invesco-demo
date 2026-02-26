# Headless YouTube Channel Plan: FlipMyEra Promotion

*Created: 2026-02-14 | Status: Implementation Ready*

---

## Channel Strategy

### Channel Name Ideas

| Name | Rationale |
|------|-----------|
| **Era Archives** | Evokes curated, collectible content; fits Swiftie "archive" culture |
| **The Eras Lounge** | Cozy, inviting; suggests a hangout for fans |
| **Midnight Chapters** | Nods to Midnights album + "chapters" ties to ebooks |
| **Enchanted Eras** | Uses a beloved deep cut title; instantly recognizable |
| **All Too Era** | Play on "All Too Well"; catchy, meme-friendly |

**Recommended: Midnight Chapters** — directly bridges music (Midnights) and books (Chapters → FlipMyEra ebooks), unique enough to rank, Swiftie-coded without being generic.

### Channel Description

```
✨ Your Taylor Swift era, reimagined through AI storytelling ✨
Quizzes, era deep dives, and AI-generated stories inspired by every Taylor Swift era.
Discover which era defines YOU → flipmyera.com

New videos every Mon/Thu 🌙
```

### Branding

- **Color palette:** Deep purple/midnight blue gradient with gold accents (Midnights aesthetic, works across eras)
- **Thumbnail style:** Bold era-specific color blocking + large text overlay + AI-generated character art (via RUNWARE/FLUX, same models as FlipMyEra)
- **Channel banner:** Collage of era aesthetics generated via FLUX, text: "Which era are you living in?"
- **Profile pic:** Stylized crescent moon with book pages (generated once, static)

### Content Categories

1. **Quiz Videos** (40%) — "Which era are you?" personality quizzes, interactive-style
2. **Era Story Narrations** (30%) — AI-narrated story excerpts from FlipMyEra-style ebooks
3. **Era Explainers** (20%) — Aesthetic breakdowns, era rankings, "what your fav era says about you"
4. **Shorts** (10%) — 30-60s clips: quick era facts, one-question quizzes, aesthetic montages

### Upload Schedule

- **Minimum viable:** 2 long-form videos/week (Mon + Thu) + 3 Shorts/week
- **Phase 1 (Month 1-2):** 2/week long-form, 5 Shorts/week (build library fast)
- **Phase 2 (Month 3+):** 3/week long-form, 5 Shorts/week

---

## Video Production Pipeline (Fully Automated)

### Architecture Overview

```
n8n Cron Trigger
    │
    ├─→ OpenAI GPT-4o: Generate script + metadata
    │
    ├─→ ElevenLabs API: Generate narration audio
    │
    ├─→ RUNWARE/FLUX: Generate 8-12 images per video
    │
    ├─→ FFmpeg: Assemble video (images + audio + text overlays)
    │
    └─→ YouTube Data API v3: Upload + set metadata
```

### Step-by-Step Pipeline

#### Step 1: Script Generation
- **Tool:** OpenAI GPT-4o API
- **Input:** Video type template + era topic (from a content calendar JSON)
- **Output:** JSON with: title, description, tags, script sections (each with narration text + image prompt + on-screen text)
- **Cost:** ~$0.03-0.08 per script (1500-3000 tokens out)
- **Implementation time:** 2 hours

#### Step 2: AI Narration
- **Tool:** ElevenLabs API (Turbo v2.5)
- **Voice:** Pick a warm female voice (e.g., "Rachel" or clone a custom voice) — consistent across all videos
- **Input:** Script narration text sections
- **Output:** MP3 audio files per section + combined audio
- **Cost:** ~$0.15-0.30 per video (1000-2000 characters, Pro plan at $22/mo includes 100k chars ≈ 50-100 videos/mo)
- **Implementation time:** 1 hour

#### Step 3: Image Generation
- **Tool:** RUNWARE API with FLUX model (already integrated in FlipMyEra)
- **Input:** Image prompts from script (8-12 per video)
- **Output:** 1920x1080 images, era-themed aesthetics
- **Cost:** ~$0.08-0.15 per video (RUNWARE pricing ~$0.01/image)
- **Implementation time:** 1 hour (reuse FlipMyEra integration)

#### Step 4: Video Assembly
- **Tool:** FFmpeg (installed on n8n server or via Execute Command node)
- **Process:**
  1. Create image slideshow with Ken Burns effect (zoom/pan)
  2. Add text overlays (on-screen quiz options, era names)
  3. Overlay narration audio
  4. Add background music (royalty-free lo-fi/ambient, pre-uploaded library)
  5. Add intro/outro bumpers (pre-made, 3-5 seconds each)
  6. Export as 1080p MP4, H.264
- **FFmpeg command template:**
  ```bash
  ffmpeg -y \
    -loop 1 -t ${duration} -i image_%03d.png \
    -i narration.mp3 \
    -i bgm.mp3 \
    -filter_complex "
      [0:v]zoompan=z='min(zoom+0.001,1.5)':d=${fps*duration}:s=1920x1080,
      drawtext=text='${overlay_text}':fontsize=48:fontcolor=white:x=(w-tw)/2:y=h-100;
      [2:a]volume=0.15[bgm];
      [1:a][bgm]amix=inputs=2:duration=first
    " \
    -c:v libx264 -preset medium -crf 23 \
    -c:a aac -b:a 128k \
    output.mp4
  ```
- **Cost:** $0 (runs on server)
- **Implementation time:** 4 hours (most complex step — templating the FFmpeg commands)

#### Step 5: Thumbnail Generation
- **Tool:** RUNWARE/FLUX + ImageMagick
- **Process:** Generate hero image via FLUX, add bold text overlay via ImageMagick
- **Cost:** ~$0.01 per thumbnail
- **Implementation time:** 1 hour

#### Step 6: Upload to YouTube
- **Tool:** YouTube Data API v3 (via n8n HTTP Request node or YouTube node)
- **Input:** Video file, title, description (with FlipMyEra links), tags, thumbnail, category, schedule time
- **Output:** Published/scheduled video
- **Cost:** $0 (API is free)
- **Implementation time:** 2 hours (OAuth setup is the slowest part)

### Total Cost Per Video

| Component | Cost |
|-----------|------|
| Script (GPT-4o) | $0.05 |
| Narration (ElevenLabs) | $0.22 |
| Images (RUNWARE) | $0.12 |
| Thumbnail | $0.01 |
| FFmpeg / Upload | $0.00 |
| **Total per video** | **~$0.40** |

At 2 videos/week = **$3.20/month** for long-form content. Add Shorts at ~$0.15 each = **$5.60/month total**.

---

## Video Types (with Example Scripts)

### Type 1: "Which Taylor Swift Era Are You?" Quiz Video

**Title:** "Which Taylor Swift Era Are You? Take This Quiz! ✨"
**Duration:** 5-7 minutes

```
[INTRO - 15 seconds]
IMAGE: Collage of all eras in a mystical swirl
NARRATION: "Every Swiftie has that one era that just... gets them. The one that plays on repeat during your main character moments. But have you ever wondered which Taylor Swift era truly matches your soul? Let's find out."
ON-SCREEN: "WHICH ERA ARE YOU?"

[QUESTION 1 - 45 seconds]
IMAGE: Split screen of four aesthetic scenes — cozy cabin, neon city, flower garden, dark forest
NARRATION: "Question one. It's a Friday night. What's your ideal vibe? 
A — Curled up with fairy lights and a journal. 
B — Out with your crew, city lights, no curfew. 
C — A picnic in a meadow, everything golden. 
D — Alone in your room, writing poetry about someone who doesn't deserve it."
ON-SCREEN: Options A B C D with aesthetic icons

[QUESTION 2 - 45 seconds]
IMAGE: Four outfit aesthetics
NARRATION: "Question two. Pick an outfit. 
A — Flowy sundress with cowboy boots. 
B — Sequin blazer, red lip, high ponytails. 
C — Cardigan. Just... the cardigan. 
D — All black. Leather. Reputation energy."
ON-SCREEN: Options with outfit illustrations

[QUESTION 3 - 45 seconds]
IMAGE: Four color palettes
NARRATION: "Question three. Choose a color that speaks to your soul right now. 
A — Gold, like the autumn light. 
B — Midnight blue, full of secrets. 
C — Lavender, soft and dreamy. 
D — Blood red. No explanation needed."
ON-SCREEN: Color swatches

[QUESTION 4 - 45 seconds]
IMAGE: Four lyric snippets as aesthetic text
NARRATION: "Question four. Which lyric hits different? 
A — 'Long story short, I survived.' 
B — 'I'm the problem, it's me.' 
C — 'Please don't ever become a stranger whose laugh I could recognize anywhere.' 
D — 'I did something bad, then why's it feel so good?'"

[QUESTION 5 - 45 seconds]
IMAGE: Four settings
NARRATION: "Last question. Where do you feel most yourself? 
A — A small town where everyone knows your name. 
B — The spotlight. Center stage. All eyes on you. 
C — A quiet lake house where time moves differently. 
D — A city at 2 AM when the world is yours."

[RESULTS - 90 seconds]
IMAGE: Each era aesthetic shown as result is described
NARRATION: "Okay, let's see your results. 
If you picked mostly A's — you're the Folklore era. You're introspective, creative, and you find magic in ordinary moments. You write your own story, literally.
Mostly B's — you're the 1989 era. Pop princess energy. You've shaken it off and you're thriving.
Mostly C's — you're the Lover era. Soft, romantic, unapologetically yourself. You believe in love even when it's terrifying.
Mostly D's — you're Reputation. Misunderstood, powerful, and absolutely iconic. The snake emojis only made you stronger."
ON-SCREEN: Era results with aesthetic backgrounds

[CTA - 30 seconds]
IMAGE: FlipMyEra app screenshots, ebook examples
NARRATION: "Now that you know your era — want to live in it? FlipMyEra lets you create your own AI-generated storybook set in ANY Taylor Swift era. Your name, your story, your aesthetic. Link in the description to create yours. It takes like two minutes and honestly? It's kind of addictive."
ON-SCREEN: "flipmyera.com" with arrow + "Link in description ↓"
```

---

### Type 2: AI-Generated Era Story Narration

**Title:** "A Folklore Love Story — AI-Generated Taylor Swift Era Fiction 🍂"
**Duration:** 8-10 minutes

```
[INTRO - 20 seconds]
IMAGE: Misty forest with a cabin in the distance, golden light filtering through trees
NARRATION: "Close your eyes. Imagine you're in a world where every Taylor Swift lyric is real. Where the folklore cabin exists. Where cardigan weather never ends. This is a story set in the Folklore era — written by AI, inspired by Taylor, and starring... well, it could be you."
ON-SCREEN: "A FOLKLORE LOVE STORY" in serif font

[CHAPTER 1: THE LAKES - 2 minutes]
IMAGE: A figure standing at the edge of a mist-covered lake at dawn
NARRATION: "The lake had no name. At least, none that the locals agreed on. Emma called it the Wishing Lake, because her grandmother once told her that if you whispered a secret to the water before sunrise, the universe would hold it for you.

She'd been coming here every morning since she moved back. Back to this small town that smelled like pine and nostalgia. Back to the house with the blue shutters where she'd spent every summer until she was seventeen and decided she was too big for small places.

She wasn't too big for anything anymore. The city had made sure of that."

IMAGE: A worn journal open on a wooden dock, pen resting on the pages
NARRATION: "She wrote in her journal: 'Day 12. The quiet is so loud here. I think that's the point.'

The coffee in her thermos had gone cold. She didn't mind. Cold coffee tasted like patience, and patience was something she was learning."

[CHAPTER 2: THE STRANGER - 2 minutes]  
IMAGE: A figure in a cable-knit sweater walking through autumn woods
NARRATION: "He appeared on day fifteen. Not appeared — that makes it sound like magic. He just... was there. At the general store, buying the same oat milk she bought, apologizing with his eyes when they reached for the last one at the same time.

'You take it,' he said. His voice was the kind of warm that made you forget the temperature.

'No, you — I can get almond,' she said.

'I actually hate oat milk,' he admitted. 'I just saw it on some list of things you're supposed to like now.'

She laughed. Actually laughed. It had been a while since she'd done that without planning to."

IMAGE: Two mugs of tea on a porch railing, autumn leaves falling
NARRATION: "They started having tea on her porch. No reason. No plan. Just two people who happened to be in the same small town, running from different versions of the same big feeling."

[CHAPTER 3: CARDIGAN WEATHER - 2 minutes]
IMAGE: Two figures sitting on porch steps wrapped in oversized cardigans, fairy lights above
NARRATION: "On day twenty-three, it rained. The kind of rain that doesn't stop — it just becomes the soundtrack of your life for a while.

'I have a theory,' he said, pulling his cardigan tighter. 'That every great love story starts with terrible weather.'

'That's not a theory, that's every romance novel,' she said.

'Maybe romance novels are onto something.'

She looked at him. Really looked. The way you look at someone when you realize they might matter. It's terrifying, that look. Because once you see someone clearly, you can't unsee them.

'Maybe,' she said."

[OUTRO - 30 seconds]
IMAGE: FlipMyEra interface showing a folklore-themed ebook being created
NARRATION: "This story was generated by AI — but the feeling? That's real. If you want your own personalized story set in any Taylor Swift era, with your name, your details, your aesthetic — FlipMyEra creates custom AI storybooks in minutes. Your era. Your story. Link below."
ON-SCREEN: "Create your era story → flipmyera.com"
```

---

### Type 3: "Taylor Swift Era Aesthetics Explained" Educational Content

**Title:** "The Folklore Aesthetic Explained: Why It Changed Everything 🌿"
**Duration:** 6-8 minutes

```
[INTRO - 20 seconds]
IMAGE: Iconic folklore album cover recreation (AI-generated, avoiding copyright — misty forest, figure in cardigan from behind)
NARRATION: "In July 2020, Taylor Swift did something no one expected. She dropped an entire album with zero promo, zero singles, zero build-up. Just a tweet and a forest. And somehow, folklore didn't just change Taylor's career — it created an entire aesthetic movement. Let's break down exactly why."
ON-SCREEN: "THE FOLKLORE AESTHETIC — EXPLAINED"

[SECTION 1: THE VISUAL LANGUAGE - 90 seconds]
IMAGE: Mood board — misty woods, cable-knit textures, handwritten letters, autumn leaves, old bridges
NARRATION: "The folklore aesthetic isn't just a color palette. It's a feeling. Visually, it lives in these elements: muted earth tones — forest green, stone grey, cream, faded gold. Organic textures — wool, wood, dried flowers, linen. And a specific kind of light — overcast, diffused, like the world is wrapped in gauze.

But here's what made it different from cottagecore, which already existed. Folklore added melancholy. Cottagecore says 'isn't nature lovely?' Folklore says 'isn't nature lovely, and aren't you a little bit heartbroken standing in it?' That emotional layer is what made it stick."

IMAGE: Side-by-side: cottagecore (bright, cheerful) vs folklore (moody, wistful)
NARRATION: "The distinction matters. Cottagecore is aspirational. Folklore is reflective. One is about where you want to be. The other is about who you are when no one's watching."

[SECTION 2: THE CULTURAL MOMENT - 90 seconds]
IMAGE: Empty cities, people at home, windows with rain
NARRATION: "Context is everything. Folklore dropped during lockdown. Everyone was isolated, introspective, staring out windows. Taylor basically soundtracked the collective emotional state of millions of people. The aesthetic wasn't escapism — it was validation. 'Yes, it's okay to be quiet right now. It's okay to feel too much. Here's an album that does both.'

The cardigan became a literal and metaphorical symbol. Taylor sold actual cardigans. But more than that, 'being in your cardigan era' became shorthand for choosing comfort over performance. Choosing depth over spectacle."

[SECTION 3: THE AESTHETIC'S DNA - 90 seconds]
IMAGE: Visual breakdown — typography (serif fonts), photography style (film grain), interiors (cozy, warm-lit rooms with books)
NARRATION: "Let's get specific about what makes something 'folklore-coded.'

Typography: Serif fonts. Lowercase. Handwritten elements. The album title itself is in a delicate serif — it whispers instead of shouts.

Photography: Film grain or desaturated digital. Shallow depth of field. Subjects often looking away from camera. Movement blur. Nothing too crisp — perfection isn't the point.

Interiors: Books everywhere. Warm lighting from lamps, not overheads. Visible textures — a wool throw, a worn rug, a mug with a chip in it. Lived-in, not styled.

Music references: Piano-forward. Acoustic guitar. Layered vocals that sound like memories."

[SECTION 4: LEGACY AND INFLUENCE - 60 seconds]
IMAGE: Examples of folklore influence — fashion, interior design, book covers, social media aesthetics
NARRATION: "Folklore's aesthetic ripple effect is still going. BookTok adopted it wholesale — dark academia and folklore aesthetics drive book sales. Interior design trends shifted toward warmth and texture. And in fashion, the 'quiet luxury' movement owes a debt to folklore's 'less is more' energy.

For Swifties, being in your folklore era means something specific: you're processing, you're growing, you're choosing depth. It's become one of the most coveted eras to claim."

[CTA - 30 seconds]
IMAGE: FlipMyEra ebook in folklore aesthetic — misty cover, serif fonts, character in forest setting
NARRATION: "Want to step into the folklore aesthetic with your own story? FlipMyEra creates AI-generated storybooks set in any Taylor Swift era — including folklore. Your character, your story, wrapped in this exact aesthetic. Create yours at flipmyera.com — link in the description."
ON-SCREEN: "flipmyera.com — Your Era, Your Story"
```

---

## Monetization

### YouTube Partner Program (YPP)

**Requirements:**
- 1,000 subscribers
- 4,000 watch hours (last 12 months) OR 10 million Shorts views (last 90 days)

**Realistic Timeline:**
- Month 1-2: 0-200 subscribers (building library, SEO indexing)
- Month 3-4: 200-600 subscribers (algorithm starts recommending)
- Month 5-7: 600-1,000 subscribers (if content resonates with Swiftie niche)
- **Target YPP eligibility: Month 5-7**

Shorts views could accelerate this significantly — Swiftie Shorts content can go viral.

### Revenue Streams

#### 1. YouTube Ad Revenue
- **Taylor Swift content CPM:** $4-8 (entertainment/lifestyle niche, US-heavy audience)
- Conservative projections:

| Month | Monthly Views | Ad Revenue | Notes |
|-------|-------------|------------|-------|
| 1-3 | 5K-20K | $0 | Pre-YPP |
| 4-6 | 20K-80K | $0-$40 | YPP pending |
| 7-12 | 80K-300K | $40-$200/mo | Post-YPP |
| 12-24 | 300K-1M | $200-$700/mo | Established |

#### 2. FlipMyEra Affiliate Revenue (Primary Goal)
Every video description includes:

```
✨ Create YOUR Taylor Swift era story → https://flipmyera.com?utm_source=youtube&utm_medium=video&utm_campaign={video_id}
```

- **Expected CTR from description:** 1-3% of viewers
- **FlipMyEra conversion rate assumption:** 5-10% of clicks
- **Average order value:** $5-15

| Monthly Views | Clicks (2%) | Conversions (7%) | Revenue ($10 avg) |
|--------------|-------------|-------------------|--------------------|
| 50K | 1,000 | 70 | $700 |
| 200K | 4,000 | 280 | $2,800 |
| 500K | 10,000 | 700 | $7,000 |

**This is the real monetization play.** Even modest view counts drive targeted, high-intent Swiftie traffic.

#### 3. Merch Shelf
- Once YPP is active, link merch (if FlipMyEra sells physical books or branded items)
- Era-themed merch could work: "I'm in my Folklore Era" shirts, etc.

#### 4. Channel Memberships
- At 500+ subscribers (post-YPP): offer membership perks
- Perks: early access to quizzes, exclusive era stories, poll access for next video topics

### Revenue Projection Summary

| Timeline | YouTube Ads | FlipMyEra Affiliate | Total |
|----------|------------|--------------------:|------:|
| Month 6 | $20 | $300 | $320 |
| Month 12 | $150 | $1,500 | $1,650 |
| Month 18 | $400 | $4,000 | $4,400 |
| Month 24 | $700 | $7,000 | $7,700 |

**Break-even point:** Month 1 (costs are ~$6/month, revenue from first FlipMyEra sale covers it).

---

## Technical Implementation

### n8n Workflow Design (Node by Node)

#### Workflow 1: "Video Production Pipeline"
**Trigger:** Cron — Mon/Thu at 2:00 AM UTC

```
Node 1: Cron Trigger
  → Fires Mon and Thu at 02:00 UTC

Node 2: Read Content Calendar (Google Sheets / Airtable / JSON file)
  → Fetches next unprocessed row
  → Fields: video_type, era, topic, status
  → Filter: status = "pending"

Node 3: Generate Script (HTTP Request → OpenAI API)
  → POST https://api.openai.com/v1/chat/completions
  → Model: gpt-4o
  → System prompt: Video type template (quiz/narration/explainer)
  → User prompt: "Create a {video_type} about {era}. Topic: {topic}"
  → Response format: JSON with sections[]{narration, image_prompt, overlay_text}
  → Parse JSON output

Node 4: Split Into Sections (SplitInBatches)
  → Iterate over script sections

Node 5: Generate Images (HTTP Request → RUNWARE API)
  → For each section, generate image from image_prompt
  → Model: FLUX
  → Size: 1920x1080
  → Store image URLs/files

Node 6: Generate Audio (HTTP Request → ElevenLabs API)
  → POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
  → Concatenate all narration text or generate per-section
  → Save as MP3

Node 7: Merge Results
  → Combine: images[], audio file, script metadata

Node 8: Generate Thumbnail (HTTP Request → RUNWARE)
  → Use title + era to generate eye-catching thumbnail
  → Bold, colorful, era-specific

Node 9: Assemble Video (Execute Command → FFmpeg)
  → Download all assets to temp directory
  → Run FFmpeg command to:
    - Create slideshow from images with transitions
    - Overlay audio
    - Add text overlays
    - Add intro/outro
    - Export MP4
  → Shell script template (stored on server)

Node 10: Upload to YouTube (HTTP Request → YouTube Data API v3)
  → POST https://www.googleapis.com/upload/youtube/v3/videos
  → Set: title, description, tags, categoryId=22 (People & Blogs)
  → Set: privacyStatus = "private" or "scheduled"
  → Upload thumbnail separately via thumbnails.set endpoint

Node 11: Update Content Calendar
  → Set row status = "published"
  → Add video URL

Node 12: Error Handler (on failure at any node)
  → Send notification via Telegram/email
  → Set status = "failed" in calendar
```

#### Workflow 2: "Shorts Generator" (separate, simpler)

```
Node 1: Cron Trigger (daily, 06:00 UTC)
Node 2: OpenAI → Generate 30-second quiz question or era fact
Node 3: RUNWARE → Generate 1 vertical image (1080x1920)
Node 4: ElevenLabs → Generate 20-30 second audio
Node 5: FFmpeg → Assemble vertical video (9:16)
Node 6: YouTube API → Upload as Short (title includes #Shorts)
```

### YouTube API Setup

1. **Google Cloud Console:**
   - Create project "Midnight Chapters"
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials (type: Web Application)
   - Add redirect URI for n8n OAuth callback
   - Request quota increase if needed (default: 10,000 units/day; upload = 1,600 units)

2. **OAuth Flow in n8n:**
   - Use n8n's built-in Google/YouTube OAuth2 credential
   - Or use HTTP Request with manual OAuth2 token management
   - Store refresh token securely in n8n credentials

3. **Channel Setup:**
   - Create Brand Account (not personal) for the channel
   - Set channel name, description, banner, profile pic
   - Create default playlists: "Era Quizzes", "Era Stories", "Era Aesthetics"
   - Set default upload settings: description template with FlipMyEra link

### Storage & Asset Management

- **n8n server storage:** Use Railway's ephemeral filesystem for temp processing, upload to YouTube, delete
- **Persistent assets:** Store in S3-compatible bucket (e.g., Cloudflare R2 — free egress)
  - `/templates/` — intro/outro clips, background music tracks, fonts
  - `/archive/` — completed videos (optional backup)
- **Background music:** Source 5-10 royalty-free ambient/lo-fi tracks, store permanently
- **Content calendar:** Google Sheets (free, easy to edit manually if needed)

### Monthly Cost Breakdown

| Item | Monthly Cost |
|------|-------------|
| Video production (8 long-form + 20 Shorts) | $5.20 |
| ElevenLabs Pro plan | $22.00 |
| OpenAI API | $2.00 |
| RUNWARE credits | $3.00 |
| Railway (n8n hosting, existing) | $0 (already running) |
| Cloudflare R2 storage | $0.50 |
| Background music (one-time) | $0 |
| **Total monthly** | **~$33/month** |

*Note: ElevenLabs is the biggest cost. Could reduce to $5/mo Starter plan initially (30k chars ≈ 15 videos/mo — sufficient for launch).*

**With ElevenLabs Starter plan: ~$16/month total.**

---

## Launch Plan

### Week 1: Foundation

| Day | Action |
|-----|--------|
| Mon | Create YouTube Brand Account "Midnight Chapters". Generate channel art (banner + profile pic) via FLUX. Write channel description. |
| Tue | Set up Google Cloud project. Enable YouTube Data API. Create OAuth2 credentials. Test upload via API. |
| Wed | Build n8n script generation node. Create prompt templates for all 3 video types. Test with GPT-4o. |
| Thu | Set up ElevenLabs account. Pick voice. Test TTS API. Integrate into n8n. |
| Fri | Build FFmpeg assembly step. Create intro/outro bumpers. Source 5 background music tracks. Test full assembly locally. |
| Sat | Build complete n8n workflow end-to-end. Test with one video of each type. Debug. |
| Sun | Create content calendar (Google Sheet) for Month 1. Pre-fill 12 video entries. |

### Week 2: Soft Launch

| Day | Action |
|-----|--------|
| Mon | **Publish Video 1:** "Which Taylor Swift Era Are You? The Ultimate Quiz ✨" |
| Tue | Publish 2 Shorts (era aesthetic clips). Create channel playlists. |
| Wed | Review Video 1 analytics. Adjust thumbnail style if CTR < 4%. |
| Thu | **Publish Video 2:** "A Folklore Love Story — AI Era Fiction 🍂" |
| Fri | Publish 2 Shorts. Start community posts (polls: "Which era are you?") |
| Sat | **Publish Video 3:** "The Reputation Aesthetic Explained 🐍" |
| Sun | Week review. Adjust scripts/pacing based on retention data. |

### Week 3: Optimize

| Day | Action |
|-----|--------|
| Mon | **Publish Video 4:** "What Your Favorite Taylor Swift Era Says About You" |
| Tue | 2 Shorts. Analyze which format gets best retention → double down. |
| Wed | Cross-promote: post Shorts to TikTok and Instagram Reels (repurpose vertical content). |
| Thu | **Publish Video 5:** "An Enchanted 1989 Summer — AI Era Story 🌆" |
| Fri | 2 Shorts. Engage with Swiftie comments (can automate basic responses via n8n). |
| Sat | **Publish Video 6:** "Why Midnights Is Taylor's Most Underrated Era" |
| Sun | Review analytics. Update content calendar for Month 2. |

### Week 4: Scale

| Day | Action |
|-----|--------|
| Mon | **Publish Video 7:** "Taylor Swift Era Quiz: Valentine's Edition 💕" |
| Tue | 3 Shorts. Community post: "What era story should we write next?" |
| Thu | **Publish Video 8:** "A Lover Era Romance — AI Story 🦋" |
| Fri | 2 Shorts. |
| Sat | Month 1 retrospective. Document: best-performing video type, average retention, sub growth. |
| Sun | Refine pipeline based on learnings. Adjust prompts, pacing, image styles. |

### First Month Content Calendar

| # | Date | Type | Title |
|---|------|------|-------|
| 1 | Mon W2 | Quiz | Which Taylor Swift Era Are You? The Ultimate Quiz ✨ |
| 2 | Thu W2 | Story | A Folklore Love Story — AI Era Fiction 🍂 |
| 3 | Sat W2 | Explainer | The Reputation Aesthetic Explained 🐍 |
| 4 | Mon W3 | Explainer | What Your Favorite Era Says About You |
| 5 | Thu W3 | Story | An Enchanted 1989 Summer — AI Era Story 🌆 |
| 6 | Sat W3 | Explainer | Why Midnights Is Taylor's Most Underrated Era |
| 7 | Mon W4 | Quiz | Taylor Swift Era Quiz: Valentine's Edition 💕 |
| 8 | Thu W4 | Story | A Lover Era Romance — AI Story 🦋 |

**Shorts (20 total across the month):**
- 5x "One-question era quiz" (vertical text + aesthetic bg)
- 5x "Era aesthetic in 30 seconds" (image montage + music)
- 5x "Era fact you didn't know" (narrated fact)
- 5x "Which era is this?" (show aesthetic, reveal answer)

### Growth Tactics

1. **SEO:** Every title includes "Taylor Swift Era" — high search volume, moderate competition. Tags: taylor swift era, swiftie quiz, folklore aesthetic, taylor swift personality quiz.

2. **Shorts funnel:** Every Short ends with "Full quiz on our channel!" — drives to long-form content where FlipMyEra CTA lives.

3. **Community Posts:** Weekly polls ("Folklore or Evermore?") — free engagement, algorithm loves active channels.

4. **Cross-promotion:** Repost Shorts to TikTok (@midnightchapters) and Instagram Reels. Add FlipMyEra link in bio.

5. **Swiftie Reddit/Discord:** Share videos in r/TaylorSwift, Swiftie Discord servers (carefully — add value, don't spam).

6. **Trend-jacking:** When Taylor announces tours, albums, or makes news → rapid-response Shorts within hours (n8n can trigger manually).

7. **Collab potential:** Once at 500+ subs, reach out to small Swiftie creators for collab quizzes.

8. **Playlist strategy:** Organize into playlists so YouTube auto-plays through your content.

---

## Summary

| Metric | Value |
|--------|-------|
| Setup time | ~1 week |
| Monthly cost | ~$16-33 |
| Videos per month | 8 long-form + 20 Shorts |
| Human time per month | ~2 hours (monitoring + calendar updates) |
| Break-even | Month 1 (first FlipMyEra sale) |
| Target YPP | Month 5-7 |
| Year 1 projected revenue | $10K-20K (mostly FlipMyEra affiliate) |

**The channel costs less than a Netflix subscription to run and drives targeted Swiftie traffic to FlipMyEra 24/7. The ROI is asymmetric — even 100 views per video puts FlipMyEra in front of exactly the right audience.**
