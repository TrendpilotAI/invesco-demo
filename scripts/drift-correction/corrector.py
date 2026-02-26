"""Corrector module for applying drift corrections to running subagents.

Sends steer commands via openclaw subagents steer, or kills/respawns
agents exhibiting severe drift.
"""

from __future__ import annotations

import json
import logging
import subprocess
import time
from typing import Optional

from strategies import CorrectionStrategy

log = logging.getLogger(__name__)


class Corrector:
    """Applies corrections to drifting subagents."""

    def __init__(self) -> None:
        self._correction_history: list[dict] = []

    def apply_correction(
        self,
        session_id: str,
        label: str,
        correction: CorrectionStrategy,
        original_task: str,
    ) -> bool:
        """Apply a correction strategy to a running agent.
        
        Args:
            session_id: The subagent session ID.
            label: Human-readable agent label.
            correction: The correction strategy to apply.
            original_task: The original task for respawn context.
        
        Returns:
            True if correction was applied successfully.
        """
        if correction.action == "steer":
            return self._steer_agent(session_id, label, correction.message_template)
        elif correction.action == "kill_respawn":
            return self._kill_and_respawn(session_id, label, original_task, correction.message_template)
        elif correction.action == "ignore":
            log.info("Ignoring drift for agent %s (action=ignore)", label)
            return True
        else:
            log.warning("Unknown correction action: %s", correction.action)
            return False

    def _steer_agent(self, session_id: str, label: str, message: str) -> bool:
        """Send a steer command to redirect an agent.
        
        Args:
            session_id: The subagent session ID.
            label: Agent label for logging.
            message: The steering message to send.
        
        Returns:
            True if steer command succeeded.
        """
        log.info("Steering agent %s (session=%s)", label, session_id)
        
        # Try steering by session ID
        result = self._run_openclaw(
            ["openclaw", "subagents", "steer", "--target", session_id, "--message", message]
        )
        
        if result is None:
            # Fallback: try by label
            result = self._run_openclaw(
                ["openclaw", "subagents", "steer", "--target", label, "--message", message]
            )

        success = result is not None
        self._record_correction(session_id, label, "steer", message, success)
        
        if success:
            log.info("Successfully steered agent %s", label)
        else:
            log.error("Failed to steer agent %s", label)
        
        return success

    def _kill_and_respawn(
        self,
        session_id: str,
        label: str,
        original_task: str,
        reason: str,
    ) -> bool:
        """Kill a severely drifted agent and respawn with hints.
        
        Args:
            session_id: The subagent session ID.
            label: Agent label.
            original_task: Original task to include in respawn.
            reason: Why the agent is being killed.
        
        Returns:
            True if kill succeeded (respawn is best-effort).
        """
        log.warning("Killing agent %s due to severe drift: %s", label, reason)
        
        # Kill the agent
        kill_result = self._run_openclaw(
            ["openclaw", "subagents", "kill", "--target", session_id]
        )
        
        if kill_result is None:
            kill_result = self._run_openclaw(
                ["openclaw", "subagents", "kill", "--target", label]
            )

        killed = kill_result is not None
        self._record_correction(session_id, label, "kill_respawn", reason, killed)

        if not killed:
            log.error("Failed to kill agent %s", label)
            return False

        log.info("Agent %s killed. Respawn should be handled by orchestrator.", label)
        # Note: Actual respawn is delegated to the orchestrator or main agent
        # since we need model selection and proper session setup.
        # We publish the event and let the orchestrator handle it.
        
        return True

    def _run_openclaw(self, cmd: list[str], timeout: int = 30) -> Optional[str]:
        """Run an openclaw CLI command.
        
        Args:
            cmd: Command and arguments.
            timeout: Max seconds to wait.
        
        Returns:
            stdout on success, None on failure.
        """
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
            if result.returncode == 0:
                return result.stdout.strip()
            log.debug(
                "Command failed (rc=%d): %s\nstderr: %s",
                result.returncode, " ".join(cmd), result.stderr[:200],
            )
            return None
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            log.debug("Command error: %s — %s", " ".join(cmd), e)
            return None

    def _record_correction(
        self,
        session_id: str,
        label: str,
        action: str,
        message: str,
        success: bool,
    ) -> None:
        """Record a correction attempt for tracking."""
        self._correction_history.append({
            "timestamp": time.time(),
            "session_id": session_id,
            "label": label,
            "action": action,
            "message": message[:200],
            "success": success,
        })

    @property
    def history(self) -> list[dict]:
        """Get correction history."""
        return list(self._correction_history)

    def success_rate(self) -> float:
        """Calculate correction success rate.
        
        Returns:
            Success rate as 0.0-1.0, or 1.0 if no corrections attempted.
        """
        if not self._correction_history:
            return 1.0
        successes = sum(1 for c in self._correction_history if c["success"])
        return successes / len(self._correction_history)
