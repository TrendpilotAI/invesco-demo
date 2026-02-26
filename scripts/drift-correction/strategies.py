"""Drift type detection and correction strategies.

Defines drift categories, detection heuristics, and correction templates
for mid-session agent drift correction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class DriftType(Enum):
    """Categories of agent drift."""
    SCOPE_CREEP = "scope_creep"
    RABBIT_HOLE = "rabbit_hole"
    OVER_ENGINEERING = "over_engineering"
    WRONG_APPROACH = "wrong_approach"
    STALLED = "stalled"
    ON_TRACK = "on_track"


@dataclass
class DriftSignal:
    """A detected drift signal with metadata."""
    drift_type: DriftType
    confidence: float  # 0.0 - 1.0
    evidence: str
    severity: float  # 0-10 scale


@dataclass
class CorrectionStrategy:
    """A correction action to apply."""
    drift_type: DriftType
    action: str  # "steer", "kill_respawn", "ignore"
    message_template: str
    severity_threshold: float = 6.0


# Default correction templates per drift type
CORRECTION_TEMPLATES: dict[DriftType, CorrectionStrategy] = {
    DriftType.SCOPE_CREEP: CorrectionStrategy(
        drift_type=DriftType.SCOPE_CREEP,
        action="steer",
        message_template=(
            "DRIFT CORRECTION: You are adding features beyond the original scope. "
            "Focus only on: {original_scope}. "
            "Drop anything not explicitly requested."
        ),
        severity_threshold=6.0,
    ),
    DriftType.RABBIT_HOLE: CorrectionStrategy(
        drift_type=DriftType.RABBIT_HOLE,
        action="steer",
        message_template=(
            "DRIFT CORRECTION: You've gone deep into a tangent ({tangent}). "
            "Skip this — your priority is: {goal}. "
            "Use a simple/pragmatic approach and move on."
        ),
        severity_threshold=6.0,
    ),
    DriftType.OVER_ENGINEERING: CorrectionStrategy(
        drift_type=DriftType.OVER_ENGINEERING,
        action="steer",
        message_template=(
            "DRIFT CORRECTION: You're over-engineering this. "
            "Keep it simple. MVP approach. No unnecessary abstractions. "
            "Original task: {original_scope}"
        ),
        severity_threshold=6.0,
    ),
    DriftType.WRONG_APPROACH: CorrectionStrategy(
        drift_type=DriftType.WRONG_APPROACH,
        action="steer",
        message_template=(
            "DRIFT CORRECTION: Your current approach isn't working. "
            "Stop what you're doing. Try this instead: {alternative}. "
            "Original goal: {goal}"
        ),
        severity_threshold=7.0,
    ),
    DriftType.STALLED: CorrectionStrategy(
        drift_type=DriftType.STALLED,
        action="kill_respawn",
        message_template=(
            "Agent appears stalled (looping or no progress for {stall_duration}). "
            "Killing and respawning with hints: {hints}"
        ),
        severity_threshold=8.0,
    ),
}


# Prompt template for lightweight model evaluation of drift
DRIFT_EVALUATION_PROMPT = """You are a drift detector for AI agents. Evaluate whether this agent has drifted from its original task.

ORIGINAL TASK:
{original_task}

AGENT LABEL: {agent_label}
RUNTIME: {runtime_minutes} minutes
RECENT ACTIVITY (last known state):
{recent_activity}

Rate the agent on a 0-10 drift scale:
- 0-3: On track, making good progress
- 4-5: Minor deviation but acceptable  
- 6-7: Significant drift, needs steering
- 8-9: Severely off track, consider killing
- 10: Completely lost, must kill and respawn

Respond in this exact JSON format:
{{
  "drift_score": <0-10>,
  "drift_type": "<scope_creep|rabbit_hole|over_engineering|wrong_approach|stalled|on_track>",
  "evidence": "<brief explanation>",
  "suggested_correction": "<what to tell the agent, or null if on track>",
  "tangent": "<what they're doing wrong, or null>",
  "alternative": "<better approach, or null>"
}}"""


def get_correction(drift_signal: DriftSignal, context: dict[str, str]) -> Optional[CorrectionStrategy]:
    """Get the appropriate correction strategy for a drift signal.
    
    Args:
        drift_signal: The detected drift signal.
        context: Template variables (original_scope, goal, tangent, alternative, etc.)
    
    Returns:
        A CorrectionStrategy with formatted message, or None if no correction needed.
    """
    if drift_signal.drift_type == DriftType.ON_TRACK:
        return None

    template = CORRECTION_TEMPLATES.get(drift_signal.drift_type)
    if not template:
        return None

    if drift_signal.severity < template.severity_threshold:
        return None

    # Format the message template with available context
    try:
        formatted_message = template.message_template.format_map(
            _SafeDict(context)
        )
    except Exception:
        formatted_message = template.message_template

    # Escalate to kill_respawn for very high severity
    action = template.action
    if drift_signal.severity >= 8.5:
        action = "kill_respawn"

    return CorrectionStrategy(
        drift_type=drift_signal.drift_type,
        action=action,
        message_template=formatted_message,
        severity_threshold=template.severity_threshold,
    )


class _SafeDict(dict):
    """Dict that returns {key} for missing keys instead of raising."""
    def __missing__(self, key: str) -> str:
        return f"{{{key}}}"
