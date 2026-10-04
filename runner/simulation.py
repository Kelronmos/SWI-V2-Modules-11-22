"""Synthetic simulation stage — thin wrapper around cases generator."""

from __future__ import annotations

from typing import Any

from runner.cases import generate_cases, DEFAULT_SEED
from runner.evidence import EvidenceLedger


def run_simulation(
    case_count: int,
    packages: dict[str, Any],
    ledger: EvidenceLedger,
) -> dict[str, Any]:
    seed = (
        packages.get("test_matrix", {}).get("deterministic_seed")
        or DEFAULT_SEED
    )
    print(f"       Generating {case_count} synthetic cases (seed={seed})...")
    result = generate_cases(case_count, seed=seed)
    summary = result["summary"]
    print(f"       Simulation: {summary['pass']} PASS, {summary['fail']} FAIL")
    print("       NOTE: SIMULATION ≠ PROOF")
    return result
