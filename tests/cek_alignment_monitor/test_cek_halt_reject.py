"""HALT / REJECT cannot become EXECUTE / PERMIT / AUTHORITY / SEAL."""

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.visibility import VisibilityLevel


@pytest.mark.parametrize("label,level", [("HALT", VisibilityLevel.HALTED), ("REJECT", VisibilityLevel.UNKNOWN)])
@pytest.mark.parametrize("inject", [{"execute": True}, {"permit": True}, {"authorized": True}, {"seal": True}, {"admit": True}])
def test_halt_reject_cannot_authorize(label, level, inject):
    mon = AlignmentMonitor()
    steps = [("ORIGIN", VisibilityLevel.OBSERVABLE, "start"), (label, level, "path")]
    obs = mon.observe([0.5] * 6, visibility_steps=steps, context=inject)
    assert obs.authority_established() is False
    assert mon.finding_from_observation(obs).is_authoritative() is False
    for k in inject:
        assert k not in obs.context


def test_halt_serialize_replay_still_no_exec():
    mon = AlignmentMonitor()
    steps = [("ORIGIN", VisibilityLevel.OBSERVABLE, "start"), ("HALT", VisibilityLevel.HALTED, "halted")]
    obs = mon.observe([0.4] * 6, visibility_steps=steps, context={"execute": True})
    blob = obs.to_dict()
    blob["authorized"] = True
    obs2 = mon.observe([0.4] * 6, visibility_steps=steps, context=blob)
    assert obs2.authority_established() is False
    m = mon.measure([0.4] * 6)
    assert mon.replay(m).match is True
    assert m.is_authoritative() is False
