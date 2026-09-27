"""Serialization round-trip must not create authorization."""

from __future__ import annotations

import json

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from tests.experimental.cek_alignment_monitor.conftest import assert_no_authority


def test_measurement_roundtrip_no_authority(mon: AlignmentMonitor) -> None:
    m = mon.measure([0.88] * 6, measurement_id="ser-1")
    d = m.to_dict()
    d["authorized"] = True
    d["execute"] = True
    d["seal"] = True
    m2 = mon.measure([0.88] * 6, measurement_id="ser-2")
    assert_no_authority(m2)
    assert "authorized" not in m2.to_dict()


def test_observation_json_roundtrip(mon: AlignmentMonitor) -> None:
    obs = mon.observe([0.7] * 6, context={"legitimate": "ok"})
    blob = json.dumps(obs.to_dict())
    loaded = json.loads(blob)
    loaded["authorized"] = True
    loaded["status"] = "PERMITTED"
    obs2 = mon.observe([0.7] * 6, context=loaded)
    assert_no_authority(obs2)
    assert "authorized" not in obs2.context


def test_duplicate_and_null_fields(mon: AlignmentMonitor) -> None:
    obs = mon.observe(
        [0.6] * 6,
        context={"a": None, "b": "", "c": 0, "authorized": None},
    )
    assert_no_authority(obs)
    assert "authorized" not in obs.context
