# SWI Adversarial Test Matrix — SWI-ATM-001

**STATUS:** DESIGN  
**NOT IMPLEMENTED**  
**NOT SEALED**  
**PRODUCTION:** BLOCKED  

**Matrix ID:** SWI-ATM-001  
**Purpose:** Prove that Spider Web Reborn cannot silently cross a boundary from data → evidence → admission → verification → authority → action.

---

## 1. Test Dimensions

Every adversarial scenario is classified across:

| Dimension | Values |
|-----------|--------|
| Mode | Positive / Negative / Boundary |
| Attack | Bypass / Forgery / Confusion / Reordering / Replay / Injection / Suppression / Escalation |
| State | Defined / Implemented / Tested / Verified / Sealed / Blocked / Rejected |
| Input | Valid / Invalid / Missing / Malformed / Stale / Conflicting |
| Authority | Present / Missing / Expired / Wrong scope / Wrong subject |
| Evidence | Valid / Missing / Unverified / Stale / Conflicting |
| Expected result | ADMIT / REJECT / BLOCK / ERROR |
| Evidence | Test output + hash + provenance |
| Replay | Reproducible / Non-reproducible |
| Seal effect | None / Review required / Seal blocked |

---

## 2. Core Domains (Summary)

- **Token adversarial** (TKN-A01–A10)
- **Identifier adversarial** (ID-A01–A10)
- **Reserved vs Protected names**
- **Registry adversarial** (REG-A01–A10) — critical invariant: MISS ≠ ERROR
- **Node adversarial**
- **Edge adversarial** — OBSERVES ≠ EXECUTES, PROVES ≠ AUTHORIZES, etc.
- **Dependency / Suppressed-descendant attacks**
- **Diagnostic determinism**
- **Evidence attacks** (scope-bound)
- **Admission / ReturnGate**
- **Verification promotion shortcuts**
- **Replay attacks**
- **Authority attacks** (human vs technical)
- **Cryptographic boundary**
- **Observer / Common Sense attacks**
- **True Zero** (one missing condition → BLOCK)
- **State-transition rejection** (closed model)
- **Privacy-domain isolation**
- **Tamper quarantine & re-entry prohibition**

---

## 3. Master Invariant

```
UNTRUSTED INPUT
      ↓
TOKEN → IDENTIFIER → REGISTRY → NODE → EDGE → DEPENDENCY
      ↓
VALIDATION → EVIDENCE → ADMISSION → VERIFICATION
      ↓
HUMAN AUTHORITY → SECURITY → SAFETY → ACTION
```

At every arrow the adversary may attempt a bypass.  
The test passes when the bypass is rejected, blocked, or deterministically diagnosed and the system retains enough evidence to reproduce why.

---

## 4. Scenario Lifecycle

```
DEFINED → IMPLEMENTED → EXECUTED → OBSERVED → EVIDENCE_CAPTURED
       → REPLAYED → REPRODUCED → VERIFIED
```

Not automatically SEALED.

---

## 5. Machine-Readable Record (Required for every scenario)

```
scenario_id, domain, attack_class, preconditions, input, mutation,
expected_state, expected_result, expected_failure,
expected_primary_failure, expected_suppressed_failures,
evidence_required, authority_required, replay_required,
security_requirements, safety_requirements,
actual_result, actual_failure, reproduction_reference, status
```

---

**Next:** See `ATM_COVERAGE_MAP.md` for mapping against existing tests and prioritisation.
