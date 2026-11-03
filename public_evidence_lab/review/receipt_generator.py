#!/usr/bin/env python3
"""
SWI Public Evidence Lab — Review Receipt Generator (stub)

Produces an immutable receipt structure conforming to
swi.public-evidence-lab.review-receipt.v1.

Rules:
- Never invents reviewer identity or admission.
- Never sets proven / sealed / production_authorized to True.
- Failed or missing stages remain visible.
- Author self-review is rejected.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

SCHEMA = "swi.public-evidence-lab.review-receipt.v1"
ALLOWED_STATES = {
    "REVIEW_SUBMITTED",
    "SOURCE_VERIFIED",
    "VERSION_MATCHED",
    "EVIDENCE_VALIDATED",
    "REPRODUCED",
    "REVIEW_ADMITTED",
    "REJECTED",
    "WITHDRAWN",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def new_receipt_id() -> str:
    return f"RCPT-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:10]}"


def build_receipt(
    *,
    position: int,
    state: str,
    reviewed_commit: Optional[str] = None,
    run_id: Optional[str] = None,
    reviewer_id: Optional[str] = None,
    display_name: Optional[str] = None,
    institution: Optional[str] = None,
    evidence_refs: Optional[List[Dict[str, Any]]] = None,
    stage_results: Optional[Dict[str, Dict[str, Any]]] = None,
    independent_review_approved: bool = False,
    extra_limitations: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a receipt dict. Does not write to disk and does not update the registry."""
    if position < 1 or position > 5:
        raise ValueError("position must be 1..5")
    if state not in ALLOWED_STATES:
        raise ValueError(f"state must be one of {sorted(ALLOWED_STATES)}")

    # Hard lock: admission of a review never elevates these claims
    claims = {
        "proven": False,
        "sealed": False,
        "production_authorized": False,
        "independent_review_approved": bool(independent_review_approved),
    }

    limitations = [
        "Receipt generation does not constitute independent review completion.",
        "Admission of a review does not set PROVEN, SEALED, or PRODUCTION_AUTHORIZED.",
        "Author of the implementation cannot self-review.",
        "Missing or failed stages remain visible in stage_results.",
    ]
    if extra_limitations:
        limitations.extend(extra_limitations)

    receipt = {
        "schema": SCHEMA,
        "receipt_id": new_receipt_id(),
        "position": position,
        "state": state,
        "reviewer": {
            "reviewer_id": reviewer_id,
            "display_name": display_name,
            "institution": institution,
        },
        "reviewed_commit": reviewed_commit,
        "run_id": run_id,
        "evidence_refs": evidence_refs or [],
        "stage_results": stage_results or {},
        "generated_utc": utc_now(),
        "claims": claims,
        "limitations": limitations,
    }
    return receipt


def write_receipt(receipt: Dict[str, Any], out_dir: Path) -> Path:
    """Write receipt JSON and return path. Directory created if needed."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{receipt['receipt_id']}.json"
    data = json.dumps(receipt, indent=2, sort_keys=False).encode("utf-8")
    path.write_bytes(data)
    return path


def receipt_sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    """CLI stub: emit an empty-position placeholder receipt for inspection only."""
    import argparse

    parser = argparse.ArgumentParser(description="SWI Public Evidence Lab receipt generator (stub)")
    parser.add_argument("--position", type=int, default=1, choices=range(1, 6))
    parser.add_argument("--state", default="REVIEW_SUBMITTED", choices=sorted(ALLOWED_STATES))
    parser.add_argument("--out-dir", default="receipts")
    parser.add_argument("--commit", default=None, help="Reviewed commit SHA (optional, unverified here)")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()

    receipt = build_receipt(
        position=args.position,
        state=args.state,
        reviewed_commit=args.commit,
        run_id=args.run_id,
        stage_results={
            "SOURCE_VERIFIED": {"status": "NOT_RUN", "detail": "Stub only"},
            "VERSION_MATCHED": {"status": "NOT_RUN", "detail": "Stub only"},
            "EVIDENCE_VALIDATED": {"status": "NOT_RUN", "detail": "Stub only"},
            "REPRODUCED": {"status": "NOT_RUN", "detail": "Stub only"},
        },
        independent_review_approved=False,
        extra_limitations=["This invocation is a generation stub; no real review was performed."],
    )

    out = Path(args.out_dir)
    path = write_receipt(receipt, out)
    digest = receipt_sha256(path)

    print(json.dumps({
        "receipt_id": receipt["receipt_id"],
        "path": str(path),
        "sha256": digest,
        "state": receipt["state"],
        "claims": receipt["claims"],
        "note": "Stub only — no reviewer admitted, no claims elevated",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
