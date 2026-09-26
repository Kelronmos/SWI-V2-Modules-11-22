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

It must not silently automate away: human judgment; dignity; accountability; consent; context; required human authority; human oversight.

> «SWI optimizes human capacity. It does not optimize humans out of the system.»

---

## 1A. Audience and Intended Use

| Audience | Intended use |
|----------|----------------|
| People who use SWI | Understand workflows, review evidence, receive diagnostics, make informed decisions, retain accountability |
| Workflow owners / operators | Structure processes, define responsibilities, identify bottlenecks, enforce gates, improve operational capacity |
| Developers / engineers | Implement architecture, transitions, registries, evidence, privacy boundaries, execution controls |
| Security / privacy practitioners | Integrity, access, privacy domains, adversarial paths, security-context integration |
| Auditors / reviewers | Reconstruct events, inspect evidence, verify decisions, identify control failures |
| Governance / accountable authorities | Policy, human authority, seal review, authorize consequential actions where appropriate |
| Researchers / educators | Workflow integrity, human-machine collaboration, deterministic diagnostics, controlled automation |
| Organizations adopting SWI | Institutional capacity with human oversight and accountability |
| **Schools (deployment use-case)** | Local resilience when Internet fails; authorized local updates under school policy |

### Intended use

SWI is a **human-centred, policy-bounded** workflow intelligence and governance system.

Intended uses include: structuring complex workflows; reducing repetitive verification work; helping people understand dependencies; identifying missing or conflicting conditions; validating defined requirements; preserving evidence and provenance; replay and reproduction; detecting tampering and unsafe transitions; least-privilege and purpose-bound access; deterministic diagnostics; supporting human decision-making; preventing unauthorized transitions; auditable consequential decisions; **school continuity under local resilience infrastructure** (see below).

### School Deployment / Local Resilience (intended use — not a core module)

SWI may be deployed **alongside** school-local communication and information infrastructure so that students and staff continue receiving **authorized** local updates when external Internet is unavailable.

> «Network failure should not automatically become information failure.»

This capability is **operational infrastructure**. It is **not**, by itself, SWI production authorization.

Full specification: `docs/SCHOOL_DEPLOYMENT_SPEC.md` · architecture: `docs/LOCAL_SCHOOL_RESILIENCE.md`.

Summary boundary:

```text
SCHOOL POLICY → DEFINED WORKFLOW → SWI STRUCTURES / VALIDATES / RECORDS
  → HUMAN AUTHORITY → AUTHORIZED OPERATION

LOCAL WIFI ↛ SWI DECIDES SCHOOL POLICY
INTERNET DOWN ≠ POLICY DOWN ≠ AUTHORITY DOWN ≠ GOVERNANCE BYPASS
```

### What SWI is not intended to be

Not: a replacement for human decision-makers; an autonomous authority; a substitute for legal or institutional governance; a manufacturer of consent; a converter of technical verification into human authorization; a bypass of accountable people; a universal Zero Trust product; efficiency as justification for removing oversight; offline/local-mesh as a governance or **policy** bypass; a policy-maker for the institution.

### Intended relationship

```text
PERSON → INTENT / CONTEXT → SWI → STRUCTURE / ANALYSE / VERIFY / EXPLAIN
  → EVIDENCE + OPTIONS + RISKS + DIAGNOSTICS → PERSON
  → JUDGMENT / AUTHORITY → AUTHORIZATION → ACTION
```

> Use machines for what machines are good at; preserve people for judgment, responsibility, context, dignity, and authority.

---

## 2. The Human Remains Accountable

```text
OBSERVATION ≠ ANALYSIS ≠ RECOMMENDATION ≠ DECISION
  ≠ AUTHORITY ≠ AUTHORIZATION ≠ ACTION
```

SWI may observe, structure, analyse defined conditions, detect failures, validate requirements, preserve evidence, replay, diagnose, recommend, and block unauthorized transitions.

SWI must not manufacture human judgment, consent, human/legal/policy authority, authorization, or production permission.

---

## 3. True Zero

> «True Zero means zero unauthorized action.» (Not zero humans.)

Missing mandatory conditions → REJECT / BLOCK / QUARANTINE as appropriate. Do not fill gaps with assumptions.

---

## 4. The Canonical SWI Flow

```text
INPUT → TOKEN → IDENTIFIER → REGISTRY → NODE → EDGE → DEPENDENCY
  → VALIDATION → EVIDENCE → ADMISSION → VERIFICATION → HUMAN AUTHORITY
  → PRIVACY → SECURITY → SAFETY → AUTHORIZATION → ACTION
```

Every arrow is a testable boundary.

---

## 5. Non-Substitution

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ VERIFICATION ≠ HUMAN AUTHORITY ≠ AUTHORIZATION ≠ ACTION
CI_GREEN / SIGNATURE / CERT / TPM / HSM / DEVICE / ZTA_GRANT ↛ HUMAN_AUTHORITY / SWI_AUTHORIZATION
TESTED ≠ SEALED
SIGNATURE ≠ AUTHORITY
CI_GREEN ≠ PRODUCTION_AUTHORIZATION
```

---

## 6–7. Human Capacity and Optimization Boundary

Help capacity; do not reduce people to scores or automation targets. Optimize process metrics; do not optimize away dignity, judgment, accountability, consent, context, authority, or oversight.

> «Automating work is not the same as automating responsibility.»

---

## 8. Human Authority

Explicit, scoped authority records. Code ownership, CI, certificates, TPM/HSM, device posture, ZTA grants do not automatically create authority.

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

## 10–11. Failure Is Information · Deterministic Diagnostics

Primary root failure; suppressed descendants retained for audit. Same conditions → same primary; no order-dependent selection.

---

## 12–13. Closed Transitions · Tamper and Recovery

State existence ≠ transition permission ≠ gates pass. Undefined → REJECT; failed gate → BLOCK; integrity → QUARANTINE. Tamper → quarantine; no silent re-entry on old trust.

---

## 14–15. Privacy · Zero Trust

Domain-bound access. ZTA is security context, not SWI authority. See `docs/ZERO_TRUST_RELATIONSHIP.md`.

---

## 16–18. Common Sense · Law · Repository Ownership

Analysis ≠ authorization. Ingested ≠ executable policy. Location ≠ ownership ≠ authority. See ownership map.

---

## 19–21. Implementation Test · Rebuild · Commitment

Five human-centred questions before promotion. Rebuild preserves accountability. Keep consequential humans visible and in control.

---

## 22. Local School Resilience

Support schools when external connectivity fails. Local Wi-Fi, hub, SMS, or mesh are **means** of carrying out a **policy-defined** workflow — not independent authority.

```text
POLICY → WHO MAY PUBLISH? → WHAT? → WHO RECEIVES? → WHAT APPROVAL?
  → SWI STRUCTURES THAT WORKFLOW → LOCAL HUB / WIFI / SMS

INTERNET DOWN ≠ POLICY DOWN ≠ AUTHORITY DOWN ≠ GOVERNANCE BYPASS
NETWORK DOWN ≠ WORKFLOW DOWN
OFFLINE_MODE ≠ BYPASS_MODE
LOCAL_NODE ≠ HUMAN_AUTHORITY
SMS ≠ AUTHORITY
CACHED_DATA ≠ CURRENT_TRUTH
LOCAL_AVAILABILITY ≠ PERMISSION
```

Details: `docs/LOCAL_SCHOOL_RESILIENCE.md` · `docs/SCHOOL_DEPLOYMENT_SPEC.md`.

---

## 23. Policy-Bounded Workflow

> SWI structures a workflow defined by policy; it does not become the policy-maker.

SWI structures workflows around policies defined by the **responsible institution**. SWI does **not** create institutional policy merely because a workflow can be implemented technically.

### Hierarchy

```text
HUMAN / INSTITUTIONAL PURPOSE
        ↓
POLICY
        ↓
POLICY-DEFINED WORKFLOW
        ↓
SWI STRUCTURE
        ↓
VALIDATION
        ↓
EVIDENCE
        ↓
ADMISSION
        ↓
VERIFICATION
        ↓
HUMAN AUTHORITY
        ↓
AUTHORIZATION
        ↓
ACTION
```

### Policy comes before workflow

```text
POLICY ≠ IMPLEMENTATION ≠ DATA ≠ EVIDENCE ≠ AUTHORIZATION ≠ ACTION
```

SWI may structure, validate, test, document, monitor, and evidence a **policy-defined** workflow.

SWI must **not** silently invent: institutional policy; permissions; responsibilities; consent; legal authority; publication authority; disciplinary authority; emergency authority; student entitlements; staff authority.

Where policy is undefined or insufficient, the workflow enters **REVIEW / BLOCK / ESCALATION** — not inference that fills the gap.

### SWI answers vs does not answer

| SWI answers | SWI does not answer |
|-------------|---------------------|
| Given the policy, what workflow must be followed? | What should the institution’s policy be? |
| What conditions and evidence are required? | What permissions should exist? |
| What transitions are permitted? | Who should hold institutional authority? |

(Policy development is a separate human institutional activity when explicitly defined as such.)

### Fundamental boundary (refined)

> **POLICY DEFINES THE INSTITUTIONALLY PERMITTED WORKFLOW AND ITS GOVERNANCE BOUNDARIES.**

Policy does not necessarily define every possible action in the world; it defines the rules and boundaries **relevant to the institution**.

```text
POLICY DEFINES THE INSTITUTIONALLY PERMITTED WORKFLOW AND ITS GOVERNANCE BOUNDARIES.
SWI STRUCTURES THE WORKFLOW WITHIN THOSE BOUNDARIES.
HUMANS RETAIN AUTHORITY OVER CONSEQUENCES.
INFRASTRUCTURE PROVIDES THE MEANS OF OPERATION.

NONE OF THESE BECOME THE OTHER.
```

### Strongest non-substitution chain

```text
CAPABILITY      ≠ POLICY
POLICY          ≠ IMPLEMENTATION
IMPLEMENTATION  ≠ EVIDENCE
EVIDENCE        ≠ AUTHORITY
AUTHORITY       ≠ AUTHORIZATION
AUTHORIZATION   ≠ ACTION
```

Connected to existing doctrine:

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
TESTED ≠ SEALED
SIGNATURE ≠ AUTHORITY
CI_GREEN ≠ PRODUCTION_AUTHORIZATION
```

Offline and local networks change **connectivity**, not institutional authority.

```text
OFFLINE ≠ POLICY BYPASS
LOCAL NODE ≠ POLICY MAKER
LOCAL NETWORK ≠ AUTHORITY
INTERNET DOWN ≠ POLICY DOWN ≠ AUTHORITY DOWN ≠ GOVERNANCE BYPASS
```

This states where SWI’s responsibility **starts** (structuring a policy-defined workflow) and where it **stops** (it does not invent policy or hold consequential authority).

---

## FINAL SWI PRINCIPLE

> «SWI works with people, not instead of people. It extends human capacity without erasing human responsibility. It structures complexity without pretending complexity is certainty. It automates verification where appropriate without manufacturing authority. It blocks unsafe and unauthorized paths rather than hiding them. And when a consequential decision belongs to a human, SWI keeps that human visible, accountable, informed, and in control.»

```text
HELP PEOPLE        ≠ REPLACE PEOPLE
AUTOMATE WORK      ≠ AUTOMATE ACCOUNTABILITY
OPTIMIZE CAPACITY  ≠ REMOVE HUMANITY
TRUE ZERO          = ZERO UNAUTHORIZED ACTION
NETWORK DOWN       ≠ WORKFLOW DOWN
OFFLINE_MODE       ≠ BYPASS_MODE
INTERNET DOWN      ≠ POLICY DOWN ≠ AUTHORITY DOWN ≠ GOVERNANCE BYPASS

CAPABILITY         ≠ POLICY
POLICY             ≠ IMPLEMENTATION
IMPLEMENTATION     ≠ EVIDENCE
EVIDENCE           ≠ AUTHORITY
AUTHORITY          ≠ AUTHORIZATION
AUTHORIZATION      ≠ ACTION

TESTED ≠ SEALED · SIGNATURE ≠ AUTHORITY · CI_GREEN ≠ PRODUCTION_AUTHORIZATION
```

**SWI: Structured Workflow Intelligence — technology in service of human capacity, accountability, and agency.**
