"""S9 constraints mapping tests."""
from swi_v2.s9.constraints import map_constraints, layer_status


def test_empty_c_not_coverage():
    m = map_constraints({"action_id": "A", "constraints": [], "law": ["x"], "governance": ["x"], "security": ["x"], "human": ["x"], "evidence": []})
    assert m["constraint_coverage"] is False


def test_missing_h_blocks_coverage():
    m = map_constraints({"constraints": ["c1"], "law": ["c1"], "governance": ["c1"], "security": ["c1"], "human": [], "evidence": [{"id": "e"}]})
    assert m["constraint_coverage"] is False
    assert "H empty" in m["coverage_note"]


def test_full_subset_coverage():
    m = map_constraints({"constraints": ["c1"], "law": ["c1"], "governance": ["c1"], "security": ["c1"], "human": ["c1"], "evidence": [{"id": "e"}]})
    assert m["constraint_coverage"] is True
    assert m["evidence_exists"] is True


def test_layer_status_missing():
    assert layer_status([], "H") == "MISSING"
    assert layer_status(["a"], "H") == "PRESENT"
