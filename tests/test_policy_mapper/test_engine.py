import pytest
from swi_policy_mapper import Domain, State, Requirement, Board, evaluate

def req(d, state=State.SATISFIED, **kw):
    ev = kw.pop("evidence_refs",
                ("test:evidence",) if state == State.SATISFIED else ())
    return Requirement(
        "R-" + d.value, d, "Test requirement",
        state, evidence_refs=ev, **kw
    )

def complete():
    return [Board(d, (req(d),)) for d in Domain]

def test_complete_boards_never_issue_permit():
    x = evaluate(complete())
    assert x["status"] == "MATCH"
    assert x["permit"] == "NOT_ISSUED"
    assert x["execution"] == "NOT_PERFORMED"
    assert x["production_authorized"] is False

def test_weighted_score():
    d = Domain.POLICY
    a = Requirement("A", d, "A", State.SATISFIED,
                    weight=3, evidence_refs=("e1",))
    b = Requirement("B", d, "B", State.PARTIAL, weight=1)
    boards = [Board(d, (a,b))]
    boards += [Board(x,(req(x),)) for x in Domain if x != d]
    result = evaluate(boards)
    assert result["boards"]["POLICY"]["evidence_coverage_score"] == 87.5
    assert result["status"] == "BLOCKED"

def test_high_score_cannot_override_mandatory_unknown():
    d = Domain.POLICY
    items = [
        Requirement(str(i), d, "Satisfied", State.SATISFIED,
                    weight=100, evidence_refs=("e"+str(i),))
        for i in range(10)
    ]
    items.append(Requirement(
        "MUST", d, "Mandatory unknown", State.UNKNOWN,
        mandatory=True
    ))
    boards = [Board(d, tuple(items))]
    boards += [Board(x,(req(x),)) for x in Domain if x != d]
    result = evaluate(boards)
    assert result["status"] == "BLOCKED"
    assert "MUST" in result["boards"]["POLICY"]["mandatory_blockers"]

def test_satisfied_without_evidence_rejected():
    r = Requirement("X", Domain.POLICY, "X", State.SATISFIED)
    with pytest.raises(ValueError):
        r.validate()

def test_not_applicable_needs_evidence():
    r = Requirement("X", Domain.LAW, "X", State.NOT_APPLICABLE)
    with pytest.raises(ValueError):
        r.validate()

def test_cross_domain_rejected():
    r = req(Domain.LAW, State.UNKNOWN)
    with pytest.raises(ValueError):
        Board(Domain.POLICY, (r,)).validate()

def test_prohibition_denies():
    d = Domain.LAW
    r = Requirement("BAN", d, "Prohibition", State.FAILED,
                    evidence_refs=("law:section",),
                    prohibits_action=True)
    boards = [Board(x,(r,) if x == d else (req(x),)) for x in Domain]
    assert evaluate(boards)["status"] == "DENY"

def test_missing_board_blocks():
    result = evaluate(complete()[:3])
    assert result["status"] == "BLOCKED"
    assert result["permit"] == "NOT_ISSUED"

def test_duplicate_board_blocks():
    boards = complete()
    result = evaluate(boards + [boards[0]])
    assert result["status"] == "BLOCKED"

def test_unknown_blocks_match():
    boards = [Board(d,(req(d,State.UNKNOWN),)) for d in Domain]
    assert evaluate(boards)["status"] == "BLOCKED"

def test_all_na_not_assessed():
    boards = []
    for d in Domain:
        r = Requirement(
            "NA-"+d.value, d, "N/A", State.NOT_APPLICABLE,
            rationale="Scope review",
            na_evidence_ref="scope:evidence"
        )
        boards.append(Board(d,(r,)))
    assert evaluate(boards)["status"] == "NOT_ASSESSED"
