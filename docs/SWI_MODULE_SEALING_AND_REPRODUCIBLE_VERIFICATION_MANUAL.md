# SWI Module Sealing & Reproducible Verification Manual

**Document:** SWI Module Sealing & Reproducible Verification Manual  
**Version:** 1.0 Draft (adapted to V1/V2 Python repositories)  
**Applies to:** SWI V1 (`SWI-V1-Module-1-10`), V2 (`SWI-V2-Modules-11-22`)  
**Purpose:** Convert documented modules into independently testable, reproducible, evidence-backed **SEALED** modules without overstating production readiness.

---

## 1. Purpose

A module may be marked **SEALED** only when its documented contract has been converted into **executable, regenerable evidence**.

```text
DOCUMENTED → IMPLEMENTED → CONTRACT TESTED → UNIT VERIFIED
  → NEGATIVE TESTED → DETERMINISM VERIFIED (if required)
  → SECURITY VERIFIED (claimed properties only)
  → REPRODUCED → SEALED
```

Where a dimension is not applicable, **record the reason** — do not silently omit it.

---

## 2. Core principle

> **No claim without executable evidence.**

**Not** sealing evidence by themselves:

- README statements · screenshots · developer assertions  
- Prior CI without tip + fixtures  
- One happy-path test · “looks correct” code  
- Crypto-looking output · simulated crypto as production security  
- Historical claims that cannot be reproduced  

Evidence must be regenerable from the repository at an **immutable commit**.

---

## 3. Terminology

| State | Meaning |
|-------|--------|
| **IMPLEMENTED** | Executable form exists |
| **TESTED** | Executable tests cover documented behavior |
| **VERIFIED** | Defined gates passed; evidence reproducible |
| **SEALED** | Sealing requirements passed; impl/tests/fixtures frozen to that evidence |
| **INTEGRATION_READY** | Stronger integration gate (separate) |
| **RELEASED** | System-level release (never inferred from module seal) |

**SEALED ≠ PRODUCTION READY**

Also allowed: **DEFERRED · BLOCKED · REJECTED · REVALIDATION_REQUIRED**

Forbidden skips: `IMPLEMENTED → RELEASED`, `TESTED → production_ready=true` without a separate production gate.

---

## 4. Alignment with existing V1/V2 practice

| Draft idea | Current SWI reality |
|------------|---------------------|
| Immutable commit seal | **Required** — e.g. M11 freezes V1+V2 SHAs |
| Negative / tamper tests | M11 admission + post-admission seal |
| Reproducibility | Two-checkout CI + Python 3.10–3.12 matrix |
| Evidence record | `docs/M11_SEAL_RECORD.md` (+ optional future `evidence/`) |
| Node/`npm ci`/`tsc` | **Not** the V1/V2 stack — use **Python + pytest + pip freeze/lock** |
| `npm run swi:seal` | Optional future tooling; today: documented checklist + CI + seal record |
| Registry `production_ready: false` | Matches SWI doctrine |

**M11 current status:** **SEALED** under `docs/M11_SEAL_RECORD.md` (CI run `35253244912`, frozen SHAs). This manual does **not** unseal M11. Future modules (or tip re-validation) should follow the same *kinds* of gates, adapted to Python.

---

## 5. Evidence model (recommended layout)

Optional directory (not required to exist for historical M11 seal):

```text
evidence/
  M11/
    contract/
    unit/
    negative/
    determinism/
    security/
    integration/
    reproducibility/
    manifest.json
    commit.txt
```

Categories must stay identifiable even if paths differ.

---

## 6. Module contract (before seal)

Machine-readable or explicit doc answering:

1. What is accepted / rejected?  
2. What is returned?  
3. Invariants?  
4. Expected errors?  
5. Dependencies?  
6. Determinism requirements?  
7. **Which security properties are actually claimed?**

Every normative statement → ≥1 executable test ID (traceability table).

---

## 7. Freeze the candidate

```bash
git rev-parse HEAD          # → evidence/<MODULE>/commit.txt
git status --short          # prefer clean tree
git branch --show-current
```

Seal against a **specific SHA**, never “latest” / “main” alone.

For cross-repo modules (M11): freeze **producer and consumer** SHAs.

---

## 8. Environment & dependencies (Python)

Record:

```bash
python --version
pip freeze | sha256sum   # or lockfile hash if present
uname -a
```

Prefer reproducible install from `requirements.txt` / lock where available.

Static checks: project-defined (ruff/mypy only if the repo already requires them for that module).

---

## 9. Verification steps

| Step | Requirement |
|------|-------------|
| Unit | Valid / boundary / malformed / missing / invariants |
| Contract | Interface-level expected accept/reject |
| Negative | Null/empty/wrong type/extra fields/tamper/expired/replay **as relevant to contract** |
| Determinism | Same fixture → same **canonical** result (if required) |
| Security | Only **documented** claims (authz, integrity verify, isolation limits, etc.) |
| Integration | Prior module → this module boundary |
| Cross-repo | V1 envelope → V2 admit; no V1 import into V2 |
| CI | Named workflow run ID + matrix where required |
| Reproduce | Clean checkout + re-run + hash/compare where claimed |

**Crash ≠ successful security rejection** unless the contract defines that behavior.

### Canonicalization (before hashing structured evidence)

Sort keys · normalize newlines · forbid NaN where required · UTF-8 · version the algorithm · SHA-256.

### Cryptography

If simulated/non-production crypto:

```json
{ "crypto_test": "PASS", "security_assurance": "NOT_PRODUCTION_CRYPTOGRAPHIC_ASSURANCE" }
```

Ed25519/SHA-256 **primitives** ≠ CRTG ≠ production key lifecycle.

---

## 10. Seal decision algorithm

```text
IF missing module / contract / mapped tests     → FAIL
IF unit or required negative tests fail        → FAIL
IF determinism required and fails              → FAIL
IF security claims required and fail           → FAIL
IF dependency gates fail                       → FAIL
IF reproducibility required and fails          → FAIL
IF evidence not tied to immutable commit(s)    → FAIL
ELSE                                           → ALLOW SEALED
```

Never convert FAIL → warning → SEALED.  
Operator override, if any, must be labeled **OVERRIDE**, not **SEALED**.

---

## 11. Seal record (minimum)

Write a permanent record (example: `docs/M11_SEAL_RECORD.md` or `evidence/.../seal-record.json`) containing:

- module id · repository · **commit SHAs**  
- CI run id / URL (if used)  
- contract scope  
- test/CI matrix results  
- algorithms used (if any)  
- **explicit non-claims**  
- decision **SEALED** or **NOT SEALED**  
- date · limitations  

Update module status **only after** the record exists.

---

## 12. What must not change during sealing

Do not: remove failing fixtures · weaken asserts · disable security tests · catch-all → “reject” · mark simulated crypto as production · hand-edit registry to bypass · delete failing evidence · claim reproducibility without a second run.

---

## 13. Seal invalidation

Material change to implementation, contract, security behavior, determinism, dependencies, fixtures, or canonicalization → **REVALIDATION_REQUIRED** (or drop to TESTED).

Historical fixtures must keep passing (regression).

---

## 14. M11 mapping (worked example)

| Manual gate | M11 evidence |
|-------------|--------------|
| Immutable commits | V2 `1d6d7dc…` · V1 `e0c6a521…` |
| Contract | Admit schema/integrity → `AdmittedInput`; seal on AdmittedInput only |
| Negative / security (integrity) | Tamper reject on admit + seal path |
| Cross-repo + isolation | Two-checkout; V1 not importable |
| Matrix | Python 3.10 / 3.11 / 3.12 |
| Reproduce | CI run `35253244912` |
| Non-claims | No CRTG · no Seal 5 · no production keys · no payload truth |
| Decision | **SEALED** |

Tip commits after the freeze (e.g. pre-R) do **not** automatically invalidate M11 unless behavior under the **sealed contract** changes without revalidation.

---

## 15. Dependency gate

Example: **M12** must not be integration-enabled or sealed while M11 is not in the required trusted state. Today: M11 **SEALED**; M12 **FROZEN** until Gates A–D (`docs/MODULE_STATUS.md`).

---

## 16. Production readiness (separate)

```text
state: SEALED
production_ready: false   # default unless separate system gate passes
```

Production readiness needs threat model, ops, monitoring, deployment, incident response, regulatory fit — **not** module unit tests alone.

---

## 17. Definition of done

```text
DOCUMENTATION + IMPLEMENTATION + EXECUTABLE TESTS
+ NEGATIVE TESTS + REQUIRED SECURITY TESTS
+ DETERMINISM (if required) + DEPENDENCY VALIDATION
+ REPRODUCIBILITY + IMMUTABLE COMMIT(S)
+ EVIDENCE RECORD + STATUS UPDATE
= SEALED
```

Anything less remains IMPLEMENTED / TESTED / VERIFIED / DEFERRED / BLOCKED.

---

## 18. Final principle

A sealed module means:

> This exact implementation, under this defined environment and contract, passed the specified executable gates, and another verifier can reproduce the evidence.

It does **not** mean the entire SWI system is production-ready.

Related: `docs/M11_SEAL_RECORD.md` · `docs/M11_CLOSURE_CHECKLIST.md` · `docs/SWI_MODULE_LIFECYCLE_MANUAL.md` · `docs/MODULE_STATUS.md`
