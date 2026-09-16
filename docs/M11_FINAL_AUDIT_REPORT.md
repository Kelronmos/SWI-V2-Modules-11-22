# M11 Final Audit Report

**Final decision: M11 NOT SEALED**

**Date:** 2026-09-16  
**Auditor:** automated evidence run (local clean path + Actions UI inspection)

## 1. Scope

Serialized V1 foundation evidence admission into V2 M11 under the frozen contract.  
Does **not** claim producer identity, CRTG, live V1↔V2 communication, or Foundation Seal 5.

## 2–3. Exact SHAs (frozen for this report)

| Repo | SHA |
|------|-----|
| V1 SWI-V1-Module-1-10 | `c09253a6a4832084f017e13411e125117a450178` |
| V2 SWI-V2-Modules-11-22 | `8c7a42fde0adac5aad46f9821f7769b39065fe79` |

## 4. Environment

| Item | Value |
|------|--------|
| Python (this run) | **3.12.3 only** |
| OS | Linux (audit host) |
| Clean dual-venv | **PENDING** (`python3-venv` unavailable on host; used isolated PYTHONPATH) |
| V1 tests | **140 passed** |
| V2 tests | **41 passed** |

## 5. Contract (Gate A)

Integrity covers: `payload`, `foundation_version`, `evidence_schema_version`, `evidence_id`, `source_reference`.  
`created_at` excluded — **PROVEN** (change created_at only → ADMITTED).

## 6. Gate B — Boundary

| Test | Result |
|------|--------|
| `PYTHONPATH=v2 only` → `import swi_core` | **PASS** (ModuleNotFoundError) |
| M10 as handoff | **PASS** (docs deny) |

## 7. Gate C — Real V1 producer

| Item | Value |
|------|--------|
| Command | `scripts/export_travel_evidence.py --out foundation_evidence.json` |
| evidence_id | `v1-two-checkout-travel-001` |
| verification_status | `v1_trainer_pipeline_completed` |
| foundation_version | `1.0-proposed` |
| File SHA-256 | `f44df8fe435376d940d44ee1ed7520145999afa067efc25d09e5482301b1eef3` |
| Size | 695 bytes |
| Result | **PROVEN** |

## 8–9. Gate D — Admission + adversarial

| Case | Expected | Actual |
|------|----------|--------|
| Valid V1 JSON | ACCEPT | **PASS** (ADMITTED) |
| Payload tamper | REJECT | **PASS** (IntegrityVerificationError) |
| Integrity field tamper | REJECT | **PASS** |
| Malformed JSON | REJECT | **PASS** |
| Missing `payload` | REJECT | **PASS** |
| Unsupported foundation_version | REJECT | **PASS** |
| Invalid verification_status | REJECT | **PASS** |
| created_at only change | ACCEPT | **PASS** |

Raw dict / PipelineResult / Kernel isolation: covered by V2 pytest (`test_kernel_isolation`, travel tests) — **TESTED** (41 passed).

## 10. Gate E — Kernel isolation

**TESTED** via suite (raw dict/string blocked; path via AdmittedInput only). Not re-logged step-by-step in this file beyond pytest green.

## 11. Gate F — Matrix & two-checkout CI

| Item | Result |
|------|--------|
| Python 3.12 local | **PASS** (pytest + travel scripts) |
| Python 3.10 | **NOT PROVEN** (this host) |
| Python 3.11 | **NOT PROVEN** (this host) |
| Tip-specific `two_checkout_travel` SUCCESS + logs for `8c7a42f` | **NOT PROVEN** |
| Historical runs on older SHAs | **NOT** current-tip verification |

Actions UI at audit time did not establish SUCCESS for tip `8c7a42f` with inspectable job logs.

## 12. Gate G — Documentation

Status docs state **NOT SEALED** / two-checkout not CI_VERIFIED — **consistent** with this decision.

## 13. Known limitations

- Admission ≠ identity / truth / trust  
- CI artifact transport ≠ live communication  
- Ed25519 primitive ≠ CRTG  
- Single-host Python 3.12 only for this report  

## 14. Failed / open gates

1. **Current-tip two-checkout CI_VERIFIED**  
2. **Python 3.10 and 3.11** reproducibility on this audit host  
3. Formal dual-venv isolation (ensurepip missing on host)

## 15. Final seal decision

```text
M11 NOT SEALED
```

Reason: mandatory Gate F items remain **NOT PROVEN**. Local adversarial and positive paths are strong but **insufficient alone** for seal under the manual.

## 16. Next action

1. Obtain tip-specific green `two_checkout_travel` with produce/admit logs + V1 SHA  
2. Confirm matrix 3.10–3.12 on CI  
3. Re-run A–G worksheet  
4. Only then write `M11_SEAL_RECORD.md` and set SEALED  
5. **No M12 implementation** until seal record exists  
