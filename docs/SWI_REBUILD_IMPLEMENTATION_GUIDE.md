# SWI REBUILD — FULL IMPLEMENTATION & UNDERSTANDING GUIDE

**Project:** Structured Workflow Intelligence (SWI)  
**Repository family:** SWI V1 / SWI V2  
**Purpose:** Define, implement, test, verify, document, and maintain SWI without conflating implementation behaviour with foundational claims.

---

## GUIDE STATUS

| Field | Status |
|-------|--------|
| **Document** | SWI REBUILD — FULL IMPLEMENTATION & UNDERSTANDING GUIDE |
| **Guide Type** | Normative implementation and understanding guide |
| **Guide Status** | ACTIVE — CONTROLLED DEVELOPMENT REFERENCE |
| **Foundation / Floor** | SWI: **inherited computational floor** |
| **Floor Definition** | Explicitly defined in this guide (§2) |
| **Scope** | Foundation, architecture, workflow, implementation, testing, evidence, verification, sealing, authority, security, safety, execution boundaries |
| **Primary Rule** | SWI structures **policy-defined** workflows; it does not invent policy or authority |
| **Human Authority** | Required for consequential actions where the governing workflow requires it |
| **Production Status** | **NOT AUTHORIZED BY THIS GUIDE** |
| **Seal Status** | This guide does **not** seal any implementation or module |
| **Verification Status** | Documentation status is **not** implementation verification |
| **Evidence Status** | Evidence must be generated and preserved **separately** for each implementation state |
| **Test Status** | Tests must be executed against the **actual** repository state; this guide does not substitute for test execution |
| **Replay Status** | Replay must be demonstrated from preserved evidence and inputs |
| **Reproduction Status** | Reproduction must be demonstrated under defined conditions |
| **Change Control** | Changes require impact assessment, testing, evidence review, and seal review where applicable |
| **Floor-Change Rule** | Implementation, testing, terminology, or hardening changes do **not** constitute a floor change unless the foundation itself is explicitly changed |
| **System Boundary** | SWI remains distinct from other systems whose foundations are separately defined |
| **Execution Rule** | No required condition may be silently inferred; unresolved authority, evidence, security, safety, or policy conditions require review, escalation, or block |

### Status interpretation

This block defines the status of the **guide**, not the status of every implementation component.

```text
GUIDE ACTIVE
  ≠ IMPLEMENTATION VERIFIED
  ≠ IMPLEMENTATION SEALED
  ≠ PRODUCTION AUTHORIZED
```

The guide is an authoritative **development reference** for the rules and distinctions it explicitly defines. It does not manufacture evidence, authority, verification, seal status, or production authorization.

### Guide change rule

Changes affecting floor definition, foundational architecture, authority model, policy boundary, state/transition models, security/safety, evidence, verification, sealing, or production requirements are **controlled specification changes**:

```text
GUIDE CHANGE → IMPACT ASSESSMENT → IMPLEMENTATION REVIEW → TEST
  → EVIDENCE → REPLAY / REPRODUCTION → VERIFICATION → SEAL REVIEW (if applicable)
```

The guide defines the rules. The repository implementation must **prove** compliance with those rules.

---

## 1. PURPOSE

SWI is a structured workflow system designed to make consequential workflows more explicit, testable, observable, evidence-aware, and bounded by human authority.

SWI is not defined merely by code, tests, terminology, security controls, signatures, certificates, automation, a particular interface, deployment, or test suite.

The rebuild separates:

```text
FOUNDATION → DEFINITION → ARCHITECTURE → IMPLEMENTATION → TESTING
  → EVIDENCE → VERIFICATION → SEAL → AUTHORIZED USE
```

No lower layer silently establishes a higher layer.

---

## 2. DEFINITION OF “FLOOR”

### 2.1 Normative definition

**Floor** means:

> The foundational layer from which a system’s objects, relationships, rules of validity, permitted transformations, and consequential behaviour are constructed.

The floor is deeper than implementation, workflow configuration, terminology, test cases, security mechanisms, evidence records, and deployment infrastructure.

```text
IMPLEMENTATION ≠ FLOOR
TEST ≠ FLOOR
TERMINOLOGY ≠ FLOOR
EVIDENCE ≠ FLOOR
SECURITY CONTROL ≠ FLOOR
DEPLOYMENT ≠ FLOOR
```

### 2.2 Floor-change rule

A change to implementation does **not** constitute a floor change unless the foundational layer itself is explicitly changed.

```text
PATCH ≠ FLOOR CHANGE
NEW TEST ≠ FLOOR CHANGE
NEW GATE ≠ FLOOR CHANGE
STRONGER SECURITY ≠ FLOOR CHANGE
NEW TERMINOLOGY ≠ FLOOR CHANGE
REFACTOR ≠ FLOOR CHANGE
HARDENING ≠ FLOOR CHANGE
```

A claimed floor change requires explicit identification of: previous floor; proposed floor; foundational elements that changed; consequences; new definitions; new dependency structure; required verification; supporting evidence.

---

## 3. SWI’S FLOOR

SWI is documented and tested as a system built on the **inherited computational floor**.

This defines SWI’s architectural starting point. It does **not** claim that every property of that floor has been independently established by SWI. It means SWI does not silently redefine its foundation while modifying implementation.

```text
SWI = SYSTEM BUILT ON INHERITED COMPUTATIONAL FLOOR
```

Workflow-control model:

```text
INPUT → TOKEN → IDENTIFIER → REGISTRY → NODE → EDGE → DEPENDENCY
  → VALIDATION → EVIDENCE → ADMISSION → VERIFICATION → HUMAN AUTHORITY
  → SECURITY → SAFETY → AUTHORIZATION → ACTION
```

Compact view: **ADMISSION → AUTHORITY → ENFORCEMENT → EXECUTION**

---

## 4. OTHER SYSTEMS MUST REMAIN DISTINCT

A separately defined system may describe its own foundation as a different floor.

**The Shift** is described by its proponents as constructed from a corrected floor involving: Classical Mathematics, Genesis 2.0ut, RB1, AHMR, URK, Elements Basin, Lawful Continuance.

SWI records that description as belonging to the other system. SWI does not automatically validate or invalidate those claims merely because they are mentioned.

```text
TESTING SWI ≠ TESTING THE SHIFT
TESTING THE SHIFT ≠ TESTING SWI
USING SHIFT TESTS ≠ MOVING SWI TO SHIFT'S FLOOR
USING SHIFT TERMINOLOGY ≠ MOVING SWI TO SHIFT'S FLOOR
HARDENING SWI ≠ MOVING SWI TO ANOTHER FLOOR
TEST TRANSFER ≠ FLOOR TRANSFER
```

> **Different floor = different system.**

Comparative methodology: `docs/COMPARATIVE_TEST_FRAMEWORK.md`.

---

## 5. CORE SWI DISTINCTIONS

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
TESTED ≠ VERIFIED ≠ SEALED
SIGNATURE ≠ TRUTH · SIGNATURE ≠ AUTHORITY
CERTIFICATE ≠ HUMAN AUTHORIZATION
OBSERVATION ≠ EXECUTION · RECOMMENDATION ≠ AUTHORIZATION
AUTHORIZATION ≠ ACTION · SIMULATION ≠ PRODUCTION PROOF
CI GREEN ≠ PRODUCTION AUTHORIZATION
```

---

## 6. HUMAN AUTHORITY

SWI does not manufacture authority.

```text
VALID CONDITION ≠ AUTHORITY ≠ AUTHORIZATION ≠ ACTION
```

Absent required authority → **BLOCK**. Ambiguous → **REVIEW / ESCALATE / BLOCK**.

Do not infer authority from credentials, signatures, TLS, HSM, TPM, sessions, successful tests, CI, recommendations, or previous authorizations alone.

---

## 7. TRUE ZERO

True Zero ≠ zero humans.  
True Zero = **zero unauthorized consequential actions**.

The system may observe, analyse, collect evidence, report, request review, ask for authority, block, escalate.

---

## 8. HUMAN-CENTRED DESIGN

SWI works with people, not instead of people.

```text
AUTOMATION ≠ AUTONOMY · EFFICIENCY ≠ HUMAN REPLACEMENT
PREDICTION ≠ DECISION · OBSERVATION ≠ AUTHORITY · RECOMMENDATION ≠ AUTHORIZATION
```

---

## 9–12. REBUILD, SCAR, CLEAN STRUCTURE, SEEDER

Historical material: evidence, provenance, regression, adversarial, scar, replay — not automatic current trust.

```text
HISTORICAL ≠ CURRENT TRUST · SCAR ≠ AUTHORITY · SCAR ≠ CURRENT VERIFICATION
NEW → NEW (default) · NEW → SEEDED_REFERENCE (controlled) · NEW → OLD_IMPLEMENTATION (forbidden unless explicit)
```

Seeder: classify → validate → select → seed with provenance.

---

## 13–19. TOKEN, IDENTIFIER, RESERVED, PROTECTED, OPERATORS, REGISTRY, LOOKUP

```text
TOKEN CATEGORY ≠ REGISTRY
RESERVED ≠ PROTECTED
OPERATOR ≠ IDENTIFIER REGISTRY · LITERAL ≠ IDENTIFIER REGISTRY
LOOKUP ERROR ≠ LOOKUP MISS
LEXICAL VALIDITY → IDENTIFIER VALIDITY → REGISTRY LOOKUP
```

---

## 20–22. DIAGNOSTICS

Learner-facing vs implementation diagnostics. Multiple failures: collect → normalize → dedupe → causal graph → precedence → stable tie-break → primary → suppressed descendants (retained for audit).

---

## 23–25. NODE, EDGE, DEPENDENCY

```text
NODE EXISTS ≠ NODE AUTHORIZED
EDGE EXISTS ≠ TRANSITION AUTHORIZED
```

Dependencies: explicit, typed, validated; invalid/missing/stale/unverified/conflicting/forbidden block required transitions.

---

## 26–27. LAW / POLICY · POLICY-BOUNDED WORKFLOW

```text
INGESTED ≠ VALIDATED ≠ APPLICABLE ≠ AUTHORIZED ≠ EXECUTABLE
CAPABILITY ≠ POLICY

PURPOSE → POLICY → POLICY-DEFINED WORKFLOW → SWI STRUCTURE
  → VALIDATION → EVIDENCE → ADMISSION → VERIFICATION
  → HUMAN AUTHORITY → AUTHORIZATION → ACTION
```

Undefined policy where required → DO NOT INFER → REVIEW / ESCALATE / BLOCK.

---

## 28–31. OFFLINE SCHOOL, PUBLICATION, SYNC, PRIVACY

Local hub + Wi-Fi/LAN + optional SMS = operational infrastructure, not human authority.

```text
LOCAL NODE ≠ HUMAN AUTHORITY · OFFLINE ≠ POLICY BYPASS
SMS ≠ AUTHORITY · CONNECTIVITY ≠ AUTHORIZATION
LOCAL_ACCESS ≠ UNIVERSAL_ACCESS
```

See `docs/SCHOOL_DEPLOYMENT_SPEC.md`, `docs/LOCAL_SCHOOL_RESILIENCE.md`.

---

## 32–39. EVIDENCE, ADMISSION, RETURNGATE, VERIFICATION, REPLAY, REPRODUCTION, SEAL

```text
EVIDENCE ≠ AUTHORITY · ADMITTED ≠ AUTHORIZED
REJECT → NO SILENT CONTINUATION
TESTED ≠ VERIFIED ≠ SEALED · SEALED OBJECT ≠ SEALED SYSTEM
SEALED ≠ PRODUCTION AUTHORIZATION
```

Lifecycle: Implemented → Tested → Diagnosed → Evidence → Replayed → Reproduced → Verified → Seal review → Sealed.

---

## 40–43. SECURITY, ZTA, OBSERVER, COMMON SENSE

```text
TLS / PKI / CERT / HSM / TPM / SIGNATURE VALID ↛ HUMAN AUTHORIZATION
ZTA_SIGNAL ≠ HUMAN_AUTHORITY · ZTA_ACCESS_DECISION ≠ SWI_AUTHORIZATION
OBSERVATION ≠ EXECUTION
```

---

## 44–47. EXECUTION GATE, DIAGNOSTIC-FIRST, REPAIR, AUDIT

Mandatory conditions (defined, implemented, dependencies, evidence, admitted, verified, authority, security, safety, production authorization) — any false → **BLOCK**.

Repair → retest → evidence → replay → reproduce → verify → review. Repair ≠ seal/production authority.

Audit: what, who, when, why, authority, evidence, resulting state.

---

## 48–54. ADVERSARIAL TESTING, SCHEMA, LIFECYCLE, CROSS-VERSION, FAILURE CODES, DETERMINISM

Every arrow on the master chain is an attack surface. ATM lifecycle: Defined → … → Verified (not auto-sealed). Deterministic primary failure selection. Stable failure codes.

---

## 55–60. STATE MACHINE, PROMOTION, PRODUCTION, CHANGE MANAGEMENT, FULL CHECK, SEAL IMPACT

```text
STATE EXISTS ≠ TRANSITION EXISTS ≠ GATES PASS ≠ AUTHORITY EXISTS ≠ AUTHORIZATION ≠ ACTION
NO EVIDENCE → NO PROMOTION
CI_GREEN ≠ PRODUCTION_AUTHORIZED
```

Every change: does it alter the **floor**? Most changes → `FLOOR_UNCHANGED`.

---

## 61–67. DOCUMENTATION, STATUS LANGUAGE, NO AUTOMATIC PROMOTION, REPO STRUCTURE, EXPERIMENTAL, EXTERNAL TESTS/TERMS

Precise vocabulary: Defined / Implemented / Tested / Evidence Captured / Replayed / Reproduced / Verified / Sealed / Production Authorized — never substituted.

```text
EXPERIMENTAL ≠ PRODUCTION
TEST TRANSFER ≠ FLOOR TRANSFER
```

---

## 68. COMPARISON RULE

Compare explicitly: floor, purpose, object model, rules, workflow, authority, security, evidence, test, execution, production boundary. Floor-level difference must remain visible.

---

## 69. IMPLEMENTATION CHECKLIST

**Before implementation:** floor, boundary, purpose, terms, authority, policy, security, safety, state, transition models defined.  
**During:** typed objects/registries, deterministic lookups/diagnostics, dependencies, evidence, audit, reject enforcement, authority checks, execution blocking.  
**Before verification:** tests, adversarial, evidence, replay, reproduction, cross-version, failure/suppression, security/safety.  
**Before sealing:** verification, dependencies, evidence, replay, reproduction, seal scope, impact, human review.  
**Before production:** purpose, policy, authority, human authorization, security, safety, production evidence, execution gate.

---

## 70. MASTER SWI INVARIANTS

(See §5 plus:)

```text
CAPABILITY ≠ POLICY ≠ IMPLEMENTATION ≠ EVIDENCE ≠ AUTHORITY
IMPLEMENTATION CHANGE ≠ FLOOR CHANGE
TESTING SWI ≠ TESTING ANOTHER SYSTEM
TEST TRANSFER ≠ FLOOR TRANSFER
```

---

## 71. FINAL EXECUTION RULE

```text
IF REQUIRED CONDITION UNKNOWN → DO NOT INFER → REVIEW / ESCALATE / BLOCK
IF REQUIRED EVIDENCE ABSENT → BLOCK PROMOTION
IF REQUIRED AUTHORITY ABSENT → BLOCK AUTHORIZATION
IF AUTHORIZATION ABSENT → BLOCK ACTION
IF SAFETY OR SECURITY FAILS → BLOCK ACTION
```

---

## 72. FINAL SYSTEM MODEL

```text
HUMAN PURPOSE → POLICY → WORKFLOW DEFINITION → SWI MODEL
  → OBSERVE / VALIDATE → ANALYSE / EVIDENCE → ADMISSION → VERIFICATION
  → HUMAN AUTHORITY → AUTHORIZATION → SECURITY / SAFETY → ACTION
```

Central responsibility: make conditions visible; prevent invalid or unauthorized transitions from silently becoming action.

---

## 73. CORE MANIFESTO

«SWI works with people, not instead of people…»  
`HELP PEOPLE ≠ REPLACE PEOPLE` · `TRUE ZERO = ZERO UNAUTHORIZED ACTION`

Full text: `docs/SWI_MANIFESTO.md`.

---

## 74. FINAL FLOOR RULE

The first question when discussing a system must be:

> **«What floor is this system built on?»**

Only after that question is answered should implementation, testing, terminology, evidence, and comparison be interpreted.

```text
For SWI:     FLOOR = INHERITED COMPUTATIONAL FLOOR
For another: FLOOR = THAT SYSTEM'S EXPLICITLY DEFINED FOUNDATION
```

The systems must not be conflated. **Different floor = different system.**
