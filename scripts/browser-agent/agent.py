#!/usr/bin/env python3
"""
BrowserUse Agent Wrapper for Monster Agents
============================================
Provides browser automation for debugging, verification, and web tasks.

Usage:
    python3 agent.py "Go to https://example.com and check if it's working"
    python3 agent.py --model gpt-4o-mini "Log into Railway and check service status"
    python3 agent.py --model claude-sonnet-4-6 "Navigate to the demo and take a screenshot"
"""

import asyncio
import argparse
import json
import os
import sys
from datetime import datetime


async def run_browser_task(task: str, model: str = "gpt-4o-mini", 
                           provider: str = "openai", max_steps: int = 10,
                           headless: bool = True, use_vision: bool = False,
                           save_recording: str = None):
    """Run a browser task using browser-use."""
    from browser_use import Agent
    from browser_use.browser.profile import BrowserProfile
    
    # Select LLM based on provider
    if provider == "openai":
        from browser_use.llm.openai.chat import ChatOpenAI as LLM
        llm = LLM(model=model, api_key=os.environ["OPENAI_API_KEY"])
    elif provider == "anthropic":
        from browser_use.llm.anthropic.chat import ChatAnthropic as LLM
        llm = LLM(model=model, api_key=os.environ["ANTHROPIC_API_KEY"])
    else:
        raise ValueError(f"Unknown provider: {provider}")
    
    profile = BrowserProfile(
        headless=headless,
        disable_security=True,
    )
    
    agent = Agent(
        task=task,
        llm=llm,
        browser_profile=profile,
        use_vision=use_vision,
        max_actions_per_step=5,
    )
    
    start_time = datetime.utcnow()
    result = await agent.run(max_steps=max_steps)
    end_time = datetime.utcnow()
    
    final_result = result.final_result()
    history = result.history
    
    output = {
        "task": task,
        "model": model,
        "provider": provider,
        "result": final_result,
        "steps": len(history) if isinstance(history, list) else 0,
        "duration_ms": int((end_time - start_time).total_seconds() * 1000),
        "timestamp": start_time.isoformat() + "Z",
        "success": True,
    }
    
    await agent.close()
    return output


def main():
    parser = argparse.ArgumentParser(description="BrowserUse Agent for Monster Agents")
    parser.add_argument("task", help="Task description for the browser agent")
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM model to use")
    parser.add_argument("--provider", default="openai", choices=["openai", "anthropic"],
                        help="LLM provider")
    parser.add_argument("--max-steps", type=int, default=10, help="Max browser steps")
    parser.add_argument("--vision", action="store_true", help="Enable vision mode")
    parser.add_argument("--show", action="store_true", help="Show browser (not headless)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    try:
        result = asyncio.run(run_browser_task(
            task=args.task,
            model=args.model,
            provider=args.provider,
            max_steps=args.max_steps,
            headless=not args.show,
            use_vision=args.vision,
        ))
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n🌐 Browser Task Complete")
            print(f"   Model: {result['model']} ({result['provider']})")
            print(f"   Steps: {result['steps']}")
            print(f"   Time: {result['duration_ms']}ms")
            print(f"\n📄 Result:\n{result['result']}")
            
    except Exception as e:
        error = {"task": args.task, "success": False, "error": str(e)}
        if args.json:
            print(json.dumps(error, indent=2))
        else:
            print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
