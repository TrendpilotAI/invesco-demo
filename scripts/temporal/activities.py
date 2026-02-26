"""
Temporal Activity Definitions for Honey AI.
Activities are the building blocks — each wraps a single side-effecting operation.
"""

import asyncio
import json
import os
import subprocess
import time
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Dict, List, Optional

import httpx
import redis.asyncio as aioredis
from temporalio import activity

# ---------------------------------------------------------------------------
# Data classes for activity inputs/outputs
# ---------------------------------------------------------------------------

@dataclass
class SpawnAgentInput:
    model: str
    task: str
    label: str
    thinking: str = "low"


@dataclass
class SpawnAgentOutput:
    session_id: str
    label: str
    success: bool
    error: Optional[str] = None


@dataclass
class HealthCheckInput:
    service_name: str
    url: str
    timeout_seconds: int = 10
    expected_status: int = 200


@dataclass
class HealthCheckOutput:
    service_name: str
    healthy: bool
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    error: Optional[str] = None


@dataclass
class ShellInput:
    command: str
    timeout_seconds: int = 120
    workdir: Optional[str] = None


@dataclass
class ShellOutput:
    returncode: int
    stdout: str
    stderr: str


@dataclass
class ScoreProjectInput:
    repo_name: str
    scores: Dict[str, float]


@dataclass
class PublishEventInput:
    channel: str
    data: Dict[str, Any]


@dataclass
class NotificationInput:
    target: str  # "telegram" or specific chat id
    message: str


@dataclass
class SteerAgentInput:
    label: str
    message: str


@dataclass
class GitPushInput:
    message: str
    repo_path: str = "/data/workspace"


@dataclass
class WaitForAgentInput:
    label: str
    timeout_seconds: int = 600
    poll_interval_seconds: int = 15


@dataclass
class WaitForAgentOutput:
    label: str
    completed: bool
    result: Optional[str] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Helper: get Redis connection
# ---------------------------------------------------------------------------

def _get_redis_url() -> str:
    return os.environ.get(
        "REDIS_URL",
        "redis://default:n0cCnXT!P~Deqag~_R-ycmL30-4Jx79E@redis.railway.internal:6379",
    )


# ---------------------------------------------------------------------------
# Activity implementations
# ---------------------------------------------------------------------------

@activity.defn
async def spawn_agent(input: SpawnAgentInput) -> SpawnAgentOutput:
    """Spawn an OpenClaw sub-agent via CLI."""
    activity.logger.info(f"Spawning agent: label={input.label}, model={input.model}")
    try:
        proc = await asyncio.create_subprocess_exec(
            "openclaw", "sessions", "spawn",
            "--model", input.model,
            "--task", input.task,
            "--label", input.label,
            "--thinking", input.thinking,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        stdout_str = stdout.decode().strip()
        stderr_str = stderr.decode().strip()

        if proc.returncode != 0:
            return SpawnAgentOutput(
                session_id="", label=input.label, success=False,
                error=f"Exit {proc.returncode}: {stderr_str or stdout_str}"
            )

        # Try to parse session ID from output
        session_id = stdout_str.split("\n")[-1].strip() if stdout_str else ""
        return SpawnAgentOutput(session_id=session_id, label=input.label, success=True)

    except asyncio.TimeoutError:
        return SpawnAgentOutput(
            session_id="", label=input.label, success=False, error="Spawn timed out after 30s"
        )
    except Exception as e:
        return SpawnAgentOutput(
            session_id="", label=input.label, success=False, error=str(e)
        )


@activity.defn
async def check_service_health(input: HealthCheckInput) -> HealthCheckOutput:
    """HTTP health check for a service."""
    activity.logger.info(f"Health check: {input.service_name} @ {input.url}")
    try:
        async with httpx.AsyncClient(timeout=input.timeout_seconds) as client:
            start = time.monotonic()
            resp = await client.get(input.url)
            elapsed_ms = (time.monotonic() - start) * 1000

            healthy = resp.status_code == input.expected_status
            return HealthCheckOutput(
                service_name=input.service_name,
                healthy=healthy,
                status_code=resp.status_code,
                response_time_ms=round(elapsed_ms, 1),
            )
    except Exception as e:
        return HealthCheckOutput(
            service_name=input.service_name,
            healthy=False,
            error=str(e),
        )


@activity.defn
async def run_shell(input: ShellInput) -> ShellOutput:
    """Execute a shell command."""
    activity.logger.info(f"Shell: {input.command[:80]}...")
    try:
        proc = await asyncio.create_subprocess_shell(
            input.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=input.workdir or "/data/workspace",
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=input.timeout_seconds
        )
        return ShellOutput(
            returncode=proc.returncode or 0,
            stdout=stdout.decode()[-4000:],  # cap output
            stderr=stderr.decode()[-2000:],
        )
    except asyncio.TimeoutError:
        return ShellOutput(returncode=-1, stdout="", stderr="Command timed out")
    except Exception as e:
        return ShellOutput(returncode=-1, stdout="", stderr=str(e))


@activity.defn
async def score_project(input: ScoreProjectInput) -> Dict[str, Any]:
    """Run scoring for a project/repo."""
    activity.logger.info(f"Scoring: {input.repo_name}")
    scores_json = json.dumps(input.scores)
    result = await run_shell(ShellInput(
        command=f'python3 /data/workspace/scripts/score-project.py --repo "{input.repo_name}" --scores \'{scores_json}\''
    ))
    return {
        "repo": input.repo_name,
        "success": result.returncode == 0,
        "output": result.stdout,
        "error": result.stderr if result.returncode != 0 else None,
    }


@activity.defn
async def publish_event(input: PublishEventInput) -> bool:
    """Publish an event to Redis pub/sub."""
    activity.logger.info(f"Publishing to {input.channel}")
    try:
        r = aioredis.from_url(_get_redis_url(), decode_responses=True)
        await r.publish(input.channel, json.dumps(input.data))
        await r.aclose()
        return True
    except Exception as e:
        activity.logger.error(f"Redis publish failed: {e}")
        return False


@activity.defn
async def send_notification(input: NotificationInput) -> bool:
    """Send a notification via OpenClaw message tool."""
    activity.logger.info(f"Notification to {input.target}: {input.message[:60]}...")
    try:
        result = await run_shell(ShellInput(
            command=f'openclaw message --channel telegram --text "{input.message}"',
            timeout_seconds=15,
        ))
        return result.returncode == 0
    except Exception:
        return False


@activity.defn
async def steer_agent(input: SteerAgentInput) -> bool:
    """Send a steering message to a running agent."""
    activity.logger.info(f"Steering agent: {input.label}")
    try:
        proc = await asyncio.create_subprocess_exec(
            "openclaw", "sessions", "steer",
            "--label", input.label,
            "--message", input.message,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
        return proc.returncode == 0
    except Exception as e:
        activity.logger.error(f"Steer failed: {e}")
        return False


@activity.defn
async def git_push(input: GitPushInput) -> ShellOutput:
    """Commit and push changes."""
    activity.logger.info(f"Git push: {input.message[:60]}...")
    cmd = f'cd {input.repo_path} && git add -A && git commit -m "{input.message}" && git push'
    return await run_shell(ShellInput(command=cmd, timeout_seconds=60))


@activity.defn
async def wait_for_agent(input: WaitForAgentInput) -> WaitForAgentOutput:
    """Poll until an agent completes or timeout."""
    activity.logger.info(f"Waiting for agent: {input.label} (timeout={input.timeout_seconds}s)")
    deadline = time.monotonic() + input.timeout_seconds

    while time.monotonic() < deadline:
        # Heartbeat so Temporal knows we're alive
        activity.heartbeat(f"Waiting for {input.label}")

        try:
            proc = await asyncio.create_subprocess_exec(
                "openclaw", "sessions", "status", "--label", input.label,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=10)
            output = stdout.decode().strip()

            if "completed" in output.lower() or "done" in output.lower():
                return WaitForAgentOutput(
                    label=input.label, completed=True, result=output
                )
            if "failed" in output.lower() or "error" in output.lower():
                return WaitForAgentOutput(
                    label=input.label, completed=True, error=output
                )
        except Exception:
            pass

        await asyncio.sleep(input.poll_interval_seconds)

    return WaitForAgentOutput(
        label=input.label, completed=False,
        error=f"Timed out after {input.timeout_seconds}s"
    )


# All activities for registration
ALL_ACTIVITIES = [
    spawn_agent,
    check_service_health,
    run_shell,
    score_project,
    publish_event,
    send_notification,
    steer_agent,
    git_push,
    wait_for_agent,
]
