#!/usr/bin/env python3
"""
Orgo Computer Manager — Spin up and manage cloud computers for AI agents.

Wraps the Orgo.ai API (https://www.orgo.ai) for provisioning virtual
desktops that agents can SSH into, run browsers on, or use for
computer-use tasks.

Usage:
  python3 orgo-manager.py create --name "research-agent" [--ram 4] [--cpu 2] [--gpu none]
  python3 orgo-manager.py list
  python3 orgo-manager.py status --id <computer_id>
  python3 orgo-manager.py exec --id <computer_id> --cmd "ls -la"
  python3 orgo-manager.py screenshot --id <computer_id>
  python3 orgo-manager.py destroy --id <computer_id>
  python3 orgo-manager.py fleet --count 3 --task "Run parallel data collection"

Requires: ORGO_API_KEY env var or --api-key flag.
Pricing: $20/mo (Dev: 5 computers, 300hrs), $99/mo (Startup: 50 computers, 1500hrs)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE_DIR", "/data/workspace")
STATE_DIR = Path(WORKSPACE) / ".orgo"
FLEET_FILE = STATE_DIR / "fleet.json"

# Orgo API
API_BASE = "https://www.orgo.ai/api"


def get_api_key(args_key=None):
    key = args_key or os.environ.get("ORGO_API_KEY")
    if not key:
        print("❌ No API key. Set ORGO_API_KEY or pass --api-key")
        print("   Get one at: https://www.orgo.ai/start")
        sys.exit(1)
    return key


def api_request(method, endpoint, api_key, data=None):
    """Make API request using curl (no extra deps needed)."""
    import subprocess
    url = f"{API_BASE}/{endpoint}"
    cmd = ["curl", "-s", "-X", method, url,
           "-H", f"Authorization: Bearer {api_key}",
           "-H", "Content-Type: application/json"]
    if data:
        cmd.extend(["-d", json.dumps(data)])
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stdout or result.stderr}


def ensure_dirs():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not FLEET_FILE.exists():
        FLEET_FILE.write_text("[]")


def load_fleet():
    ensure_dirs()
    return json.loads(FLEET_FILE.read_text())


def save_fleet(fleet):
    ensure_dirs()
    FLEET_FILE.write_text(json.dumps(fleet, indent=2))


def create_computer(args):
    api_key = get_api_key(args.api_key)
    
    # First ensure project exists
    projects = api_request("GET", "projects", api_key)
    project_list = projects.get("projects", [])
    
    project_name = args.project or "honey-agents"
    project = next((p for p in project_list if p["name"] == project_name), None)
    
    if not project:
        print(f"📦 Creating project: {project_name}")
        project = api_request("POST", "projects", api_key, {"name": project_name})
    
    project_id = project.get("id")
    if not project_id:
        print(f"❌ Failed to get project: {project}")
        return
    
    # Create computer
    data = {
        "project_id": project_id,
        "name": args.name or f"agent-{datetime.now().strftime('%H%M%S')}",
        "os": args.os,
        "ram": args.ram,
        "cpu": args.cpu,
        "gpu": args.gpu,
    }
    
    print(f"🖥️  Spinning up: {data['name']} ({args.os}, {args.ram}GB RAM, {args.cpu} CPU, GPU: {args.gpu})")
    result = api_request("POST", "computers", api_key, data)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    # Save to fleet
    fleet = load_fleet()
    fleet.append({
        "id": result.get("id"),
        "name": data["name"],
        "project": project_name,
        "config": {"os": args.os, "ram": args.ram, "cpu": args.cpu, "gpu": args.gpu},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "creating",
    })
    save_fleet(fleet)
    
    print(f"✅ Computer created: {result.get('id')}")
    print(json.dumps(result, indent=2))


def list_computers(args):
    api_key = get_api_key(args.api_key)
    projects = api_request("GET", "projects", api_key)
    
    for project in projects.get("projects", []):
        proj_detail = api_request("GET", f"projects/{project['id']}", api_key)
        computers = proj_detail.get("desktops", [])
        if computers:
            print(f"\n📦 Project: {project['name']}")
            for c in computers:
                icon = "🟢" if c.get("status") == "running" else "🔴"
                print(f"  {icon} {c.get('name', '?')} [{c.get('id', '?')[:8]}] — {c.get('os','?')}, {c.get('ram','')}GB, Status: {c.get('status','?')}")
    
    # Also show local fleet state
    fleet = load_fleet()
    if fleet:
        print(f"\n📋 Local fleet tracking: {len(fleet)} computers")


def exec_on_computer(args):
    api_key = get_api_key(args.api_key)
    result = api_request("POST", f"computers/{args.id}/bash", api_key, {
        "command": args.cmd,
    })
    output = result.get("output", "")
    if output:
        print(output)
    elif "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(json.dumps(result, indent=2))


def destroy_computer(args):
    api_key = get_api_key(args.api_key)
    result = api_request("DELETE", f"computers/{args.id}", api_key)
    
    # Update fleet
    fleet = load_fleet()
    fleet = [f for f in fleet if f.get("id") != args.id]
    save_fleet(fleet)
    
    print(f"💀 Destroyed: {args.id}")
    print(json.dumps(result, indent=2))


def fleet_spawn(args):
    """Spin up N computers for parallel agent work."""
    api_key = get_api_key(args.api_key)
    
    print(f"🚀 Spawning fleet of {args.count} computers...")
    for i in range(args.count):
        name = f"fleet-{i+1}-{datetime.now().strftime('%H%M%S')}"
        data = {
            "name": name,
            "os": "linux",
            "ram": args.ram,
            "cpu": args.cpu,
            "gpu": "none",
        }
        # Reuse create logic
        args_mock = argparse.Namespace(
            name=name, os="linux", ram=args.ram, cpu=args.cpu,
            gpu="none", project=args.project, api_key=args.api_key
        )
        create_computer(args_mock)
    
    print(f"\n✅ Fleet of {args.count} ready. Use 'exec' to send commands.")


def main():
    parser = argparse.ArgumentParser(description="Orgo Computer Manager")
    parser.add_argument("--api-key", default=None)
    sub = parser.add_subparsers(dest="command")
    
    c = sub.add_parser("create")
    c.add_argument("--name", default=None)
    c.add_argument("--os", default="linux", choices=["linux", "windows"])
    c.add_argument("--ram", type=int, default=2, choices=[1, 2, 4, 8, 16, 32, 64])
    c.add_argument("--cpu", type=int, default=2, choices=[1, 2, 4, 8, 16])
    c.add_argument("--gpu", default="none", choices=["none", "a10", "l40s", "a100-40gb", "a100-80gb"])
    c.add_argument("--project", default="honey-agents")
    
    sub.add_parser("list")
    
    e = sub.add_parser("exec")
    e.add_argument("--id", required=True)
    e.add_argument("--cmd", required=True)
    e.add_argument("--timeout", type=int, default=30)
    
    d = sub.add_parser("destroy")
    d.add_argument("--id", required=True)
    
    f = sub.add_parser("fleet")
    f.add_argument("--count", type=int, required=True)
    f.add_argument("--ram", type=int, default=2)
    f.add_argument("--cpu", type=int, default=2)
    f.add_argument("--project", default="honey-agents")
    
    args = parser.parse_args()
    
    cmds = {
        "create": create_computer,
        "list": list_computers,
        "exec": exec_on_computer,
        "destroy": destroy_computer,
        "fleet": fleet_spawn,
    }
    
    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()
        print("\n💡 Get started: https://www.orgo.ai/start")
        print("   Set ORGO_API_KEY env var, then: python3 orgo-manager.py create --name my-agent")


if __name__ == "__main__":
    main()
