SWI V2 — G1 BASELINE RECONCILIATION

Date: 2026-09-22
Status: RESEARCH / EXPERIMENTAL
Production: NOT AUTHORIZED
Seal: NOT AUTHORIZED

---

0. PURPOSE

Close Gate G1 of the 800-step controlled experimental path by reconciling
the documented tip identity with the actual repository HEAD.

This document does not rewrite history.
It records the discrepancy and the corrected baseline.

---

1. TIP IDENTITY RECONCILIATION

| Role | SHA | Classification |
|------|-----|----------------|
| Previous audited tip (recorded in CURRENT-TIP AUDIT manual) | 8a5c533b514c13eff575b6822d79f0889d8a5664 | HISTORICAL |
| Actual main HEAD at G1 reconstruction | 9dbdcbe92fe4058b15e94270477dffca584f22a3 | CURRENT |

The commit 9dbdcbe9 is documentation-only:

  docs: add CURRENT-TIP AUDIT & EVIDENCE RECONCILIATION MANUAL (2026-09-22)

Explicit statements in that commit:
- No runtime changes
- No seal changes
- Research / experimental only
- Production = NONE

Therefore:

  8a5c533b  = previous audited tip (CEK architecture freeze)
  9dbdcbe9  = current tip (audit manual added)

Both remain part of the evidence chain. Neither is erased.

---

2. TECHNICAL BASELINE EVIDENCE (on 9dbdcbe9)

| Proposition | Evidence | Classification |
|-------------|----------|----------------|
| Repository identity | Kelronmos/SWI-V2-Modules-11-22 | VERIFIED |
| Current main tip | 9dbdcbe92fe4058b15e94270477dffca584f22a3 | VERIFIED |
| Full V2 suite | 144 passed (reported CI) | CI-VERIFIED |
| Python 3.10 / 3.11 / 3.12 | Repository Verification passed | CI-VERIFIED |
| pre-R suite | 35 passed | CI-VERIFIED / LOCALLY REPRODUCED |
| V1 → V2 travel + tamper rejection | Successful (reported CI) | CI-VERIFIED |
| PR-009 protected-path tests | 35 passed locally on tip | TESTED |
| Distributed-node containment | 6 passed (simulation package) | TESTED |
| CEK runtime implementation | Explicitly absent | NOT IMPLEMENTED |
| Universal / process / OS enforcement | No proof | NOT PROVEN |
| PR-009 seal | None | NOT SEALED |
| Production authorization | None | NOT AUTHORIZED |
| M11 | Sealed historical record; unchanged by 9dbdcbe9 | SEALED (historical) |

Local reproduction (2026-09-22):

  tests/pre_r/test_pr009_enforcement.py + test_response_boundary.py
  → 35 passed

  tests/pre_r/test_distributed_node_containment.py (attachment package)
  → 6 passed

---

3. ARTIFACT HASHES (baseline)

| Artifact | SHA-256 |
|----------|--------|
| experimental/response_boundary/enforcement.py | bc250b09efff904b9743ac8b29ccd15bbb1b9b02c646b7699bb98bfa717e99a8 |
| experimental/response_boundary/core.py | c420f01951d4e06b9e7404a647f4eb8a2b2f78756d81d8504bd1db1b02af8dfc |
| tests/pre_r/test_pr009_enforcement.py | 4134b4d0fde8880f4b21107d1c21a41978766c28548d480d9abcf5ad06dbdf3e |
| docs/CURRENT_TIP_AUDIT_AND_EVIDENCE_RECONCILIATION_MANUAL.md | 0d95658dbefc50e309f1eac85c9fb5e152d990774e98fa7c525e042c03ccee4f |
| experimental/distributed_node/node.py (attachment) | b55e23d241b945ebe9776e35e3c7f71dc5c0d607f635eef99adb745a71a6ade8 |
| tests/pre_r/test_distributed_node_containment.py (attachment) | 4d5ff0175fe14787ae64eefd22e6acd6b817af741267c87e3382103c10270418 |
| cek_live_path_monitor_simulation.csv (attachment) | 52dfc21d20850295f140eed498e00d69d6f0d20eeec5f263fdb1fd6a1f9f71a2 |

---

4. KNOWN LIMITATIONS (unchanged)

- Universal / arbitrary-caller / process-wide / OS-wide enforcement = NOT PROVEN
- Distributed-node package = logical simulation only (no real network/OS isolation)
- CEK = architecture freeze + simulation; no runtime authority grant
- authorized= fixture still present in node package (Phase 3 target)
- Production = NOT AUTHORIZED
- Seal (for new work) = NOT AUTHORIZED

---

5. DEMONSTRATED GAP THAT THIS RECONCILIATION CLOSES

BEFORE:

  CURRENT-TIP AUDIT DOCUMENT claimed tip 8a5c533b
  ACTUAL main HEAD                = 9dbdcbe9

  CURRENT REPOSITORY ≠ CURRENT-TIP AUDIT DOCUMENT

AFTER:

  Previous audited tip preserved as HISTORICAL (8a5c533b)
  Current tip recorded as         9dbdcbe9
  Discrepancy itself is evidence

No runtime code was written to “fix” the discrepancy.
Documentation was reconciled to reality.

---

6. G1 DECISION

Gate G1 is CLOSED.

Baseline is internally consistent:

  CURRENT TIP IDENTIFIED
        ↓
  9dbdcbe92fe4058b15e94270477dffca584f22a3
        ↓
  CI + local test evidence exists on that tip
        ↓
  Limitations recorded
        ↓
  Historical tip preserved

Phase 2 (Steps 051–100 — Exact Next-Path Engine) is now unblocked.

---

7. EXPLICIT NON-CLAIMS

Closing G1 does not:

- reseal M11
- implement CEK runtime
- prove universal enforcement
- authorize production use
- convert TESTED into SEALED
- convert MATCHED TRANSITION into AUTHORIZED ACTION

---

8. NEXT CONTROLLED ACTION

G1 CLOSED
  ↓
051–100 UNBLOCKED
  ↓
EXACT NEXT-PATH ENGINE (observational only)
  ↓
J-01 … J-15
  ↓
G2 evidence package

Implementation of the Exact Next-Path Engine remains EXPERIMENTAL,
NOT SEALED, NOT PRODUCTION AUTHORIZED.

End of G1 reconciliation record.
