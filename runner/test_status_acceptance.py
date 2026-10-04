"""
Acceptance tests: status engine must not manufacture certainty.

A01–A20 core matrix. Acceptance PASS ≠ SWI PRODUCTION READY.
"""
from __future__ import annotations

import json

from runner.status_engine import (
    YES, NO, UNKNOWN, CONFLICT, UNRESOLVED,
    resolve_status, repository_status_object, overall_swi_ceiling,
)


def test_a03_no_declaration_is_unknown():
    r = resolve_status(declared=None, observed=None)
    assert r.effective_status == UNKNOWN
    assert r.resolution == UNRESOLVED


def test_a01_explicit_false_is_no():
    r = resolve_status(declared=False, observed=False, evidence_present=True)
    assert r.effective_status == NO


def test_a08_conflict_declared_yes_observed_no():
    r = resolve_status(declared=True, observed=False, evidence_present=True)
    assert r.effective_status == CONFLICT
    assert r.resolution == UNRESOLVED
    assert r.declared_status == YES
    assert r.observed_status == NO


def test_a09_conflict_does_not_become_yes():
    r = resolve_status(declared=True, observed=False)
    assert r.effective_status != YES


def test_a10_conflict_does_not_silently_become_no():
    r = resolve_status(declared=True, observed=False)
    # effective is CONFLICT, not silent NO
    assert r.effective_status == CONFLICT


def test_a13_build_pass_does_not_imply_production_ready():
    obj = repository_status_object(
        "demo", "abc",
        declared={},
        observed={"tested": True},  # tests observed only
    )
    assert obj["production_ready"]["effective_status"] != YES


def test_a14_tests_pass_do_not_imply_production_ready():
    obj = repository_status_object(
        "demo", "abc",
        declared={},
        observed={"tested": True, "implemented": True},
    )
    assert obj["production_ready"]["effective_status"] != YES
    assert obj["proven"]["effective_status"] != YES


def test_a15_proven_does_not_imply_sealed():
    obj = repository_status_object(
        "demo", "abc",
        declared={"proven": True},
        observed={"proven": True},
    )
    assert obj["proven"]["effective_status"] == YES
    assert obj["sealed"]["effective_status"] != YES


def test_a16_sealed_does_not_imply_production_ready():
    obj = repository_status_object(
        "demo", "abc",
        declared={"sealed": True},
        observed={"sealed": True},
    )
    assert obj["sealed"]["effective_status"] == YES
    assert obj["production_ready"]["effective_status"] != YES


def test_a17_production_ready_does_not_imply_authorized():
    obj = repository_status_object(
        "demo", "abc",
        declared={"production_ready": True},
        observed={"production_ready": True},
    )
    assert obj["production_ready"]["effective_status"] == YES
    assert obj["production_authorized"]["effective_status"] != YES


def test_a18_boot_pass_does_not_imply_production_ready():
    ceiling = overall_swi_ceiling()
    assert ceiling["production_ready"] != YES
    assert ceiling["production_authorized"] == NO


def test_a19_unknown_authorization_stays_unknown_or_no():
    r = resolve_status(declared=None, observed=None)
    assert r.effective_status == UNKNOWN


def test_a20_conflict_authorization_stays_conflict():
    r = resolve_status(declared=True, observed=False)
    assert r.effective_status == CONFLICT


def test_conflict_survives_serialization():
    r = resolve_status(declared=True, observed=False)
    raw = json.dumps(r.to_dict())
    restored = json.loads(raw)
    assert restored["effective_status"] == CONFLICT
    assert restored["declared_status"] == YES
    assert restored["observed_status"] == NO


def test_unknown_survives_serialization():
    r = resolve_status()
    restored = json.loads(json.dumps(r.to_dict()))
    assert restored["effective_status"] == UNKNOWN
    assert restored["resolution"] == UNRESOLVED


def test_empty_fixture_all_unknown_or_no_ceiling():
    obj = repository_status_object("empty", None, declared={}, observed={})
    for key in ("proven", "sealed", "production_ready"):
        assert obj[key]["effective_status"] in (UNKNOWN, NO)
        assert obj[key]["effective_status"] != YES
