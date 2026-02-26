#!/usr/bin/env bash
# =============================================================================
# tctl.sh — Honey AI Temporal CLI Wrapper
# =============================================================================
# Pipes temporal CLI operations into the Codex/Ops agent pipeline.
# Usage:
#   ./tctl.sh <command> [args...]
#   ./tctl.sh start-worker          # Start the Temporal worker
#   ./tctl.sh setup-schedules       # Create all Temporal schedules
#   ./tctl.sh health                # Self-heal workflow: check & launch
#   ./tctl.sh judge <repo1,repo2>   # Run judge swarm on repos
#   ./tctl.sh orchestrate "goal"    # Run orchestrator workflow
#   ./tctl.sh status                # Show all running workflows + schedules
#   ./tctl.sh query <wf-id>         # Query workflow state
#   ./tctl.sh signal <wf-id> <sig>  # Send signal to workflow
#   ./tctl.sh cancel <wf-id>        # Cancel a workflow
#   ./tctl.sh terminate <wf-id>     # Force-terminate a workflow
#   ./tctl.sh logs <wf-id>          # Show workflow event history
#   ./tctl.sh ns                    # List namespaces
#   ./tctl.sh schedules             # List all schedules
#   ./tctl.sh nuke                  # ⚠️  Terminate ALL running workflows
# =============================================================================

set -euo pipefail

export PATH="$PATH:/root/.temporalio/bin"

TEMPORAL_HOST="${TEMPORAL_HOST:-temporal.railway.internal:7233}"
TEMPORAL_NAMESPACE="${TEMPORAL_NAMESPACE:-honey-agents}"
TASK_QUEUE="${TEMPORAL_TASK_QUEUE:-honey-main}"
SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKER_PID_FILE="/tmp/honey-temporal-worker.pid"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${BLUE}[tctl]${NC} $*"; }
ok()   { echo -e "${GREEN}[✅]${NC} $*"; }
warn() { echo -e "${YELLOW}[⚠️]${NC} $*"; }
err()  { echo -e "${RED}[❌]${NC} $*"; }

TCLI="temporal --address $TEMPORAL_HOST -n $TEMPORAL_NAMESPACE"

# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

cmd_start_worker() {
    log "Starting Temporal worker (namespace=$TEMPORAL_NAMESPACE, queue=$TASK_QUEUE)..."

    if [ -f "$WORKER_PID_FILE" ] && kill -0 "$(cat "$WORKER_PID_FILE")" 2>/dev/null; then
        warn "Worker already running (PID $(cat "$WORKER_PID_FILE"))"
        return 0
    fi

    cd "$SCRIPTS_DIR"
    TEMPORAL_NAMESPACE="$TEMPORAL_NAMESPACE" \
    TEMPORAL_HOST="$TEMPORAL_HOST" \
    TEMPORAL_TASK_QUEUE="$TASK_QUEUE" \
    nohup python3 worker.py > /tmp/honey-temporal-worker.log 2>&1 &
    echo $! > "$WORKER_PID_FILE"
    ok "Worker started (PID $!, log: /tmp/honey-temporal-worker.log)"
}

cmd_stop_worker() {
    if [ -f "$WORKER_PID_FILE" ] && kill -0 "$(cat "$WORKER_PID_FILE")" 2>/dev/null; then
        kill "$(cat "$WORKER_PID_FILE")"
        rm -f "$WORKER_PID_FILE"
        ok "Worker stopped"
    else
        warn "No worker running"
    fi
}

cmd_worker_status() {
    if [ -f "$WORKER_PID_FILE" ] && kill -0 "$(cat "$WORKER_PID_FILE")" 2>/dev/null; then
        ok "Worker running (PID $(cat "$WORKER_PID_FILE"))"
        echo "--- Last 20 log lines ---"
        tail -20 /tmp/honey-temporal-worker.log 2>/dev/null || true
    else
        warn "Worker not running"
    fi
}

cmd_setup_schedules() {
    log "Creating Temporal schedules..."
    cd "$SCRIPTS_DIR"
    TEMPORAL_NAMESPACE="$TEMPORAL_NAMESPACE" \
    TEMPORAL_HOST="$TEMPORAL_HOST" \
    python3 schedules.py
}

cmd_health() {
    log "Starting SelfHealingWorkflow..."
    $TCLI workflow start \
        --task-queue "$TASK_QUEUE" \
        --type SelfHealingWorkflow \
        --workflow-id "self-healing-$(date +%s)" \
        --input '{
            "services": [
                {"name": "django-backend", "url": "https://django-backend-production-3b94.up.railway.app/healthz"},
                {"name": "signal-studio", "url": "https://signal-studio-production-a258.up.railway.app"},
                {"name": "signal-builder", "url": "https://signal-builder-api-production.up.railway.app/docs"}
            ],
            "check_interval_seconds": 300,
            "max_retries": 3
        }'
    ok "SelfHealingWorkflow started"
}

cmd_judge() {
    local repos="${1:-signal-studio-backend,signal-studio-platform,signal-builder-backend}"
    local repo_array
    IFS=',' read -ra repo_list <<< "$repos"
    repo_array=$(printf '"%s",' "${repo_list[@]}")
    repo_array="[${repo_array%,}]"

    log "Starting JudgeSwarmWorkflow for: $repos"
    $TCLI workflow start \
        --task-queue "$TASK_QUEUE" \
        --type JudgeSwarmWorkflow \
        --workflow-id "judge-swarm-$(date +%s)" \
        --input "{
            \"repos\": $repo_array,
            \"model\": \"anthropic/claude-sonnet-4-20250514\",
            \"judge_model\": \"anthropic/claude-sonnet-4-20250514\"
        }"
    ok "JudgeSwarmWorkflow started"
}

cmd_orchestrate() {
    local goal="${1:?Usage: tctl.sh orchestrate \"your goal here\"}"
    local model="${2:-anthropic/claude-sonnet-4-20250514}"
    local parallel="${3:-3}"

    log "Starting OrchestratorWorkflow: $goal"
    $TCLI workflow start \
        --task-queue "$TASK_QUEUE" \
        --type OrchestratorWorkflow \
        --workflow-id "orchestrator-$(date +%s)" \
        --input "{
            \"goal\": $(echo "$goal" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))'),
            \"model\": \"$model\",
            \"max_parallel\": $parallel
        }"
    ok "OrchestratorWorkflow started"
}

cmd_monitor() {
    log "Starting HealthMonitorWorkflow (continuous)..."
    $TCLI workflow start \
        --task-queue "$TASK_QUEUE" \
        --type HealthMonitorWorkflow \
        --workflow-id "health-monitor-continuous" \
        --input '{
            "services": [
                {"name": "django-backend", "url": "https://django-backend-production-3b94.up.railway.app/healthz"},
                {"name": "signal-studio", "url": "https://signal-studio-production-a258.up.railway.app"},
                {"name": "signal-builder", "url": "https://signal-builder-api-production.up.railway.app/docs"},
                {"name": "agent-ops-center", "url": "https://agent-ops-center-production.up.railway.app"}
            ],
            "interval_seconds": 60,
            "alert_after_failures": 3
        }'
    ok "HealthMonitorWorkflow started (alerts after 3 consecutive failures)"
}

cmd_status() {
    echo -e "${CYAN}=== Temporal Status (namespace: $TEMPORAL_NAMESPACE) ===${NC}"
    echo ""
    echo -e "${YELLOW}--- Running Workflows ---${NC}"
    $TCLI workflow list --limit 20 2>&1 || warn "No workflows found"
    echo ""
    echo -e "${YELLOW}--- Schedules ---${NC}"
    $TCLI schedule list 2>&1 || warn "No schedules found"
    echo ""
    echo -e "${YELLOW}--- Worker ---${NC}"
    cmd_worker_status
}

cmd_query() {
    local wf_id="${1:?Usage: tctl.sh query <workflow-id>}"
    $TCLI workflow query --type get_status -w "$wf_id" 2>&1 || \
    $TCLI workflow query --type status -w "$wf_id" 2>&1 || \
    warn "Query failed — workflow may not support queries"
}

cmd_signal() {
    local wf_id="${1:?Usage: tctl.sh signal <workflow-id> <signal-name> [data]}"
    local signal="${2:?Missing signal name}"
    local data="${3:-{}}"
    $TCLI workflow signal -w "$wf_id" --name "$signal" --input "$data"
    ok "Signal '$signal' sent to $wf_id"
}

cmd_cancel() {
    local wf_id="${1:?Usage: tctl.sh cancel <workflow-id>}"
    $TCLI workflow cancel -w "$wf_id"
    ok "Cancelled $wf_id"
}

cmd_terminate() {
    local wf_id="${1:?Usage: tctl.sh terminate <workflow-id>}"
    $TCLI workflow terminate -w "$wf_id" --reason "Terminated by tctl.sh"
    ok "Terminated $wf_id"
}

cmd_logs() {
    local wf_id="${1:?Usage: tctl.sh logs <workflow-id>}"
    $TCLI workflow show -w "$wf_id" 2>&1
}

cmd_ns() {
    $TCLI operator namespace list 2>&1
}

cmd_schedules() {
    $TCLI schedule list 2>&1
}

cmd_nuke() {
    warn "Terminating ALL running workflows in namespace '$TEMPORAL_NAMESPACE'..."
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        log "Aborted"
        return 0
    fi

    $TCLI workflow list --fields workflowId -o json 2>/dev/null | \
        python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for wf in data:
        print(wf.get('execution', {}).get('workflowId', wf.get('workflowId', '')))
except: pass
" | while read -r wid; do
        [ -z "$wid" ] && continue
        $TCLI workflow terminate -w "$wid" --reason "Nuked by tctl.sh" 2>/dev/null || true
        echo "  Terminated: $wid"
    done
    ok "All workflows terminated"
}

# ---------------------------------------------------------------------------
# Main dispatch
# ---------------------------------------------------------------------------

case "${1:-help}" in
    start-worker|start)     cmd_start_worker ;;
    stop-worker|stop)       cmd_stop_worker ;;
    worker-status|ws)       cmd_worker_status ;;
    setup-schedules|setup)  cmd_setup_schedules ;;
    health|heal)            cmd_health ;;
    judge)                  cmd_judge "${2:-}" ;;
    orchestrate|orch)       cmd_orchestrate "${2:-}" "${3:-}" "${4:-}" ;;
    monitor|mon)            cmd_monitor ;;
    status|st)              cmd_status ;;
    query|q)                cmd_query "${2:-}" ;;
    signal|sig)             cmd_signal "${2:-}" "${3:-}" "${4:-}" ;;
    cancel)                 cmd_cancel "${2:-}" ;;
    terminate|term)         cmd_terminate "${2:-}" ;;
    logs|show)              cmd_logs "${2:-}" ;;
    ns|namespaces)          cmd_ns ;;
    schedules|sched)        cmd_schedules ;;
    nuke)                   cmd_nuke ;;
    help|--help|-h)
        echo "Usage: tctl.sh <command> [args...]"
        echo ""
        echo "Workflow Commands:"
        echo "  start-worker          Start the Temporal worker"
        echo "  stop-worker           Stop the Temporal worker"
        echo "  worker-status         Check worker status + recent logs"
        echo "  setup-schedules       Create all Temporal schedules"
        echo "  health                Start SelfHealingWorkflow"
        echo "  judge <repos>         Start JudgeSwarmWorkflow (comma-separated repos)"
        echo "  orchestrate \"goal\"    Start OrchestratorWorkflow"
        echo "  monitor               Start continuous HealthMonitorWorkflow"
        echo ""
        echo "Management Commands:"
        echo "  status                Show all workflows, schedules, worker"
        echo "  query <wf-id>         Query workflow state"
        echo "  signal <wf-id> <sig>  Send signal to workflow"
        echo "  cancel <wf-id>        Cancel a workflow"
        echo "  terminate <wf-id>     Force-terminate a workflow"
        echo "  logs <wf-id>          Show workflow event history"
        echo "  ns                    List namespaces"
        echo "  schedules             List all schedules"
        echo "  nuke                  ⚠️  Terminate ALL running workflows"
        ;;
    *)
        # Pass-through to temporal CLI
        $TCLI "$@"
        ;;
esac
