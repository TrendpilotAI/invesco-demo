"""
Bragi Content Generator — AI-powered social media content generation.
Uses DeepSeek (cheap) or OpenAI as fallback for generating platform-specific posts.
"""

import os
import json
import uuid
from datetime import datetime, timezone
from typing import Optional

from content_rules import PERSONAS, GLOBAL_FORBIDDEN, validate_post

# Try to import OpenAI-compatible client (works with DeepSeek too)
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def _get_llm_client():
    """Get an LLM client — prefer DeepSeek, fall back to OpenAI."""
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if deepseek_key:
        return OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com"), "deepseek-chat"
    elif openai_key:
        return OpenAI(api_key=openai_key), "gpt-4o-mini"
    else:
        return None, None


def _build_system_prompt(persona_key: str) -> str:
    """Build a system prompt for content generation based on persona."""
    persona = PERSONAS[persona_key]
    forbidden_list = "\n".join(f"- {f}" for f in GLOBAL_FORBIDDEN[:6])
    persona_forbidden = "\n".join(f"- {f}" for f in persona["forbidden_topics"])
    examples = "\n".join(f'- "{e}"' for e in persona["example_tones"])

    return f"""You are a social media content writer for Nathan Stevenson.
You write as Nathan — first person, authentic voice.

PERSONA: {persona['label']} ({persona['handle']})
PLATFORM: {persona['platform']}
TONE: {persona['tone']}
MAX LENGTH: {persona['max_length']} characters (STRICT — never exceed this)

FOCUS AREAS:
{chr(10).join('- ' + f for f in persona['focus'])}

HASHTAG STRATEGY: {persona['hashtag_strategy']}

EXAMPLE TONES:
{examples}

🚫 NEVER MENTION:
{forbidden_list}
{persona_forbidden}

RULES:
1. Write ONLY the post text. No explanations, no meta-commentary.
2. Stay within the character limit. Count carefully.
3. Sound like a real person, not an AI. No corporate buzzwords.
4. Be specific when possible — vague platitudes are boring.
5. Hashtags go at the end if used. Keep them minimal.
6. NEVER use these words/phrases: "delve", "leverage", "ecosystem", "synergy", "game-changer", "revolutionary"
7. No emojis on Twitter/LinkedIn unless very natural. Threads/TikTok can be more casual.
"""


class ContentGenerator:
    def __init__(self):
        self.client, self.model = _get_llm_client()

    def generate_post(
        self,
        topic: str,
        persona: str,
        platform: Optional[str] = None,
        style: Optional[str] = None,
    ) -> dict:
        """Generate a post tailored for a specific persona + platform.

        Returns: {id, text, hashtags, platform, persona, account_id, status, created_at}
        """
        if persona not in PERSONAS:
            raise ValueError(f"Unknown persona: {persona}. Use: {list(PERSONAS.keys())}")

        persona_config = PERSONAS[persona]
        platform = platform or persona_config["platform"]

        # Build the generation prompt
        user_prompt = f"Write a {platform} post about: {topic}"
        if style:
            user_prompt += f"\nStyle: {style}"

        # Generate via LLM if available, otherwise use template
        if self.client:
            text = self._generate_via_llm(persona, user_prompt)
        else:
            text = self._generate_template(topic, persona)

        # Extract hashtags
        hashtags = [w for w in text.split() if w.startswith("#")]

        # Validate
        violations = validate_post(text, persona)
        if violations:
            # Try to fix — truncate if too long
            if any("Too long" in v for v in violations):
                max_len = persona_config["max_length"]
                text = text[:max_len - 3].rsplit(" ", 1)[0] + "..."
                violations = validate_post(text, persona)

        return {
            "id": str(uuid.uuid4())[:8],
            "text": text,
            "hashtags": hashtags,
            "platform": platform,
            "persona": persona,
            "persona_label": persona_config["label"],
            "account_id": persona_config["account_id"],
            "handle": persona_config["handle"],
            "status": "draft",
            "violations": violations,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def _generate_via_llm(self, persona: str, user_prompt: str) -> str:
        """Generate content using an LLM."""
        system_prompt = _build_system_prompt(persona)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip().strip('"')

    def _generate_template(self, topic: str, persona: str) -> str:
        """Fallback template-based generation when no LLM API key is available."""
        templates = {
            "enterprise": [
                f"Shipped {topic} today. The compounding effect of small daily improvements is real.",
                f"Been thinking about {topic}. The teams that win are the ones that ship fast and iterate faster.",
                f"{topic} — this is what we've been building toward. More soon.",
            ],
            "blend": [
                f"Spent the morning on {topic}. The open source community keeps raising the bar. 🔧",
                f"Building {topic} locally and it's working better than expected. The future is self-hosted.",
                f"{topic} is one of those things that sounds complex but the tools are finally there.",
            ],
            "professional": [
                f"At ForwardLane, we've been investing heavily in {topic}. Here's what we've learned:\n\nThe key insight is that enterprise AI isn't about having the best model — it's about having the best workflow around the model.\n\n{topic} represents a shift in how we think about AI deployment in regulated industries.",
                f"Three things I've learned about {topic} in enterprise AI:\n\n1. Start with the workflow, not the technology\n2. Compliance isn't a blocker — it's a design constraint\n3. The best AI products are the ones users forget are AI",
            ],
            "consumer": [
                f"Built {topic} in 20 minutes with local LLMs 🔥 No API costs. No rate limits. Just vibes.",
                f"Stop paying for AI APIs when you can run {topic} yourself. Here's the move. 🤖",
                f"{topic} — the open source version is actually better now. We're in the golden age. ✨",
            ],
        }
        import random
        options = templates.get(persona, templates["enterprise"])
        return random.choice(options)

    def generate_daily_batch(self, topics: Optional[list[str]] = None) -> list[dict]:
        """Generate a full day's content across all personas/platforms.

        Returns list of draft posts for approval.
        """
        if not topics:
            topics = [
                "AI agent workflows",
                "shipping product updates",
                "open source AI tools",
            ]

        drafts = []

        for persona_key, persona_config in PERSONAS.items():
            num_posts = persona_config["posts_per_day"]
            for i in range(num_posts):
                topic = topics[i % len(topics)]
                try:
                    post = self.generate_post(
                        topic=topic,
                        persona=persona_key,
                    )
                    drafts.append(post)
                except Exception as e:
                    drafts.append({
                        "id": str(uuid.uuid4())[:8],
                        "error": str(e),
                        "persona": persona_key,
                        "platform": persona_config["platform"],
                        "status": "error",
                    })

        return drafts


def save_drafts(drafts: list[dict], path: str = "drafts.json"):
    """Save drafts to a JSON file for the approval dashboard."""
    with open(path, "w") as f:
        json.dump({"drafts": drafts, "generated_at": datetime.now(timezone.utc).isoformat()}, f, indent=2)
    print(f"💾 Saved {len(drafts)} drafts to {path}")


# ── Quick test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    gen = ContentGenerator()
    print("Generating sample posts...\n")

    samples = [
        ("AI agent fleet management", "enterprise"),
        ("Running local LLMs on consumer hardware", "blend"),
        ("Enterprise AI compliance", "professional"),
    ]

    for topic, persona in samples:
        post = gen.generate_post(topic, persona)
        print(f"[{post['persona_label']}] {post['handle']} ({post['platform']})")
        print(f"  {post['text']}")
        if post['violations']:
            print(f"  ⚠️  Violations: {post['violations']}")
        print()
