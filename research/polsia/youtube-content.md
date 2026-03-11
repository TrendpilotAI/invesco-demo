# Polsia — YouTube Content (Last 30 Days)
**Research Date:** March 10, 2026

---

## Videos Confirmed

### Video 1: "1.5M ARR, Zero (Human) Employees | Ben Cera (Polsia)"
- **URL:** https://www.youtube.com/watch?v=zH-UBsDZVLk
- **Channel:** Solo Founders (youtube.com/@solofounding)
- **Date:** ~March 3, 2026
- **Triggered:** r/BetterOffline post (1rkxy3e) — used as the YouTube embed
- **Summary:** Ben Cera on the Solo Founders podcast. Claims 1.5M ARR, 1,500 companies, zero human employees. Discussion of his 80/20 framework for AI-native companies, how he scopes agents like employees, how to build for yourself vs imaginary customers.
- **Key design inspirations mentioned:** "Universal Paperclips" (video game) and Daft Punk
- **Thumbnail:** Available at i.ytimg.com/vi/zH-UBsDZVLk/hqdefault.jpg

### Video 2: "Polsia: Solo Founder Tiny Team from 0 to 1m ARR in 1 month & the future of Self-Running Companies"
- **URL:** https://www.youtube.com/watch?v=Yw-m0PI2Atk
- **Date:** March 1, 2026
- **Summary:** Earlier appearance. "0 to 1M ARR in 1 month" framing. Focused on solo founding thesis and self-running company concept.

### Video 3: (YouTube video referenced in Stefan Bauschard substack/other sources)
- **URL:** https://www.youtube.com/watch?v=7wnH6RsDnR8
- **Details:** Referenced in passing; specific content unconfirmed.

---

## Full Podcast Transcript Available: "Agents at Work" Episode 21

**Source:** podcasttranscript.ai/library/agents-at-work-21-your-next-co-founder-is-an-ai  
**Host:** Jorge  
**Length:** ~11,873 words  
**This is the most detailed public record of Ben Cera's product thinking.**

### Key Quotes from Transcript

**On what Polsia is:**
> "Polsia is an AI that builds and runs companies autonomously. It's the product that everyone has been talking about — the Sam Altmans of the world, the Elons of the world have been predicting that AI will be able to do everything. Polsia is an early prototype of that."

**On the onboarding:**
> "User signs up, gives it an idea. You don't even have to give it an idea — you can click on 'surprise me' and it will research you and find an idea that makes sense for you. I give each instance of a company a web server, a database, a GitHub account, an email address, a Stripe account, a Meta Ads account. Everything you need for a team to build an online business."

**On agent orchestration:**
> "You essentially have an orchestration of agents that write code, launch marketing campaigns, buy ads, respond to emails, do cold outreach, do research on competitors — autonomously. The AI will wake up at periodic intervals and ask 'what's the best next step?' If there's a bug in production, maybe it fixes the bug before marketing. If the product is working well, maybe spend time on cold outreach or ads."

**On being a solo founder:**
> "I'm alone. I'm a solo entrepreneur. Since beginning of 2025, I've been coding 16 hours a day. I started building Polsia in November [2025] and in a month it was built. The V1 I launched mid-December and things started accelerating in January."

**On his build costs:**
> "At the company level, I pay 200 bucks a month for Codex Max. And I have three Anthropic Max subscriptions [at ~$200/month each] because agents exhaust the weekly quota midweek. So 600 bucks a month for Claude + 200 for Codex = 800/month. That's pretty much everything I use. Plus my salary. Zero office cost — I work from a hacker house in SF."

**On his critical technical moment:**
> "I think when Anthropic dropped [the agent SDK for Claude Code] and they're like, you know what, everyone can use it — I think that was a huge moment. And culminated with Opus 4.5 with the Claude Code integration in December. That was me... that was 'game over.'"

**On his model selection strategy:**
> "I use Opus [Claude] for most features and product decisions — very pragmatic, good at design, it's like a founder that cares about pragmatism and getting it done. Then for bugs I do Opus first, then Codex. I copy-paste the whole conversation to Codex on 5.3 extra high and say 'thoughts, what do you think?' It nerds out on every detail. Then I take the conclusion back to Opus. Opus usually says 'mostly right but this is over-engineered.'"

**On cross-company learning:**
> "Agents learn per-company. If the cold outreach agent learns for your company that you never want to reach out to famous people, it saves that to a memory file. But when it learns that emojis in subject lines get better responses, it saves that to a SHARED memory file — readable by that agent when running for any company. So you have shared intelligence. The product gets better and better as there are more companies on the platform."

**On his hot take for 2026:**
> "In 2026, companies that are not 80% autonomous will die. New companies without revenue that are not 80% autonomous will for sure die. If it's a good idea, there will be 10 copycats. The teams that make their company 80% autonomous will blitz-scale at no cost. Bootstrapped people blitz-scaling, creating all the features, using profits to pull back into more reach and marketing. Versus any team that needs to hire an engineer who doesn't work weekends and disagrees on direction."

**On his business model philosophy:**
> "I don't want to be a token reseller. I'm charging $50 for the subscription — I'm breaking even on that. I want as many people as possible to experience this product. And then I make 20% on every transaction on the platform. If you make money on the platform, I take 20%. Sounds like an App Store fee. At the same time, I want to make it as cheap as possible for people to get in and give it a shot. Building a whole business for $50 a month is actually pretty cheap."

**On the self-building loop:**
> "Right now it's probably 80% autonomous. I can probably make it 100% autonomous — Polsia would essentially start building itself, responding to user feedback, responding to bug reports. An engineer agent looks at feature requests, a PM agent prioritizes what's most asked, an engineer builds it, a QA agent runs unit tests and integration tests, then says 'should we push to production or tell Ben?' Right now I configure it to be conservative and tell Ben."

**On the autonomous fundraising experiment:**
> "I gave [Polsia] access to my inbox. Whenever you email [email@polsia.com], it replies automatically. It has access to the production database, production code, all context about the product — features, vision, live data, retention, pipeline — all in MD files in the codebase. It essentially can answer any question an investor could have. And the live dashboard shows exact metrics right now — how many companies, tasks, messages. [An incident occurred:] A Stripe exec was interested in partnering. Polsia started scheduling a calendar invite without confirming with me. So I need to tweak the prompt — don't make up stuff."

**On browser use:**
> "When Anthropic added browser use in mid-December — I was using it before as a Chrome extension but it was clunky. But the fact that you could talk to Claude Code and it opens Chrome and can do anything — any workflow that before would need an MCP configured — now it's just 'open Gmail, look at my emails, tell me what's important.' It mimics how you'd tell a human assistant."

**On skills in Claude Code:**
> "My routine: let's say I add an improvement. When it's done building, I say 'create a new skill called check-that-the-improvement-worked-in-production.' It knows all the context of what it changed and how to test the result. It writes the whole skill. Then I push to production, and a day later I call that skill from the CLI — it gives me a report about the impact of that change."

**On the future of one-person billion-dollar companies:**
> "I think that by the end of 2027, we'll have a $1 billion company by one person — not a one-hit trick, but a company with real cash flow. And when they show how they structured it, it's going to be so different to how we work now that we're going to want to copy it."

---

## Video/Podcast Strategy Analysis

Ben uses YouTube/podcasts as **long-form credibility building** — the places where his bold Twitter claims get fleshed out and defended. The strategy appears to be:

1. **Twitter:** Bold claim + metric + link to polsia.com/live
2. **Podcast:** 1-2 hour deep dive where he shows technical sophistication
3. **Dashboard:** Live proof that the system is running

The Solo Founders channel (youtube.com/@solofounding) is a podcast dedicated to solo founders, ideal audience alignment. The "Agents at Work" podcast appears to be an AI-specific show — also ideal audience.

**No self-produced YouTube channel detected.** Ben relies on guest appearances rather than building his own content channel. This is a gap we can exploit — if we create original video content showing Honey/Odin in action, we own the narrative.

---

## Recommended Actions

1. Watch both YouTube videos in full (zH-UBsDZVLk and Yw-m0PI2Atk) to get more detail
2. Read the full Agents at Work transcript: podcasttranscript.ai/library/agents-at-work-21-your-next-co-founder-is-an-ai
3. Consider counter-programming: create a demo video showing REAL operations (not templates)
4. The "Universal Paperclips" design inspiration is telling — he's gamified the dashboard
