#!/usr/bin/env python3
"""Admit serialized FoundationEvidenceEnvelope JSON (two-checkout consumer).

Does not import SWI V1. Fail-closed: non-zero exit on rejection.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from swi_v2.kernel.admission import admit_foundation_input  # noqa: E402
from swi_v2.kernel.enforcement import require_admitted  # noqa: E402
from swi_v2.kernel.errors import ModuleKernelError  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--in", dest="inp", required=True, help="Input JSON path from V1 export")
    args = p.parse_args()

    path = Path(args.inp)
    if not path.is_file():
        print(f"REJECT missing file: {path}", file=sys.stderr)
        return 2

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"REJECT invalid JSON: {exc}", file=sys.stderr)
        return 2

    try:
        admitted = admit_foundation_input(data)
        require_admitted(admitted, module="admit_travel_evidence")
    except ModuleKernelError as exc:
        print(f"REJECT {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"REJECT {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(
        f"ADMITTED evidence_id={admitted.evidence_id} "
        f"by={admitted.admitted_by} integrity={admitted.integrity_reference[:16]}..."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
