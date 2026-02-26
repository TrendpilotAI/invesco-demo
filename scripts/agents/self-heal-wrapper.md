# Self-Heal Wrapper — Inject into every cron job

## On Failure Protocol
If your task fails for ANY reason (build error, API failure, service down, code error):

1. **DO NOT give up.** Diagnose the failure.
2. **Spawn a Debug Agent** to fix it:
```
sessions_spawn with model openai-codex/gpt-5.3-codex:
"Read /data/workspace/scripts/agents/debug-agent.md. FAILURE: {describe what failed and the error message}. Diagnose, fix, and report. Check source code, logs, configs. Push fix to GitHub if needed."
```
3. **Spawn an Ops Agent** if it's infrastructure:
```
sessions_spawn with model openai-codex/gpt-5.3-codex:
"Read /data/workspace/scripts/agents/ops-agent.md. INFRA FAILURE: {describe what failed}. Check Railway deployment, env vars, resources. Fix and report."
```
4. **After fix attempt, verify** by running the health check:
```bash
bash /data/workspace/scripts/self-healing-monitor.sh
```
5. **If still broken, retry up to 3 times** with different approaches.
6. **If all retries fail**, report to Nathan with full diagnostics.
7. **Log the incident** to /data/workspace/.orchestrator/learnings.json
