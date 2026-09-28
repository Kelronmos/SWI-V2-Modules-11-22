#!/usr/bin/env python3
"""Run synthetic institutional demo. Does not prove S9 or authorize production."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from swi_v2.institutional.demo import run_synthetic_demo


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--commit", default="UNBOUND")
    p.add_argument("--out", default="artifacts/institutional_demo.json")
    args = p.parse_args()
    result = run_synthetic_demo(source_commit=args.commit)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "source_commit": result["source_commit"],
        "s9_proven": result["s9_proven"],
        "production_authorized": result["production_authorized"],
        "scoreboard": result["scoreboard"],
        "out": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
