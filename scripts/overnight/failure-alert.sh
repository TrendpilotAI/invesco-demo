#!/usr/bin/env bash
# 1. Failure Alert System
# Monitors overnight batch agents and alerts on consecutive failures.
# Usage: Called by overnight-batch.sh after each repo task completes.

set -euo pipefail

STATE_FILE="/data/workspace/scripts/overnight/state/failure-state.json"
ALERT_THRESHOLD=${ALERT_THRESHOLD:-1}  # Alert after N consecutive failures

mkdir -p "$(dirname "$STATE_FILE")"

# Initialize state if missing
if [[ ! -f "$STATE_FILE" ]]; then
  echo '{"consecutive_failures": 0, "total_failures": 0, "total_successes": 0, "last_failure": null, "failure_log": []}' > "$STATE_FILE"
fi

report_success() {
  local repo="$1"
  local task="$2"
  python3 -c "
import json, time
with open('$STATE_FILE') as f: state = json.load(f)
state['consecutive_failures'] = 0
state['total_successes'] = state.get('total_successes', 0) + 1
with open('$STATE_FILE', 'w') as f: json.dump(state, f, indent=2)
print(f'✅ {\"$repo\"}: {\"$task\"} succeeded (streak reset)')
"
}

report_failure() {
  local repo="$1"
  local task="$2"
  local error_msg="${3:-unknown error}"
  
  python3 -c "
import json, time
with open('$STATE_FILE') as f: state = json.load(f)
state['consecutive_failures'] = state.get('consecutive_failures', 0) + 1
state['total_failures'] = state.get('total_failures', 0) + 1
state['last_failure'] = {
    'repo': '$repo',
    'task': '$task',
    'error': '''$error_msg''',
    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
}
state.setdefault('failure_log', []).append(state['last_failure'])
# Keep only last 50 failures
state['failure_log'] = state['failure_log'][-50:]
with open('$STATE_FILE', 'w') as f: json.dump(state, f, indent=2)

if state['consecutive_failures'] >= $ALERT_THRESHOLD:
    print(f'🚨 ALERT: {state[\"consecutive_failures\"]} consecutive failures!')
    print(f'   Last: {\"$repo\"} — {\"$error_msg\"}')
    # Write alert file for Honey to pick up
    alert = {
        'type': 'overnight_failure',
        'consecutive': state['consecutive_failures'],
        'repo': '$repo',
        'task': '$task',
        'error': '''$error_msg''',
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }
    with open('/data/workspace/scripts/overnight/state/ALERT.json', 'w') as f:
        json.dump(alert, f, indent=2)
else:
    print(f'⚠️ {\"$repo\"}: {\"$task\"} failed ({state[\"consecutive_failures\"]}/{\"$ALERT_THRESHOLD\"} threshold)')
"
}

# CLI interface
case "${1:-}" in
  success) report_success "${2:-unknown}" "${3:-unknown}" ;;
  failure) report_failure "${2:-unknown}" "${3:-unknown}" "${4:-}" ;;
  status)
    cat "$STATE_FILE" | python3 -m json.tool
    ;;
  reset)
    echo '{"consecutive_failures": 0, "total_failures": 0, "total_successes": 0, "last_failure": null, "failure_log": []}' > "$STATE_FILE"
    rm -f /data/workspace/scripts/overnight/state/ALERT.json
    echo "🔄 Failure state reset"
    ;;
  *)
    echo "Usage: $0 {success|failure|status|reset} [repo] [task] [error_msg]"
    exit 1
    ;;
esac
