"""JSON, HTML and FINAL_STATUS reporting."""

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


def write_html_report(reports_dir: Path, final_report: dict) -> Path:
    path = reports_dir / "final_report.html"
    claims = final_report.get("claims", FINAL_CLAIMS)
    comps = final_report.get("components", [])
    present = sum(1 for c in comps if c.get("status", {}).get("present"))
    sim = final_report.get("simulation", {})

    rows = "".join(
        f"<tr><td>{c.get('id')}</td><td>{c.get('display_name')}</td>"
        f"<td>{c.get('source_status')}</td>"
        f"<td>{'yes' if c.get('status',{}).get('present') else 'no'}</td></tr>"
        for c in comps
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>SWI Execution Report</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem; }}
h1,h2 {{ color: #222; }}
.ceiling {{ background: #fef3c7; border: 2px solid #d97706; padding: 1rem; margin: 1rem 0; }}
table {{ border-collapse: collapse; width: 100%; }}
td,th {{ border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; }}
th {{ background: #f3f4f6; }}
</style>
</head>
<body>
<h1>SWI EXECUTION REPORT</h1>
<div class="ceiling">
<strong>EXECUTION EVIDENCE — NOT PRODUCTION AUTHORIZATION</strong><br/>
SYSTEM COMPLETION: {claims.get('system_completion')}<br/>
PROVEN: {'YES' if claims.get('proven') else 'NO'}<br/>
SEALED: {'YES' if claims.get('sealed') else 'NO'}<br/>
PRODUCTION AUTHORIZED: {'YES' if claims.get('production_authorized') else 'NO'}
</div>

<h2>Run</h2>
<p>RUN_ID: {final_report.get('execution',{}).get('run_id')}<br/>
Platform: {final_report.get('execution',{}).get('platform')}<br/>
Runner: {final_report.get('execution',{}).get('runner_version')}</p>

<h2>Components</h2>
<p>Declared: {len(comps)} &nbsp; Present (filesystem evidence): {present}</p>
<table>
<tr><th>ID</th><th>Name</th><th>Source status</th><th>Present</th></tr>
{rows}
</table>

<h2>Simulation</h2>
<p>{sim.get('note', 'SIMULATION ≠ PROOF')}<br/>
Seed: {sim.get('seed')} &nbsp; Summary: {sim.get('summary')}</p>

<h2>Limitations</h2>
<ul>
{''.join(f'<li>{x}</li>' for x in final_report.get('limitations', []))}
</ul>

<p><em>BUILD/TEST/SIMULATION INFRASTRUCTURE ≠ SWI PROOF</em></p>
</body>
</html>"""
    path.write_text(html, encoding="utf-8")
    return path


def write_final_status(
    reports_dir: Path,
    ledger: EvidenceLedger,
    components: list | None = None,
    simulation: dict | None = None,
) -> Path:
    txt_path = reports_dir / "FINAL_STATUS.txt"

    materialized = sum(1 for r in ledger.repositories if r.get("status") == "MATERIALIZED")
    dirty = sum(1 for r in ledger.repositories if r.get("status") == "SOURCE_DIRTY")
    present = sum(1 for c in (components or []) if c.get("status", {}).get("present"))
    sim_summary = (simulation or {}).get("summary", {})

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
        "",
        "Components:",
        f"  Declared             : {len(components or [])}",
        f"  Present (evidence)   : {present}",
        "",
        "Simulation:",
        f"  Summary              : {sim_summary}",
        "  Note                 : SIMULATION ≠ PROOF",
        "",
        "Evidence:",
        "  Repository SHAs       : RECORDED (where materialized)",
        "  JSON / HTML reports   : GENERATED",
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
        "BUILD/TEST/SIMULATION INFRASTRUCTURE ≠ SWI PROOF",
        "",
    ]
    txt_path.write_text("\n".join(lines), encoding="utf-8")
    write_json_report(reports_dir, "FINAL_STATUS.json", ledger.to_dict())
    print("\n".join(lines))
    return txt_path
