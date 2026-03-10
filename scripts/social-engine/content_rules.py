"""
Bragi Content Rules — Content strategy as structured data.
Defines per-persona rules, forbidden content, and platform limits.
"""

# ── Account IDs ──────────────────────────────────────────────────────────────
ACCOUNTS = {
    "twitter":  {"id": "13496",  "handle": "@NathanStvnsn", "name": "Twitter/X"},
    "threads":  {"id": "4948",   "handle": "@n8.made",      "name": "Threads"},
    "linkedin": {"id": "14262",  "handle": "Nathan Stevenson", "name": "LinkedIn"},
    "tiktok":   {"id": "31967",  "handle": "@n8.ai0",       "name": "TikTok"},
    "youtube_enterprise": {"id": "29040", "handle": "ForwardLane", "name": "YouTube (Enterprise)"},
    "youtube_personal":   {"id": "29041", "handle": "Nathan Stevenson", "name": "YouTube (Personal)"},
}

# ── Persona Definitions ──────────────────────────────────────────────────────
PERSONAS = {
    "enterprise": {
        "label": "Enterprise",
        "platform": "twitter",
        "account_id": "13496",
        "handle": "@NathanStvnsn",
        "tone": "Thought leader, builder, shipping fast. Confident but not arrogant.",
        "focus": [
            "What we're SHIPPING",
            "Workflow updates",
            "AI agent insights",
            "Leadership thoughts",
            "Enterprise AI trends",
        ],
        "forbidden_topics": [
            "Specific architecture details",
            "Competitive advantages (internal)",
            "Internal tooling names",
            "HypeBase",
        ],
        "max_length": 280,
        "posts_per_day": 3,
        "hashtag_strategy": "1-2 relevant hashtags max. Never more than 2. No hashtag spam.",
        "example_tones": [
            "Shipped X today. The compounding is real.",
            "Agents that manage agents. That's the unlock.",
            "Most teams are still building chatbots. We're building fleets.",
        ],
        "color": "#3B82F6",  # blue
    },
    "blend": {
        "label": "Blend",
        "platform": "threads",
        "account_id": "4948",
        "handle": "@n8.made",
        "tone": "Building in public. Personal + enterprise blend. Authentic, slightly nerdy.",
        "focus": [
            "Enterprise insights mixed with consumer AI building",
            "Open source tools and local AI",
            "Self-hosted solutions",
            "Building in public journey",
            "Personal takes on AI trends",
        ],
        "forbidden_topics": [
            "HypeBase",
            "Internal credentials or secrets",
        ],
        "max_length": 500,
        "posts_per_day": 2,
        "hashtag_strategy": "2-3 hashtags. Can be more casual/creative.",
        "example_tones": [
            "Running local models on a Mac Mini and it's surprisingly good.",
            "The gap between open source and closed AI shrinks every week.",
            "Built an agent that manages my social media. Meta? Maybe. Useful? Definitely.",
        ],
        "color": "#8B5CF6",  # purple
    },
    "professional": {
        "label": "Professional",
        "platform": "linkedin",
        "account_id": "14262",
        "handle": "Nathan Stevenson",
        "tone": "Polished, authoritative, professional. Longer form. Thought leadership.",
        "focus": [
            "ForwardLane updates and vision",
            "Signal Studio / SignalHaus",
            "Enterprise AI strategy",
            "Leadership and team building",
            "Industry trends and analysis",
        ],
        "forbidden_topics": [
            "HypeBase",
            "Overly casual language",
            "Internal architecture details",
            "Competitor bashing",
        ],
        "max_length": 3000,
        "posts_per_day": 1,
        "hashtag_strategy": "3-5 professional hashtags. #AI #EnterpriseAI #FinTech etc.",
        "example_tones": [
            "At ForwardLane, we've been thinking about...",
            "The enterprise AI landscape is shifting. Here's what I'm seeing...",
            "Three lessons from building AI products for regulated industries:",
        ],
        "color": "#1E3A5F",  # navy
    },
    "consumer": {
        "label": "Consumer AI",
        "platform": "tiktok",
        "account_id": "31967",
        "handle": "@n8.ai0",
        "tone": "Builder energy. Open source advocate. Short and punchy. Excited about tech.",
        "focus": [
            "Building in public",
            "Open source AI tools",
            "Local/self-hosted AI solutions",
            "Agent building tutorials/insights",
            "Consumer SaaS ideas",
        ],
        "forbidden_topics": [
            "HypeBase",
            "Enterprise client details",
            "ForwardLane internal info",
        ],
        "max_length": 300,
        "posts_per_day": 2,
        "hashtag_strategy": "3-5 trending/discovery hashtags. #AI #OpenSource #BuildInPublic etc.",
        "example_tones": [
            "Built this in 20 minutes with local LLMs 🔥",
            "Stop paying for AI APIs. Run it yourself.",
            "My agent just deployed itself. We're cooked. 🤖",
        ],
        "color": "#10B981",  # green
    },
}

# ── Global Forbidden Content ─────────────────────────────────────────────────
GLOBAL_FORBIDDEN = [
    "HypeBase",
    "hypebase",
    "Hype Base",
    "hype base",
    "HYPEBASE",
    "Internal API keys or credentials",
    "Customer names without permission",
    "Specific revenue numbers",
    "Unreleased product names (unless cleared)",
    "Negative comments about competitors by name",
]

# ── Platform Limits ──────────────────────────────────────────────────────────
PLATFORM_LIMITS = {
    "twitter":  {"max_chars": 280,  "max_images": 4, "max_videos": 1},
    "threads":  {"max_chars": 500,  "max_images": 10, "max_videos": 1},
    "linkedin": {"max_chars": 3000, "max_images": 20, "max_videos": 1},
    "tiktok":   {"max_chars": 300,  "max_images": 0, "max_videos": 1},
    "youtube":  {"max_chars": 5000, "max_images": 0, "max_videos": 1},
}

# ── Posting Schedule (ET) ────────────────────────────────────────────────────
POSTING_SCHEDULE = {
    "twitter":  {"times": ["09:00", "13:00", "17:00"], "timezone": "America/New_York"},
    "threads":  {"times": ["10:00", "15:00"],          "timezone": "America/New_York"},
    "linkedin": {"times": ["08:00"],                   "timezone": "America/New_York"},
    "tiktok":   {"times": ["12:00", "18:00"],          "timezone": "America/New_York"},
}


def validate_post(text: str, persona_key: str) -> list[str]:
    """Validate a post against content rules. Returns list of violations (empty = OK)."""
    violations = []
    persona = PERSONAS.get(persona_key)
    if not persona:
        return [f"Unknown persona: {persona_key}"]

    # Check length
    if len(text) > persona["max_length"]:
        violations.append(
            f"Too long: {len(text)}/{persona['max_length']} chars"
        )

    # Check global forbidden content
    text_lower = text.lower()
    for forbidden in GLOBAL_FORBIDDEN:
        if forbidden.lower() in text_lower:
            violations.append(f"Forbidden content detected: '{forbidden}'")

    # Check persona-specific forbidden topics
    for topic in persona["forbidden_topics"]:
        if topic.lower() in text_lower:
            violations.append(f"Persona-forbidden topic: '{topic}'")

    return violations
