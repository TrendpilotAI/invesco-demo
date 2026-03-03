"""
Composio + Claude Agent SDK — ForwardLane Sales Pipeline Monitor
Connects HubSpot + Gmail for pipeline monitoring
"""
import asyncio
import os
from composio import Composio
from composio_claude_agent_sdk import ClaudeAgentSDKProvider

# Initialize Composio
composio = Composio(
    api_key=os.environ.get("COMPOSIO_API_KEY"),
    provider=ClaudeAgentSDKProvider()
)

external_user_id = "nathan-stevenson-forwardlane"

async def setup_connections():
    """Authorize HubSpot and Gmail"""
    session = composio.create(
        user_id=external_user_id,
        manage_connections=False,
    )

    # HubSpot
    print("=== HubSpot Authorization ===")
    try:
        hs_request = session.authorize(
            toolkit='hubspot',
            callback_url='https://backend.composio.dev/'
        )
        print(f"🔗 HubSpot auth URL: {hs_request.redirect_url}")
    except Exception as e:
        print(f"HubSpot error: {e}")

    # Gmail
    print("\n=== Gmail Authorization ===")
    try:
        gmail_request = session.authorize(
            toolkit='gmail',
            callback_url='https://backend.composio.dev/'
        )
        print(f"🔗 Gmail auth URL: {gmail_request.redirect_url}")
    except Exception as e:
        print(f"Gmail error: {e}")

    return session

async def check_connections():
    """Check if connections are active"""
    session = composio.create(
        user_id=external_user_id,
    )
    tools = session.tools()
    print(f"\nAvailable tools: {len(tools)}")
    for t in tools[:20]:
        print(f"  - {t.name if hasattr(t, 'name') else t}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        asyncio.run(check_connections())
    else:
        asyncio.run(setup_connections())
