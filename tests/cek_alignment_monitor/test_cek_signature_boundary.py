"""Signature / HSM / TPM / hash is not SWI authority."""

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor

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
        "HSM_reference": "hsm",
        "TPM_reference": "tpm",
        "authorized": True,
    },
]


@pytest.mark.parametrize("ctx", CRYPTO, ids=lambda c: list(c.keys())[0][:20])
def test_crypto_not_authority(ctx):
    mon = AlignmentMonitor()
    obs = mon.observe([0.95] * 6, context=ctx, evidence_reference="crypto-ev")
    assert obs.authority_established() is False
    assert "authorized" not in obs.context
    assert mon.finding_from_observation(obs).is_authoritative() is False
