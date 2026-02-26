"""
Reactions Engine — load YAML reaction definitions, match events, execute actions.

A reaction has:
  - name: human label
  - match: { channel: glob, event: glob }  (fnmatch patterns)
  - actions: list of { type: ..., params: ... }
  - cooldown: optional seconds between firings (dedup)
"""

import fnmatch
import logging
import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger("reactions")

REACTIONS_PATH = os.environ.get(
    "REACTIONS_YAML",
    str(Path(__file__).resolve().parents[2] / "config" / "reactions.yaml"),
)


@dataclass
class Reaction:
    name: str
    match_channel: str
    match_event: str
    actions: list[dict[str, Any]]
    cooldown: float = 0
    _last_fired: float = 0

    def matches(self, channel: str, event: str) -> bool:
        return fnmatch.fnmatch(channel, self.match_channel) and fnmatch.fnmatch(event, self.match_event)

    def is_cooled_down(self) -> bool:
        if self.cooldown <= 0:
            return True
        return (time.time() - self._last_fired) >= self.cooldown

    def mark_fired(self):
        self._last_fired = time.time()


def load_reactions(path: str = REACTIONS_PATH) -> list[Reaction]:
    """Load reactions from YAML config."""
    with open(path) as f:
        data = yaml.safe_load(f)

    reactions = []
    for r in data.get("reactions", []):
        match = r.get("match", {})
        reactions.append(Reaction(
            name=r["name"],
            match_channel=match.get("channel", "*"),
            match_event=match.get("event", "*"),
            actions=r.get("actions", []),
            cooldown=r.get("cooldown", 0),
        ))
    logger.info("Loaded %d reactions from %s", len(reactions), path)
    return reactions


# ── Action Executors ─────────────────────────────────────────────────

def _action_log(params: dict, event: dict):
    """Just log the event."""
    level = params.get("level", "warning").upper()
    msg = params.get("message", "Event: {event}").format(**event, **event.get("data", {}))
    logger.log(getattr(logging, level, logging.WARNING), "[reaction] %s", msg)


def _action_notify_human(params: dict, event: dict):
    """Send notification via OpenClaw message tool (best-effort)."""
    msg = params.get("message", "⚠️ Event: {event}").format(**event, **event.get("data", {}))
    channel = params.get("channel", "telegram")
    logger.warning("[notify_human] %s → %s", channel, msg)
    # Use openclaw CLI if available
    try:
        subprocess.run(
            ["openclaw", "message", "--channel", channel, "--text", msg],
            timeout=15, capture_output=True,
        )
    except FileNotFoundError:
        logger.warning("openclaw CLI not found, logging notification: %s", msg)
    except Exception:
        logger.exception("Failed to send notification")


def _action_run_command(params: dict, event: dict):
    """Run a shell command."""
    cmd = params.get("command", "echo no-op").format(**event, **event.get("data", {}))
    timeout = params.get("timeout", 30)
    logger.info("[run_command] %s", cmd)
    try:
        result = subprocess.run(cmd, shell=True, timeout=timeout, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("Command failed (rc=%d): %s", result.returncode, result.stderr[:500])
    except subprocess.TimeoutExpired:
        logger.error("Command timed out after %ds: %s", timeout, cmd)


def _action_publish_event(params: dict, event: dict):
    """Publish a follow-up event (for chaining)."""
    from event_bus import EventBus
    channel = params["channel"].format(**event, **event.get("data", {}))
    evt = params.get("event", "reaction_triggered")
    bus = EventBus()
    bus.publish(channel, evt, data={"triggered_by": event.get("event")}, source="reactions")
    bus.close()


ACTION_REGISTRY: dict[str, callable] = {
    "log": _action_log,
    "notify_human": _action_notify_human,
    "run_command": _action_run_command,
    "publish_event": _action_publish_event,
}


def execute_actions(reaction: Reaction, event: dict):
    """Execute all actions for a matched reaction."""
    for action in reaction.actions:
        action_type = action.get("type")
        params = action.get("params", {})
        executor = ACTION_REGISTRY.get(action_type)
        if executor:
            try:
                executor(params, event)
            except Exception:
                logger.exception("Action %s failed for reaction %s", action_type, reaction.name)
        else:
            logger.warning("Unknown action type: %s", action_type)


def process_event(reactions: list[Reaction], event: dict):
    """Match an event against all reactions and execute."""
    channel = event.get("channel", "")
    evt = event.get("event", "")
    for reaction in reactions:
        if reaction.matches(channel, evt) and reaction.is_cooled_down():
            logger.info("Reaction '%s' triggered by %s/%s", reaction.name, channel, evt)
            reaction.mark_fired()
            execute_actions(reaction, event)
