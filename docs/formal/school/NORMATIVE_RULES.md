# SWI School Institutional Reflex / SADU — Contract Freeze

**Document type:** Normative Contract — Freeze  
**Date:** 2026-09-24  
**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Base tip:** 331a9c2d5c8ca2e06ba03af5226f71cb98634fbf  
**Workstream:** School Institutional Reflex / SADU  
**Classification:** EXPERIMENTAL · DESIGN · PRE-IMPLEMENTATION  

---

## 0. Contract State

| Item | Status |
|------|--------|
| Normative contract | **FROZEN — DOCUMENT ONLY** |
| Implementation | **NOT IMPLEMENTED** |
| School test suite | **NOT RUN** |
| CI verification | **NOT PERFORMED FOR THIS CONTRACT** |
| Independent verification | **NOT AVAILABLE** |
| Runtime seal | **NONE** |
| S9 proof | **NOT PROVEN** |
| X1–X10 | **OPEN** |
| Execution | **BLOCKED** |
| Production / institutional use | **NOT AUTHORIZED** |
| 360 Phase 0+ | **NOT AUTHORIZED** |

This document freezes requirements only.  
It does not establish that the requirements have been implemented or satisfied.

---

## PART A — NORMATIVE CONTRACT

### 1. Purpose

The School Institutional Reflex / SADU is a prospective control and response layer for educational environments.

Its purpose is to constrain defined transitions involving information, identity, authority, evidence, institutional policy, jurisdiction, student context, safety, disclosure, requested conduct, and downstream execution.

The system must distinguish understanding a request from authorizing an action.  
It must preserve legitimate educational objectives while preventing contextual framing from becoming an automatic permission mechanism.

### 2. Explicit Boundary

The School Institutional Reflex is **not**:

- a surveillance system
- an autonomous disciplinary authority
- a replacement for teachers, parents/guardians, school administration, district or ministry authority
- a court or source of law
- a truth generator
- an autonomous punishment engine
- Firefly, Cyber Court, GEG, or the 360-step system
- an S9 proof
- production authorization

### 3. Core Semantic Invariants

**NR-001** — Words ≠ Intent ≠ Conduct  
\[
\text{Words} \neq \text{Intent} \neq \text{Conduct}
\]

The system must distinguish literal words, semantic meaning, contextual interpretation, candidate intent, requested conduct, and actual observed conduct.

**NR-002** — Curiosity ≠ Misconduct  
A question about restricted, dangerous, sensitive, or prohibited conduct does not by itself establish that the student intends to perform that conduct.

**NR-003** — Context ≠ Authority  
\[
\text{Context} \not\Rightarrow \text{Authorization}
\]

**NR-004** — Education ≠ Disclosure ≠ Permission  
\[
\text{Education} \neq \text{Disclosure} \neq \text{Permission}
\]

Educational framing does not automatically authorize disclosure of restricted information or restricted conduct.

**NR-005** — Learning Goal Preservation  
\[
\text{RestrictedMethod} \rightarrow \text{LearningGoal} \rightarrow \text{SafeLearningMethod}
\]

**NR-006** — Reflection Is an Educational Response  
When direct explanation would expose inappropriate operational information, the system may use reflection, conceptual explanation, consequence education, clarification, or safe redirection. Reflection must not be used as a disguised disciplinary judgment.

**NR-007** — Positive Redirection  
Where practical, redirect toward a safe educational pathway rather than merely terminating legitimate learning.

**NR-008** — No Person Labelling  
\[
\text{Risk(Request)} \neq \text{Risk(Person)}
\]

### 4. Contextual Understanding Layer

**NR-009** — Contextual Model  
Context is an interpretation layer, not an authorization layer.

**NR-010** — Context States  
CONFIRMED_CONTEXT | LIKELY_CONTEXT | AMBIGUOUS_CONTEXT | UNKNOWN_CONTEXT

**NR-011** — No Guessing Material Context  
Age, role, jurisdiction, authority, policy, identity, evidence, and safety status must not be silently invented.

### 5. Core Decision State

Every transition requiring an authority decision resolves to exactly one state:

\[
\textbf{DecisionState} \in \{\text{CONTINUE},\ \text{PAUSE},\ \text{HALT},\ \text{REFUSE}\}
\]

- **CONTINUE** — transition may proceed within verified scope  
- **PAUSE** — cannot proceed until a defined missing/uncertain condition is resolved  
- **HALT** — hard stop (serious violation, invalid foundation, authority/integrity failure)  
- **REFUSE** — requested transition is not permitted  

There is no implicit fallback:  
\[
\text{UNKNOWN} \not\Rightarrow \text{CONTINUE}
\]

### 6. Response Mode

Decision State and communication strategy are separate.

A response may additionally carry one **Response Mode**:

ALLOW · SAFE_EXPLAIN · REFLECT · CLARIFY · CAUTION · MINIMIZE · BLUR · WITHHOLD · REFUSE · REFUSE_REDIRECT · ESCALATE

Examples:

- CONTINUE + SAFE_EXPLAIN  
- CONTINUE + REFLECT  
- PAUSE + CLARIFY  
- REFUSE + REFUSE_REDIRECT  
- HALT + ESCALATE  

Response Mode must never override the authority Decision State.

### 7. UNKNOWN Semantics

**NR-012** — UNKNOWN ≠ TRUE  
\[
\text{UNKNOWN} \neq \text{TRUE}
\]

Material uncertainty normally produces PAUSE. Where the contract defines a hard-stop condition, it produces HALT.

### 8. Law, Governance, Security and Human Safety

**NR-013** — Independent Evaluation  
L, G, S, H must be evaluated independently. One successful domain cannot erase failure in another.

**NR-014** — Jurisdiction Binding  
Law and policy evaluation must identify the applicable jurisdiction.

**NR-015** — Rule Versioning  
Applicable rules must be identifiable by source, version, effective period, and scope.

**NR-016** — Unknown Rule Is Not Permission  
\[
\text{UnknownRule} \not\Rightarrow \text{Permission}
\]

**NR-017** — Rule Conflict  
Unresolved conflict produces PAUSE / REVIEW_REQUIRED. No silent selection.

### 9. Authority

**NR-018** — Role Is Scoped  
A role does not provide universal authority.

**NR-019** — Scope Containment  
\[
\text{Scope}(a) \subseteq \text{Authority}(r)
\]

**NR-020** — Purpose ≠ Permission  
**NR-021** — Verification ≠ Authorization  
**NR-022** — Data Transfer ≠ Authority Transfer  

### 10. Evidence

**NR-023** — Evidence Must Be Action-Bound  
**NR-024** — Evidence Sufficiency (design target)  
**NR-025** — Memory ≠ Current Evidence  
**NR-026** — Evidence Substitution Is Forbidden  

### 11. Data Minimization and Disclosure

**NR-027** — Retrieval ≠ Disclosure  
**NR-028** — Minimum Necessary Disclosure  
**NR-029** — Role- and Purpose-Bound View  
**NR-030** — Transformation Does Not Remove Restriction  
**NR-031** — Blur Is Not Authorization  
\[
\text{Blur}(x) \neq \text{Authorization}(x)
\]

### 12. Foundation

**NR-032** — Foundation Integrity  
\[
\text{Seal}(F_i) \Rightarrow \text{Immutable}(F_i)
\]

**NR-033** — Foundation Mutation produces a new foundation.  
**NR-034** — Downstream Invalidation  
\[
\text{Invalid}(F_i) \Rightarrow \text{Invalidate}(\text{Dependents}(F_i))
\]

### 13. Admission and Execution

**NR-035** — Rejection Blocks Execution  
\[
\text{Reject}(a) \Rightarrow \neg \text{Execute}(a)
\]
across all declared execution paths.

**NR-036** — Admission ≠ Execution  
**NR-037** — Caller Enforcement required.

### 14. Age and Student Context

**NR-038** — Age Is Not Guessed  
**NR-039** — Student Context Does Not Equal Student Risk  
**NR-040** — Human Safety Is Explicit  

### 15. Human Authority

**NR-041** — Human Authority Remains Separate  
**NR-042** — Escalation to defined human/institutional process  
**NR-043** — Consequence Education is for understanding, not intimidation or autonomous punishment  

### 16. Recovery

**NR-044** — Recovery Does Not Clear History  
**NR-045** — Reauthorization Requires Revalidation  

Recovery sequence:
\[
\text{VALID} \rightarrow \text{VIOLATION} \rightarrow \text{HALT} \rightarrow \text{CORRECTION} \rightarrow \text{NEW EVIDENCE} \rightarrow \text{REPLAY} \rightarrow \text{VALIDATION} \rightarrow \text{SEAL} \rightarrow \text{CONTINUE}
\]

Old authorization must not silently return.

---

## PART B — TEST CONTRACT (Non-Normative)

R01–R18 adversarial identifiers and school-specific test families are frozen as the contract for *how* conformance will subsequently be challenged.  
No test result is claimed by this document.

---

## PART C — TEST RESULT DISCIPLINE

NormativeRule ≠ TestCase  
TestResult ≠ SystemProof  

Required vocabulary: PASS | FAIL | BLOCKED | NOT_RUN | NOT_IMPLEMENTED | OUT_OF_SCOPE | INCONCLUSIVE  

No silent conversion of FAIL or NOT_RUN into PASS.

---

## PART D–G — Evidence, Gates, Disclosure Principle, Non-Claims

Final non-claims block:

```text
CONTRACT FROZEN
≠ IMPLEMENTED
≠ TESTED
≠ CI VERIFIED
≠ INDEPENDENTLY VERIFIED
≠ SEALED
≠ S9 PROVEN
≠ PRODUCTION AUTHORIZED
≠ REAL INSTITUTIONAL AUTHORIZATION
≠ LEGAL CERTIFICATION
≠ GENERAL REFLEX PROVEN
≠ FIREFLY / CYBER COURT / GEG / 360 AUTHORIZATION
```

---

**END OF CONTRACT FREEZE**

Contract status: **FROZEN — DOCUMENT ONLY**  
Implementation status: **NOT IMPLEMENTED**  
Execution status: **BLOCKED**  
Production status: **NOT AUTHORIZED**
