"""S9 evidence adequacy tests."""
from swi_v2.s9.evidence import evidence_adequacy, evaluate_evidence_item


def test_empty_evidence():
    r = evidence_adequacy([])
    assert r["evidence_exists"] is False
    assert r["adequate"] is False


def test_full_pass_adequate():
    r = evidence_adequacy([{
        "evidence_id": "E1", "exists": True,
        "relevance": "PASS", "freshness": "PASS", "scope": "PASS",
        "provenance": "PASS", "integrity": "PASS",
    }])
    assert r["adequate"] is True


def test_stale_not_adequate():
    r = evidence_adequacy([{
        "evidence_id": "E1", "exists": True,
        "relevance": "PASS", "freshness": "FAIL", "scope": "PASS",
        "provenance": "PASS", "integrity": "PASS",
    }])
    assert r["adequate"] is False


def test_missing_dims_unresolved_not_pass():
    item = evaluate_evidence_item({"evidence_id": "E1", "exists": True})
    assert item["relevance"] == "UNRESOLVED"
    assert item["freshness"] == "UNRESOLVED"
