from swi_v2.s9.evaluator import evaluate_s9
from swi_v2.s9.replay import replay_evaluate


def test_replay_equivalent_blocked():
    action = {
        "action_id": "A",
        "constraints": ["c1"],
        "law": [],
        "governance": [],
        "security": [],
        "human": [],
        "evidence": [],
    }
    orig = evaluate_s9(action).to_dict()
    rep = replay_evaluate(action, orig)
    assert rep["equivalent"] is True
    assert rep["DURABLE_REPLAY"] == "NOT IMPLEMENTED"
