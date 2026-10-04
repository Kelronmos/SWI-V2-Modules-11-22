"""JSON and FINAL_STATUS reporting."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runner.evidence import EvidenceLedger, FINAL_CLAIMS


def write_json_report(reports_dir: Path, filename: str, data: Any) -> Path:
    path = reports_dir / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    return path


def write_final_status(reports_dir: Path, ledger: EvidenceLedger) -> Path:
    """Write FINAL_STATUS.txt and FINAL_STATUS.json with locked claims."""
    txt_path = reports_dir / "FINAL_STATUS.txt"
    json_path = reports_dir / "FINAL_STATUS.json"

    materialized = sum(
        1 for r in ledger.repositories if r.get("status") == "MATERIALIZED"
    )
    dirty = sum(1 for r in ledger.repositories if r.get("status") == "SOURCE_DIRTY")
    failed = sum(
        1 for r in ledger.repositories if r.get("status") in ("FAIL", "SOURCE_MISSING")
    )

    lines = [
        "=" * 60,
        "SWI UNIVERSAL TEST COMPLETE",
        "=" * 60,
        "",
        f"RUN_ID                 : {ledger.run_id}",
        f"Runner version         : {ledger.runner_version}",
        "",
        "Repositories:",
        f"  Declared             : {len(ledger.repositories)}",
        f"  Materialized         : {materialized}",
        f"  SOURCE_DIRTY         : {dirty}",
        f"  Failed / Missing     : {failed}",
        "",
        "Build / Test results are recorded in:",
        "  BUILD_RESULTS.json",
        "  TEST_RESULTS.json",
        "",
        "Firefly / 8K cases:",
        "  (engines not yet implemented — NOT_RUN)",
        "",
        "Evidence:",
        "  Repository SHAs       : RECORDED (where materialized)",
        "  JSON reports          : GENERATED",
        "",
        "=" * 60,
        "",
        f"SYSTEM COMPLETION      : {FINAL_CLAIMS['system_completion']}",
        f"PROVEN                 : {'YES' if FINAL_CLAIMS['proven'] else 'NO'}",
        f"SEALED                 : {'YES' if FINAL_CLAIMS['sealed'] else 'NO'}",
        f"PRODUCTION AUTHORIZED  : {FINAL_CLAIMS['production_authorized_str']}",
        "",
        f"production_authorized  = {str(FINAL_CLAIMS['production_authorized']).lower()}",
        "",
        "=" * 60,
        "",
        "NOTE: Successful builds/tests do not upgrade evidence claims.",
        "      BUILD/TEST INFRASTRUCTURE ≠ SWI PROOF",
        "",
    ]

    txt_path.write_text("\n".join(lines), encoding="utf-8")
    write_json_report(reports_dir, "FINAL_STATUS.json", ledger.to_dict())

    print("\n".join(lines))

    return txt_path
