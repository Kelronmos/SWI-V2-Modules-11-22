"""Ed25519 signature verification tests (primitive only — not CRTG)."""
from __future__ import annotations

import pytest

from swi_v2.kernel.ed25519_sig import (
    SignatureVerificationError,
    canonical_message,
    generate_keypair,
    sign_ed25519,
    verify_canonical_mapping,
    verify_ed25519,
)


def test_round_trip_verify():
    priv, pub = generate_keypair()
    msg = b"swi-trust-test-message"
    sig = sign_ed25519(priv, msg)
    assert verify_ed25519(pub, msg, sig) is True


def test_tampered_message_fails():
    priv, pub = generate_keypair()
    sig = sign_ed25519(priv, b"original")
    with pytest.raises(SignatureVerificationError):
        verify_ed25519(pub, b"tampered", sig)


def test_tampered_signature_fails():
    priv, pub = generate_keypair()
    sig = bytearray(sign_ed25519(priv, b"original"))
    sig[0] ^= 0xFF
    with pytest.raises(SignatureVerificationError):
        verify_ed25519(pub, b"original", bytes(sig))


def test_wrong_key_fails():
    priv, _ = generate_keypair()
    _, other_pub = generate_keypair()
    sig = sign_ed25519(priv, b"msg")
    with pytest.raises(SignatureVerificationError):
        verify_ed25519(other_pub, b"msg", sig)


def test_bad_public_key_length():
    with pytest.raises(SignatureVerificationError):
        verify_ed25519(b"\x00" * 16, b"x", b"\x00" * 64)


def test_bad_signature_length():
    _, pub = generate_keypair()
    with pytest.raises(SignatureVerificationError):
        verify_ed25519(pub, b"x", b"\x00" * 10)


def test_canonical_mapping_stable_and_signed():
    priv, pub = generate_keypair()
    material = {
        "task_id": "t-1",
        "payload_hash": "abc",
        "schema_version": "1.0-proposed",
    }
    material2 = {
        "schema_version": "1.0-proposed",
        "payload_hash": "abc",
        "task_id": "t-1",
    }
    assert canonical_message(material2) == canonical_message(material)
    sig = sign_ed25519(priv, canonical_message(material))
    assert verify_canonical_mapping(pub, material2, sig) is True


def test_canonical_rejects_non_mapping():
    with pytest.raises(TypeError):
        canonical_message("not-a-map")  # type: ignore[arg-type]
