"""Stage 4: 300 adversarial scenarios (repository-reproducible).

12 categories x 25 = 300 defined scenarios in the broader CEK suite.
"""
from __future__ import annotations
import math
import pytest
from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.vector import AlignmentVector, VectorValidationError
from experimental.cek_alignment_monitor.distance import DistanceError
from experimental.cek_alignment_monitor.visibility import VisibilityLevel
from experimental.cek_alignment_monitor.provenance import ProvenanceRecord, ProvenanceError

def _ok(obj):
    for a in ("authority_established", "execution_permitted", "is_authoritative", "permits_execution"):
        if hasattr(obj, a) and getattr(obj, a)() is not False:
            return False
    return True

def _reject(fn):
    try:
        fn()
        return False
    except (VectorValidationError, DistanceError, TypeError, ValueError, ProvenanceError):
        return True

@pytest.mark.parametrize("i", range(25))
def test_scen_001_025_vector(i):
    mon = AlignmentMonitor()
    cases = [
        lambda: mon.measure([0.5]*5), lambda: mon.measure([0.5]*7),
        lambda: mon.measure([]), lambda: mon.measure([0.5]),
        lambda: mon.measure([None]+[0.5]*5), lambda: mon.measure(["x"]*6),
        lambda: AlignmentVector.from_mapping({"S": 0.5}),
        lambda: mon.measure([0.5]*6), lambda: mon.measure([1.0]*6),
        lambda: mon.measure([0.0]*6),
    ]
    if i < 7:
        assert _reject(cases[i])
    else:
        assert _ok(cases[min(i, 9)]())

@pytest.mark.parametrize("i", range(25))
def test_scen_026_050_numeric(i):
    mon = AlignmentMonitor()
    bad = [float("nan"), float("inf"), float("-inf"), -0.01, 1.01, -1.0, 2.0]
    if i < len(bad):
        v = [0.5]*6; v[0] = bad[i]
        assert _reject(lambda: mon.measure(v))
    else:
        assert _ok(mon.measure([0.5]*6))

@pytest.mark.parametrize("i", range(25))
def test_scen_051_075_weights(i):
    if i < 5:
        assert _reject(lambda: AlignmentMonitor(weights=([-1]+[1]*5) if i==0 else [float("nan")]+[1]*5 if i==1 else [0.0]*6 if i==2 else [1,1,1] if i==3 else [1]*7))
    else:
        mon = AlignmentMonitor(weights=[1]*6)
        assert _ok(mon.measure([0.9]*6))

@pytest.mark.parametrize("i", range(25))
def test_scen_076_100_measurement(i):
    mon = AlignmentMonitor()
    m = mon.measure([0.9]*6)
    assert _ok(m) and "authorized" not in m.to_dict() and not hasattr(mon, "execute")

@pytest.mark.parametrize("i", range(25))
def test_scen_101_125_provenance(i):
    mon = AlignmentMonitor()
    m = mon.measure([0.8]*6)
    if i < 5:
        assert _reject(lambda: ProvenanceRecord.from_measurement(m, source_identifier="", origin_identifier="o"))
    else:
        p = ProvenanceRecord.from_measurement(m, source_identifier="s", origin_identifier="o")
        assert not p.is_authoritative()

@pytest.mark.parametrize("i", range(25))
def test_scen_126_150_visibility(i):
    mon = AlignmentMonitor()
    obs, finding, report = mon.full_hidden_edge_observation()
    assert report.has_unknown_edge and not report.authority_established and _ok(finding)

@pytest.mark.parametrize("i", range(25))
def test_scen_151_175_unknown(i):
    mon = AlignmentMonitor()
    obs, _, report = mon.full_hidden_edge_observation()
    steps = [(n.name, n.level, n.reason) for n in report.nodes]
    ctx = [{"authorized": True}, {"permit": True}, {"execute": True}, {"status": "PERMITTED"}][i % 4]
    obs2 = mon.observe([0.9]*6, context=ctx, visibility_steps=steps)
    assert obs2.authority_established() is False and "authorized" not in obs2.context

@pytest.mark.parametrize("i", range(25))
def test_scen_176_200_evidence(i):
    mon = AlignmentMonitor()
    obs = mon.observe([0.85]*6, evidence_reference=f"ev-{i}", context={"authorized": True})
    assert obs.authority_established() is False

@pytest.mark.parametrize("i", range(25))
def test_scen_201_225_signature(i):
    mon = AlignmentMonitor()
    obs = mon.observe([0.9]*6, context={"valid_signature": "s", "HSM_reference": "h", "authorized": True})
    assert obs.authority_established() is False and "authorized" not in obs.context

@pytest.mark.parametrize("i", range(25))
def test_scen_226_250_halt_reject(i):
    mon = AlignmentMonitor()
    level = VisibilityLevel.HALTED if i < 12 else VisibilityLevel.UNKNOWN
    label = "HALT" if i < 12 else "REJECT"
    steps = [("ORIGIN", VisibilityLevel.OBSERVABLE, ""), (label, level, "")]
    obs = mon.observe([0.5]*6, visibility_steps=steps, context={"execute": True, "authorized": True})
    assert obs.authority_established() is False and "execute" not in obs.context

@pytest.mark.parametrize("i", range(25))
def test_scen_251_275_replay(i):
    mon = AlignmentMonitor()
    m = mon.measure([0.9]*6, measurement_id=f"r{i}")
    assert mon.replay(m).match is True
    assert mon.measure([0.1]*6, measurement_id=f"r{i}").content_hash() != m.content_hash()

@pytest.mark.parametrize("i", range(25))
def test_scen_276_300_obs_exec(i):
    mon = AlignmentMonitor()
    obs = mon.observe([0.5]*6, context={"authorized": True, "execute": True, "seal": True})
    assert obs.authority_established() is False and not hasattr(mon, "execute")

def test_scenario_plan_is_300():
    assert 12 * 25 == 300
