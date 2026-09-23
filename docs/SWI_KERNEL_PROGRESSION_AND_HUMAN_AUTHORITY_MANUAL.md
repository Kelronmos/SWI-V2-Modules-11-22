# SWI Kernel Progression & Human Authority Manual

**Status:** Research / Architecture Manual  
**Date:** 23 September 2026  
**Branch:** `architecture/kernel-progression-human-authority`  
**Principle:** Human authority remains above system execution.  
**Core doctrine:** `DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION`

This document is a **manual and governance architecture**, not an automatic “unlock” mechanism.  
It does **not** open any blocked execution path, does **not** claim any new seal, and does **not** authorize production.

---

## 1. Purpose

SWI is designed to grow from a micro-kernel into a main kernel without abandoning the principles established at the lowest layer.

Each new kernel must inherit the security boundaries of the previous kernel and, where justified, introduce stronger controls.

A larger kernel must never weaken a smaller kernel merely because it has more capability.

> «More capability requires more boundary, not less.»

---

## 2. Micro-Kernel → Main Kernel

The progression is:

```text
MICRO-KERNEL
    ↓
CORE KERNEL
    ↓
MAIN KERNEL
    ↓
SEALED CORE
    ↓
GOVERNED EXECUTION
    ↓
PRODUCTION-READY CANDIDATE
```

Each transition requires evidence.

- A kernel cannot promote itself.
- A module cannot promote itself.
- A successful test cannot automatically authorize production.

---

## 3. Kernel Inheritance Rule

Every new kernel must inherit:

- fail-closed behaviour;
- authority separation;
- evidence provenance;
- tamper detection;
- replayability;
- explicit policy boundaries;
- human escalation;
- auditability;
- minimum-necessary execution;
- separation between admission and authorization.

The inherited controls become the **minimum security floor**.

New controls may raise that floor.  
They may not silently remove it.

---

## 4. Core Execution Modules (protected boundary)

The six core execution modules are treated as a protected execution boundary.

Their state is **not**:

```text
PASS → EXECUTE
```

Instead:

```text
TESTED
  → EVIDENCE REVIEW
  → SEALED
  → BLOCKED / AWAIT HUMAN AUTHORITY
  → GOVERNANCE REVIEW
  → CONDITIONAL RELEASE
  → PRODUCTION-READY CANDIDATE
```

Even after reaching production-ready candidate status:

> «Execution still requires appropriate human authority.»

Production readiness is therefore **not** equivalent to unrestricted autonomous execution.

---

## 5. Human Vote Gate (governance threshold)

For a proposed continental-level governance transition, SWI may establish a defined human-governance threshold.

One proposed **research** threshold is:

- **87 verified human votes** from at least **46 countries**.

This is a **governance threshold**, not a technical security score.

The system must **not** interpret:

```text
87 votes
```

as:

```text
automatic authorization to execute anything
```

Instead, the threshold means that the specified governance condition has been satisfied **for the particular proposal and scope that was voted upon**.

The vote record must therefore contain at minimum:

- proposal identifier;
- version;
- scope;
- participating jurisdictions;
- voter eligibility;
- timestamp;
- decision;
- evidence reference;
- quorum rules;
- conflict / abstention handling;
- audit trail.

---

## 6. Continental Unlock Principle

The phrase “continental unlock” should mean a **governance milestone**, not unrestricted technical access.

Conceptually:

```text
SEALED SECURITY PATHS
+ VERIFIED EVIDENCE
+ DEFINED HUMAN GOVERNANCE
+ 87 VERIFIED VOTES
+ 46+ COUNTRIES
+ SCOPE MATCH
        ↓
CONTINENTAL GOVERNANCE MILESTONE
```

It must **not** mean:

```text
87 VOTES → AUTOMATIC EXECUTION
```

Execution remains separately bounded by:

```text
LAW → POLICY → AUTHORITY → SYSTEM PERMISSION → ACTION
```

---

## 7. Evidence Requirements for Execution Modules

Before a core execution path can progress, each module must have an evidence record showing:

1. What the module claims to do.
2. What was actually implemented.
3. What tests were executed.
4. What adversarial tests were executed.
5. What the tests actually prove.
6. What remains untested.
7. What limitations remain.
8. Whether the evidence is reproducible.
9. Whether the record is sealed.
10. Whether human authorization is required.

**Status vocabulary** (must never be collapsed):

- `DESIGNED`
- `IMPLEMENTED`
- `TESTED`
- `ADVERSARIAL-TESTED`
- `REPLAY-VERIFIED`
- `AUDITED`
- `SEALED`
- `BLOCKED`
- `AWAITING-HUMAN-AUTHORITY`
- `PRODUCTION-READY-CANDIDATE`
- `PRODUCTION-AUTHORIZED`

---

## 8. Sensitive Data Boundary

Where a module touches sensitive information, the kernel must enforce:

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

- Possession of data does not establish permission.
- A valid record does not automatically establish authority.
- An admitted request does not automatically authorize execution.
- A valid authorization does not make an untested implementation safe.

> «The kernel governs the transition between layers.»

(This is consistent with the existing `docs/AUTHORITY_BOUNDARY_MODEL.md`.)

---

## 9. Old-System / Legacy Adoption

SWI should not assume that every existing system must be destroyed and replaced.

Many legacy systems may still provide useful capabilities in particular jurisdictions.

Adoption strategy:

```text
DISCOVER
  → INGEST
  → DIAGNOSE
  → BOUND
  → TEST
  → ISOLATE
  → ADAPT
  → VERIFY
  → CONDITIONALLY INTEGRATE
```

The old system becomes an **ingested dependency**, not an authority over SWI.

---

## 10. Ingestion Does Not Equal Trust

An existing system may be ingested for compatibility without becoming trusted by default.

SWI must establish:

- what the system does;
- what data it receives;
- what authority it claims;
- what laws/policies govern it;
- what interfaces it exposes;
- what assumptions it makes;
- what security controls exist;
- what failures have occurred;
- what cannot yet be verified.

The ingestion process must **not** create a bypass around the kernel.

> «Useful legacy capability may be preserved without inheriting legacy authority.»

---

## 11. Sustainable Adoption

The objective is not to replace every existing system immediately.

The objective is to create a controlled transition path.

A jurisdiction may retain an existing component where it remains useful while SWI progressively introduces:

- policy boundaries;
- evidence requirements;
- identity controls;
- authorization controls;
- audit trails;
- replay;
- tamper detection;
- human escalation;
- security testing.

This allows adoption to occur incrementally rather than requiring every country to rebuild its entire digital infrastructure simultaneously.

---

## 12. Law and Policy Ingestion

Where legislation or policy changes, SWI should be capable of running a diagnostic process against the affected system:

```text
NEW / AMENDED LAW
  → LAW INGESTION
  → CHANGE ANALYSIS
  → AFFECTED MODULES
  → POLICY BOUNDARY UPDATE
  → REGRESSION TEST
  → ADVERSARIAL TEST
  → REPLAY
  → EVIDENCE
  → HUMAN REVIEW
```

A law-ingestion mechanism must **not** silently rewrite the system and declare itself authorized.

---

## 13. Locked Kernel Principle

A kernel reaches a locked state only when the defined path has been independently verified and sealed.

A locked kernel means:

> «The verified boundary cannot be casually changed by downstream modules.»

Any proposed change must create a new versioned path:

```text
LOCKED KERNEL
  → CHANGE REQUEST
  → AUTHORITY CHECK
  → NEW VERSION
  → TEST
  → ADVERSARIAL TEST
  → REPLAY
  → AUDIT
  → SEAL
```

No hidden mutation. No silent replacement. No bypass.

---

## 14. Production-Ready Is Not Autonomous Authority

Even if every technical path has been sealed and the system has reached production-ready candidate status, SWI does **not** acquire human authority merely from technical completion.

The final relationship remains:

```text
HUMAN AUTHORITY
    ↓
LAW / POLICY
    ↓
SWI GOVERNANCE BOUNDARY
    ↓
KERNEL
    ↓
AUTHORIZED EXECUTION
    ↓
AUDITABLE RESULT
```

Where authority is absent: **HALT**.

---

## 15. The Core Principle

SWI should become harder to unlock as capability increases.

Not because the system distrusts humans.

Because consequential systems should make authority visible.

The architecture therefore moves from:

> “Can the system execute?”

toward:

> “Who authorized this execution, under which rule, using which evidence, through which tested path, and can the result be reproduced?”

That is the purpose of the kernel progression.

---

## 16. Final Invariant

The complete architecture must preserve:

> «No module becomes its own authority.  
> No test becomes authorization.  
> No data becomes evidence merely by being processed.  
> No ingestion becomes trust.  
> No seal becomes permanent immunity from review.  
> No production readiness becomes unrestricted execution.»

And above all:

> «SWI may automate workflow. It must not manufacture human authority.»

---

## 17. Proposed Layer Map (architecture only)

```text
SWI
│
├── 00 MICRO-KERNEL
│   ├── identity
│   ├── canonicalization
│   ├── evidence boundary
│   ├── authority boundary
│   ├── halt
│   └── replay
│
├── 01 CORE KERNEL
│   ├── module registry
│   ├── policy binding
│   ├── law binding
│   ├── evidence verification
│   ├── authorization boundary
│   ├── execution gate
│   └── audit
│
├── 02 MAIN KERNEL
│   ├── kernel composition
│   ├── inter-module contracts
│   ├── sensitive-data boundary
│   ├── legacy-system adapter boundary
│   ├── law/amendment diagnostics
│   ├── consequence controls
│   └── human escalation
│
├── 03 SIX CORE EXECUTION MODULES
│   ├── E01 … E06
│
├── 04 SECURITY / ADVERSARIAL LAYER
│
├── 05 LAW INGESTION
│
├── 06 LEGACY ADOPTION
│
├── 07 EVIDENCE / REPLAY
│
├── 08 HUMAN GOVERNANCE
│   ├── proposal / jurisdiction / eligibility / vote
│   ├── 87-vote threshold + 46-country diversity (governance contract)
│   └── human authorization
│
└── 09 PRODUCTION GATE
    ├── all required paths sealed
    ├── independent audit
    ├── unresolved limitations
    ├── legal/policy review
    ├── human governance decision
    ├── production readiness (candidate)
    └── execution authorization (separate human step)
```

---

## 18. State Machine (no skips)

```text
DESIGNED
  → IMPLEMENTED
  → TESTED
  → ADVERSARIAL-TESTED
  → REPLAY-VERIFIED
  → INDEPENDENTLY AUDITED
  → SEALED
  → BLOCKED / AWAITING HUMAN AUTHORITY
  → GOVERNANCE REVIEW
  → CONDITIONALLY RELEASED
  → PRODUCTION-READY-CANDIDATE
  → HUMAN AUTHORIZATION
  → AUTHORIZED EXECUTION
```

Forbidden transitions (examples):

- `TESTED` → `AUTHORIZED`
- `SEALED` → `EXECUTION`
- `87 VOTES` → automatic execution
- `LAW INGESTED` → law authority
- `LEGACY SYSTEM INGESTED` → trust

---

## 19. Relationship to Existing Repository

This manual builds on, and does not contradict:

- `docs/AUTHORITY_BOUNDARY_MODEL.md`
- `docs/CURRENT_POSITION.md`
- `docs/MODULE_STATUS.md`
- M11 evidence / seal discipline
- PRE-R separation
- existing law-ingestion design paths

Current repository position (as of tip used for this branch):

- M11: treated with historical seal records; active claims remain under freshness / audit discipline.
- PRE-R: not production-authorized.
- Execution modules: blocked pending human authority and sealed evidence paths.

No change to those positions is made by this document.

---

## 20. Next Repository Steps (ordered)

1. Keep this document on the architecture branch until reviewed.
2. Do **not** merge to `main` until explicit human decision.
3. Align any future Mxx contracts with the state machine and inheritance rule above.
4. Treat 87/46 as a governance contract object, never a hard-coded technical bypass.
5. Continue evidence freshness, replay, and adversarial work under the existing freeze rules.

---

## 21. Seal Eligibility Equation (mandatory before every seal)

**Rule:** The Seal Eligibility Equation **MUST** be evaluated and recorded **every time** before any seal decision is issued.

No seal may be written, claimed, or relied upon unless the equation evaluates to true **and** the evaluation itself is preserved as evidence.

### 21.1 The Equation

```text
SEAL_ELIGIBLE  ⇔
    CONTRACT_FROZEN
  ∧ ARCHITECTURAL_BOUNDARY
  ∧ REAL_PRODUCER
  ∧ ADMISSION_BEHAVIOUR
  ∧ KERNEL_ISOLATION
  ∧ REPRODUCIBILITY_CI
  ∧ DOCUMENTATION_HONESTY
  ∧ TIP_SPECIFIC_CI_GREEN
  ∧ ADVERSARIAL_MATRIX_PASS
  ∧ EVIDENCE_FRESH
  ∧ LIMITATIONS_DECLARED
```

Where each term is a boolean that is true only when the corresponding gate has been independently demonstrated for the **exact tip** under consideration.

### 21.2 Mandatory evaluation procedure

Before every seal:

1. **Instantiate** the equation for the specific module / kernel / tip.
2. **Evaluate** every term against current evidence (not historical claims).
3. **Record** the evaluation (term → true/false + evidence pointer).
4. **Refuse** the seal if any term is false or lacks tip-specific evidence.
5. **Only then** may a seal record be written, and the evaluation must be referenced inside the seal record.

### 21.3 Non-negotiable constraints

- The equation is **not** a one-time checklist. It is re-run for every seal attempt.
- Historical seals do not satisfy the equation for a new tip.
- Local green tests do not satisfy `TIP_SPECIFIC_CI_GREEN`.
- “Tests passed last week” does not satisfy `EVIDENCE_FRESH`.
- Documentation that still says “PENDING” while claiming “SEALED” falsifies `DOCUMENTATION_HONESTY`.
- A missing limitation list falsifies `LIMITATIONS_DECLARED`.

### 21.4 Formal statement

```text
∀ seal decision S:
    Evaluate(SealEligibilityEquation, tip(S)) = TRUE
    ∧ EvidenceRecord(Evaluation) exists
    ⇒ S may be written
    otherwise
    ⇒ HALT (no seal)
```

### 21.5 Relationship to core doctrine

The equation operationalises the doctrine:

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

A passing equation yields a **seal** (a controlled dependency boundary).  
It never yields **authorization** or **action**. Those remain separate human / legal steps.

### 21.6 Implementation note (future)

When the Mathematical Evidence Engine or claim-ledger tooling is wired in, the equation evaluation itself should become a first-class evidence artifact that can be replayed. Until then, the evaluation must still be performed manually and recorded in the seal record or an attached worksheet.

> «Run the equation every time before seal.  
> No equation → no seal.  
> Stale equation → no seal.»

---

## 22. Common Sense Equation (authority boundary)

**Position:** Below the Seal Eligibility Equation.  
**Role:** Reasoning and correction path for human error.  
**Rule:** Common Sense may detect, analyse, diagnose, correct, and produce evidence.  
It must **never** execute, promote, seal, or authorize.

### 22.1 Command contract

```text
SWI::COMMONSENSE(HUMAN_ERROR)
        ↓
DETECT
        ↓
ANALYSE
        ↓
DIAGNOSE
        ↓
CORRECT / REDIRECT
        ↓
EVIDENCE
        ↓
HUMAN AUTHORITY
        │
        ├── absent  → HALT
        │
        └── present → AUTHORIZED PATH
```

### 22.2 Formal equation

```text
COMMON_SENSE(HumanError)
  → DETECT + ANALYSE + DIAGNOSE + CORRECT/REDIRECT + EVIDENCE
  ↛ EXECUTE
  ↛ PROMOTE
  ↛ SEAL
  ↛ AUTHORIZE
```

Or boxed:

```text
COMMON_SENSE(HumanError) → Correction → Evidence ↛ Authority
```

### 22.3 Core invariants

```text
CS ∩ {EXECUTION, PROMOTION, SEAL, AUTHORIZATION} = ∅

ERROR      ≠ AUTHORITY
CORRECTION ≠ EXECUTION
PROOF      ≠ PROMOTION
PROOF      ≠ AUTHORIZATION
```

### 22.4 Allowed vs forbidden outcomes

| Common Sense may | Common Sense must not |
|------------------|------------------------|
| DETECT human error | EXECUTE any path |
| ANALYSE the failure | PROMOTE a module or kernel |
| DIAGNOSE the boundary defect | Issue or imply a SEAL |
| CORRECT / REDIRECT the claim or implementation | Manufacture AUTHORIZATION |
| Produce EVIDENCE of the correction | Bypass HUMAN AUTHORITY |

### 22.5 Relationship to Section 21

- Section 21 governs when a **seal** may be written.
- Section 22 governs how **human error** is handled without converting reasoning into power.
- A successful Common Sense correction may improve evidence that later feeds the Seal Eligibility Equation.
- It never short-circuits the equation and never grants execution rights.

### 22.6 Relationship to core doctrine

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

Common Sense operates in the space of reasoning and evidence production.  
It stops at the authority boundary. Where human authority is absent: **HALT**.

> «Common Sense may reason about error.  
> It must not acquire execution or promotion authority from that reasoning.»

---

## 23. Core Test Loop (evidence cycle)

```text
CLAIM
  → IMPLEMENT
  → TEST
  → REPLAY
  → RECORD
  → ANALYSE
  → DIAGNOSE
  → RE-IMPLEMENT
  → RE-TEST
  → EVIDENCE
  → PROOF
        ↓
LIMITATION
        ↓
NEXT CLAIM
```

**Distinction:** Proof is the end of the evidence cycle, not the beginning of the next assumption.

```text
PROOF ≠ AUTHORIZATION
```

A proven mechanism can still remain blocked and awaiting human authority.

---

*End of manual.*
