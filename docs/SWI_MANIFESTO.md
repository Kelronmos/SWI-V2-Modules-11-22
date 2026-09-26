# SWI MANIFESTO

**Structured Workflow Intelligence (SWI)**

| Field | Value |
|-------|--------|
| **Status** | NORMATIVE DESIGN / REBUILD CONTRACT |
| **Production** | BLOCKED unless separately and explicitly authorized |
| **Seal** | This manifesto does not create, extend, or imply a seal |
| **Date** | 26 September 2026 |

---

## 1. Why SWI Exists

SWI is built to work with people, not to replace people.

Its purpose is to optimize human capacity without removing humanity from the workflow.

SWI should help people handle complexity, reduce avoidable workload, identify failures, preserve evidence, understand dependencies, challenge assumptions, and make better-informed decisions.

SWI can automate structure and verification where appropriate.

It must not silently automate away:

- human judgment;
- human dignity;
- human accountability;
- consent;
- context;
- required human authority;
- human oversight.

> «SWI optimizes human capacity. It does not optimize humans out of the system.»

---

## 1A. Audience and Intended Use

SWI is intended for several audiences, with different purposes:

| Audience | Intended use |
|----------|----------------|
| **People who use SWI** | Understand workflows, review evidence, receive diagnostics, make informed decisions, and retain accountability |
| **Workflow owners / operators** | Structure processes, define responsibilities, identify bottlenecks, enforce gates, and improve operational capacity |
| **Developers / engineers** | Implement the SWI architecture, state transitions, registries, evidence handling, privacy boundaries, and execution controls |
| **Security / privacy practitioners** | Examine integrity, access, privacy domains, adversarial paths, and security-context integration |
| **Auditors / reviewers** | Reconstruct what happened, inspect evidence, verify decisions, and identify control failures |
| **Governance / accountable authorities** | Define policy, exercise human authority, conduct seal review, and authorize consequential actions where appropriate |
| **Researchers / educators** | Study workflow integrity, human-machine collaboration, deterministic diagnostics, failure handling, and controlled automation |
| **Organizations adopting SWI** | Improve institutional capacity while preserving human oversight and accountability |

### Intended use

SWI is intended to be used as a **human-centred workflow intelligence and governance system**.

Its intended uses include:

- structuring complex workflows;
- reducing repetitive administrative and verification work;
- helping people understand dependencies and consequences;
- identifying missing or conflicting conditions;
- validating defined workflow requirements;
- preserving evidence and provenance;
- supporting replay and reproduction;
- detecting tampering and unsafe transitions;
- enforcing least-privilege and purpose-bound access;
- providing deterministic diagnostics;
- supporting human decision-making;
- preventing unauthorized workflow transitions;
- maintaining an auditable record of consequential decisions;
- supporting school continuity when external connectivity is unreliable (see §22).

### What SWI is not intended to be

SWI is **not** intended to be:

- a replacement for human decision-makers;
- an autonomous authority;
- a substitute for legal or institutional governance;
- a system that manufactures consent;
- a system that converts technical verification into human authorization;
- a mechanism for bypassing accountable people;
- a universal Zero Trust implementation;
- a system that treats efficiency as sufficient justification for removing human oversight;
- a system that treats offline or local-mesh operation as a bypass of governance.

### Intended relationship

```text
PERSON
  ↓
INTENT / CONTEXT
  ↓
SWI
  ↓
STRUCTURE / ANALYSE / VERIFY / EXPLAIN
  ↓
EVIDENCE + OPTIONS + RISKS + DIAGNOSTICS
  ↓
PERSON
  ↓
JUDGMENT / AUTHORITY
  ↓
AUTHORIZATION
  ↓
ACTION
```

The central design objective is therefore:

> Use machines for what machines are good at, preserve people for what requires human judgment, responsibility, context, dignity, and authority.

---

## 2. The Human Remains Accountable

SWI distinguishes:

```text
OBSERVATION ≠ ANALYSIS ≠ RECOMMENDATION ≠ DECISION
  ≠ AUTHORITY ≠ AUTHORIZATION ≠ ACTION
```

SWI may: observe; collect and structure information; analyse defined conditions; identify conflicts; detect failures; validate requirements; preserve provenance and evidence; replay and reproduce; generate diagnostics; recommend questions or next steps; block unauthorized transitions.

SWI must not manufacture or impersonate: human judgment; consent; human, legal, or policy authority; authorization; production permission.

When a consequential decision belongs to a human, the human remains accountable for that decision.

---

## 3. True Zero

True Zero does not mean zero humans.

> «True Zero means zero unauthorized action.»

A missing mandatory condition cannot silently become permission.

```text
No definition → REJECT · No valid transition → REJECT · No integrity → QUARANTINE
No evidence / admission / verification / human authority → BLOCK
No privacy basis → BLOCK / ESCALATE · No security / safety / authorization → BLOCK
```

The system does not fill a missing permission with an assumption.

---

## 4. The Canonical SWI Flow

```text
INPUT → TOKEN → IDENTIFIER → REGISTRY → NODE → EDGE → DEPENDENCY
  → VALIDATION → EVIDENCE → ADMISSION → VERIFICATION → HUMAN AUTHORITY
  → PRIVACY → SECURITY → SAFETY → AUTHORIZATION → ACTION
```

Every arrow is a boundary that can fail and can be tested. A later stage cannot silently satisfy an earlier missing stage.

---

## 5. Non-Substitution

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ VERIFICATION
  ≠ HUMAN AUTHORITY ≠ AUTHORIZATION ≠ ACTION

CI_GREEN / SIGNATURE / CERTIFICATE / TPM / HSM / DEVICE_COMPLIANT
  ↛ HUMAN_AUTHORITY
ZTA_GRANT ↛ SWI_AUTHORIZATION
```

Technical controls can provide evidence or security context. They do not become the accountable human decision.

---

## 6. Human Capacity

SWI helps people understand complexity, reduce repetition, find primary failures, preserve knowledge, distinguish claims from evidence, and retain responsibility for consequential decisions.

SWI must not reduce people to identity, score, credential, data source, risk score, or automation target.

---

## 7. The Optimization Boundary

SWI may optimize time, attention, repetition, complexity, error detection, evidence handling, clarity, coordination, and reproducibility.

SWI must not optimize away dignity, judgment, accountability, consent, context, human authority, or oversight.

> «Automating work is not the same as automating responsibility.»

---

## 8. Human Authority

Human authority must be explicit and scoped (issuer, actor, subject, action, scope, purpose, times, revocation, evidence, policy, audit).

`CODE_OWNER` / `CI_GREEN` / certificates / TPM / HSM / device compliance / ZTA grants do **not** automatically create authority.

```text
CODE_OWNER ≠ HUMAN_AUTHORITY ≠ SEAL_AUTHORITY ≠ PRODUCTION_AUTHORITY
```

---

## 9. Evidence Before Promotion

```text
CLAIM → IMPLEMENTATION → TEST → RESULT → EVIDENCE
  → REPLAY → REPRODUCTION → VERIFICATION → SEAL REVIEW → SEAL
```

> «No evidence → no promotion.» · «No verified path → no execution.»

---

## 10. Failure Is Information

Root failure remains primary; descendants may be suppressed for presentation but retained for audit. Suppression is not deletion. Do not promote a convenient descendant as primary.

---

## 11. Deterministic Diagnostics

Same controlled conditions → same diagnostic decision. Primary-failure selection must not depend on dictionary order, filesystem order, test insertion order, parallel completion order, arbitrary traversal, or error wording.

---

## 12. Closed Transitions

```text
STATE EXISTS ≠ TRANSITION EXISTS ≠ GATES PASS
  ≠ AUTHORITY EXISTS ≠ AUTHORIZATION ≠ ACTION

Undefined transition → REJECT
Defined + failed gate → BLOCK
Integrity failure → QUARANTINE
All required gates pass → ALLOW
```

REJECT/BLOCK do not mutate trusted state. No implicit reverse transitions.

---

## 13. Tamper and Recovery

```text
OBJECT → INTEGRITY CHECK → TAMPER → QUARANTINE → NO RE-ENTRY
  → HUMAN AUTHORITY → NEW VALIDATION → NEW EVIDENCE
  → NEW ADMISSION → NEW VERIFICATION → SEAL REVIEW
```

Old verification does not automatically become current after integrity-affecting change.

---

## 14. Privacy

```text
IDENTITY_ACCESS ≠ MEDICAL_ACCESS ≠ FAMILY_ACCESS ≠ EDUCATION_ACCESS
```

Access considers subject, purpose, scope, domain, authority, evidence. Human consequences matter.

---

## 15. Zero Trust and SWI

Zero Trust supplies security context / resource access. SWI supplies workflow integrity / transition control.

```text
ZTA_SIGNAL ≠ HUMAN_AUTHORITY
ZTA_ACCESS_DECISION ≠ SWI_AUTHORIZATION
```

See `docs/ZERO_TRUST_RELATIONSHIP.md`.

---

## 16. Common Sense

May observe, analyse, question, propose tests, diagnose. May not authorize, seal, promote, execute, override law/policy, or impersonate human authority.

```text
ANALYSIS ≠ AUTHORIZATION · RECOMMENDATION ≠ DECISION
```

---

## 17. Law and Policy

```text
INGESTED ≠ VALIDATED ≠ APPLICABLE ≠ AUTHORIZED ≠ EXECUTABLE
```

Do not manufacture permission from uncertainty.

---

## 18. Repository and Ownership

```text
LOCATION ≠ OWNERSHIP ≠ RESPONSIBILITY ≠ EVIDENCE
  ≠ VERIFICATION ≠ HUMAN AUTHORITY ≠ AUTHORIZATION ≠ ACTION
```

See `docs/REPOSITORY_OWNERSHIP_MAP.md`.

---

## 19. Human-Centred Implementation Test

1. What human capacity does this improve?  
2. What human responsibility does it preserve?  
3. What decision remains with a person?  
4. What can the system refuse or block?  
5. What evidence proves that the boundary works?

---

## 20. Rebuild Philosophy

```text
CLONE STRUCTURE → REBUILD TRUST → PROVE TRANSITIONS
  → PRESERVE HUMAN ACCOUNTABILITY → CONTROL ACTION
```

Historical evidence informs rebuild; it does not silently become current trust.

---

## 21. The SWI Commitment

SWI is judged by what it refuses to automate without accountability conditions, as much as by what it automates. Keep consequential humans visible, accountable, informed, authorized, and in control.

---

## 22. Local School Resilience

SWI should support schools where external connectivity is unreliable, interrupted, expensive, or unavailable.

A school should not become operationally blind solely because its Internet connection has failed.

SWI may therefore support a **local resilience layer**:

- local Wi-Fi and LAN;
- school-local SWI nodes;
- local content and update services;
- controlled synchronization;
- SMS-based fallback where appropriate;
- offline queues and reconciliation;
- local evidence and audit records.

The purpose is **continuity of useful, authorized information** — not bypassing governance.

### Offline-First Principle

```text
NETWORK DOWN ≠ WORKFLOW DOWN
```

When external connectivity is unavailable, the school may continue providing information that has **already been locally authorized** and made available for offline use (timetables, notices, assignments, learning resources, examination schedules, emergency information, teacher-approved material).

### Connectivity states

```text
ONLINE → CONNECTIVITY_DEGRADED → OFFLINE_LOCAL_MODE → LOCAL_OPERATION
  → SYNC_PENDING → CONNECTIVITY_RESTORED → RECONCILIATION
  → VERIFIED → SYNCED
```

### Hard boundaries

```text
OFFLINE_MODE ≠ BYPASS_MODE
LOCAL_NODE ≠ HUMAN_AUTHORITY
LOCAL_WIFI ≠ AUTHORIZATION
SMS ≠ AUTHORITY
SMS_RECEIVED ≠ VERIFIED_TRUTH
CACHED_DATA ≠ CURRENT_TRUTH
LOCAL_AVAILABILITY ≠ PERMISSION
OFFLINE_LOCAL_MODE ≠ PRODUCTION_AUTHORIZATION
```

### Local mesh (conceptual)

```text
STUDENT DEVICE → LOCAL WI-FI / LAN → SCHOOL LOCAL NODE
  → LOCAL CONTENT | UPDATES | DIAGNOSTICS | EVIDENCE | SYNC QUEUE
```

The local node provides continuity, not sovereignty over the wider system.

### SMS resilience

```text
AUTHORIZED SCHOOL SOURCE → MESSAGE VALIDATION → SMS GATEWAY → RECIPIENT
```

Receipt does not establish truth or authority. Preserve provenance; verify independently where required.

### Offline synchronization

```text
LOCAL CHANGE → VALIDATION → EVIDENCE → LOCAL STORAGE → SYNC_PENDING
  → CONNECTIVITY RESTORED → RECONCILIATION → VERIFICATION → AUTHORIZED SYNC
```

Conflicts must be surfaced, not silently overwritten.

### Student safety and privacy

Offline availability must not broaden distribution beyond least privilege, purpose limitation, privacy-domain separation, safety rules, institutional authority, auditability, and data minimization.

Connecting to the school network does not entitle a student to every local resource.

### Human-centred objective

> Keep people connected to useful information when infrastructure fails, without removing human responsibility or weakening the boundaries that protect them.

A resilient school is not one that operates without people. It is one that gives people enough reliable local infrastructure to continue learning, teaching, communicating, and responding while connectivity is restored.

Full architecture: `docs/LOCAL_SCHOOL_RESILIENCE.md`.

---

## FINAL SWI PRINCIPLE

> «SWI works with people, not instead of people. It extends human capacity without erasing human responsibility. It structures complexity without pretending complexity is certainty. It automates verification where appropriate without manufacturing authority. It blocks unsafe and unauthorized paths rather than hiding them. And when a consequential decision belongs to a human, SWI keeps that human visible, accountable, informed, and in control.»

```text
HELP PEOPLE           ≠ REPLACE PEOPLE
AUTOMATE WORK         ≠ AUTOMATE ACCOUNTABILITY
OPTIMIZE CAPACITY     ≠ REMOVE HUMANITY
TRUE ZERO             = ZERO UNAUTHORIZED ACTION
NETWORK DOWN          ≠ WORKFLOW DOWN
OFFLINE_MODE          ≠ BYPASS_MODE
```

**SWI: Structured Workflow Intelligence — technology in service of human capacity, accountability, and agency.**
