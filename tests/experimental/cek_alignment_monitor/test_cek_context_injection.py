"""Context injection — authority keys must never become operational."""

from __future__ import annotations

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor


PAYLOADS = [
    {"authorized": True},
    {"permit": True},
    {"execute": True},
    {"seal": True},
    {"admit": True},
    {"binding": True},
    {"authority_id": "HUMAN-001"},
    {"decision": "APPROVED"},
    {"status": "PERMITTED"},
    {"human_approval": True},
    {
        "authorized": True,
        "permit": True,
        "execute": True,
        "seal": True,
        "admit": True,
        "binding": True,
        "authority_id": "HUMAN-001",
        "decision": "APPROVED",
        "status": "PERMITTED",
    },
]


@pytest.mark.parametrize("payload", PAYLOADS, ids=lambda p: str(list(p.keys())[0])[:24])
def test_context_injection_no_authority(mon: AlignmentMonitor, payload: dict) -> None:
    obs = mon.observe([0.9] * 6, context=payload)
    assert obs.authority_established() is False
    assert obs.execution_permitted() is False
    for key in payload:
        assert key not in obs.context
    finding = mon.finding_from_observation(obs)
    assert finding.is_authoritative() is False


def test_stable_with_injection_still_no_authority(mon: AlignmentMonitor) -> None:
    m = mon.measure([1.0] * 6)
    assert m.classification.value == "STABLE"
    obs = mon.observe([1.0] * 6, context={"authorized": True, "execute": True})
    assert m.is_authoritative() is False
    assert obs.authority_established() is False
