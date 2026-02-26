# HEARTBEAT.md

## Cron Jobs Active (9 jobs)

### Every 15 Minutes
- **rapid-health** — Quick service check, detect-only, no fixes (DeepSeek, silent)

### Hourly
- **hourly-consolidate** — Every hour (:30), consolidates learnings, cleans stale state (DeepSeek, silent)

### Every Few Hours
- **service-health** — Every 2h, **SELF-HEALING** — detects failures, spawns Debug/Ops/QA agents to auto-fix (Codex 5.3)
- **todo-progress** — Every 4h, picks next unblocked task and executes it (Codex 5.3 → Sonnet 4-6 sub-agents)
- **git-sync** — Every 6h, commits and pushes workspace changes (DeepSeek, silent)
- **invesco-sprint** — Every 8h, focused P0 Invesco demo work (Codex 5.3 → Sonnet 4-6 sub-agents)

### Daily
- **daily-judge-swarm** — 3AM ET, spawns Kimi K2.5 judges per repo, generates TODO lists (Codex orchestrator)
- **daily-cleanup** — 5AM ET, git sync, prune old state, compress large files (DeepSeek, silent)

### Weekly
- **project-scoring** — Monday 6AM ET, re-scores all 42 projects (Codex 5.3)

## On Heartbeat
- Check if any cron jobs failed recently (`openclaw cron list`)
- Review TODO.md for anything urgent that crons missed
- If Nathan is awake (08:00-23:00 ET), summarize recent cron progress

## Known Issues
- Entity Extraction: expected to be 404 (needs rewrite as FastAPI)
- Bedrock discovery error: cosmetic, ignore

## Config
- Use **DeepSeek** model for heartbeat checks (save costs)
- Judge swarms use **Kimi K2.5** (cheap, good reasoning)
- Coding tasks use **Codex 5.3** orchestrating **Sonnet 4-6** sub-agents
