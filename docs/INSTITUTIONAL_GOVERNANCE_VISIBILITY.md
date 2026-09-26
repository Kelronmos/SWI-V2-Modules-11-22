# Governance Communication + Authority Visibility

**Status:** DRAFT — IMPLEMENTATION SPECIFICATION  
**System:** SWI / SAMH Institutional Governance (design)  
**Seal:** NOT SEALED  
**Production:** BLOCKED  
**Date:** 26 September 2026

> Who can see what, at what level of detail, for what purpose, under which authority, for how long, and what they are prohibited from doing with it?

Related: `docs/SCHOOL_DEPLOYMENT_SPEC.md` · `docs/PROGRAM_PROOF_BOUNDARY.md`

---

## 1. Core principle

Governance travels downward as an explicit chain:

```text
LAW → REGULATION → POLICY → STANDARD → GOVERNANCE RULE
  → ROLE AUTHORITY → RELATIONSHIP → PURPOSE → DATA SCOPE
  → DETAIL LEVEL → ACTION PERMISSION → AUDIT
```

Upstream provides evidence and accountability (not automatic authority escalation):

```text
EVENT → EVIDENCE → AUTHORIZED ACTOR → AUTHORIZED REPORT
  → AGGREGATION / REDACTION → … → MINISTRY / GOVERNMENT
```

```text
UPSTREAM ≠ AUTHORITY ESCALATION
DOWNSTREAM ≠ AUTOMATIC EXECUTION
```

No layer silently invents authority for the next.

---

## 2. Authority questions (all required)

WHO · WHAT · WHY · WHICH SUBJECT/GROUP · WHICH DATA · WHAT DETAIL · WHICH PURPOSE · WHICH POLICY · WHICH AUTHORITY · HOW LONG · WHAT ACTION · WHO APPROVED · WHAT AUDIT

If unanswered → **ACCESS = BLOCKED**

---

## 3. Detail levels (not binary)

| Level | Meaning |
|-------|---------|
| L0 | NONE |
| L1 | EXISTENCE |
| L2 | AGGREGATE |
| L3 | DE-IDENTIFIED |
| L4 | PSEUDONYMISED |
| L5 | RELATIONSHIP-LIMITED INDIVIDUAL |
| L6 | IDENTIFIED INDIVIDUAL |
| L7 | SENSITIVE DETAIL |
| L8 | RESTRICTED PROFESSIONAL DETAIL |

Higher organizational rank ≠ automatic higher detail.  
MINISTRY ≠ automatic access to all student records.  
TEACHER ≠ automatic counselling notes.

---

## 4. Permission equation

```text
PERMISSION =
  ROLE ∩ RELATIONSHIP ∩ PURPOSE ∩ DATA ∩ DETAIL
  ∩ POLICY ∩ TIME ∩ AUTHORITY
```

Role alone is insufficient. Machine-readable authority registry entries include: role, resource, scope, detail_level, purpose, actions, prohibited, approval, audit.

---

## 5. Separate concepts

```text
DATA SUBJECT ≠ DATA STEWARD ≠ ACCESS AUTHORITY ≠ ACTION AUTHORITY ≠ AUDITOR
SYSTEM ADMIN ≠ POLICY AUTHORITY ≠ COUNSELLING AUTHORITY ≠ LEGAL AUTHORITY
```

---

## 6. Institutional actors (bounded nodes)

Student · Parent · Teacher · School Admin · Counselling · Community · Ministry · Government  

Each: inputs, outputs, visible/restricted data, authority, non-authority, escalation, audit.

**Counselling** remains a human-support boundary, not an AI diagnosis engine.  
**Ministry** defaults to aggregate/de-identified unless a specific lawful workflow requires otherwise.  
**Government** policy flows as LAW → POLICY → STANDARD → AUTHORIZED PROGRAM — not POLICY → AUTOMATIC STUDENT ACTION.

Upstream ≠ authority escalation. Downstream ≠ automatic execution.

Central contract for every transition:

```text
DATA → SIGNAL → EVIDENCE → INTERPRETATION → RECOMMENDATION
  → HUMAN REVIEW → AUTHORIZATION → ACTION
```

---

## 7. Explain authority (not grant)

`explain_authority`: ALLOW/BLOCK with numbered reasons and limitations.  
Human-readable **authority card**: what you can see / cannot see / may / may not.

```text
AI EXPLAINS AUTHORITY ≠ AI CREATES AUTHORITY
```

Governance updates produce communication records (policy, change, effective date, affected roles/resources, previous/new detail, acknowledgement, verification pending).

---

## 8. Upstream / downstream transforms

Upstream: RAW → VALIDATE → MINIMIZE → AGGREGATE → DE-IDENTIFY → AUTHORIZE → REPORT  
Downstream: POLICY → PROGRAM → RULE → SCHOOL CONFIG → ROLE INSTRUCTION → USER COMMUNICATION (with version, authority, acknowledgement).

---

## 9. Test families (design)

T01–T12 relationship flows; A01–A15 boundary attacks (role/relationship/purpose spoof, detail escalation, expired authority, AI self-authorization, signature-as-authority, upstream privilege inheritance, etc.).  
Outcomes: ALLOW | REDACT | AGGREGATE | REJECT | HALT | ESCALATE — not merely PASS/FAIL.

Governance communication tests G-001…: access **and** correct boundary explanation.

---

## 10. Implementation order (authority graph before UI)

```text
1  ACTOR REGISTRY
2  RELATIONSHIP REGISTRY
3  RESOURCE / DATA CLASSIFICATION
4  DETAIL-LEVEL REGISTRY
5  PURPOSE REGISTRY
6  GOVERNANCE / POLICY REGISTRY
7  AUTHORITY REGISTRY
8  PERMISSION EVALUATOR
9  AUTHORITY EXPLANATION ENGINE
10 UPSTREAM/DOWNSTREAM FLOW ENGINE
11 AUDIT + SEMANTIC SCARS
12 ADVERSARIAL TEST SUITE
13 REPLAY
14 FULL REGRESSION
15 INDEPENDENT REVIEW
16 SCOPED SEAL
```

**Do not start with dashboards.** The dashboard is the surface; the authority graph is the foundation.

Core institutional test:

> Can SWI demonstrate, test, explain, replay, and (eventually) scoped-seal **exactly why** each actor can see each piece of information at each detail level—and **exactly why** they cannot see or do more?

---

## 11. SWI as control plane (not a new authority)

```text
        GOVERNMENT ↔ MINISTRY ↔ DISTRICT/COMMUNITY ↔ SCHOOL ADMIN
              ↙                    ↘
         TEACHER              COUNSELLING
              ↕                    ↕
           PARENT ←→ STUDENT
                    │
              SWI CONTROL
         (governance, authority, provenance, evidence,
          privacy, security, verification, audit/replay)
```

Seal, when ever granted, is **scoped** (flows, tests, evidence, limitations).  
Never: SAMH = PROVEN · SWI = PRODUCTION AUTHORIZED from graph unit tests alone.

**Non-claims:** Design specification only; no implemented actor graph, no real student data, no production deployment.
