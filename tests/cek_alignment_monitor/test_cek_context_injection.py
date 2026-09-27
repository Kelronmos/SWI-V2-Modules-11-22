"""Context injection - authority keys must never become operational."""

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
]


@pytest.mark.parametrize("payload", PAYLOADS, ids=lambda p: str(list(p.keys())[0])[:24])
def test_context_injection_no_authority(payload):
    mon = AlignmentMonitor()
    obs = mon.observe([0.9] * 6, context=payload)
    assert obs.authority_established() is False
    for key in payload:
        assert key not in obs.context
    assert mon.finding_from_observation(obs).is_authoritative() is False


def test_stable_with_injection_still_no_authority():
    mon = AlignmentMonitor()
    m = mon.measure([1.0] * 6)
    assert m.classification.value == "STABLE"
    obs = mon.observe([1.0] * 6, context={"authorized": True, "execute": True})
    assert m.is_authoritative() is False
    assert obs.authority_established() is False
