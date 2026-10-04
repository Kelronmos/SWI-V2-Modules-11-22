"""Tests for SWI Trusted-Source Spine Inspector (fail-closed)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from swi_v2.trusted_source.spine_inspector import (
    FieldStatus,
    format_report,
    inspect_paths,
    inspect_record,
    main,
)

FIX = ROOT / "test" / "fixtures" / "trusted_source"


def _load(name: str) -> dict:
    return json.loads((FIX / name).read_text(encoding="utf-8"))


def test_valid_record_structural_pass():
    r = inspect_record(_load("valid_record.json"), path="valid")
    assert r.structural_green is True
    assert r.spine_break is False
    for stage in (
        "HEADER",
        "SOURCE",
        "PROVENANCE",
        "VERSION",
        "STATUS",
        "SCOPE",
        "JURISDICTION",
        "EVIDENCE",
        "BOUNDARY",
        "CLAIM",
    ):
        assert r.status_for(stage) == FieldStatus.PASS


def test_missing_fields_fail():
    r = inspect_record(_load("missing_fields.json"), path="missing")
    assert r.spine_break is True
    assert r.status_for("SOURCE") in (FieldStatus.FAIL, FieldStatus.UNKNOWN)
    assert r.status_for("PROVENANCE") == FieldStatus.FAIL
    assert r.status_for("JURISDICTION") == FieldStatus.FAIL
    assert r.structural_green is False


def test_unknown_values_never_pass():
    r = inspect_record(_load("unknown_values.json"), path="unknown")
    assert r.spine_break is True
    for stage in ("PROVENANCE", "VERSION", "STATUS", "SCOPE", "JURISDICTION", "EVIDENCE", "BOUNDARY"):
        assert r.status_for(stage) == FieldStatus.UNKNOWN
    assert r.structural_green is False


def test_conflict_standard_claiming_law():
    r = inspect_record(_load("conflict_standard_as_law.json"), path="conflict")
    assert r.spine_break is True
    assert r.status_for("CLAIM") == FieldStatus.CONFLICT
    assert "STANDARD != LAW" in " ".join(f.detail for f in r.findings)


def test_forbidden_api_as_authorization():
    r = inspect_record(_load("forbidden_api_authority.json"), path="forbidden")
    assert r.spine_break is True
    assert r.status_for("CLAIM") == FieldStatus.CONFLICT
    details = " ".join(f.detail for f in r.findings)
    assert "API != AUTHORIZATION" in details or "SOURCE != AUTHORIZATION" in details


def test_malformed_json_fail_closed():
    results = inspect_paths([FIX / "malformed.json"])
    assert len(results) == 1
    assert results[0].spine_break is True
    assert results[0].status_for("HEADER") == FieldStatus.FAIL


def test_format_report_halt_language():
    r = inspect_record(_load("missing_fields.json"), path="missing")
    text = format_report([r])
    assert "HALT" in text
    assert "AUTHORIZATION" in text
    assert "NO" in text


def test_format_report_structural_only_on_pass():
    r = inspect_record(_load("valid_record.json"), path="valid")
    text = format_report([r])
    assert "STRUCTURAL" in text
    assert "NOT PROVEN" in text or "AUTHORIZATION      NO" in text


def test_cli_nonzero_on_spine_break(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"swi_header": "x"}), encoding="utf-8")
    code = main([str(bad)])
    assert code == 1


def test_cli_zero_on_valid(tmp_path):
    good = tmp_path / "good.json"
    good.write_text((FIX / "valid_record.json").read_text(encoding="utf-8"), encoding="utf-8")
    code = main([str(good)])
    assert code == 0


def test_placeholder_evidence_record_structural():
    path = ROOT / "evidence" / "trusted_source_boundary_placeholder.json"
    if not path.exists():
        pytest.skip("placeholder not present")
    data = json.loads(path.read_text(encoding="utf-8"))
    r = inspect_record(data, path=str(path))
    assert r.structural_green is True
    assert data.get("production_authorized") is False


def test_never_upgrade_unknown_to_pass():
    rec = _load("unknown_values.json")
    r = inspect_record(rec)
    assert FieldStatus.PASS not in {
        r.status_for("PROVENANCE"),
        r.status_for("VERSION"),
        r.status_for("STATUS"),
    }
