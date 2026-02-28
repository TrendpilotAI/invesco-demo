# Alerting System

The monitoring stack now includes push notifications via Telegram and Discord.

## How It Works

On every `run-all.ts` invocation (typically via cron), the alert layer:

1. **Checks all services** via HTTP healthchecks
2. **Loads persistent state** from `dashboard/alert-state.json`
3. **Detects transitions**: alive→down, down→alive, SUCCESS→FAILED
4. **Deduplicates** — suppresses repeat alerts for the same issue within 30 minutes
5. **Escalates** — re-alerts every 15 minutes while a service remains down
6. **Sends recovery** — notifies immediately when a service comes back up
7. **Saves state** for the next run

## Setup

Set environment variables:

```bash
# Telegram (required for Telegram alerts)
TELEGRAM_BOT_TOKEN=<your bot token>
TELEGRAM_CHAT_ID=<your chat id>   # Nathan's is 8003607839

# Discord (optional)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Dry-run mode (logs instead of sending)
ALERT_DRY_RUN=true
```

### Getting a Telegram Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. `/newbot` → follow prompts
3. Copy the token

## Alert Types

| Type           | When Fired                                      |
|----------------|------------------------------------------------|
| `down`         | Service first becomes unreachable               |
| `escalation`   | Service still down after 15+ minutes            |
| `recovered`    | Service comes back up (bypasses dedupe window)  |
| `slow`         | Response time exceeds 5s threshold              |
| `task_failed`  | Task result transitions to FAILED/ERROR         |
| `task_recovered` | Task result recovers from FAILED → SUCCESS   |

## Cron Setup

Run every 5 minutes:

```cron
*/5 * * * * cd /data/workspace/infrastructure/monitoring && pnpm check-all >> /var/log/monitoring.log 2>&1
```

## State File

`dashboard/alert-state.json` tracks per-service:
- `lastStatus` — previous health state
- `lastAlertSentAt` — timestamp of last alert (for deduplication)
- `downSince` — when the service first went down (for escalation timing)
- `escalatedAt` — timestamp of last escalation alert
- `taskLastResult` — last task result string
