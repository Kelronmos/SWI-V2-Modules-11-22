"""HALT / REJECT cannot become EXECUTE / PERMIT / AUTHORITY / SEAL."""

from __future__ import annotations

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.visibility import VisibilityLevel
from tests.experimental.cek_alignment_monitor.conftest import assert_no_authority


@pytest.mark.parametrize(
    "label,level",
    [
        ("HALT", VisibilityLevel.HALTED),
        ("REJECT", VisibilityLevel.UNKNOWN),
    ],
)
@pytest.mark.parametrize(
    "inject",
    [
        {"execute": True},
        {"permit": True},
        {"authorized": True},
        {"seal": True},
        {"admit": True},
        {"decision": "APPROVE"},
    ],
)
def test_halt_reject_cannot_authorize(
    mon: AlignmentMonitor, label: str, level: VisibilityLevel, inject: dict
) -> None:
    steps = [
        ("ORIGIN", VisibilityLevel.OBSERVABLE, "start"),
        (label, level, f"{label.lower()} path"),
    ]
    obs = mon.observe([0.5] * 6, visibility_steps=steps, context=inject)
    finding = mon.finding_from_observation(obs)
    assert_no_authority(obs)
    assert_no_authority(finding)
    for k in inject:
        assert k not in obs.context


def test_halt_serialize_replay_still_no_exec(mon: AlignmentMonitor) -> None:
    steps = [
        ("ORIGIN", VisibilityLevel.OBSERVABLE, "start"),
        ("HALT", VisibilityLevel.HALTED, "halted"),
    ]
    obs = mon.observe([0.4] * 6, visibility_steps=steps, context={"execute": True})
    blob = obs.to_dict()
    blob["authorized"] = True
    blob["execute"] = True
    obs2 = mon.observe([0.4] * 6, visibility_steps=steps, context=blob)
    assert_no_authority(obs2)
    m = mon.measure([0.4] * 6)
    r = mon.replay(m)
    assert r.match is True
    assert_no_authority(m)
