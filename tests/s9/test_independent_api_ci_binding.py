"""Independent S9 API, authority-boundary and package-integrity checks.

These tests do not claim mathematical proof or production authorization.
"""
from __future__ import annotations

import hashlib
import importlib
import inspect
import json
import zipfile
from pathlib import Path

from swi_v2 import s9
from swi_v2.s9 import evaluate_s9
from swi_v2.s9.package import build_package


def valid_action(**changes):
    action = {
        "action_id": "INDEPENDENT-S9-API-001",
        "claim_id": "INDEPENDENT-CLAIM-001",
        "constraints": ["C1"],
        "law": ["C1"],
        "governance": ["C1"],
        "security": ["C1"],
        "human": ["C1"],
        "evidence": [{
            "evidence_id": "E1",
            "exists": True,
            "relevance": "PASS",
            "freshness": "PASS",
            "scope": "PASS",
            "provenance": "PASS",
            "integrity": "PASS",
        }],
        "dependencies": [],
        "unknown_conditions": [],
        "authority": {"required": False, "present": False},
    }
    action.update(changes)
    return action


def test_public_s9_api_exports_are_importable():
    expected = {
        "evaluate_s9",
        "EvaluationResult",
        "build_package",
        "PackageRefused",
        "build_manifest",
    }
    assert expected.issubset(set(s9.__all__))
    assert callable(s9.evaluate_s9)
    assert callable(s9.build_package)
    assert callable(s9.build_manifest)
    assert inspect.signature(evaluate_s9)


def test_valid_case_is_not_authorization():
    result = evaluate_s9(valid_action())
    assert result.system_result == "SATISFIED"
    assert result.promotion_eligible is False
    assert result.to_dict()["promotion_eligible"] is False


def test_unknown_condition_never_becomes_pass():
    result = evaluate_s9(
        valid_action(unknown_conditions=["UNRESOLVED-INPUT"])
    )
    assert result.system_result == "UNRESOLVED"
    assert result.promotion_eligible is False


def test_missing_human_layer_blocks():
    result = evaluate_s9(valid_action(human=[]))
    assert result.human == "MISSING"
    assert result.system_result == "BLOCKED"


def test_missing_evidence_blocks():
    result = evaluate_s9(valid_action(evidence=[]))
    assert result.evidence_exists is False
    assert result.evidence_adequacy_result == "BLOCKED"
    assert result.system_result == "BLOCKED"


def test_unresolved_evidence_dimensions_block():
    evidence = [{
        "evidence_id": "E-UNKNOWN",
        "exists": True,
    }]
    result = evaluate_s9(valid_action(evidence=evidence))
    assert result.evidence_exists is True
    assert result.evidence_adequate is False
    assert result.system_result == "BLOCKED"


def test_mismatched_constraint_is_blocked():
    result = evaluate_s9(
        valid_action(
            constraints=["C1", "C2"],
            law=["C1"],
            governance=["C1"],
            security=["C1"],
            human=["C1"],
        )
    )
    assert result.constraint_coverage is False
    assert result.system_result == "BLOCKED"


def test_required_authority_absence_blocks():
    result = evaluate_s9(
        valid_action(authority={
            "required": True,
            "present": False,
            "signature": "NOT-AUTHORITY",
        })
    )
    assert result.system_result == "BLOCKED"
    assert result.promotion_eligible is False


def test_replay_is_only_in_process_equivalence():
    from swi_v2.s9.replay import replay_evaluate

    action = valid_action()
    original = evaluate_s9(action).to_dict()
    replay = replay_evaluate(action, original)

    assert replay["equivalent"] is True
    assert replay["replay_scope"] == "in-process pure function only"
    assert replay["DURABLE_REPLAY"] == "NOT IMPLEMENTED"


def test_binding_runtime_absence_is_explicit_gap():
    """A passing absence check is NOT a passing binding implementation test."""
    root = Path(s9.__file__).resolve().parent

    assert not (root / "binding.py").exists()
    assert not (root / "api.py").exists()

    exposed = set(s9.__all__)
    assert not exposed.intersection({
        "bind_runtime",
        "resolve_binding",
        "authorize",
        "execute",
    })


def test_package_zip_manifest_and_hashes_are_verifiable(tmp_path):
    root = Path(__file__).resolve().parents[2]
    import subprocess

    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
    ).strip()

    result = build_package(
        repo_root=root,
        source_commit=commit,
        action=valid_action(),
        out_dir=tmp_path / "package",
        report_id="S9-INDEPENDENT-" + commit[:12],
    )

    archive = Path(result["zip_path"])
    assert archive.is_file()
    assert result["source_commit"] == commit
    assert result["s9_proven"] is False
    assert result["production_authorized"] is False

    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())

        manifest_path = "S9/00_MANIFEST.json"
        report_path = "S9/12_REPORT/S9_AUDIT_REPORT.json"
        hashes_path = "S9/11_INTEGRITY/hashes.json"

        assert {manifest_path, report_path, hashes_path}.issubset(names)

        manifest = json.loads(zf.read(manifest_path))
        report = json.loads(zf.read(report_path))
        hashes = json.loads(zf.read(hashes_path))

        assert manifest["source_commit"] == commit
        assert manifest["s9_proven"] is False
        assert manifest["production_authorized"] is False

        canonical = {
            k: v for k, v in manifest.items()
            if k != "manifest_hash"
        }
        encoded = json.dumps(
            canonical,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

        assert hashlib.sha256(encoded).hexdigest() == manifest["manifest_hash"]

        assert report["s9_proven"] is False
        assert report["production_authorized"] is False
        assert report["DURABLE_REPLAY"] == "NOT IMPLEMENTED"

        for rel, expected_hash in hashes.items():
            member = "S9/" + rel
            assert member in names
            actual = hashlib.sha256(zf.read(member)).hexdigest()
            assert actual == expected_hash
