"""End-to-end: V1-shaped envelope → M11 admit → seal → verify (no V1 import)."""
from __future__ import annotations

from dataclasses import replace

from swi_v2.kernel.admission import admit_foundation_input, compute_integrity_reference
from swi_v2.kernel.ed25519_sig import generate_keypair
from swi_v2.kernel.seal import create_seal, verify_seal


def _v1_shaped_envelope():
    payload = {
        "allowed": True,
        "reason": None,
        "security": {
            "risk_score": 0.0,
            "triggered": [],
            "block_threshold": 0.5,
            "blocked": False,
        },
        "sync": {"gap_seconds": 0.0, "stale": False, "out_of_order": False},
        "redaction": {
            "redacted_text": "travel-test [EMAIL]",
            "match_categories": ["EMAIL"],
        },
        "drift": {"similarity": 0.0, "drifted": True},
    }
    base = {
        "payload": payload,
        "foundation_version": "1.0-proposed",
        "evidence_schema_version": "1.0-proposed",
        "evidence_id": "v1-shaped-e2e-001",
        "verification_status": "v1_trainer_pipeline_completed",
        "source_reference": "serialized-v1-shaped / no V1 import",
    }
    base["integrity_reference"] = compute_integrity_reference(
        payload=base["payload"],
        foundation_version=base["foundation_version"],
        evidence_schema_version=base["evidence_schema_version"],
        evidence_id=base["evidence_id"],
        source_reference=base["source_reference"],
    )
    return base


def test_real_v1_shaped_to_m11_to_seal_to_verify():
    envelope = _v1_shaped_envelope()
    admitted = admit_foundation_input(envelope)
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    assert verify_seal(admitted, sealed) is True


def test_tampered_admitted_payload_fails_e2e():
    envelope = _v1_shaped_envelope()
    admitted = admit_foundation_input(envelope)
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    tampered = replace(admitted, payload={**admitted.payload, "allowed": False})
    assert verify_seal(tampered, sealed) is False


def test_chain_of_two_seals():
    envelope = _v1_shaped_envelope()
    a1 = admit_foundation_input(envelope)
    priv, pub = generate_keypair()
    s1 = create_seal(a1, priv, pub, previous_chain_hash=None)
    assert verify_seal(a1, s1) is True

    env2 = _v1_shaped_envelope()
    env2["evidence_id"] = "v1-shaped-e2e-002"
    env2["integrity_reference"] = compute_integrity_reference(
        payload=env2["payload"],
        foundation_version=env2["foundation_version"],
        evidence_schema_version=env2["evidence_schema_version"],
        evidence_id=env2["evidence_id"],
        source_reference=env2["source_reference"],
    )
    a2 = admit_foundation_input(env2)
    s2 = create_seal(a2, priv, pub, previous_chain_hash=s1.chain_hash)
    assert verify_seal(a2, s2) is True
    assert s2.previous_chain_hash == s1.chain_hash
