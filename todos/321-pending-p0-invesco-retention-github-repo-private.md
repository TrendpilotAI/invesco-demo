# TODO-321 — GitHub Repo Privacy Check (Invesco Retention)

**Priority:** P0  
**Project:** invesco-retention  
**Status:** pending  
**Estimated Effort:** XS (15-30 min)  
**Created:** 2026-02-28  

---

## Task Description

The Invesco demo is deployed via GitHub Pages at `https://trendpilotai.github.io/invesco-demo/`. This means the source repo under `trendpilotai` GitHub org is at minimum publicly accessible for Pages to serve. 

Before the Brian Kiley demo, we must verify:
1. Whether the source code repo is **public or private**
2. Whether synthetic advisor data, mock Salesforce payloads, or any ForwardLane IP is exposed in the repo
3. Whether GitHub Pages can serve from a private repo (requires GitHub Pro/Team — check org plan)
4. If public: assess risk and either make private + configure Pages correctly, or sanitize sensitive content

**Risk:** If Invesco, Vanguard, or competitor contacts find the public repo and see mock data referencing real advisor names or Invesco internal framing, it could surface awkwardly before the deal closes.

---

## Coding Prompt (Agent-Executable)

```
TASK: Audit and secure the GitHub repo for the Invesco demo.

1. Check repo visibility:
   curl -H "Authorization: Bearer <GITHUB_TOKEN>" \
     https://api.github.com/repos/trendpilotai/invesco-demo
   → Look for "private": true/false in response

2. If PUBLIC, scan for sensitive content:
   - grep -r "Invesco" /data/workspace/projects/invesco-retention/demo-app/src --include="*.ts" --include="*.tsx" -l
   - grep -r "Vanguard\|Marcus Thompson\|Brian Kiley\|Kelly\|Craig\|Megan" ... -l
   - List any files with real names, internal framing, or client-specific data

3. Decision tree:
   a) If repo is PRIVATE → confirm Pages still serves correctly → DONE ✅
   b) If repo is PUBLIC + no sensitive data → document as acceptable risk → DONE ✅
   c) If repo is PUBLIC + sensitive data found:
      - Option A: Make repo private (requires trendpilotai org on GitHub Pro/Team)
        gh repo edit trendpilotai/invesco-demo --visibility private
      - Option B: Sanitize data — replace real names with generic placeholders in source
        then redeploy
      - Option C: Move to Vercel deploy (no source exposure) and point URL there

4. Document findings in a brief audit note:
   - Current visibility
   - Sensitive content found (if any)
   - Action taken
   - Final repo state

5. If any changes made, verify https://trendpilotai.github.io/invesco-demo/ still loads (200 OK):
   curl -I https://trendpilotai.github.io/invesco-demo/

GitHub org: trendpilotai
Repo: invesco-demo
Local path: /data/workspace/projects/invesco-retention/demo-app
```

---

## Acceptance Criteria

- [ ] Repo visibility confirmed (public or private) and documented
- [ ] Sensitive content scan completed — findings logged
- [ ] If public + sensitive: remediation applied (private repo OR content sanitized)
- [ ] Demo URL still returns 200 after any changes
- [ ] Audit note written summarizing final state
- [ ] Nathan notified of outcome (especially if action was required)

---

## Why This Matters

A $300K deal requires protecting ForwardLane's strategic approach and any Invesco-specific framing from accidental public exposure. 15 minutes now prevents a potentially embarrassing or legally awkward discovery during due diligence. This is a standard pre-demo security hygiene check.
