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
- maintaining an auditable record of consequential decisions.

### What SWI is not intended to be

SWI is **not** intended to be:

- a replacement for human decision-makers;
- an autonomous authority;
- a substitute for legal or institutional governance;
- a system that manufactures consent;
- a system that converts technical verification into human authorization;
- a mechanism for bypassing accountable people;
- a universal Zero Trust implementation;
- a system that treats efficiency as sufficient justification for removing human oversight.

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
OBSERVATION
    ≠
ANALYSIS
    ≠
RECOMMENDATION
    ≠
DECISION
    ≠
AUTHORITY
    ≠
AUTHORIZATION
    ≠
ACTION
```

SWI may:

- observe workflow state;
- collect information;
- structure information;
- analyse defined conditions;
- identify conflicts;
- detect failures;
- validate defined requirements;
- preserve provenance;
- preserve evidence;
- replay workflows;
- reproduce results;
- generate diagnostics;
- recommend questions or possible next steps;
- block unauthorized transitions.

SWI must not manufacture or impersonate:

- human judgment;
- human consent;
- human authority;
- legal authority;
- policy authority;
- authorization;
- production permission.

When a consequential decision belongs to a human, the human remains accountable for that decision.

---

## 3. True Zero

True Zero does not mean zero humans.

> «True Zero means zero unauthorized action.»

A missing mandatory condition cannot silently become permission.

```text
No definition              → REJECT
No valid transition        → REJECT
No integrity               → QUARANTINE
No evidence                → BLOCK
No admission               → BLOCK
No verification            → BLOCK
No human authority         → BLOCK
No privacy basis           → BLOCK / ESCALATE
No security basis          → BLOCK
No safety basis            → BLOCK
No authorization           → BLOCK
```

The system does not fill a missing permission with an assumption.

---

## 4. The Canonical SWI Flow

SWI follows a controlled progression:

```text
INPUT
  ↓
TOKEN
  ↓
IDENTIFIER
  ↓
REGISTRY
  ↓
NODE
  ↓
EDGE
  ↓
DEPENDENCY
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
PRIVACY
  ↓
SECURITY
  ↓
SAFETY
  ↓
AUTHORIZATION
  ↓
ACTION
```

Every arrow is a boundary.

Every boundary can fail.

Every boundary can therefore be tested.

A later stage cannot silently satisfy an earlier missing stage.

---

## 5. Non-Substitution

SWI preserves distinctions between things that may otherwise be incorrectly treated as equivalent.

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ VERIFICATION
  ≠ HUMAN AUTHORITY ≠ AUTHORIZATION ≠ ACTION
```

Technical signals do not become human authority merely because they are technically valid.

```text
CI_GREEN           ↛ HUMAN_AUTHORITY
SIGNATURE          ↛ HUMAN_AUTHORITY
CERTIFICATE        ↛ HUMAN_AUTHORITY
TPM                ↛ HUMAN_AUTHORITY
HSM                ↛ HUMAN_AUTHORITY
DEVICE_COMPLIANT   ↛ HUMAN_AUTHORITY
ZTA_GRANT          ↛ SWI_AUTHORIZATION
```

Technical controls can provide evidence, integrity information, security context, or other signals.

They do not become the accountable human decision.

---

## 6. Human Capacity

SWI exists to help people use their capacity more effectively.

It should help people:

- understand complex systems;
- reduce repetitive work;
- identify the primary failure;
- understand dependencies;
- find missing evidence;
- preserve institutional knowledge;
- distinguish claims from evidence;
- reproduce results;
- challenge unsafe assumptions;
- understand why a workflow was blocked;
- make decisions with better information;
- retain responsibility for consequential decisions.

SWI should not reduce people to:

```text
IDENTITY · SCORE · CREDENTIAL · DATA SOURCE · RISK SCORE · AUTOMATION TARGET
```

A person is more than the machine-readable representation of that person.

---

## 7. The Optimization Boundary

SWI may optimize:

```text
TIME · ATTENTION · REPETITION · COMPLEXITY · ERROR DETECTION
EVIDENCE HANDLING · WORKFLOW CLARITY · COORDINATION · REPRODUCIBILITY
```

SWI must not optimize away:

```text
DIGNITY · JUDGMENT · ACCOUNTABILITY · CONSENT
CONTEXT · HUMAN AUTHORITY · HUMAN OVERSIGHT
```

Efficiency is valuable only when accountability survives the optimization.

> «Automating work is not the same as automating responsibility.»

---

## 8. Human Authority

Human authority must be explicit and scoped.

A controlled authority record should identify, as applicable:

```text
authority_id
issuer
accountable_actor
subject
action
scope
purpose
decision
issued_at
expires_at
revocation_state
evidence_reference
policy_reference
audit_reference
```

The following do **not** automatically create authority:

```text
CODE_OWNER · REPOSITORY_ADMIN · CI_GREEN · SIGNATURE_VALID
CERTIFICATE_VALID · TPM_VERIFIED · HSM_SIGNED · DEVICE_COMPLIANT
ZTA_ACCESS_GRANTED
```

Therefore:

```text
CODE_OWNER ≠ HUMAN_AUTHORITY ≠ SEAL_AUTHORITY ≠ PRODUCTION_AUTHORITY
```

---

## 9. Evidence Before Promotion

SWI follows an evidence-first progression:

```text
CLAIM → IMPLEMENTATION → TEST → RESULT → EVIDENCE
  → REPLAY → REPRODUCTION → VERIFICATION → SEAL REVIEW → SEAL
```

Testing does not automatically create a seal.

Verification does not automatically create production authorization.

> «No evidence → no promotion.»  
> «No verified path → no execution.»

---

## 10. Failure Is Information

A failure is not permission to continue.

If `A → B → C → ACTION` and A is the root failure:

```text
A = PRIMARY FAILURE
B = SUPPRESSED DESCENDANT
C = SUPPRESSED DESCENDANT
ACTION = BLOCKED
```

Suppression does not mean deletion.

All relevant failures remain available for audit and analysis.

The system must not report a convenient descendant as the primary failure simply because the actual root failure is harder to explain.

---

## 11. Deterministic Diagnostics

The same controlled conditions should produce the same decision.

Primary-failure selection must not depend on:

- dictionary order;
- filesystem order;
- test insertion order;
- parallel completion order;
- arbitrary traversal order;
- wording of an error message.

Deterministic diagnostics are necessary for meaningful replay and reproduction.

---

## 12. Closed Transitions

SWI does not infer permission merely because a state exists.

```text
STATE EXISTS ≠ TRANSITION EXISTS ≠ GATES PASS
  ≠ AUTHORITY EXISTS ≠ AUTHORIZATION ≠ ACTION
```

Canonical transition behaviour:

```text
Undefined transition              → REJECT
Defined transition + failed gate  → BLOCK
Integrity failure                 → QUARANTINE
All required gates pass           → ALLOW
```

REJECT and BLOCK do not mutate trusted state.

QUARANTINE does not restore trust.

There are no implicit reverse transitions.

---

## 13. Tamper and Recovery

Tampering is a trust-boundary event.

```text
OBJECT → INTEGRITY CHECK → TAMPER DETECTED → QUARANTINE → NO RE-ENTRY
  → HUMAN AUTHORITY / ESCALATION → NEW VALIDATION → NEW EVIDENCE
  → NEW ADMISSION → NEW VERIFICATION → SEAL REVIEW
```

Old evidence may remain historical evidence.

Old verification does not automatically become current verification after an integrity-affecting change.

A previous signature, certificate, authorization, or successful test must not silently restore trust.

---

## 14. Privacy

SWI treats private information as domain-bound.

For example:

```text
IDENTITY_ACCESS ≠ MEDICAL_ACCESS
MEDICAL_ACCESS ≠ FAMILY_ACCESS
EDUCATION_ACCESS ≠ MEDICAL_ACCESS
```

Access must consider:

```text
SUBJECT · PURPOSE · SCOPE · DOMAIN · AUTHORITY · EVIDENCE
```

Knowing who someone is does not automatically create permission to access everything about them.

Human consequences matter.

SWI should expose important boundaries rather than hide them behind automation.

---

## 15. Zero Trust and SWI

Zero Trust Architecture provides security context.

SWI is not an implementation of NIST SP 800-207.

The distinction is:

```text
ZERO TRUST → SECURITY CONTEXT / RESOURCE ACCESS
SWI        → WORKFLOW INTEGRITY / TRANSITION CONTROL
```

Zero Trust signals may inform SWI security evaluation.

They do not replace SWI authority.

```text
ZTA_SIGNAL          ≠ HUMAN_AUTHORITY
ZTA_ACCESS_DECISION ≠ SWI_AUTHORIZATION
```

SWI retains its own evidence, admission, verification, authority, privacy, security, safety, and authorization boundaries.

See also: `docs/ZERO_TRUST_RELATIONSHIP.md`.

---

## 16. Common Sense

Common Sense may operate as an observer and analytical capability.

It may: observe; analyse; identify anomalies; question assumptions; propose tests; generate diagnostics; suggest possible paths.

It may **not**: AUTHORIZE; SEAL; PROMOTE; EXECUTE; OVERRIDE LAW; OVERRIDE POLICY; IMPERSONATE HUMAN AUTHORITY.

```text
ANALYSIS ≠ AUTHORIZATION
RECOMMENDATION ≠ DECISION
```

---

## 17. Law and Policy

SWI distinguishes:

```text
INGESTED ≠ VALIDATED ≠ APPLICABLE ≠ AUTHORIZED ≠ EXECUTABLE
```

A machine-readable rule is not automatically a legal determination.

Ambiguous, conflicting, expired, or inapplicable rules must be surfaced for appropriate human or institutional review.

The system must not manufacture permission from uncertainty.

---

## 18. Repository and Ownership

Every controlled SWI unit should identify:

```text
module_or_unit · repository · branch · path · owner · reviewer
responsibility · dependencies · evidence_scope · authority_boundary
seal_status · production_status
```

| Question | Answered by |
|----------|-------------|
| Where is it? | Repository / path |
| Who is accountable for it? | Ownership |
| Who may authorize the consequential decision? | Authority |

These are different questions.

```text
LOCATION ≠ OWNERSHIP ≠ RESPONSIBILITY ≠ EVIDENCE
  ≠ VERIFICATION ≠ HUMAN AUTHORITY ≠ AUTHORIZATION ≠ ACTION
```

Experimental code may generate evidence.

It must not manufacture seal status or production authorization.

See also: `docs/REPOSITORY_OWNERSHIP_MAP.md`.

---

## 19. Human-Centred Implementation Test

Before promoting a new SWI capability, ask:

1. What human capacity does this improve?
2. What human responsibility does it preserve?
3. What decision remains with a person?
4. What can the system refuse or block?
5. What evidence proves that the boundary works?

If these questions cannot be answered clearly, the capability is not ready for promotion.

---

## 20. Rebuild Philosophy

The SWI rebuild is not a race to make the machine more autonomous.

It is a process of making workflows more understandable, testable, reproducible, accountable, resistant to bypass, and safer for the people who rely on them.

```text
CLONE STRUCTURE → REBUILD TRUST → PROVE TRANSITIONS
  → PRESERVE HUMAN ACCOUNTABILITY → CONTROL ACTION
```

Historical evidence informs the rebuild.

Historical evidence does not silently become current trust.

---

## 21. The SWI Commitment

SWI will be judged not only by what it can automate, but by what it refuses to automate without the conditions required for accountability.

The system should make people more capable, not less human.

It should make complexity more understandable, not disguise uncertainty as certainty.

It should make evidence easier to inspect, not manufacture evidence.

It should make failures easier to find, not hide them.

It should make workflows more controlled, not make authority invisible.

And when a consequential decision belongs to a human, SWI should keep that human:

```text
VISIBLE · ACCOUNTABLE · INFORMED · AUTHORIZED · IN CONTROL
```

---

## FINAL SWI PRINCIPLE

> «SWI works with people, not instead of people. It extends human capacity without erasing human responsibility. It structures complexity without pretending complexity is certainty. It automates verification where appropriate without manufacturing authority. It blocks unsafe and unauthorized paths rather than hiding them. And when a consequential decision belongs to a human, SWI keeps that human visible, accountable, informed, and in control.»

```text
HELP PEOPLE           ≠ REPLACE PEOPLE
AUTOMATE WORK         ≠ AUTOMATE ACCOUNTABILITY
OPTIMIZE CAPACITY     ≠ REMOVE HUMANITY
TRUE ZERO             = ZERO UNAUTHORIZED ACTION
```

**SWI: Structured Workflow Intelligence — technology in service of human capacity, accountability, and agency.**
