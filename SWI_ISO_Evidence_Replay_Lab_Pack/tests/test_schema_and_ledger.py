"""Stage 1 acceptance: schema + serial + ledger. Fail closed."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from swi_iso_lab.schema_validator import validate_record, load_schema
from swi_iso_lab.serial_allocator import SerialAllocator
from swi_iso_lab.ledger import SerialLedger, LedgerEntry, LedgerError
from swi_iso_lab.record_builder import build_proof_record
from swi_iso_lab.status_model import LedgerMark, Scope, Outcome

SCHEMA = ROOT / "evidence" / "schema" / "swi_iso_proof_record_v1.schema.json"

@pytest.fixture
def schema():
    return load_schema(SCHEMA)

@pytest.fixture
def tmp_alloc(tmp_path):
    return SerialAllocator(tmp_path / "serial_state.json")

@pytest.fixture
def tmp_ledger(tmp_path):
    return SerialLedger(tmp_path / "ledger.jsonl")

def _valid_record(serial="SWI-ISO-ISO-IEC-42001-2023-20261031-000001", previous_hash=None):
    return build_proof_record(
        serial=serial,
        standard_id="ISO-IEC-42001-2023",
        run_id="RUN-TEST",
        outcome=Outcome.PASS.value,
        scope=Scope.SCHEMA_VALIDATION.value,
        repository_url="https://github.com/Kelronmos/SWI-V2-Modules-11-22",
        commit_sha="deadbeef",
        previous_hash=previous_hash,
        test_id="UNIT",
        record_type="SCHEMA_VALIDATION",
        schema_path=SCHEMA,
    )

def test_valid_record_passes(schema):
    rec = _valid_record()
    ok, errors = validate_record(rec, schema)
    assert ok, errors

def test_missing_required_field_rejected(schema):
    rec = _valid_record()
    del rec["serial"]
    ok, errors = validate_record(rec, schema)
    assert not ok

def test_invalid_field_type_rejected(schema):
    rec = _valid_record()
    rec["governance"] = "not-an-object"
    ok, errors = validate_record(rec, schema)
    assert not ok

def test_unknown_status_rejected(schema):
    rec = _valid_record()
    rec["outcome"] = "TOTALLY_UNKNOWN_STATUS"
    ok, errors = validate_record(rec, schema)
    assert not ok

def test_invalid_schema_version_rejected(schema):
    rec = _valid_record()
    rec["schema_version"] = "wrong_version"
    ok, errors = validate_record(rec, schema)
    assert not ok

def test_unique_serials(tmp_alloc):
    a = tmp_alloc.allocate("ISO-IEC-42001-2023")
    b = tmp_alloc.allocate("ISO-IEC-42001-2023")
    assert a.serial != b.serial
    assert b.sequence == a.sequence + 1

def test_monotonic_sequence(tmp_alloc):
    seqs = [tmp_alloc.allocate(f"STD-{i}").sequence for i in range(5)]
    assert seqs == sorted(seqs)
    assert len(set(seqs)) == 5

def test_duplicate_serial_rejected_on_ledger(tmp_ledger):
    e1 = LedgerEntry("S1", "r1", "h1", None, LedgerMark.ACTIVE.value, "run", "T")
    tmp_ledger.append(e1)
    e2 = LedgerEntry("S1", "r2", "h2", "h1", LedgerMark.ACTIVE.value, "run", "T")
    with pytest.raises(LedgerError):
        tmp_ledger.append(e2)

def test_broken_hash_link_rejected(tmp_ledger):
    e1 = LedgerEntry("S1", "r1", "h1", None, LedgerMark.ACTIVE.value, "run", "T")
    tmp_ledger.append(e1)
    e2 = LedgerEntry("S2", "r2", "h2", "WRONG", LedgerMark.ACTIVE.value, "run", "T")
    with pytest.raises(LedgerError):
        tmp_ledger.append(e2)

def test_chain_verify_pass(tmp_ledger):
    e1 = LedgerEntry("S1", "r1", "h1", None, LedgerMark.ACTIVE.value, "run", "T")
    tmp_ledger.append(e1)
    e2 = LedgerEntry("S2", "r2", "h2", "h1", LedgerMark.ACTIVE.value, "run", "T")
    tmp_ledger.append(e2)
    assert tmp_ledger.verify_chain()["ok"] is True

def test_historical_duplicate_mark_allowed(tmp_ledger):
    e1 = LedgerEntry("S1", "r1", "h1", None, LedgerMark.HISTORICAL_DUPLICATE.value, "run", "T", note="hist")
    tmp_ledger.append(e1)
    e2 = LedgerEntry("S1", "r2", "h2", "h1", LedgerMark.HISTORICAL_DUPLICATE.value, "run", "T", note="hist")
    tmp_ledger.append(e2)
    assert tmp_ledger.verify_chain()["ok"] is True
