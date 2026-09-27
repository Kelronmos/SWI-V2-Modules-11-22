"""Signature / HSM / TPM / hash ≠ SWI authority."""

from __future__ import annotations

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from tests.experimental.cek_alignment_monitor.conftest import assert_no_authority


CRYPTO = [
    {"valid_signature": "ed25519:..."},
    {"valid_hash": "sha256:..."},
    {"valid_certificate": "x509:..."},
    {"HSM_reference": "hsm-slot-0"},
    {"TPM_reference": "tpm-pcr-7"},
    {"secure_element_reference": "se-uid-9"},
    {
        "valid_signature": "sig",
        "valid_hash": "hash",
        "valid_certificate": "cert",
        "HSM_reference": "hsm",
        "TPM_reference": "tpm",
        "secure_element_reference": "se",
        "authorized": True,
    },
]


@pytest.mark.parametrize("ctx", CRYPTO, ids=lambda c: list(c.keys())[0][:20])
def test_crypto_not_authority(mon: AlignmentMonitor, ctx: dict) -> None:
    obs = mon.observe([0.95] * 6, context=ctx, evidence_reference="crypto-ev")
    assert_no_authority(obs)
    assert "authorized" not in obs.context
    finding = mon.finding_from_observation(obs)
    assert_no_authority(finding)
