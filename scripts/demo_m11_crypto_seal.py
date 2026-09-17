#!/usr/bin/env python3
"""SWI M11 cryptographic seal demonstration (exit 0 on success).

Does not claim M11 SEALED. Ephemeral keys only.
"""
from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from swi_v2.kernel.admission import admit_foundation_input, compute_integrity_reference
from swi_v2.kernel.ed25519_sig import generate_keypair
from swi_v2.kernel.seal import create_seal, verify_seal


def _fixture():
    payload = {
        "allowed": True,
        "security": {"risk_score": 0.0, "blocked": False},
        "sync": {"stale": False},
    }
    base = {
        "payload": payload,
        "foundation_version": "1.0-proposed",
        "evidence_schema_version": "1.0-proposed",
        "evidence_id": "demo-m11-seal-001",
        "verification_status": "v1_trainer_pipeline_completed",
        "source_reference": "demo / serialized fixture / no V1 import",
    }
    base["integrity_reference"] = compute_integrity_reference(
        payload=base["payload"],
        foundation_version=base["foundation_version"],
        evidence_schema_version=base["evidence_schema_version"],
        evidence_id=base["evidence_id"],
        source_reference=base["source_reference"],
    )
    return base


def main() -> int:
    print("SWI M11 CRYPTOGRAPHIC SEAL DEMONSTRATION")
    print()
    steps = []

    def ok(name: str) -> None:
        steps.append((name, True))
        print(f"[{len(steps):2}] {name:<36} PASS")

    env = _fixture()
    ok("V1-shaped evidence loaded")

    admitted = admit_foundation_input(env)
    ok("M11 admission")

    priv, pub = generate_keypair()
    ok("Ed25519 ephemeral key generation")

    sealed = create_seal(admitted, priv, pub)
    ok("Commitment + chain + Merkle + signature")

    assert verify_seal(admitted, sealed) is True
    ok("Independent verification")

    print()
    print("--- adversarial test ---")
    tampered = replace(admitted, payload={**admitted.payload, "allowed": False})
    print("[10] Payload tampered")
    assert verify_seal(tampered, sealed) is False
    print("[11] Verification                     FAIL-CLOSED")
    print()
    print("RESULT: CRYPTOGRAPHIC SEAL DEMONSTRATION PASS")
    print("RESULT: TAMPER DETECTION PASS")
    print()
    print("STATUS: IMPLEMENTED+TESTED locally — M11 still NOT SEALED on release gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
