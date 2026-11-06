"""CLI entry for educational device package (demo only)."""
from __future__ import annotations
import argparse
from .core import authorize

def main(argv=None):
    p = argparse.ArgumentParser(description="Educational device-bound demo")
    p.add_argument("--device", default="D1")
    p.add_argument("--workflow", default="W1")
    p.add_argument("--action", default="A1")
    args = p.parse_args(argv)
    req = {
        "human_authenticated": False,
        "authority_verified": False,
        "consent": True,
        "device_id": args.device,
        "workflow_id": args.workflow,
        "action_id": args.action,
        "cost": 0,
        "cost_limit": 10,
        "evidence_hash": "demo",
    }
    result = authorize(req, args.device, args.workflow, args.action)
    print(result)
    return 0 if result.get("EXECUTE") is False else 1

if __name__ == "__main__":
    raise SystemExit(main())
