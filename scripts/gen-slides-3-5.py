#!/usr/bin/env python3
"""
Generate carousel slides 3, 4, 5 using Gemini image generation.
Dark minimal aesthetic matching slides 1, 2, 6, 7.
"""

import os
import sys
import time
from google import genai
from google.genai import types

client = genai.Client()
OUTPUT_DIR = "/data/workspace/drafts/carousel-slides"

STYLE_BASE = """
VISUAL STYLE REQUIREMENTS (follow exactly):
- Background: deep dark navy-black (#0B1120), NOT pure black
- Subtle circuit board / PCB trace texture in the background, very faint, glowing with cyan and amber light at an oblique 3D angle
- Primary text color: pure white, heavy bold sans-serif (Inter/Helvetica Neue Black)
- Accent/emphasis text: warm honey gold (#D4A84B)
- Accent glow colors in graphics only: electric cyan (#00C8FF) and amber gold (#D4A84B)
- NO emoji in the slide whatsoever
- NO neon rainbow colors - only the exact 3-color palette: dark navy, white, and honey gold
- NO sparkle particles or sci-fi lightning effects
- Layout: bold headline at top-left, visual/diagram in lower 60%, "ForwardLane" small text bottom-right
- Minimal text - let the diagram speak
- Premium, enterprise fintech aesthetic - clean, confident, minimal
- 1:1 square aspect ratio
- Font: heavy weight sans-serif, sentence case, tight line height
- NO drop shadows on text, NO gradient text
- The mood: a Bloomberg terminal meets Apple product launch
""".strip()

SLIDES = [
    {
        "filename": "slide3-judge-swarm.png",
        "headline": "Twice daily: 17 repos put on trial.",
        "subtext": "3 AM + Noon ET",
        "diagram_description": """
A clean timeline diagram showing:
- A horizontal dark timeline bar with two glowing gold nodes labeled "3 AM" and "12 PM"
- From each node, three thin gold/white lines branch downward to three dark rectangular cards
- Cards labeled: "BRAINSTORM.md", "PLAN.md", "AUDIT.md" 
- Each card has a subtle cyan glow edge
- Below the cards, a single output line converges to a dark panel showing upward/downward score arrows (+/-) and the label "TODOs generated"
- The diagram is centered in the lower 60% of the slide
- Very minimal, clean, no clutter
""".strip(),
        "prompt": None  # will be assembled
    },
    {
        "filename": "slide4-agent-swarm.png",
        "headline": "P0 found. Agent spawned. Code shipped.",
        "subtext": "No humans.",
        "diagram_description": """
A vertical pipeline/flowchart with 5 dark rounded-rectangle steps connected by thin gold arrows pointing downward:
1. "P0 FLAGGED" — subtle red-tinted card (very dark, just a hint of red glow on the border)
2. "AGENT SPAWNED" — electric blue border glow
3. "CODE WRITTEN + TESTS PASS" — neutral dark card
4. "COMMITTED + PUSHED" — honey gold border glow  
5. "SCORE UPDATED. NEXT TASK." — neutral dark card

On the right side, a small stat card: "10-15 agents / night"
The pipeline is centered, clean, with lots of dark breathing room around it
""".strip(),
        "prompt": None
    },
    {
        "filename": "slide5-self-healing.png",
        "headline": "Failures fix themselves.",
        "subtext": "Every 2 hours: health check.",
        "diagram_description": """
A circular loop diagram with three dark rounded-rectangle nodes arranged in a triangle:
- Top: "DEBUG AGENT" with a subtle cyan blue glow
- Bottom-left: "OPS AGENT" with a subtle amber glow  
- Bottom-right: "QA AGENT" with a subtle white glow
- Thin directional arrows (in honey gold) connect them in a clockwise cycle
- In the center of the triangle: small dark circle with the number "3" and text "retries" below it
- Below the main diagram: a thin horizontal bar showing "FAILURE DETECTED" → loop → "RESOLVED"
- Very clean, symmetric, minimal
""".strip(),
        "prompt": None
    }
]

# Assemble full prompts
for slide in SLIDES:
    slide["prompt"] = f"""Create a single square (1:1) social media carousel slide image with this exact content:

HEADLINE (top of slide, large bold white text): "{slide['headline']}"
SUBTEXT (smaller, honey gold, below headline): "{slide['subtext']}"

DIAGRAM TO RENDER (lower 60% of slide):
{slide['diagram_description']}

SMALL TEXT (bottom-right corner, very small, white): "ForwardLane"

{STYLE_BASE}

This is slide for a professional B2B SaaS company (ForwardLane) that builds AI infrastructure. The design must feel premium and enterprise-grade. Study the exact palette. Render as a polished, complete image ready for social media posting. NO placeholder text, NO watermarks."""


def generate_slide(slide: dict, attempt: int = 1) -> bool:
    out_path = os.path.join(OUTPUT_DIR, slide["filename"])
    print(f"\n{'='*60}")
    print(f"Generating: {slide['filename']} (attempt {attempt})")
    print(f"Headline: {slide['headline']}")
    print(f"{'='*60}")
    
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[slide["prompt"]],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
            )
        )
        
        image_saved = False
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                img = part.as_image()
                img.save(out_path)
                print(f"  [OK] Saved to {out_path}")
                image_saved = True
                break
            elif hasattr(part, 'text') and part.text:
                print(f"  [TEXT] {part.text[:200]}")
        
        if not image_saved:
            print(f"  [WARN] No image in response for {slide['filename']}")
            return False
        return True
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    results = []
    for i, slide in enumerate(SLIDES):
        success = generate_slide(slide)
        results.append((slide["filename"], success))
        
        if i < len(SLIDES) - 1:
            print("  Waiting 3s between requests...")
            time.sleep(3)
    
    print("\n" + "="*60)
    print("RESULTS:")
    for fname, ok in results:
        status = "OK" if ok else "FAILED"
        print(f"  [{status}] {fname}")
    
    all_ok = all(ok for _, ok in results)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
