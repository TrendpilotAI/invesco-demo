# ElevenLabs Pricing Analysis

**Date:** 2026-02-18
**Purpose:** Evaluate ElevenLabs TTS for Nathan's projects (Ultrafone, NarrativeReactor)

---

## 1. ElevenLabs Pricing Tiers (Monthly)

| Tier | Price/mo | TTS Flash chars | TTS Multilingual chars | Voices | API | Commercial License |
|------|----------|----------------|----------------------|--------|-----|-------------------|
| **Free** | $0 | 20K (Flash) / 10K (ML) | ✅ | Limited | ❌ No API TTS | ❌ |
| **Starter** | $5 | 60K / 30K | ✅ | 10 custom | ✅ | ✅ |
| **Creator** | $22 | 200K / 100K | ✅ | 30 custom | ✅ | ✅ |
| **Pro** | $99 | 1M / 500K | ✅ | 160 custom | ✅ | ✅ |
| **Scale** | $330 | 4M / 2M | ✅ | 660 custom | ✅ | ✅ |
| **Business** | $1,320 | 22M / 11M | ✅ | Unlimited | ✅ | ✅ |
| **Enterprise** | Custom | Custom | ✅ | Unlimited | ✅ | ✅ + SLA/SSO/SOC2 |

**Yearly billing saves ~17% (2 months free).**

## 2. Per-Character API Pricing (TTS)

### Flash/Turbo Models (~75ms latency, 32 languages)

| Tier | Included per 1K chars | Overage per 1K chars |
|------|----------------------|---------------------|
| Starter | $0.083 | N/A (no overage) |
| Creator | $0.110 | $0.15 |
| Pro | $0.099 | $0.12 |
| Scale | $0.083 | $0.09 |
| Business | $0.060 | $0.06 |

### Multilingual v2/v3 Models (~250-300ms latency, higher quality)

| Tier | Included per 1K chars | Overage per 1K chars |
|------|----------------------|---------------------|
| Starter | $0.167 | N/A |
| Creator | $0.220 | $0.30 |
| Pro | $0.198 | $0.24 |
| Scale | $0.165 | $0.18 |
| Business | $0.120 | $0.12 |

## 3. Cost Per Minute of Generated Audio

**Key conversion: ~1,000 characters ≈ 1 minute of audio** (per ElevenLabs docs)

### Flash/Turbo (low latency, ideal for real-time/Ultrafone)

| Tier | Cost/minute (included) | Cost/minute (overage) |
|------|----------------------|----------------------|
| Starter ($5) | $0.083 | N/A |
| Creator ($22) | $0.110 | $0.15 |
| Pro ($99) | $0.099 | $0.12 |
| Scale ($330) | $0.083 | $0.09 |
| Business ($1,320) | $0.060 | $0.06 |

### Multilingual v2/v3 (premium quality)

| Tier | Cost/minute (included) | Cost/minute (overage) |
|------|----------------------|----------------------|
| Starter ($5) | $0.167 | N/A |
| Creator ($22) | $0.220 | $0.30 |
| Pro ($99) | $0.198 | $0.24 |
| Scale ($330) | $0.165 | $0.18 |
| Business ($1,320) | $0.120 | $0.12 |

## 4. Competitor Comparison

| Provider | Cost/1M chars | Cost/min (approx) | Latency | Voice Cloning | Languages | Streaming |
|----------|-------------|-------------------|---------|---------------|-----------|-----------|
| **ElevenLabs (Pro Flash)** | $99 | $0.099 | ~75ms | ✅ Instant + Pro | 32 | ✅ WebSocket |
| **ElevenLabs (Pro ML v2)** | $198 | $0.198 | ~250ms | ✅ Instant + Pro | 32 | ✅ WebSocket |
| **Fish Audio** | ~$15/1M chars | ~$0.015 | ~200ms | ✅ | 13+ | ✅ |
| **OpenAI TTS** | $15/1M chars | ~$0.015 | ~300ms | ❌ | 57 | ✅ |
| **OpenAI TTS HD** | $30/1M chars | ~$0.030 | ~500ms | ❌ | 57 | ✅ |
| **Google Cloud TTS (Standard)** | $4/1M chars | ~$0.004 | ~200ms | ❌ | 50+ | ✅ |
| **Google Cloud TTS (Neural)** | $16/1M chars | ~$0.016 | ~300ms | ❌ | 50+ | ✅ |
| **Amazon Polly (Standard)** | $4/1M chars | ~$0.004 | ~150ms | ❌ | 30+ | ✅ |
| **Amazon Polly (Neural)** | $16/1M chars | ~$0.016 | ~200ms | ❌ | 30+ | ✅ |
| **Azure Speech (Neural)** | $16/1M chars | ~$0.016 | ~200ms | ✅ (limited) | 100+ | ✅ |

### Key Takeaways
- **ElevenLabs is 5-25x more expensive** than alternatives on a per-character basis
- **Quality is best-in-class** — widely regarded as most natural-sounding TTS
- **Fish Audio is ~6-13x cheaper** than ElevenLabs at comparable quality levels
- **OpenAI TTS is ~6x cheaper** but no voice cloning
- **Google/Amazon/Azure are cheapest** but sound more robotic

## 5. API Capabilities Comparison

| Feature | ElevenLabs | Fish Audio | OpenAI TTS | Google Cloud | Amazon Polly | Azure Speech |
|---------|-----------|------------|------------|-------------|-------------|-------------|
| Voice Cloning | ✅ Instant + Pro | ✅ | ❌ | ❌ | ❌ | ✅ (limited) |
| Multilingual | 32 langs | 13+ langs | 57 langs | 50+ langs | 30+ langs | 100+ langs |
| Streaming | ✅ WebSocket + REST | ✅ | ✅ | ✅ | ✅ | ✅ |
| Real-time latency | ~75ms (Flash) | ~200ms | ~300ms | ~200ms | ~150ms | ~200ms |
| SSML Support | Limited | ❌ | ❌ | ✅ Full | ✅ Full | ✅ Full |
| Voice Design | ✅ Text prompt | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sound Effects | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Dubbing | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Speech-to-Text | ✅ (Scribe) | ❌ | ✅ (Whisper) | ✅ | ✅ | ✅ |
| Music Generation | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

## 6. Cost Projections at Scale

### 1,000 minutes/month

| Provider | Monthly Cost |
|----------|-------------|
| ElevenLabs Pro (Flash) | $99 (included in plan) |
| ElevenLabs Creator (Flash) | $22 + overage: ~$120 total |
| Fish Audio | ~$15 |
| OpenAI TTS | ~$15 |
| Google Neural | ~$16 |
| Amazon Polly Neural | ~$16 |

### 10,000 minutes/month

| Provider | Monthly Cost |
|----------|-------------|
| ElevenLabs Scale (Flash) | $330 + $540 overage = ~$870 |
| ElevenLabs Business (Flash) | $1,320 (included) |
| Fish Audio | ~$150 |
| OpenAI TTS | ~$150 |
| Google Neural | ~$160 |
| Amazon Polly Neural | ~$160 |

### 100,000 minutes/month

| Provider | Monthly Cost |
|----------|-------------|
| ElevenLabs Business (Flash) | $1,320 + $4,680 overage = ~$6,000 |
| ElevenLabs Enterprise | Custom (likely $3K-5K+) |
| Fish Audio | ~$1,500 |
| OpenAI TTS | ~$1,500 |
| Google Neural | ~$1,600 |
| Amazon Polly Neural | ~$1,600 |

## 7. Recommendations for Nathan's Projects

### Ultrafone (Currently Fish Audio)

**Recommendation: Stay with Fish Audio** 🐟

- Ultrafone is a telephony/voice product where **cost per minute matters enormously** at scale
- Fish Audio provides good quality at ~$0.015/min vs ElevenLabs ~$0.06-0.10/min
- Fish Audio already integrated and working
- **Exception:** If voice quality complaints emerge from users, consider ElevenLabs Flash for premium tier at ~$0.06/min (Business tier), offering it as an upgrade option
- At 10K min/month: Fish = ~$150, 11Labs = ~$870-1,320. **That's 6-9x cost difference.**

### NarrativeReactor (Content TTS)

**Recommendation: ElevenLabs Starter ($5/mo) or Creator ($22/mo) for now** 📖

- Content generation values **quality over cost** — ElevenLabs excels here
- NarrativeReactor content is pre-generated (not real-time), so latency doesn't matter
- Use **Multilingual v2/v3** for maximum quality
- Starter gives 30K multilingual chars (~30 min audio) for $5/mo — plenty for testing
- Creator gives 100K chars (~100 min) for $22/mo with overage option
- **Voice cloning** could be a differentiator for NarrativeReactor (clone narrator voices)
- Consider the **Startup Grants Program** — 12 months free with 33M characters if eligible

### Hybrid Strategy

1. **Fish Audio** → Ultrafone production TTS (cost-optimized)
2. **ElevenLabs Starter/Creator** → NarrativeReactor content (quality-optimized)
3. **Deepgram** → STT (already configured, excellent value)
4. **ElevenLabs Scribe** → Consider for STT if Deepgram becomes insufficient

### Should Nathan Get an ElevenLabs API Key?

**Yes, at Starter ($5/mo) minimum.** The quality gap is worth $5/mo for content use cases. The free tier has no API access for TTS, so Starter is the entry point.

---

## 8. Additional Notes

- **Credits roll over** for up to 2 months on paid plans
- **Flash/Turbo models** use 0.5 credits per character (effectively half price)
- **Yearly billing** saves ~17% across all tiers
- **Startup Grants**: 12 months free + 33M characters — worth applying if eligible
- **ElevenLabs Conversational AI (Agents)**: Included with plans, $0.09/min for calls — could be interesting for Ultrafone's AI agent features

---

*Analysis based on elevenlabs.io/pricing scraped 2026-02-18. Prices may change.*
