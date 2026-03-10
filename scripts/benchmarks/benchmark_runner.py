"""Main benchmark orchestrator — runs tasks across models, collects metrics."""

import os
import json
import time
import httpx
from datetime import datetime, timezone
from typing import Optional

# Model configurations
MODELS = {
    "claude-sonnet-4-6": {
        "provider": "anthropic",
        "model_id": "claude-sonnet-4-20250514",
        "display_name": "Claude Sonnet 4",
        "pricing": {"input_per_1m": 3.00, "output_per_1m": 15.00},
    },
    "claude-opus-4-6": {
        "provider": "anthropic",
        "model_id": "claude-opus-4-20250514",
        "display_name": "Claude Opus 4",
        "pricing": {"input_per_1m": 15.00, "output_per_1m": 75.00},
    },
    "gpt-5.4": {
        "provider": "openai",
        "model_id": "gpt-4.1",
        "display_name": "GPT-4.1",
        "pricing": {"input_per_1m": 2.00, "output_per_1m": 8.00},
    },
    "deepseek-chat": {
        "provider": "deepseek",
        "model_id": "deepseek-chat",
        "display_name": "DeepSeek Chat",
        "pricing": {"input_per_1m": 0.27, "output_per_1m": 1.10},
    },
}

MAX_RETRIES = 3
RETRY_BACKOFF = [2, 5, 15]  # seconds


def get_api_key(provider: str) -> str:
    """Get API key for provider from environment."""
    key_map = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
    }
    env_var = key_map[provider]
    key = os.environ.get(env_var)
    if not key:
        raise ValueError(f"Missing {env_var} environment variable")
    return key


def call_anthropic(model_id: str, system: str, prompt: str, max_tokens: int, api_key: str) -> dict:
    """Call Anthropic Messages API."""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": model_id,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }

    start = time.monotonic()
    with httpx.Client(timeout=300) as client:
        resp = client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
    elapsed_ms = (time.monotonic() - start) * 1000

    data = resp.json()
    content = "".join(b["text"] for b in data.get("content", []) if b["type"] == "text")
    usage = data.get("usage", {})
    stop_reason = data.get("stop_reason", "unknown")

    return {
        "content": content,
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "elapsed_ms": elapsed_ms,
        "stop_reason": stop_reason,
        "status": "complete" if stop_reason == "end_turn" else ("truncated" if stop_reason == "max_tokens" else stop_reason),
    }


def call_openai(model_id: str, system: str, prompt: str, max_tokens: int, api_key: str) -> dict:
    """Call OpenAI Chat Completions API."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_id,
        "max_completion_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    }

    start = time.monotonic()
    with httpx.Client(timeout=300) as client:
        resp = client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
    elapsed_ms = (time.monotonic() - start) * 1000

    data = resp.json()
    choice = data["choices"][0]
    content = choice["message"]["content"] or ""
    usage = data.get("usage", {})
    finish = choice.get("finish_reason", "unknown")

    return {
        "content": content,
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
        "elapsed_ms": elapsed_ms,
        "stop_reason": finish,
        "status": "complete" if finish == "stop" else ("truncated" if finish == "length" else finish),
    }


def call_deepseek(model_id: str, system: str, prompt: str, max_tokens: int, api_key: str) -> dict:
    """Call DeepSeek API (OpenAI-compatible)."""
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_id,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    }

    start = time.monotonic()
    with httpx.Client(timeout=300) as client:
        resp = client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
    elapsed_ms = (time.monotonic() - start) * 1000

    data = resp.json()
    choice = data["choices"][0]
    content = choice["message"]["content"] or ""
    usage = data.get("usage", {})
    finish = choice.get("finish_reason", "unknown")

    return {
        "content": content,
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
        "elapsed_ms": elapsed_ms,
        "stop_reason": finish,
        "status": "complete" if finish == "stop" else ("truncated" if finish == "length" else finish),
    }


PROVIDER_CALLERS = {
    "anthropic": call_anthropic,
    "openai": call_openai,
    "deepseek": call_deepseek,
}


def estimate_cost(model_key: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate cost in USD."""
    pricing = MODELS[model_key]["pricing"]
    return (input_tokens / 1_000_000 * pricing["input_per_1m"]) + (
        output_tokens / 1_000_000 * pricing["output_per_1m"]
    )


def run_single(model_key: str, task_key: str, task: dict, dry_run: bool = False) -> dict:
    """Run a single benchmark: one model × one task."""
    model_cfg = MODELS[model_key]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    result = {
        "timestamp": timestamp,
        "model_key": model_key,
        "model_id": model_cfg["model_id"],
        "model_display": model_cfg["display_name"],
        "provider": model_cfg["provider"],
        "task_key": task_key,
        "task_name": task["name"],
        "max_tokens": task["max_tokens"],
    }

    if dry_run:
        result.update({
            "dry_run": True,
            "status": "dry_run",
            "elapsed_ms": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "tokens_per_second": 0,
            "cost_usd": 0,
            "content_chars": 0,
            "content_lines": 0,
            "content": "",
        })
        return result

    caller = PROVIDER_CALLERS[model_cfg["provider"]]
    api_key = get_api_key(model_cfg["provider"])

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            api_result = caller(
                model_id=model_cfg["model_id"],
                system=task["system"],
                prompt=task["prompt"],
                max_tokens=task["max_tokens"],
                api_key=api_key,
            )
            break
        except httpx.HTTPStatusError as e:
            last_error = e
            if e.response.status_code == 429:
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                print(f"  ⏳ Rate limited, retrying in {wait}s...")
                time.sleep(wait)
            elif e.response.status_code >= 500:
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                print(f"  ⏳ Server error {e.response.status_code}, retrying in {wait}s...")
                time.sleep(wait)
            else:
                # 400 or other client error — don't retry
                error_body = ""
                try:
                    error_body = e.response.text[:200]
                except Exception:
                    pass
                result.update({
                    "status": "error",
                    "error": f"HTTP {e.response.status_code}: {error_body}",
                    "elapsed_ms": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "tokens_per_second": 0,
                    "cost_usd": 0,
                    "content_chars": 0,
                    "content_lines": 0,
                    "content": "",
                })
                return result
        except (httpx.ConnectError, httpx.ReadTimeout) as e:
            last_error = e
            wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
            print(f"  ⏳ Connection error, retrying in {wait}s...")
            time.sleep(wait)
    else:
        result.update({
            "status": "error",
            "error": str(last_error),
            "elapsed_ms": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "tokens_per_second": 0,
            "cost_usd": 0,
            "content_chars": 0,
            "content_lines": 0,
            "content": "",
        })
        return result

    content = api_result["content"]
    output_tokens = api_result["output_tokens"]
    elapsed_s = api_result["elapsed_ms"] / 1000
    tps = output_tokens / elapsed_s if elapsed_s > 0 else 0

    result.update({
        "status": api_result["status"],
        "stop_reason": api_result["stop_reason"],
        "elapsed_ms": round(api_result["elapsed_ms"], 1),
        "input_tokens": api_result["input_tokens"],
        "output_tokens": output_tokens,
        "tokens_per_second": round(tps, 1),
        "cost_usd": round(estimate_cost(model_key, api_result["input_tokens"], output_tokens), 6),
        "content_chars": len(content),
        "content_lines": content.count("\n") + 1 if content else 0,
        "content": content,
    })
    return result


def save_result(result: dict, results_dir: str = "results") -> str:
    """Save a single result to JSON file."""
    os.makedirs(results_dir, exist_ok=True)
    filename = f"{result['timestamp']}_{result['task_key']}_{result['model_key']}.json"
    filepath = os.path.join(results_dir, filename)
    with open(filepath, "w") as f:
        json.dump(result, f, indent=2)
    return filepath


def format_markdown_table(results: list[dict]) -> str:
    """Format results as a markdown table."""
    if not results:
        return "No results."

    lines = [
        "| Model | Task | Time (ms) | In Tokens | Out Tokens | TPS | Cost ($) | Chars | Lines | Status |",
        "|-------|------|-----------|-----------|------------|-----|----------|-------|-------|--------|",
    ]
    for r in results:
        lines.append(
            f"| {r['model_display']} | {r['task_name']} | {r['elapsed_ms']:,.0f} | "
            f"{r['input_tokens']:,} | {r['output_tokens']:,} | {r['tokens_per_second']:.1f} | "
            f"${r['cost_usd']:.4f} | {r['content_chars']:,} | {r['content_lines']:,} | {r['status']} |"
        )
    return "\n".join(lines)


def save_combined_results(results: list[dict], results_dir: str = "results") -> str:
    """Save all results (without content) to a combined results.json for the dashboard."""
    os.makedirs(results_dir, exist_ok=True)
    # Strip content for the combined file to keep it small
    slim = []
    for r in results:
        slim_r = {k: v for k, v in r.items() if k != "content"}
        slim.append(slim_r)
    filepath = os.path.join(results_dir, "results.json")
    with open(filepath, "w") as f:
        json.dump(slim, f, indent=2)
    return filepath
