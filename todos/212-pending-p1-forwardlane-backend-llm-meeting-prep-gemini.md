# 212 · REAL LLM CALLS IN MEETINGPREPVIEW (GEMINI)

**Repo:** forwardlane-backend  
**Priority:** P1 (high demo value — replaces canned templates with personalized AI briefs)  
**Effort:** M (4–6 hours)  
**Status:** pending

---

## Task Description

`MeetingPrepView._generate_talking_points()` (around line 1000–1065 in `easy_button/views.py`)
currently builds talking points using string templates that return identical boilerplate for
every advisor. This is immediately obvious to demo audiences.

Replace it with a real Gemini API call reusing the existing `_call_gemini` / `_call_kimi`
infrastructure already implemented in `NLQueryView`. The result should be a personalized,
context-aware meeting brief referencing the specific advisor's name, AUM figures, signal types,
and Invesco product holdings.

Cache the result in Redis for 300 seconds (same advisor = same brief during a demo session).

---

## Coding Prompt (Agent-Executable)

```
You are modifying forwardlane-backend at /data/workspace/projects/forwardlane-backend/.

CONTEXT: 
- easy_button/views.py contains MeetingPrepView (around line 877)
- NLQueryView (around line 1111) has working _call_gemini() and _call_kimi() methods
- GEMINI_API_KEY env var is already in use
- KIMI_API_KEY env var is the fallback
- Redis is available via django.core.cache

TASK: Replace _generate_talking_points() with a real LLM meeting brief generator.

STEP 1 — Add a shared LLM mixin or copy the methods:
In MeetingPrepView, add the following methods (copy from NLQueryView and adjust):

  def _call_gemini(self, prompt: str) -> str:
      """Call Gemini Flash API. Returns response text or raises Exception."""
      import os, json
      import urllib.request as _req
      import urllib.error as _err
      
      api_key = os.environ.get('GEMINI_API_KEY', '')
      if not api_key:
          raise ValueError("GEMINI_API_KEY not configured")
      
      url = (
          "https://generativelanguage.googleapis.com/v1beta/models/"
          f"gemini-2.0-flash:generateContent?key={api_key}"
      )
      body = json.dumps({
          "contents": [{"parts": [{"text": prompt}]}],
          "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024}
      }).encode()
      req = _req.Request(url, data=body, headers={"Content-Type": "application/json"})
      with _req.urlopen(req, timeout=15) as resp:
          data = json.loads(resp.read())
      return data["candidates"][0]["content"]["parts"][0]["text"]

  def _call_kimi(self, prompt: str) -> str:
      """Fallback LLM: Kimi K2.5 via Moonshot AI. Returns response text."""
      import os, json
      import urllib.request as _req
      
      api_key = os.environ.get('KIMI_API_KEY', '')
      if not api_key:
          raise ValueError("KIMI_API_KEY not configured")
      
      url = "https://api.moonshot.ai/v1/chat/completions"
      body = json.dumps({
          "model": "kimi-k2-0711-preview",
          "messages": [{"role": "user", "content": prompt}],
          "temperature": 0.7,
          "max_tokens": 1024
      }).encode()
      req = _req.Request(url, data=body, headers={
          "Content-Type": "application/json",
          "Authorization": f"Bearer {api_key}"
      })
      with _req.urlopen(req, timeout=15) as resp:
          data = json.loads(resp.read())
      return data["choices"][0]["message"]["content"]

STEP 2 — Replace _generate_talking_points() with _llm_meeting_brief():

  def _llm_meeting_brief(
      self,
      advisor: dict,
      signals: list[dict],
      holdings: list[dict],
      flows: list[dict]
  ) -> dict:
      """
      Generate a personalized meeting brief using Gemini Flash.
      Falls back to Kimi K2.5, then static template on failure.
      Results cached in Redis for 300 seconds per advisor_id.
      """
      import json
      import hashlib
      from django.core.cache import cache
      
      # Cache check
      advisor_id = advisor.get('advisor_id', '')
      cache_key = f"meeting_brief:{hashlib.md5(advisor_id.encode()).hexdigest()[:12]}"
      cached = cache.get(cache_key)
      if cached:
          return cached
      
      # Build signal summary for prompt
      signal_summary = [
          {"type": s.get('signal_type'), "score": s.get('signal_score'), "label": s.get('label')}
          for s in signals[:5]
      ]
      
      # Build holdings summary
      holding_summary = [
          {"fund": h.get('symbol'), "aum": h.get('aum_in_fund')}
          for h in holdings[:5]
      ]
      
      # AUM change context
      aum_current = advisor.get('aum_current', 0)
      aum_prev = advisor.get('aum_previous', 0)
      aum_delta_pct = round(((aum_current - aum_prev) / aum_prev * 100) if aum_prev else 0, 1)
      
      prompt = f"""You are an Invesco wholesaler coach preparing a sales rep for an advisor meeting.

Advisor Profile:
- Name: {advisor.get('full_name', 'Unknown')}
- Firm: {advisor.get('firm_name', 'Unknown')}
- AUM: ${aum_current:,.0f} ({"+" if aum_delta_pct >= 0 else ""}{aum_delta_pct}% vs prior quarter)
- Channel: {advisor.get('channel', 'Unknown')}
- Region: {advisor.get('region', 'Unknown')}

Active Signals: {json.dumps(signal_summary)}
Top Invesco Holdings: {json.dumps(holding_summary)}

Generate a meeting brief with exactly this JSON structure (no markdown, pure JSON):
{{
  "opening_context": "One sentence on why we're meeting this advisor right now",
  "talking_points": ["Point 1 with specific data", "Point 2", "Point 3"],
  "product_suggestions": ["Specific Invesco product or fund suggestion 1", "Suggestion 2"],
  "risk_flags": ["Risk or concern to address 1"],
  "suggested_next_action": "Specific, actionable next step after this meeting"
}}

Be specific. Reference actual AUM numbers, fund names, signal types. Make it feel bespoke."""
      
      # Try Gemini → Kimi → static fallback
      raw = None
      for call_fn in [self._call_gemini, self._call_kimi]:
          try:
              raw = call_fn(prompt)
              break
          except Exception:
              continue
      
      if raw:
          # Strip markdown code fences if present
          import re
          raw = re.sub(r'^```(?:json)?\s*', '', raw.strip())
          raw = re.sub(r'\s*```$', '', raw.strip())
          try:
              result = json.loads(raw)
              cache.set(cache_key, result, timeout=300)
              return result
          except json.JSONDecodeError:
              pass  # Fall through to static
      
      # Static fallback (existing _generate_talking_points logic)
      return self._generate_talking_points_static(advisor, signals, holdings)

  def _generate_talking_points_static(self, advisor, signals, holdings) -> dict:
      """Static template fallback when LLM is unavailable."""
      # Keep existing _generate_talking_points() logic here, renamed
      # Return same structure as _llm_meeting_brief for consistency
      ...

STEP 3 — Update MeetingPrepView.get() to call _llm_meeting_brief:
Replace the call to self._generate_talking_points(advisor, signals, holdings)
with self._llm_meeting_brief(advisor, signals, holdings, flows)

Ensure the response includes a field: "ai_generated": True/False
(True = LLM, False = static fallback)

STEP 4 — Rename existing _generate_talking_points to _generate_talking_points_static:
Keep it as the fallback. Do not delete it.

STEP 5 — Verify:
Run: cd /data/workspace/projects/forwardlane-backend && python manage.py check
Run: python -c "from easy_button.views import MeetingPrepView; print('OK')"
```

---

## Files to Modify

| File | Change |
|------|--------|
| `easy_button/views.py` | Add `_call_gemini`, `_call_kimi`, `_llm_meeting_brief` to `MeetingPrepView` |
| `easy_button/views.py` | Rename `_generate_talking_points` → `_generate_talking_points_static` |
| `easy_button/views.py` | Update `get()` to call `_llm_meeting_brief` |

---

## Acceptance Criteria

- [ ] `MeetingPrepView.get()` calls `_llm_meeting_brief()` instead of `_generate_talking_points()`
- [ ] Response includes `ai_generated: true` when LLM call succeeds
- [ ] Response includes `ai_generated: false` when fallback is used
- [ ] Response structure is unchanged (all existing fields still present)
- [ ] Redis caches the brief for 300 seconds per `advisor_id`
- [ ] If `GEMINI_API_KEY` is missing, falls back to Kimi, then static — no 500 error
- [ ] `python manage.py check` passes
- [ ] Meeting brief includes advisor's actual name, AUM, and signal types (not generic text)

---

## Notes

- The Gemini + Kimi pattern is identical to `NLQueryView._call_gemini` / `_call_kimi`
- Consider extracting both into a shared `easy_button/llm.py` mixin module in a future refactor
- GEMINI_API_KEY is already in Railway env (used by NLQueryView in production)
- Cache TTL of 300s means one advisor = one LLM call per 5 minutes during a demo
