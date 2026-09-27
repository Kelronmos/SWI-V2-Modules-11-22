#!/usr/bin/env python3
"""
Stage-1 + Stage-2 demonstration of the CEK Alignment Monitor.

Produces:
  VECTOR → TARGET → DISTANCE → CLASSIFICATION

Then explicitly shows:

  CLASSIFICATION
        ↓
  NO AUTHORITY
        ↓
  NO EXECUTION

And the hidden-edge CEK observation proof.
"""

from __future__ import annotations

import sys

from .monitor import AlignmentMonitor
from .vector import AlignmentVector, VectorValidationError
from .visibility import VisibilityLevel


def run_stage1() -> None:
    print("=" * 60)
    print("STAGE 1 — Mathematical Measurement")
    print("=" * 60)

    monitor = AlignmentMonitor()

    cases = [
        ("Baseline (identical to target)", [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
        ("Small drift", [0.95, 0.95, 0.95, 0.95, 0.95, 0.95]),
        ("Moderate drift", [0.7, 0.7, 0.7, 0.7, 0.7, 0.7]),
        ("Large drift", [0.2, 0.2, 0.2, 0.2, 0.2, 0.2]),
    ]

    for label, coords in cases:
        m = monitor.measure(coords)
        print(f"\n--- {label} ---")
        print(f"  VECTOR         : {m.vector.as_tuple()}")
        print(f"  TARGET         : {m.target.as_tuple()}")
        print(f"  DISTANCE       : {m.distance:.6f}")
        print(f"  CLASSIFICATION : {m.classification.value}")
        print(f"  is_authoritative()   = {m.is_authoritative()}")
        print(f"  permits_execution()  = {m.permits_execution()}")

    print("\n--- Invalid vector (must fail-closed) ---")
    try:
        monitor.measure([0.5, 0.5, float("nan"), 0.5, 0.5, 0.5])
        print("  ERROR: NaN was accepted (should never happen)")
    except Exception as e:
        print(f"  Correctly rejected: {type(e).__name__}: {e}")

    print("\nCLASSIFICATION → NO AUTHORITY → NO EXECUTION  (demonstrated)")


def run_stage2() -> None:
    print("\n" + "=" * 60)
    print("STAGE 2 — CEK Observation + Hidden-Edge Demo")
    print("=" * 60)

    monitor = AlignmentMonitor()
    obs, finding, report = monitor.full_hidden_edge_observation()

    print("\nVisibility path:")
    for node in report.nodes:
        print(f"  {node.name:15} = {node.level.value:12}  ({node.reason})")

    print(f"\nFrontier          : {report.frontier}")
    print(f"Has unknown edge  : {report.has_unknown_edge}")
    print(f"Authority established : {report.authority_established}")
    print(f"obs.authority_established() : {obs.authority_established()}")
    print(f"obs.execution_permitted()   : {obs.execution_permitted()}")
    print(f"Finding visibility : {finding.visibility.value}")
    print(f"Finding reason     : {finding.reason}")
    print(f"Finding is_authoritative() : {finding.is_authoritative()}")

    print("\nExpected Stage-2 proof:")
    print("  ORIGIN / CONTEXT / EVIDENCE / ADMISSION  → VISIBLE / TRACEABLE")
    print("  NEXT_EDGE                               → UNKNOWN")
    print("  EXECUTION                               → OBSERVED")
    print("  AUTHORITY                               → NOT ESTABLISHED")
    print("  VISIBILITY FRONTIER                     → UNKNOWN EDGE")


def main() -> int:
    print("SWI-CEK Alignment Monitor — RESEARCH / EXPERIMENTAL")
    print("Production: NOT AUTHORIZED | Seal: NO | M11: UNTOUCHED")
    print()
    run_stage1()
    run_stage2()
    print("\n" + "=" * 60)
    print("Demo complete. No authority or execution path was exercised.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
