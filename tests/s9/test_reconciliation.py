from swi_v2.s9.reconciliation import classify_node, reconcile


def test_dimensions_independent():
    n = classify_node({"path": "swi_v2/x.py", "exists": True, "type": "module", "status": "INSPECTED"})
    assert n["IMPLEMENTED"] == "YES"
    assert n["AUTHORIZED"] == "NO"
    assert n["VERIFIED"] == "NO"


def test_reconcile_counts():
    inv = {
        "source_commit": "abc",
        "nodes": [
            {"path": "a.py", "exists": True, "type": "module", "status": "INSPECTED"},
            {"path": "b.py", "exists": False, "type": "module", "status": "UNABLE_TO_INSPECT"},
        ],
    }
    r = reconcile(inv)
    assert r["total"] == 2
    assert r["authorized_yes"] == 0
    assert r["not_inspected"] == 1
