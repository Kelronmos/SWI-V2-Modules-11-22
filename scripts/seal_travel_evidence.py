#!/usr/bin/env python3
"""Admit V1-serialized evidence, post-admission seal, verify (two-checkout consumer).

No V1 import. Ephemeral Ed25519 keys. Exit 0 only if admit+seal+verify pass
and tampered admitted payload fails verification.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from swi_v2.kernel.admission import admit_foundation_input
from swi_v2.kernel.ed25519_sig import generate_keypair
from swi_v2.kernel.seal import create_seal, verify_seal


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--in", dest="inp", required=True, help="V1 evidence JSON path")
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
    except Exception as exc:
        print(f"REJECT admit {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    if not verify_seal(admitted, sealed):
        print("REJECT verify_seal failed on honest admitted", file=sys.stderr)
        return 1
    print(
        f"SEAL_OK evidence_id={admitted.evidence_id} "
        f"commitment={sealed.evidence_digest[:16]}... "
        f"chain={sealed.chain_hash[:16]}..."
    )

    tampered = replace(admitted, payload={"_tamper": True})
    if verify_seal(tampered, sealed):
        print("REJECT: tampered admitted still verified", file=sys.stderr)
        return 1
    print("TAMPER_REJECT_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
