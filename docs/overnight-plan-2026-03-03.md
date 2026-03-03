# Overnight Autonomous Work Plan
## March 3, 2026 — 2:45 AM → 9:00 AM ET (07:45 → 13:00 UTC)

### Priority: Monetizable Products + ForwardLane Sales

---

## Sequence (8 tasks, ~45 min apart, no dependencies between adjacent tasks)

### Wave 1: Invesco Demo Prep (Revenue Protection — $300K)
| # | Time (ET) | Task | Model | Output |
|---|-----------|------|-------|--------|
| 1 | 2:45 AM | Invesco objection scripts | DeepSeek | `docs/invesco-objection-scripts.md` |
| 2 | 3:30 AM | Demo day checklist | DeepSeek | `docs/invesco-demo-day-checklist.md` |

### Wave 2: ForwardLane Sales Campaign (New Revenue)
| # | Time (ET) | Task | Model | Output |
|---|-----------|------|-------|--------|
| 3 | 4:15 AM | ForwardLane sales email sequences + Decision Velocity campaign | Sonnet 4 | `docs/forwardlane-sales-campaign.md` |

### Wave 3: Product Engineering (Monetizable Products)
| # | Time (ET) | Task | Model | Output |
|---|-----------|------|-------|--------|
| 4 | 5:00 AM | FlipMyEra audit + fix blockers | Sonnet 4 | Code fixes + `docs/flipmyera-ship-status.md` |
| 5 | 5:45 AM | NarrativeReactor deploy to Railway | Sonnet 4 | Deployed service + `docs/narrativereactor-deploy-guide.md` |
| 6 | 6:30 AM | Trendpilot audit + deploy prep | Sonnet 4 | `docs/trendpilot-deploy-guide.md` |

### Wave 4: Content + Distribution
| # | Time (ET) | Task | Model | Output |
|---|-----------|------|-------|--------|
| 7 | 7:30 AM | 5 LinkedIn + 5 Twitter drafts in Nathan's voice | DeepSeek | `content/linkedin-drafts-batch-1.md` + `content/twitter-threads-batch-1.md` |
| 8 | 8:30 AM | Git commit all work + memory update | DeepSeek | Clean commit + MEMORY.md |

### Note: Ultrafone
- Repo not found in TrendpilotAI GitHub org — need Nathan to share repo URL
- Will clone and audit once located

### Git Worktree Strategy
- Each engineering task (4, 5, 6) operates in its own project directory
- No worktree conflicts since they're separate repos
- Worktrees would be used within a single repo for parallel feature branches
