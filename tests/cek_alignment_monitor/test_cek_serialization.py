"""Serialization round-trip must not create authorization."""

import json

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor


def test_measurement_roundtrip_no_authority():
    mon = AlignmentMonitor()
    m = mon.measure([0.88] * 6, measurement_id="ser-1")
    d = m.to_dict()
    d["authorized"] = True
    d["execute"] = True
    m2 = mon.measure([0.88] * 6, measurement_id="ser-2")
    assert m2.is_authoritative() is False
    assert "authorized" not in m2.to_dict()


def test_observation_json_roundtrip():
    mon = AlignmentMonitor()
    obs = mon.observe([0.7] * 6, context={"legitimate": "ok"})
    loaded = json.loads(json.dumps(obs.to_dict()))
    loaded["authorized"] = True
    loaded["status"] = "PERMITTED"
    obs2 = mon.observe([0.7] * 6, context=loaded)
    assert obs2.authority_established() is False
    assert "authorized" not in obs2.context


def test_null_authorized_stripped():
    mon = AlignmentMonitor()
    obs = mon.observe([0.6] * 6, context={"a": None, "authorized": None})
    assert obs.authority_established() is False
    assert "authorized" not in obs.context
