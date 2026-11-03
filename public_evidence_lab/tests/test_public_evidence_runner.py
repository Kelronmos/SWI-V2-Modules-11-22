"""Basic tests for the Public Evidence Lab trusted runner.

These tests verify claim boundaries and record structure.
They do not establish PROVEN, SEALED, or PRODUCTION_AUTHORIZED.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

# Allow running from repository root or public_evidence_lab/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runner.public_evidence_runner import make_record, export_artifacts


def test_claims_are_locked_false():
    record = make_record(startup_kind="manual")
    claims = record["claims"]
    assert claims["proven"] is False
    assert claims["sealed"] is False
    assert claims["independent_review_approved"] is False
    assert claims["production_authorized"] is False


def test_schema_and_run_id():
    record = make_record(startup_kind="first-start")
    assert record["schema"] == "swi.public-evidence-lab.run.v1"
    assert record["run_id"].startswith("LOCAL-")
    assert record["startup_kind"] == "first-start"
    assert "timestamp_utc" in record


def test_user_entered_sha_never_verified():
    record = make_record(startup_kind="manual", expected_commit="deadbeef" * 5)
    assert record["repository"]["user_entered_sha_treated_as_verified"] is False


def test_authorization_spine_not_verified():
    record = make_record()
    spine = next(c for c in record["checks"] if c["id"] == "AUTHORIZATION_SPINE")
    assert spine["pass"] is False


def test_export_produces_manifest(tmp_path):
    record = make_record(startup_kind="subsequent-start")
    manifest = export_artifacts(record, tmp_path)
    assert manifest["schema"] == "swi.public-evidence-lab.manifest.v1"
    formats = {a["format"] for a in manifest["artifacts"]}
    assert "json" in formats
    assert "txt" in formats
    assert "csv" in formats
    # Optional formats must not pretend to be generated
    for a in manifest["artifacts"]:
        if a["format"] in ("pdf", "xlsx", "jpg"):
            assert a["status"] == "NOT_GENERATED"


def test_canonical_hash_present():
    record = make_record()
    h = record["evidence_integrity"]["canonical_record_hash"]
    assert isinstance(h, str) and len(h) == 64
