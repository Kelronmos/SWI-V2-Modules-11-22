# M11 Seal Audit Worksheet — Filled from Direct Execution

Status: **AUDIT PARTIAL — STILL NOT SEALED**

Method: both repos extracted from the zips uploaded on 2026-09-16, run in two
separate, freshly-created Python 3.12.3 virtualenvs (`venv_v1` with V1's
`requirements.txt` installed, `venv_v2` with only V2's `requirements.txt`
installed — no cross-installation). Every row below reflects something
actually executed in this session, not a restatement of the repo's own docs.
Rows I could not execute myself (GitHub Actions runs, the 3.10/3.11 leg of
the matrix, git commit SHAs — the zip download has no `.git` history) are
marked PENDING / NOT INDEPENDENTLY VERIFIED rather than assumed.

---

## A — Contract Freeze

| Requirement | Evidence | Result | Reviewer note |
|---|---|---|---|
| V1 Foundation Evidence Contract is frozen | `swi_core/foundation_evidence.py`, `docs/V1_FOUNDATION_CONTRACT.md` present and internally consistent with V2's `swi_v2/kernel/admission.py` field expectations | PASS | Consistency confirmed by successful cross-repo admission below, not by reading the doc alone |
| No contract-breaking change since freeze | N/A — single snapshot audited | NOT ASSESSABLE | Would need two commits over time to check; only one snapshot available |

## B — Architectural Boundary

| Requirement | Evidence | Result | Reviewer note |
|---|---|---|---|
| V2 does not import V1 code at runtime | `venv_v2` built from V2's `requirements.txt` only; `import swi_core` raises `ModuleNotFoundError: No module named 'swi_core'` | **PASS** | Executed directly this session |
| M11 admits only serialized evidence, never a live object | `scripts/admit_travel_evidence.py` reads JSON from disk and calls `admit_foundation_input(dict)` | PASS | Confirmed by reading `swi_v2/kernel/admission.py` and the script |

## C — Real Producer

| Requirement | Evidence | Result | Reviewer note |
|---|---|---|---|
| Real V1 producer runs and exports evidence | `venv_v1/bin/python scripts/export_travel_evidence.py --out foundation_evidence.json` | **PASS** | Ran for real; produced actual JSON, not a stub |
| Artifact filename recorded | `foundation_evidence.json` | PASS | |
| SHA-256 recorded (generated, not typed) | `6325e9385eaab4a91f389c347b30fe0b874712cebe660c89a5c97ef72a932849` | **PASS** | Computed via `sha256sum` on the real file this session |

## D — Admission Behaviour

| Requirement | Result | Evidence |
|---|---|---|
| Positive: real evidence → ACCEPT → `AdmittedInput` | **PASS** | `ADMITTED evidence_id=v1-two-checkout-travel-001 by=module_11_foundation_admission integrity=92c6219963cee179...` exit 0 |
| Payload tampered, integrity ref unchanged → REJECT | **PASS** | `IntegrityVerificationError: integrity_reference does not match computed foundation evidence digest`, exit 1 |
| Integrity ref tampered, payload unchanged → REJECT | **PASS** | Same error class, different fixture, exit 1 — confirms both tamper paths are independently checked, not one shared check |
| Malformed JSON → REJECT | **PASS** | `REJECT invalid JSON: Expecting property name...`, exit 2 |
| Missing `payload` / `foundation_version` / `evidence_schema_version` / `evidence_id` / `source_reference` → REJECT | **PASS (5/5)** | Each produced `InvalidFoundationEvidence: missing required evidence fields: [...]` naming the specific missing field, exit 1 |
| Unsupported `foundation_version` → REJECT | **PASS** | `UnsupportedFoundationVersion: unsupported foundation_version: '9.9-bogus'` |
| Unsupported `evidence_schema_version` → REJECT | **PASS** | `UnsupportedFoundationVersion: unsupported evidence_schema_version: '9.9-bogus'` |
| Unsupported `verification_status` → REJECT | **PASS** | `InvalidFoundationEvidence: verification_status not acceptable for current V2 build: 'bogus_status'` |
| Raw dict (wrong shape) → REJECT | **PASS** | Lists all 7 missing required fields |
| `PipelineResult`-shaped object → REJECT | **PASS** | Same rejection class as raw dict |

14/14 admission-layer fixtures behaved as specified, each with a distinct, legible error rather than a generic failure.

## E — Kernel Isolation

| Requirement | Result | Evidence |
|---|---|---|
| `AdmittedInput` → Kernel succeeds | **PASS** | `test_module12_accepts_only_after_m11` passes in the real suite; module12's `process()` returns `accepted_placeholder` only given a real `AdmittedInput` |
| Raw dict → Kernel fails | **PASS** | `test_module12_rejects_raw_dict` — `module12_process(_valid_envelope())` (a plain dict, not run through M11) raises `ModuleKernelError` |
| Rejected M11 input → Kernel fails | **PASS** (by construction) | `require_admitted` raises before a rejected input can reach `module12.process` — confirmed by reading `swi_v2/kernel/enforcement.py` |
| V1 import unavailable in V2 env, no `sys.path`/`PYTHONPATH` manipulation | **PASS** | `venv_v2` has V1 nowhere on disk; `sys.path` printed and contains only the venv's own site-packages — the absence is structural, not scripted |

## F — Reproducibility

| Requirement | Result | Evidence |
|---|---|---|
| Two-checkout flow (real V1 export → separate-env V2 admission) reproduces locally | **PASS** | Executed exactly this way this session, not merely re-reading the repo's CI logs |
| GitHub Actions `two_checkout_travel.yml` green on tip | **NOT INDEPENDENTLY VERIFIED** | Repo's own `docs/MODULE_STATUS.md` cites run `34987307390`, V2 `061a47f`, V1 `be31dd7` — I cannot reach GitHub Actions or confirm commit SHAs from a `.git`-less zip export; this is their claim, not something I re-ran |
| Python 3.10 | **PENDING** | Only 3.12 is available in this environment |
| Python 3.11 | **PENDING** | Same limitation |
| Python 3.12 | **PASS** | V1: 140/140 tests passed. V2: 41/41 tests passed, in the isolated venv |

## G — Documentation Honesty

| Requirement | Result | Evidence |
|---|---|---|
| Sweep for high-risk claim language (complete/secure/verified/sealed/production-ready/universal/safe/identity/truth/CRTG/Foundation Seal 5) | **PASS, with one structural caveat** | Ran an automated sweep across all 30 doc files. After filtering definitions, headers, checklist templates, and negations, the remaining hits are either (a) the same already-disclosed `CI_VERIFIED`/`TESTED-NOT-SEALED`/`BLOCKED` status repeated across docs, or (b) explicit "Do not say: X" / "It must NOT say: X" anti-pattern examples where the prohibition sits on the line *above* the quoted bad example — which a naive line-by-line scan flags as if it were an unguarded claim. Manually checked several of these (e.g. "SWI V2 is safe.", "Verified because tests passed locally.") and confirmed by context that they are illustrations of forbidden phrasing, not live claims. |
| No claim exceeds what this worksheet demonstrates | **PASS for README/MODULE_STATUS.md** | Both state exactly `TESTED / NOT SEALED` and `BLOCKED` for M12–22, matching what the code actually contains (module12 is a type-boundary stub, module13–22 are empty `__init__.py` files — confirmed by listing) |

---

## Seal Gate — current state

- [x] Real producer demonstrated
- [x] Serialized artifact identified (filename + SHA-256, generated fresh this session)
- [x] Tamper rejection demonstrated (both paths)
- [x] Kernel isolation demonstrated
- [x] Local reproducibility on Python 3.12
- [ ] Python 3.10 / 3.11 legs — **not run** (no interpreters available here)
- [ ] Two-checkout GitHub Actions run — **cited by the repo, not independently reproduced**
- [ ] Exact V1/V2 commit SHAs — **not verifiable from a `.git`-less zip export**

**Conclusion: still correctly NOT SEALED.** Everything runnable outside GitHub's own CI came back genuinely PASS. The remaining gap is entirely in the parts that require GitHub Actions and real git history, which this sandbox cannot reach — so the honest status stays `AUDIT_PARTIAL`, not `SEALED`, and I have not written `docs/M11_SEAL_RECORD.md` or flipped `M11_AUDIT_SUMMARY.json` to `SEALED`.
