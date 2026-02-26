#!/usr/bin/env python3
"""Drift detector for running subagents.

Monitors running subagents via openclaw CLI, evaluates drift using
lightweight model calls, and triggers corrections when needed.

Usage:
    python drift_detector.py run          # Run continuous monitoring (60s polling)
    python drift_detector.py check        # One-shot check all agents
    python drift_detector.py status       # Show current drift status
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# Add parent dir for sibling imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from strategies import DriftType, DriftSignal, DRIFT_EVALUATION_PROMPT, get_correction
from intent_tracker import IntentTracker
from corrector import Corrector

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [drift-detector] %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)

CORRECTIONS_FILE = Path("/data/workspace/.orchestrator/drift-corrections.json")
POLL_INTERVAL = int(os.environ.get("DRIFT_POLL_INTERVAL", "60"))


def _run_cmd(cmd: list[str], timeout: int = 30) -> Optional[str]:
    """Run a shell command and return stdout, or None on failure."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        log.warning("Command failed: %s — %s", " ".join(cmd), e)
        return None


def list_running_agents() -> list[dict]:
    """List running subagents via openclaw CLI.
    
    Returns:
        List of agent dicts with session_id, label, etc.
    """
    output = _run_cmd(["openclaw", "subagents", "list", "--json"])
    if not output:
        # Fallback: try without --json flag and parse
        output = _run_cmd(["openclaw", "subagents", "list"])
        if not output:
            return []
        # Try to parse as JSON anyway
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            log.debug("Non-JSON output from subagents list: %s", output[:200])
            return []
    
    try:
        data = json.loads(output)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "agents" in data:
            return data["agents"]
        return []
    except json.JSONDecodeError:
        return []


def evaluate_drift_lightweight(
    original_task: str,
    agent_label: str,
    runtime_minutes: float,
    recent_activity: str = "No activity data available",
) -> Optional[DriftSignal]:
    """Evaluate agent drift using a lightweight model call.
    
    Uses deepseek or similar cheap model to score drift.
    Falls back to heuristic-based detection if no model available.
    
    Args:
        original_task: The original task description.
        agent_label: Agent label/name.
        runtime_minutes: How long the agent has been running.
        recent_activity: Recent activity description.
    
    Returns:
        DriftSignal if evaluation succeeded, None otherwise.
    """
    prompt = DRIFT_EVALUATION_PROMPT.format(
        original_task=original_task,
        agent_label=agent_label,
        runtime_minutes=round(runtime_minutes, 1),
        recent_activity=recent_activity,
    )

    # Try calling a lightweight model via openclaw or direct API
    # For now, use heuristic-based detection as primary method
    return _heuristic_drift_check(runtime_minutes, recent_activity)


def _heuristic_drift_check(
    runtime_minutes: float,
    recent_activity: str,
) -> DriftSignal:
    """Heuristic-based drift detection when model calls aren't available.
    
    Simple rules based on runtime and activity patterns.
    """
    # Stalled detection: very long runtime with no activity
    if runtime_minutes > 30 and (not recent_activity or recent_activity == "No activity data available"):
        return DriftSignal(
            drift_type=DriftType.STALLED,
            confidence=0.6,
            evidence=f"Running for {runtime_minutes:.0f}min with no visible activity",
            severity=7.0 + min(runtime_minutes / 60, 3.0),
        )

    # Long runtime warning (but not necessarily drifted)
    if runtime_minutes > 45:
        return DriftSignal(
            drift_type=DriftType.RABBIT_HOLE,
            confidence=0.4,
            evidence=f"Running for {runtime_minutes:.0f}min — may be in a rabbit hole",
            severity=5.0 + min(runtime_minutes / 60, 3.0),
        )

    # Default: on track
    return DriftSignal(
        drift_type=DriftType.ON_TRACK,
        confidence=0.5,
        evidence="Within normal runtime, no obvious drift signals",
        severity=0.0,
    )


def _publish_drift_event(agent_label: str, drift_signal: DriftSignal, session_id: str) -> None:
    """Publish a drift event to the event bus if available."""
    try:
        from event_bus.event_bus import EventBus
        bus = EventBus()
        bus.publish("honey.agent.drift", {
            "agent_label": agent_label,
            "session_id": session_id,
            "drift_type": drift_signal.drift_type.value,
            "drift_score": drift_signal.severity,
            "confidence": drift_signal.confidence,
            "evidence": drift_signal.evidence,
            "timestamp": time.time(),
        })
        log.info("Published drift event for %s", agent_label)
    except ImportError:
        log.debug("Event bus not available, skipping drift event publish")
    except Exception as e:
        log.warning("Failed to publish drift event: %s", e)


def _save_correction_record(record: dict) -> None:
    """Append a correction record to the corrections log."""
    CORRECTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    corrections: list[dict] = []
    if CORRECTIONS_FILE.exists():
        try:
            corrections = json.loads(CORRECTIONS_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            corrections = []
    corrections.append(record)
    # Keep last 500 records
    corrections = corrections[-500:]
    CORRECTIONS_FILE.write_text(json.dumps(corrections, indent=2))


def check_all_agents(tracker: IntentTracker, corrector: Corrector) -> list[dict]:
    """Check all running agents for drift.
    
    Returns:
        List of drift check results.
    """
    agents = list_running_agents()
    results = []

    for agent in agents:
        session_id = agent.get("session_id") or agent.get("id", "")
        label = agent.get("label", "unknown")
        
        # Get intent data
        intent = tracker.get(session_id)
        if not intent:
            # Auto-register unknown agents
            original_task = agent.get("task", agent.get("prompt", "Unknown task"))
            tracker.register(session_id, label, original_task)
            intent = tracker.get(session_id)

        original_task = intent.get("original_task", "Unknown") if intent else "Unknown"
        spawned_at = intent.get("spawned_at", time.time()) if intent else time.time()
        runtime_minutes = (time.time() - spawned_at) / 60.0

        # Evaluate drift
        signal = evaluate_drift_lightweight(
            original_task=original_task,
            agent_label=label,
            runtime_minutes=runtime_minutes,
        )

        if not signal:
            continue

        # Record checkpoint
        tracker.checkpoint(
            session_id,
            description=signal.evidence,
            drift_score=signal.severity,
        )

        result = {
            "session_id": session_id,
            "label": label,
            "runtime_minutes": round(runtime_minutes, 1),
            "drift_type": signal.drift_type.value,
            "drift_score": signal.severity,
            "confidence": signal.confidence,
            "evidence": signal.evidence,
            "action_taken": None,
        }

        # Apply correction if needed
        if signal.drift_type != DriftType.ON_TRACK and signal.severity >= 6.0:
            context = {
                "original_scope": original_task,
                "goal": original_task,
                "tangent": signal.evidence,
                "stall_duration": f"{runtime_minutes:.0f} minutes",
                "hints": "Review the original task and focus on deliverables.",
            }
            correction = get_correction(signal, context)
            if correction:
                success = corrector.apply_correction(
                    session_id=session_id,
                    label=label,
                    correction=correction,
                    original_task=original_task,
                )
                action = correction.action if success else f"{correction.action} (failed)"
                result["action_taken"] = action
                
                tracker.checkpoint(
                    session_id,
                    description=f"Correction applied: {correction.action}",
                    drift_score=signal.severity,
                    correction=correction.message_template,
                )

                _save_correction_record({
                    **result,
                    "correction_message": correction.message_template,
                    "timestamp": time.time(),
                })

            _publish_drift_event(label, signal, session_id)

        results.append(result)
        log.info(
            "Agent %s: drift=%s score=%.1f action=%s",
            label, signal.drift_type.value, signal.severity, result["action_taken"],
        )

    return results


def show_status(tracker: IntentTracker) -> None:
    """Print current drift monitoring status."""
    summary = tracker.summary()
    print(json.dumps(summary, indent=2))

    running = tracker.get_all_running()
    if running:
        print(f"\n{'Label':<30} {'Runtime':<12} {'Drift':<8} {'Corrections'}")
        print("-" * 70)
        for intent in running:
            runtime = (time.time() - intent.get("spawned_at", time.time())) / 60
            drift = intent.get("last_drift_score", "-")
            corr = intent.get("corrections_applied", 0)
            print(f"{intent.get('label', '?'):<30} {runtime:>6.1f} min   {drift!s:<8} {corr}")
    else:
        print("\nNo running agents tracked.")


def run_daemon(tracker: IntentTracker, corrector: Corrector) -> None:
    """Run continuous drift monitoring loop."""
    log.info("Starting drift detector daemon (poll every %ds)", POLL_INTERVAL)
    while True:
        try:
            results = check_all_agents(tracker, corrector)
            drifted = [r for r in results if r.get("drift_score", 0) >= 6.0]
            if drifted:
                log.warning("Drift detected in %d/%d agents", len(drifted), len(results))
        except KeyboardInterrupt:
            log.info("Drift detector stopped.")
            break
        except Exception as e:
            log.error("Error in drift check cycle: %s", e)
        
        time.sleep(POLL_INTERVAL)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mid-session drift detector")
    parser.add_argument(
        "command",
        choices=["run", "check", "status"],
        help="run=daemon, check=one-shot, status=show state",
    )
    args = parser.parse_args()

    tracker = IntentTracker()
    corrector = Corrector()

    if args.command == "run":
        run_daemon(tracker, corrector)
    elif args.command == "check":
        results = check_all_agents(tracker, corrector)
        print(json.dumps(results, indent=2))
    elif args.command == "status":
        show_status(tracker)


if __name__ == "__main__":
    main()
