# HEARTBEAT.md

## Cron Jobs Active (9 jobs)

### Every 15 Minutes
- **rapid-health** — Quick service check, detect-only, no fixes (Kimi 2.5, silent)

### Hourly
- **hourly-consolidate** — Every hour (:30), consolidates learnings, cleans stale state (Kimi 2.5, silent)

### Every Few Hours
- **service-health** — Every 2h, **SELF-HEALING** — detects failures, spawns Debug/Ops/QA agents to auto-fix (Codex 5.3)
- **todo-progress** — Every 4h, picks next unblocked task and executes it (Codex 5.3 → Sonnet 4-6 sub-agents)
- **git-sync** — Every 6h, commits and pushes workspace changes (Kimi 2.5, silent)
- **invesco-sprint** — Every 8h, focused P0 Invesco demo work (Codex 5.3 → Sonnet 4-6 sub-agents)

### Daily
- **judge-swarm-t1** — 3:00 AM + 12:00 PM ET, Tier 1 (5 repos: invesco-retention, forwardlane-backend, signal-studio, signal-builder-backend, signal-studio-templates) — Sonnet 4.6, 30min timeout
- **judge-swarm-t2** — 3:20 AM + 12:20 PM ET, Tier 2 (5 repos: signal-studio-frontend, forwardlane_advisor, NarrativeReactor, signal-builder-frontend, Ultrafone) — Sonnet 4.6, 30min timeout
- **judge-swarm-t3** — 3:40 AM + 12:40 PM ET, Tier 3 (7 repos: signalhaus-website, core-entityextraction, signal-studio-auth, signal-studio-data-provider, Second-Opinion, flip-my-era, Trendpilot) — Kimi 2.5, 30min timeout
- **daily-cleanup** — 5AM ET, git sync, prune old state, compress large files (Kimi 2.5, silent)

### Weekly
- **project-scoring** — Monday 6AM ET, re-scores all 42 projects (Codex 5.3)

## On Heartbeat
- Check if any cron jobs failed recently (`openclaw cron list`)
- Review TODO.md for anything urgent that crons missed
- If Nathan is awake (08:00-23:00 ET), summarize recent cron progress

## Known Issues
- daily-judge-swarm: timed out on 2026-03-10 run (30min hard limit hit); prior runs OK (~22-23min). May need timeout increase or scope reduction.
- Bedrock discovery error: cosmetic, ignore

## Config
- Use **DeepSeek** model for heartbeat checks (save costs)
- Judge swarms use **Kimi K2.5** (cheap, good reasoning)
- Coding tasks use **Codex 5.3** orchestrating **Sonnet 4-6** sub-agents
