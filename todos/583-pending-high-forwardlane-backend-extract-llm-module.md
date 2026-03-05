# TODO-583: Extract easy_button/llm.py Module

**Priority:** HIGH
**Repo:** forwardlane-backend
**Effort:** M (3h)
**Status:** pending

## Problem
LLM client code (`_call_gemini`, `_call_kimi`, retry/fallback logic) lives inline inside `easy_button/views.py`. It's not reusable, not independently testable, and uses `urllib.request` instead of the `requests` library already in Pipfile.

## Fix

Create `easy_button/llm.py`:

```python
"""Shared LLM client — Gemini primary, Kimi fallback."""
import logging
import os
import requests
from typing import Iterator

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
KIMI_API_KEY = os.environ.get("KIMI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"
KIMI_MODEL = "moonshot-v1-8k"

_session = requests.Session()
_session.headers.update({"Content-Type": "application/json"})


class LLMError(Exception):
    pass


def generate(prompt: str, system: str | None = None, timeout: int = 30) -> str:
    """Generate a completion. Tries Gemini first, falls back to Kimi."""
    try:
        return _call_gemini(prompt, system, timeout)
    except Exception as e:
        logger.warning("Gemini failed (%s), trying Kimi", e)
        return _call_kimi(prompt, system, timeout)


def stream(prompt: str, system: str | None = None) -> Iterator[str]:
    """Stream a completion as SSE chunks."""
    # Gemini streaming endpoint
    ...


def _call_gemini(prompt: str, system: str | None, timeout: int) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    if system:
        body["system_instruction"] = {"parts": [{"text": system}]}
    resp = _session.post(url, json=body, timeout=timeout)
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


def _call_kimi(prompt: str, system: str | None, timeout: int) -> str:
    url = "https://api.moonshot.cn/v1/chat/completions"
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = _session.post(
        url,
        json={"model": KIMI_MODEL, "messages": messages},
        headers={"Authorization": f"Bearer {KIMI_API_KEY}"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
```

Then update `easy_button/views.py` to import from `easy_button.llm` instead of inline functions.

Also add `easy_button/tests/test_llm.py` with mocked `requests.Session`.

## Files
- `easy_button/llm.py` (create)
- `easy_button/views.py` (remove inline LLM functions, import from llm.py)
- `easy_button/tests/test_llm.py` (create)

## Acceptance Criteria
- [ ] `easy_button/llm.py` exists with `generate()` and `stream()` public API
- [ ] Uses `requests.Session` not `urllib.request`
- [ ] `NLQueryView` and `MeetingPrepView` import from `easy_button.llm`
- [ ] Unit tests mock `requests.Session.post` for both Gemini and Kimi
- [ ] Fallback chain tested: Gemini failure → Kimi called

## Dependencies
- None (standalone refactor)
