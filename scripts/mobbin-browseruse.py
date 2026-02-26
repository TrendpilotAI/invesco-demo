#!/usr/bin/env python3
"""
Mobbin crawler using BrowserUse Cloud API.
Creates a persistent profile for Mobbin login, then scrapes iOS app design patterns.
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel
from typing import Optional

os.environ["BROWSER_USE_API_KEY"] = "bu_DA6iHHkI3k3SwdvXxs6LmpNRUu5sUZD-_VTLFxwReP8"

from browser_use_sdk import AsyncBrowserUse

OUTPUT_DIR = Path("/data/workspace/projects/ultraclaw-ios/screenshots")
DATA_DIR = Path("/data/workspace/projects/ultraclaw-ios/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_FILE = DATA_DIR / "mobbin-profile-id.txt"

# Structured outputs
class MobbinApp(BaseModel):
    app_name: str
    category: str
    description: Optional[str]
    screens: list[str]  # screen names/descriptions
    notable_patterns: list[str]  # design patterns observed

class MobbinSearchResult(BaseModel):
    apps: list[MobbinApp]
    total_found: int
    query: str

async def get_or_create_profile(client: AsyncBrowserUse) -> str:
    """Get existing Mobbin profile or create a new one with login."""
    if PROFILE_FILE.exists():
        profile_id = PROFILE_FILE.read_text().strip()
        print(f"✅ Using existing Mobbin profile: {profile_id}")
        return profile_id

    print("📝 Creating new Mobbin profile with Google OAuth login...")
    profile = await client.profiles.create(name="mobbin-trendpilot")
    session = await client.sessions.create(profile_id=profile.id)

    # Login to Mobbin via Google OAuth
    result = await client.run(
        """
        Go to https://mobbin.com and log in using Google OAuth.
        Click the "Continue with Google" button.
        When Google login appears, use the email: trendpilot.ai@gmail.com
        Try password: Grenada2@26 first, if it fails try Grenada2@25
        Complete the login and make sure you land on the Mobbin dashboard.
        Confirm you are logged in by looking for user avatar or profile icon.
        Return "logged_in" if successful, "failed" if login didn't work.
        """,
        session_id=session.id,
        vision=True,
        thinking=True,
        max_steps=25,
        secrets={
            "trendpilot.ai@gmail.com": "Grenada2@26",
        },
    )

    print(f"Login result: {result.output}")

    if "logged_in" in str(result.output).lower() or "success" in str(result.output).lower():
        PROFILE_FILE.write_text(profile.id)
        print(f"✅ Profile created and saved: {profile.id}")
        await client.sessions.stop(session.id)
        return profile.id
    else:
        # Try alt password
        print("🔄 Trying alternate password...")
        result2 = await client.run(
            """
            Go to https://mobbin.com and log in using Google OAuth.
            Click "Continue with Google".
            Use email: trendpilot.ai@gmail.com and password: Grenada2@25
            Complete login and confirm you're on the Mobbin dashboard.
            Return "logged_in" if successful.
            """,
            session_id=session.id,
            vision=True,
            thinking=True,
            max_steps=20,
            secrets={
                "trendpilot.ai@gmail.com": "Grenada2@25",
            },
        )
        print(f"Alt login result: {result2.output}")
        PROFILE_FILE.write_text(profile.id)
        await client.sessions.stop(session.id)
        return profile.id


async def scrape_ios_patterns(client: AsyncBrowserUse, profile_id: str, query: str, max_apps: int = 10) -> MobbinSearchResult:
    """Scrape Mobbin for iOS design patterns matching a query."""
    session = await client.sessions.create(profile_id=profile_id)
    print(f"🔍 Scraping Mobbin for: '{query}'")

    try:
        result = await client.run(
            f"""
            Go to https://mobbin.com/browse/ios/apps
            Search for "{query}" in the search box.
            Browse the results and for each app found (up to {max_apps}):
              1. Note the app name and category
              2. Click into the app to see its screens
              3. Look at 3-5 screens and note the design patterns
              4. Note colors, typography style, layout patterns, navigation patterns
              5. Note any unique or standout UI elements

            Focus on these design aspects:
            - Navigation patterns (tab bars, side menus, bottom sheets)
            - List/grid layouts and how information is displayed
            - Typography hierarchy and font choices
            - Color usage and theming
            - Animation hints or micro-interaction indicators
            - Onboarding patterns
            - Dashboard/home screen layouts

            Return structured data with app names, categories, and notable design patterns.
            """,
            session_id=session.id,
            output_schema=MobbinSearchResult,
            vision=True,
            thinking=True,
            max_steps=50,
            allowed_domains=["mobbin.com"],
        )
        return result.output
    finally:
        await client.sessions.stop(session.id)


async def scrape_top_ios_apps(client: AsyncBrowserUse, profile_id: str) -> dict:
    """Scrape top iOS app designs from Mobbin homepage."""
    session = await client.sessions.create(profile_id=profile_id)
    print("🏆 Scraping Mobbin top iOS apps...")

    try:
        result = await client.run(
            """
            Go to https://mobbin.com/browse/ios/apps
            Look at the featured/trending iOS apps shown.
            For each of the top 15 apps visible:
              1. Note the app name, category, number of screens
              2. Click into 5-6 apps that look most relevant for a "professional AI agent management app"
              3. For each clicked app, look at 4-5 screens
              4. Capture:
                 - Primary color palette (hex codes if visible)
                 - Typography style (serif/sans, size hierarchy)
                 - Navigation pattern
                 - Information density level (sparse/medium/dense)
                 - Key UI components used
                 - Overall aesthetic (minimal, editorial, playful, corporate, etc.)
                 - Any unique/innovative UI patterns worth noting

            We are building an iOS app for AI agent management (like a Bloomberg Terminal for AI).
            Focus on apps that show:
            - Dense information display
            - Professional/premium aesthetics
            - Dashboard-style layouts
            - Dark mode implementations
            - Command/control center vibes

            Return a comprehensive list of apps and their design characteristics.
            """,
            session_id=session.id,
            output_schema=MobbinSearchResult,
            vision=True,
            thinking=True,
            max_steps=60,
            allowed_domains=["mobbin.com"],
        )
        return {"query": "top_ios_apps", "apps": result.output}
    finally:
        await client.sessions.stop(session.id)


async def main():
    client = AsyncBrowserUse()

    print("🦅 UltraClaw — Mobbin Design Research via BrowserUse Cloud")
    print("=" * 60)

    # Step 1: Get or create persistent login profile
    profile_id = await get_or_create_profile(client)

    # Step 2: Scrape design patterns for our target queries
    queries = [
        "AI assistant",
        "dashboard",
        "productivity",
        "finance",
        "news reader",
    ]

    all_results = {}

    # First scrape top apps
    print("\n📊 Phase 1: Top iOS apps overview")
    try:
        top_result = await scrape_top_ios_apps(client, profile_id)
        all_results["top_apps"] = top_result
        print(f"✅ Found top apps data")
    except Exception as e:
        print(f"⚠️  Top apps scrape error: {e}")

    # Then scrape specific queries
    print("\n🔍 Phase 2: Category-specific searches")
    for query in queries:
        try:
            result = await scrape_ios_patterns(client, profile_id, query, max_apps=5)
            all_results[query] = {
                "query": result.query,
                "total_found": result.total_found,
                "apps": [app.model_dump() for app in result.apps],
            }
            print(f"✅ '{query}': {result.total_found} apps found, {len(result.apps)} analyzed")
        except Exception as e:
            print(f"⚠️  '{query}' scrape error: {e}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_file = DATA_DIR / f"mobbin_results_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n✅ Results saved to: {output_file}")
    print(f"📦 Total queries completed: {len(all_results)}")

    # Print summary
    total_apps = sum(
        len(v.get("apps", [])) if isinstance(v, dict) else 0
        for v in all_results.values()
    )
    print(f"🎨 Total app designs analyzed: {total_apps}")

    return output_file


if __name__ == "__main__":
    asyncio.run(main())
