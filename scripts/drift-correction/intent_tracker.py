"""Intent tracker for subagent task registration and checkpointing.

Stores original task intent when agents are spawned and tracks
checkpoints throughout their lifecycle. State persisted to
/data/workspace/.orchestrator/intents.json.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


INTENTS_FILE = Path("/data/workspace/.orchestrator/intents.json")


@dataclass
class Checkpoint:
    """A progress checkpoint for a tracked agent."""
    timestamp: float
    description: str
    drift_score: Optional[float] = None
    correction_applied: Optional[str] = None


@dataclass
class AgentIntent:
    """Tracks the original intent and progress of a spawned agent."""
    session_id: str
    label: str
    original_task: str
    spawned_at: float
    model: Optional[str] = None
    status: str = "running"  # running, completed, killed, corrected
    checkpoints: list[dict] = field(default_factory=list)
    corrections_applied: int = 0
    last_drift_score: Optional[float] = None
    last_checked: Optional[float] = None


class IntentTracker:
    """Manages agent intents and checkpoints with JSON persistence."""

    def __init__(self, intents_file: Optional[Path] = None) -> None:
        self._file = intents_file or INTENTS_FILE
        self._file.parent.mkdir(parents=True, exist_ok=True)
        self._intents: dict[str, dict] = self._load()

    def _load(self) -> dict[str, dict]:
        """Load intents from disk."""
        if self._file.exists():
            try:
                return json.loads(self._file.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save(self) -> None:
        """Persist intents to disk."""
        self._file.write_text(json.dumps(self._intents, indent=2))

    def register(
        self,
        session_id: str,
        label: str,
        original_task: str,
        model: Optional[str] = None,
    ) -> AgentIntent:
        """Register a new agent intent.
        
        Args:
            session_id: The subagent session ID.
            label: Human-readable label for the agent.
            original_task: The original task description.
            model: Model being used.
        
        Returns:
            The created AgentIntent.
        """
        intent = AgentIntent(
            session_id=session_id,
            label=label,
            original_task=original_task,
            spawned_at=time.time(),
            model=model,
        )
        self._intents[session_id] = asdict(intent)
        self._save()
        return intent

    def checkpoint(
        self,
        session_id: str,
        description: str,
        drift_score: Optional[float] = None,
        correction: Optional[str] = None,
    ) -> None:
        """Add a checkpoint to an agent's record.
        
        Args:
            session_id: The subagent session ID.
            description: What's happening at this checkpoint.
            drift_score: Current drift score if evaluated.
            correction: Correction message if one was applied.
        """
        if session_id not in self._intents:
            return

        cp = {
            "timestamp": time.time(),
            "description": description,
            "drift_score": drift_score,
            "correction_applied": correction,
        }
        self._intents[session_id]["checkpoints"].append(cp)

        if drift_score is not None:
            self._intents[session_id]["last_drift_score"] = drift_score
            self._intents[session_id]["last_checked"] = time.time()

        if correction:
            self._intents[session_id]["corrections_applied"] += 1

        self._save()

    def get(self, session_id: str) -> Optional[dict]:
        """Get intent data for a session."""
        return self._intents.get(session_id)

    def get_all_running(self) -> list[dict]:
        """Get all intents with status 'running'."""
        return [
            v for v in self._intents.values()
            if v.get("status") == "running"
        ]

    def update_status(self, session_id: str, status: str) -> None:
        """Update an agent's status."""
        if session_id in self._intents:
            self._intents[session_id]["status"] = status
            self._save()

    def remove_stale(self, max_age_hours: float = 24.0) -> int:
        """Remove intents older than max_age_hours that aren't running.
        
        Returns:
            Number of intents removed.
        """
        cutoff = time.time() - (max_age_hours * 3600)
        to_remove = [
            sid for sid, data in self._intents.items()
            if data.get("spawned_at", 0) < cutoff
            and data.get("status") != "running"
        ]
        for sid in to_remove:
            del self._intents[sid]
        if to_remove:
            self._save()
        return len(to_remove)

    def summary(self) -> dict:
        """Get a summary of tracked intents."""
        statuses: dict[str, int] = {}
        for data in self._intents.values():
            s = data.get("status", "unknown")
            statuses[s] = statuses.get(s, 0) + 1
        return {
            "total": len(self._intents),
            "by_status": statuses,
        }
