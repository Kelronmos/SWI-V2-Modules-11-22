"""Tip-bound S9 package manifest."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def build_manifest(
    *,
    source_repository: str,
    source_commit: str,
    report_id: str,
    report_status: str = "NOT_PROVEN",
    structure_scope: str = "repository_walk",
    evidence_scope: str = "action_supplied",
    test_scope: str = "harness_unit",
    authority_scope: str = "declarative_only",
    parent_report: Optional[str] = None,
) -> Dict[str, Any]:
    if not source_commit or len(source_commit) < 7:
        raise ValueError("source_commit required — refuse package without tip binding")
    m = {
        "report_id": report_id,
        "source_repository": source_repository,
        "source_commit": source_commit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "structure_scope": structure_scope,
        "evidence_scope": evidence_scope,
        "test_scope": test_scope,
        "authority_scope": authority_scope,
        "report_status": report_status,
        "parent_report": parent_report,
        "integrity_algorithm": "SHA-256",
        "s9_proven": False,
        "production_authorized": False,
        "equation": "Permit(a) ⇔ (∀ L,G,S,H : C(a) ⊆ L ∩ G ∩ S ∩ H) ∧ E(a) ≠ ∅",
    }
    m["s9_proven"] = False
    m["manifest_hash"] = hashlib.sha256(_canonical({k: v for k, v in m.items() if k != "manifest_hash"})).hexdigest()
    return m
