from pathlib import Path
import subprocess
import sys
import json
import datetime

root = Path(__file__).resolve().parents[1]
package = root / "snyder_runtime_v1_audit"
head = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=root, text=True
).strip()

targets = [
    "snyder_runtime_v1_audit/tests/test_snyder_critical.py",
    "tests/s9",
    "tests/law",
    "tests/pre_r",
    "tests/cek_alignment_monitor",
    "test/test_authority_non_escalation.py",
    "test/test_kernel_isolation.py",
    "test/test_kernel_enforcement.py",
]
targets = [x for x in targets if (root / x).exists()]

report = package / "reports" / head
report.mkdir(parents=True, exist_ok=True)

print("BASELINE_HEAD=" + head)
print("TEST_TARGETS=" + str(targets))

command = [
    sys.executable, "-m", "pytest", "-q",
    "--junitxml=" + str(report / "junit.xml")
] + targets

start = datetime.datetime.now(datetime.timezone.utc).isoformat()
result = subprocess.run(
    command, cwd=root, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT
)
end = datetime.datetime.now(datetime.timezone.utc).isoformat()

(report / "pytest_output.txt").write_text(result.stdout)

after = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=root, text=True
).strip()

data = {
    "programme": "Snyder Runtime v1.0 Integrated Critical Audit",
    "baseline_head": head,
    "head_after": after,
    "baseline_unchanged": head == after,
    "started_utc": start,
    "finished_utc": end,
    "targets": targets,
    "pytest_exit_code": result.returncode,
    "execution_result": "PASS" if result.returncode == 0 else "FAIL",
    "proven": False,
    "sealed": False,
    "production_authorized": False
}

(report / "FINAL_REPORT.json").write_text(
    json.dumps(data, indent=2) + "\n"
)

summary = [
    "# Snyder Runtime v1.0 Integrated Critical Audit",
    "",
    "Baseline: `" + head + "`",
    "HEAD after run: `" + after + "`",
    "Execution: **" + data["execution_result"] + "**",
    "Baseline unchanged: **" + str(head == after) + "**",
    "Pytest exit code: `" + str(result.returncode) + "`",
    "",
    "PROVEN: **NO**",
    "SEALED: **NO**",
    "PRODUCTION AUTHORIZED: **NO**",
    "",
    "See `pytest_output.txt` and `junit.xml` for test evidence."
]
(report / "FINAL_REPORT.md").write_text("\n".join(summary) + "\n")

print(result.stdout)
print("REPORT=" + str(report))
print("BASELINE_UNCHANGED=" + str(head == after))
print("PROVEN=NO")
print("SEALED=NO")
print("PRODUCTION_AUTHORIZED=NO")

sys.exit(result.returncode)
