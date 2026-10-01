#!/usr/bin/env python3
"""Generate SWI execution-integrity + halt reports from actual runs."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from swi_v2.execution_integrity import (
    AdmittedRoute, Decision, ExecutionIntegrityGate, ExecutionRecord, IncomingNode,
)
from swi_v2.reports.test_report import TestReportBuilder, TestResultRecord, write_reports


def matching(admitted, t=10.0):
    return IncomingNode(
        node_id=admitted.node_id, workflow_id=admitted.workflow_id,
        route_hash=admitted.route_hash, input_hash=admitted.input_hash,
        policy_hash=admitted.policy_hash, admission_hash=admitted.admission_hash,
        current_time=t,
    )


def main() -> int:
    admitted = AdmittedRoute("W-104", "R-abc", "N-7", "I-1", "P-22", "A-9")
    last = ExecutionRecord("E-103", "W-104", "N-7", "R-abc", "I-1", 10.0)
    b = TestReportBuilder(report_type="execution_integrity", root=ROOT)
    b.set_command(
        "python3 scripts/generate_execution_integrity_report.py ; "
        "pytest -q test/adversarial/test_execution_integrity.py "
        "test/adversarial/test_universal_halt.py "
        "test/adversarial/test_gate_pass_fail_matrix.py"
    )

    def add(ok, **kw):
        kw["status"] = "PASS" if ok else "FAIL"
        b.add_test(TestResultRecord(**kw))

    g = ExecutionIntegrityGate(admitted, last)
    r = g.execute(matching(admitted))
    add(r.decision == Decision.EXECUTION_ALLOWED and g.execution_counter == 1,
        test_id="positive_valid", test_name="valid_bindings_execute", gate="Execution",
        module="execution_integrity", workflow_id="W-104", route_id="R-abc", node_id="N-7",
        expected_decision="EXECUTION_ALLOWED", actual_decision=r.decision.value,
        expected_execution_allowed=True, actual_execution_allowed=r.evidence.execution_allowed,
        expected_execution_occurred=True, actual_execution_occurred=r.execution_occurred,
        execution_counter=g.execution_counter, evidence_hash=r.evidence.evidence_hash)
    b.execution_results.append({"decision": r.decision.value, "counter": g.execution_counter})

    cases = [
        ("Admission", dict(admission_hash=None), "NOT_ADMITTED"),
        ("Node", dict(node_id="N-EVIL"), "NODE_MISMATCH"),
        ("Identity", dict(workflow_id="W-BAD"), "WORKFLOW_MISMATCH"),
        ("Route", dict(route_hash="R-NEW"), "ROUTE_CHANGED"),
        ("Input", dict(input_hash="I-NEW"), "INPUT_CHANGED"),
        ("Policy", dict(policy_hash="P-EVIL"), "POLICY_CHANGED"),
    ]
    for gate_name, mut, code in cases:
        gate = ExecutionIntegrityGate(admitted, last)
        node = matching(admitted)
        for k, v in mut.items():
            setattr(node, k, v)
        result = gate.check(node)
        ok = result.decision == Decision.HALT and gate.execution_counter == 0
        reason = result.reasons[0].value if result.reasons else None
        add(ok, test_id=f"fail_{gate_name.lower()}", test_name=f"{gate_name}_FAIL_halts",
            gate=gate_name, module="execution_integrity",
            expected_decision="HALT", actual_decision=result.decision.value,
            expected_execution_allowed=False, actual_execution_allowed=result.evidence.execution_allowed,
            expected_execution_occurred=False, actual_execution_occurred=result.execution_occurred,
            expected_reason_code=code, actual_reason_code=reason,
            execution_counter=gate.execution_counter, halted=True,
            evidence_hash=result.evidence.evidence_hash)
        b.halt_results.append(gate.to_halt_record(result).to_dict())

    g3 = ExecutionIntegrityGate(admitted, last)
    try:
        g3._demo_action(); bypass, actual = "FAIL", "EXECUTED"
    except PermissionError:
        bypass, actual = "PASS", "BLOCKED"
    add(bypass == "PASS", test_id="bypass_direct", test_name="direct_protected_operation_blocked",
        gate="Authorization", module="execution_integrity",
        expected_decision="HALT", actual_decision=actual,
        expected_execution_occurred=False, actual_execution_occurred=g3.execution_counter > 0,
        execution_counter=g3.execution_counter)
    b.bypass_results.append({"attack": "direct_demo_action", "result": bypass})

    g4 = ExecutionIntegrityGate(admitted, last, max_retries=2)
    node = matching(admitted); node.route_hash = "R-NEW"
    g4.check(node)
    r4 = g4.execute(node, attempt_retry=True)
    add(r4.decision == Decision.HALT and g4.execution_counter == 0,
        test_id="retry_no_auth", test_name="retry_without_revalidation_no_execution",
        gate="Retry", module="execution_integrity",
        expected_decision="HALT", actual_decision=r4.decision.value,
        expected_execution_occurred=False, actual_execution_occurred=r4.execution_occurred,
        execution_counter=g4.execution_counter, retry_attempted=True, halted=True)

    g5 = ExecutionIntegrityGate(admitted, last, max_retries=2)
    node = matching(admitted); node.route_hash = "R-NEW"
    g5.check(node); g5.check(node, attempt_retry=True)
    r5 = g5.check(node, attempt_retry=True)
    add(r5.decision == Decision.ESCALATE and g5.execution_counter == 0,
        test_id="escalate", test_name="persistent_failure_escalates",
        gate="Escalation", module="execution_integrity",
        expected_decision="ESCALATE", actual_decision=r5.decision.value,
        expected_execution_occurred=False, actual_execution_occurred=r5.execution_occurred,
        execution_counter=g5.execution_counter, escalated=r5.evidence.escalated)

    b.add_limitation("Library/gate scope; V2 kernel paths not fully wired to ExecutionIntegrityGate.")
    b.add_limitation("time_tolerance=0.0008 is experimental configuration only.")
    b.add_not_proven("Process-wide / production enforcement")
    b.add_not_proven("Universal / regulatory safety")

    paths = write_reports(b, ROOT / "reports" / "execution_integrity")
    hb = TestReportBuilder(report_type="halt", root=ROOT)
    hb.set_command(b.test_command)
    for t in b.tests:
        if t.halted or t.expected_decision in ("HALT", "ESCALATE"):
            hb.add_test(t)
    hb.halt_results = list(b.halt_results)
    hb.limitations = list(b.limitations)
    hb.not_proven = list(b.not_proven)
    hp = write_reports(hb, ROOT / "reports" / "halt")
    print("JSON_REPORT", paths["json"])
    print("MD_REPORT", paths["md"])
    print("REPORT_HASH", paths["sha256"].read_text().strip())
    print("HALT_JSON", hp["json"])
    print("SUMMARY", b.summary)
    return 1 if b.summary["failed"] or b.summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
