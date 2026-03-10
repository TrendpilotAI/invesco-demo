"""Quality scoring — uses Claude Opus to judge model outputs."""

import os
import json
import httpx
from typing import Optional


JUDGE_SYSTEM = """You are an expert evaluator comparing AI model outputs. 
Score each output on these dimensions (1-10 scale):
- **Completeness**: Does it fully address all parts of the prompt?
- **Correctness**: Are the facts, code, and reasoning accurate?
- **Depth**: Does it go beyond surface-level analysis?
- **Clarity**: Is it well-organized and easy to follow?
- **Actionability**: Can someone act on this output directly?

Return your evaluation as valid JSON with this exact structure:
{
  "evaluations": [
    {
      "model": "<model_key>",
      "scores": {
        "completeness": <1-10>,
        "correctness": <1-10>,
        "depth": <1-10>,
        "clarity": <1-10>,
        "actionability": <1-10>
      },
      "overall": <1-10>,
      "strengths": "<brief strengths>",
      "weaknesses": "<brief weaknesses>"
    }
  ],
  "ranking": ["<best_model>", "<second>", ...],
  "ranking_explanation": "<why this order>"
}

Be fair and objective. Judge the content quality, not the model brand."""


def judge_outputs(task_key: str, task_name: str, task_prompt: str, outputs: dict[str, str]) -> Optional[dict]:
    """
    Judge multiple model outputs for the same task using Claude Opus.
    
    Args:
        task_key: Task identifier
        task_name: Human-readable task name
        task_prompt: The original prompt
        outputs: Dict of {model_key: output_content}
    
    Returns:
        Evaluation dict or None on error
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ⚠️  ANTHROPIC_API_KEY not set, skipping judging")
        return None

    # Build the evaluation prompt
    parts = [f"# Task: {task_name}\n\n**Original Prompt:**\n{task_prompt}\n\n---\n"]
    for model_key, content in outputs.items():
        # Truncate very long outputs to keep within context
        truncated = content[:8000] + "\n...[truncated]" if len(content) > 8000 else content
        parts.append(f"## Output from: {model_key}\n\n{truncated}\n\n---\n")
    
    parts.append("Evaluate all outputs above. Return ONLY valid JSON, no markdown fences.")

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": "claude-opus-4-20250514",
        "max_tokens": 4000,
        "system": JUDGE_SYSTEM,
        "messages": [{"role": "user", "content": "\n".join(parts)}],
    }

    try:
        with httpx.Client(timeout=300) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
        
        data = resp.json()
        content = "".join(b["text"] for b in data.get("content", []) if b["type"] == "text")
        
        # Parse JSON from response (handle potential markdown fences)
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content[:-3]
        
        evaluation = json.loads(content)
        evaluation["task_key"] = task_key
        evaluation["task_name"] = task_name
        evaluation["models_evaluated"] = list(outputs.keys())
        return evaluation
        
    except Exception as e:
        print(f"  ❌ Judging failed: {e}")
        return None


def save_judgement(evaluation: dict, results_dir: str = "results") -> str:
    """Save judgement to file."""
    import os
    os.makedirs(results_dir, exist_ok=True)
    filepath = os.path.join(results_dir, f"judge_{evaluation['task_key']}.json")
    with open(filepath, "w") as f:
        json.dump(evaluation, f, indent=2)
    return filepath
