# SWI Educational Frontier

**Build-from-Repository Implementation Guide**

| Field | Status |
|-------|--------|
| **GUIDE_ID** | SWI-EF-BUILD-001 |
| **Mode** | EDUCATIONAL FRONTIER |
| **Guide Status** | DRAFT — IMPLEMENTATION GUIDE |
| **Implementation** | NOT AUTHORIZED BY THIS GUIDE |
| **Execution** | BLOCKED BY DEFAULT |
| **Production** | NOT AUTHORIZED |
| **Seal** | NOT CLAIMED |

This guide defines how to **build and learn** SWI from the repository.  
It does **not** establish that SWI is correct, safe, compliant, production-ready, or authorized. Those claims require evidence.

Related: `docs/PROGRAM_PROOF_BOUNDARY.md` · `docs/SWI_REBUILD_IMPLEMENTATION_GUIDE.md`

---

## 1. Educational principle

```text
READ → RUN → OBSERVE → MODIFY → TEST → BREAK
  → DIAGNOSE → REPAIR → VERIFY → REPRODUCE → UNDERSTAND
```

Start small and deterministic; progressively expose architecture.  
Do not require understanding everything before building anything.

---

## 2. Core learner question

> What did the program do, why was it allowed to do it, what evidence supports that conclusion, and what would make SWI refuse it?

---

## 3. Target repository shape (educational)

```text
/
├── README.md
├── EDUCATIONAL_FRONTIER.md   (this guide; also docs/)
├── QUICKSTART.md             (planned)
├── docs/00-start-here/ … 07-advanced/
├── examples/
│   ├── 00_hello_swi/
│   ├── 01_data_vs_evidence/
│   ├── 02_policy_gate/
│   ├── 03_pause_wake/
│   ├── 04_reflex/
│   ├── 05_s9/
│   ├── 06_human_authority/
│   └── 07_program_verification/
├── swi/  (or project package layout)
├── tests/{unit,integration,adversarial,replay,educational}/
└── ledgers/{claims,evidence,verification,seals}/
```

**Current V2 repo:** experimental design docs exist; full educational tree and `swi doctor/demo` CLI are **not** claimed implemented.

---

## 4. One-command safe start (contract)

```text
git clone <repository>
cd <repository>
./swi doctor
./swi test
./swi demo
```

Must never silently perform privileged or production actions.

### `swi doctor`

Report: Python, dependencies, repo integrity, test env, optional tools, **Production mode BLOCKED**, **External execution BLOCKED**.  
Statuses: PASS | FAIL | MISSING | NOT APPLICABLE | BLOCKED | NOT TESTED.  
Never convert MISSING → PASS.

### `swi demo`

Small demo: data/signal/evidence/policy present, authority missing → **ACTION BLOCKED**.  
Teach: a program can know something without being authorized to act on it.

---

## 5. First educational law

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

Never collapse into a single generic `do_something(data)`.

---

## 6. Program verification learning path

| Level | Question |
|-------|----------|
| 1 | Does it run? |
| 2 | Does it match specification properties? |
| 3 | Does it refuse prohibited paths? |
| 4 | Can the result be independently reproduced? |

Then formal/property work. See `docs/PROGRAM_PROOF_BOUNDARY.md`.

---

## 7. Module contract

Every module documents: PURPOSE, INPUTS, OUTPUTS, INVARIANTS, DEPENDENCIES, FAILURE STATES, SECURITY BOUNDARY, AUTHORITY REQUIREMENTS, TESTS, ADVERSARIAL TESTS, EVIDENCE, SEAL STATUS.

Maturity: DRAFT → IMPLEMENTED → TESTED → VERIFIED → REPRODUCED → REVIEWED → SEALED (not interchangeable; test pass ≠ seal).

---

## 8. Learning tracks

- **A Beginner:** basics → data vs evidence → policy gates → tests → diagnostics  
- **B Engineering:** architecture → interfaces → CI → replay → verification  
- **C Security:** trust boundaries → attack simulation → S9 → containment  
- **D Governance:** policy → authority → human review → audit  
- **E Research:** formal properties → adversarial verification → evidence ledger  

---

## 9. Learn → break → repair

Working example → controlled failure → observe → diagnose → patch → regression → replay.

Diagnostics teach: what/where/why failed; evidence present/missing; control that blocked; next educational step.

---

## 10. Safe defaults

```text
NETWORK / PRODUCTION / PRIVILEGED / EXTERNAL SIDE EFFECTS … BLOCKED
REAL STUDENT DATA / CREDENTIALS / BIOMETRICS … DISALLOWED
```

Simulated authority only in educational mode.  
`SIMULATION_AUTHORITY ≠ PRODUCTION_AUTHORITY`

---

## 11. Educational S9

Policy/Security/Evidence PASS, Authority FAIL → learner tries to ignore authority → **REJECTED**.  
Ask: which boundary prevented the bypass?

---

## 12. Evidence, replay, CI, claims, seal

Structured evidence ledger per run. `swi replay RUN-id` → match or investigate.  
CI reports categories separately; seal not automatic.  
Claims: CLAIM → TEST → EVIDENCE → VERIFICATION → REVIEW; lost evidence → UNSUPPORTED.

Scoped seals only (artifact hash, property set, evidence IDs, limitations). Never “SWI = SEALED.”

---

## 13. Frontier honesty

Expose: PROVEN | UNPROVEN | UNKNOWN | NOT TESTED | NOT APPLICABLE | BLOCKED.  
UNKNOWN is a valid scientific result.

---

## 14. Final project deliverables

Spec, source, tests, failure tests, evidence ledger, replay, threat model, authority model, verification report, limitations — and mandatory: **What does my evidence NOT prove?**

---

## 15. Educational invariants

```text
NO_EVIDENCE → NO_PROMOTION
NO_PROVENANCE → NO_TRUST
NO_VERIFICATION → NO_SEAL
NO_AUTHORITY → NO_AUTHORIZED_ACTION
FAILED_SECURITY → NO_EXECUTION
REPLAY_MISMATCH → INVESTIGATE
UNKNOWN → UNKNOWN
AI_SIGNAL ≠ HUMAN_AUTHORITY
TEST_PASS ≠ UNIVERSAL_PROOF
SIGNATURE ≠ AUTHORIZATION
```

---

## 16. Goal

Not to hide complexity — to make it progressively learnable.  
Teach not only how to make programs work, but **what evidence actually establishes**.

**Next engineering steps (when authorized):** QUICKSTART.md · module template · `swi doctor/demo/test/replay` command contract · `examples/00_hello_swi` — not more conceptual layers alone.
