"""Build and validate proof records before admission to ledger."""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from .schema_validator import assert_valid, load_schema
from .status_model import GOVERNANCE_DEFAULTS
from .ledger import sha256_hex, canonical_bytes

SCHEMA_ID = "swi_iso_proof_record_v1.schema.json"
SCHEMA_VERSION = "swi_iso_proof_record_v1"

def schema_digest(schema_path: Path) -> str:
    return sha256_hex(schema_path.read_bytes())

def build_proof_record(
    *,
    serial: str,
    standard_id: str,
    run_id: str,
    outcome: str,
    scope: str,
    repository_url: str,
    commit_sha: Optional[str],
    previous_hash: Optional[str],
    test_id: Optional[str] = None,
    record_type: str = "KERNEL_TEST",
    limitations: Optional[list] = None,
    detail: Optional[str] = None,
    schema_path: Optional[Path] = None,
) -> Dict[str, Any]:
    record: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "schema_id": SCHEMA_ID,
        "record_id": f"REC-{uuid.uuid4().hex}",
        "record_type": record_type,
        "serial": serial,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "standard_id": standard_id,
        "run_id": run_id,
        "test_id": test_id,
        "outcome": outcome,
        "scope": scope,
        "repository_url": repository_url,
        "commit_sha": commit_sha,
        "previous_hash": previous_hash,
        "limitations": list(limitations or []),
        "governance": dict(GOVERNANCE_DEFAULTS),
        "detail": detail,
    }
    body = {k: v for k, v in record.items()}
    record["content_sha256"] = sha256_hex(canonical_bytes(body))
    if schema_path and schema_path.is_file():
        record["schema_digest"] = schema_digest(schema_path)
        assert_valid(record, load_schema(schema_path))
    return record
