SWI V2 — CONTROLLED EXECUTION & SEALING MANUAL

Modules 11–22

Repository: "Kelronmos/SWI-V2-Modules-11-22"

Purpose:
Provide a controlled, evidence-driven procedure for progressing SWI V2 from the current M11 state through Modules 11–22 without repeating the earlier mistake of confusing architectural intention with implemented capability.

---

1. GOVERNING LAW

The following rule governs every module:

«EVIDENCE BEFORE CLAIM.
BOUNDARY BEFORE EXPANSION.
PRE-NAME FOR UNDERSTANDING.
CONTRACT BEFORE IMPLEMENTATION.
CODE FOR IMPLEMENTATION.
TEST FOR BEHAVIOUR.
CI FOR REPRODUCIBILITY.
AUDIT FOR CONFIDENCE.
SEAL FOR CONTROLLED DEPENDENCY.
DEPENDENCY BEFORE THE NEXT MODULE.
NEVER CLAIM WHAT THE CODE CANNOT DEMONSTRATE.»

A module is never considered complete merely because:

- the folder exists;
- the function exists;
- the tests pass locally;
- the README describes it;
- the architecture diagram contains it;
- an AI agent says it is implemented.

The evidence must demonstrate the actual boundary and behaviour.

---

2. CURRENT POSITION

The V2 architecture begins with the V1 foundation.

The intended controlled path is:

V1 Foundation
↓
Serialized V1 Evidence
↓
M11 Admission
↓
M11 Audit
↓
Two-Checkout CI
↓
M11 SEALED
↓
M12 Contract
↓
M12 Implementation
↓
M12 Tests
↓
M12 CI
↓
M12 Audit
↓
M12 SEALED
↓
Architecture Review
↓
Next Module

Do not skip a gate.

---

3. WHAT M11 ACTUALLY PROVES

M11 is the admission boundary.

M11 proves that V1 evidence can cross into V2 through a controlled serialized contract.

M11 does NOT automatically prove:

- that the evidence is true;
- that the evidence originated from a trusted human;
- identity;
- universal safety;
- CRTG;
- Foundation Seal 5;
- complete V2;
- correctness of every future module.

Therefore:

«M11 admission is not truth verification.»

And:

«M11 sealed is not V2 completed.»

---

4. M11 ACCEPTANCE GATE

M11 cannot be sealed until all seven audit groups pass.

A — Contract Freeze

Verify that the integrity-covered fields are exactly:

- "payload"
- "foundation_version"
- "evidence_schema_version"
- "evidence_id"
- "source_reference"

Verify that:

"created_at"

is explicitly outside the digest.

Verify that supported versions are explicit.

Unsupported versions must reject.

Verification status must distinguish legitimate supported states from unknown states.

Unknown status values must reject.

No silent contract changes are permitted.

---

5. B — ARCHITECTURAL BOUNDARY

M11 must consume serialized evidence.

It must NOT consume V1 runtime objects.

The following principle must remain true:

V1 runtime
    ↓
serialization
    ↓
JSON / bytes
    ↓
V2 M11

NOT:

V1 object
    ↓
V2 object

V2 must not import V1 runtime code.

Test that:

import swi_core

is unavailable inside the V2 admission environment.

Do not use:

- "PYTHONPATH" tricks;
- "sys.path" manipulation;
- hidden local imports;
- shared runtime objects.

M10 is not the V2 handoff.

The handoff is the serialized evidence artifact.

---

6. C — REAL PRODUCER

M11 must be tested against the real V1 producer pathway.

The expected chain is:

Trainer
↓
PipelineResult
↓
export_foundation_evidence()
↓
FoundationEvidenceEnvelope
↓
JSON
↓
V2 M11

Fixtures may be used for:

- unit tests;
- malformed-input tests;
- negative tests;
- isolation tests.

But fixtures must not replace the real cross-repository happy path.

The real producer must remain the primary proof.

---

7. D — ADMISSION BEHAVIOUR

The following matrix must remain tested.

Valid evidence

Expected:

ACCEPT
↓
AdmittedInput

Payload modified

Expected:

REJECT

Integrity reference modified

Expected:

REJECT

Unsupported verification status

Expected:

REJECT

Required field removed

Expected:

REJECT

Malformed JSON

Expected:

REJECT

Unsupported schema version

Expected:

REJECT

Unsupported foundation version

Expected:

REJECT

Raw dictionary

Expected:

REJECT

PipelineResult-shaped object

Expected:

REJECT

The purpose is to prove that M11 is actually enforcing its boundary.

---

8. E — KERNEL ISOLATION

Only admitted evidence may enter the V2 kernel.

The required path is:

RAW
 ↓
M11
 ↓
AdmittedInput
 ↓
Kernel

Not:

RAW
 ↓
Kernel

and not:

RAW
 ↓
M12

The kernel must reject anything that has not crossed the admission boundary.

This is one of the most important controls in the architecture.

---

9. F — TWO-CHECKOUT CI

The cross-repository test must reproduce the architecture.

Checkout 1:

V1 only

V1 produces the serialized evidence artifact.

Checkout 2:

V2 only

V2 receives the artifact.

The V2 environment must not have V1 installed as a runtime dependency.

The CI must demonstrate:

1. real V1 production;
2. serialized artifact transfer;
3. V2 admission;
4. tamper rejection;
5. bad-integrity rejection;
6. V1 import unavailable;
7. unit/isolation tests;
8. supported Python matrix.

Record:

- V1 commit SHA;
- V2 commit SHA;
- Python versions;
- workflow run;
- artifact identity;
- result of each matrix.

Do not describe CI as green without tip-specific evidence.

---

10. G — DOCUMENTATION HONESTY

Documentation must describe the same state as the code.

Search the repository for statements such as:

PENDING
NOT IMPLEMENTED
TESTED
CI_VERIFIED
SEALED
DESIGN PENDING

Resolve contradictions.

A document saying:

Two-checkout CI: PENDING

cannot remain as the current status if the audited tip has already passed the required CI.

However, historical/manual documents may retain historical language if clearly labelled as historical instructions.

Do not rewrite history merely to make documentation look clean.

---

11. M11 SEAL DECISION

M11 reaches:

SEAL ELIGIBLE

only when:

A PASS
B PASS
C PASS
D PASS
E PASS
F PASS
G PASS
+
tip-specific two-checkout CI GREEN

Then create:

docs/M11_SEAL_RECORD.md

The seal record must state exactly what was audited.

It must NOT say:

SWI V2 is safe.

It must NOT say:

SWI is fully verified.

It must NOT say:

Foundation Seal 5 achieved.

It must say what M11 actually proves.

---

12. M11 SEAL RECORD STRUCTURE

Use this structure:

# M11 Seal Record

## Module
M11 — Admission Boundary

## Scope
Serialized V1 evidence admission into V2.

## Audited V2 Commit
<exact SHA>

## Audited V1 Producer Commit
<exact SHA>

## CI Run
<exact workflow/run>

## Audit Results

A — Contract Freeze: PASS
B — Architectural Boundary: PASS
C — Real Producer: PASS
D — Admission Behaviour: PASS
E — Kernel Isolation: PASS
F — Reproducibility: PASS
G — Documentation Honesty: PASS

## Limitations

Integrity does not prove truth.

Integrity does not prove origin.

Verification status does not prove truth.

M11 does not establish identity verification.

M11 does not establish CRTG.

M11 does not establish Foundation Seal 5.

M11 does not establish universal safety.

M11 does not establish completion of V2.

## Decision

M11 SEALED.

Seal applies only to the audited M11 scope.

---

13. AFTER M11 IS SEALED

STOP.

Do not immediately implement M13, M14, M15, etc.

The next controlled dependency is:

M11 SEALED
↓
M12 CONTRACT

M12 must first receive an explicit contract.

---

14. M12 — CONTRACT FIRST

Current M12 code must continue to be treated honestly.

If the current implementation is only a type-boundary scaffold, call it:

DESIGN PENDING

or:

TYPE BOUNDARY ONLY

Do not call it:

Evidence Normalization implemented

until normalization actually exists.

Before writing substantive M12 code, define:

M12 Input

Exactly what M12 accepts.

Example:

AdmittedInput

M12 Output

Define the future output type explicitly.

For example:

NormalizedEvidence

only if that is actually the approved architecture.

M12 Transform

Define precisely what normalization means.

Do not allow vague language such as:

clean the evidence
process the evidence
make the evidence safer

Those are descriptions, not contracts.

Define:

- fields;
- transformations;
- preservation rules;
- rejected states;
- deterministic behaviour;
- error behaviour;
- invariants.

---

15. M12 CONTRACT GATE

Before implementation, create the M12 contract documentation.

It must answer:

What enters M12?

What leaves M12?

What information must never be changed?

What information may be transformed?

What must cause rejection?

What is deterministic?

What evidence proves the behaviour?

What does M12 NOT prove?

No implementation begins until those questions are answered.

---

16. M12 IMPLEMENTATION

Once the contract is frozen:

AdmittedInput
↓
M12
↓
NormalizedEvidence

Implementation must be minimal.

Do not implement future modules inside M12.

No hidden:

- M13 logic;
- CRTG;
- identity system;
- sealing engine;
- global policy engine;
- future memory architecture.

One module.

One boundary.

One responsibility.

---

17. M12 TEST GATE

Write tests for:

Valid input

Expected:

ACCEPT

Invalid input

Expected:

REJECT

Boundary violation

Expected:

REJECT

Required field missing

Expected:

REJECT

Unexpected field/state

Expected:

REJECT

Determinism

Same input:

same input
+
same contract
=
same output

Immutability

Where the contract requires preservation:

input evidence
≠
silently mutated input

---

18. M12 CI GATE

Local tests are not enough.

Run:

tests
↓
CI
↓
exact commit
↓
green

Record:

- commit;
- workflow;
- Python matrix;
- test results.

Then audit.

Then seal.

Only after that may M13 depend on M12.

---

19. REPEATABLE MODULE PROTOCOL

Every future module follows the same lifecycle:

1. PRE-NAME
2. PURPOSE
3. BOUNDARY
4. CONTRACT
5. INPUT
6. OUTPUT
7. INVARIANTS
8. REJECTION CONDITIONS
9. IMPLEMENTATION
10. TESTS
11. CI
12. AUDIT
13. DOCUMENTATION REVIEW
14. SEAL
15. DEPENDENCY RELEASE
16. ARCHITECTURE REVIEW

Never reverse the order.

---

20. MODULE STATUS LANGUAGE

Use only controlled terminology.

DESIGN PENDING

Architecture has been proposed but substantive implementation has not been demonstrated.

IMPLEMENTED

Code exists and provides the defined behaviour.

TESTED

Relevant automated tests pass.

CI_VERIFIED

The exact audited commit has passed the required CI workflow.

SEAL ELIGIBLE

All defined audit conditions have passed.

SEALED

The module has passed its defined audit and its dependency may be used by the next controlled module.

---

21. NEVER USE THESE SHORTCUTS

Do not say:

Implemented because the function exists.

Do not say:

Verified because tests passed locally.

Do not say:

Safe because CI passed.

Do not say:

Trusted because it is hashed.

Do not say:

Authenticated because it is serialized.

Do not say:

Complete because all folders exist.

Do not say:

V2 complete because M11 is sealed.

---

22. CRTG BOUNDARY

CRTG remains:

DESIGN PENDING

unless and until the actual architecture, implementation, tests and audit establish otherwise.

Do not silently introduce CRTG while implementing another module.

Do not convert a future design into an implied current capability.

---

23. FOUNDATION SEAL 5 BOUNDARY

Foundation Seal 5 remains a separate V1 architectural decision.

M11 must not quietly become:

Foundation Seal 5

The V2 evidence boundary does not rewrite V1 governance.

---

24. MODULE PRE-NAMES

Each module should retain its authoritative SWI Pre-Name from the architecture/manual.

Do not invent a Pre-Name merely to make documentation look complete.

If the authoritative Pre-Name has not yet been confirmed:

Pre-Name: PENDING ARCHITECTURAL CONFIRMATION

That is better than creating a false name.

The purpose of the Pre-Name is teaching and continuity.

The technical module number remains authoritative for implementation.

---

25. CHANGE CONTROL

Every change must answer:

Why is this change required?

Which contract does it affect?

Which module owns that contract?

Does it change an existing invariant?

Does it invalidate previous tests?

Does it invalidate a previous seal?

Does it introduce a new dependency?

Does it require an architecture review?

If the answer is unclear:

STOP.

---

26. WHEN A SEALED MODULE CHANGES

A sealed module is not casually edited.

If a sealed contract changes:

STOP
↓
identify affected seal
↓
re-open audit
↓
update tests
↓
run CI
↓
re-audit
↓
issue new seal record

Never keep an old seal while silently changing the contract underneath it.

---

27. AI/COPILOT EXECUTION RULE

When using an AI coding assistant, give it only one controlled task at a time.

Example:

Do not implement M13.

Do not modify M11.

Do not modify the frozen M11 contract.

Do not introduce V1 dependencies.

Your task is only to implement the approved M12 contract.

Stop if the contract is ambiguous.

AI should execute the contract.

AI should not invent the architecture.

---

28. THE THREE-QUESTION STOP RULE

Before accepting any change, ask:

1. WHAT CHANGED?

Exact files and behaviour.

2. WHAT PROVES IT?

Tests, CI, audit evidence.

3. WHAT DOES IT NOT PROVE?

Explicit limitations.

If the third question cannot be answered, the work is probably overclaiming.

---

29. MASTER EXECUTION ORDER

The complete controlled sequence is:

CURRENT STATE
↓
Review M11 evidence
↓
Reconcile stale documentation
↓
Complete A–G worksheet
↓
Verify exact CI tip
↓
Create M11 Seal Record
↓
M11 SEALED
↓
STOP
↓
Define M12 contract
↓
Review contract
↓
Implement M12
↓
Test M12
↓
CI M12
↓
Audit M12
↓
Seal M12
↓
STOP
↓
Architecture Review
↓
Define next module
↓
Repeat

---

30. FINAL CONTROL PRINCIPLE

SWI does not become stronger because more modules are written.

It becomes stronger when each boundary becomes demonstrably reliable.

Therefore:

«Do not measure progress only by how many modules exist. Measure progress by how many module boundaries can be independently demonstrated, tested, reproduced, audited and honestly sealed.»

The objective is not:

M11 → M12 → M13 → M14 → M15...

as fast as possible.

The objective is:

M11
✓ contract
✓ boundary
✓ implementation
✓ tests
✓ CI
✓ audit
✓ seal

↓
M12
✓ contract
✓ boundary
✓ implementation
✓ tests
✓ CI
✓ audit
✓ seal

↓
NEXT

That is the controlled path.

Never compress evidence to accelerate architecture.

Never convert intention into implementation.

Never convert tests into truth.

Never convert a seal into a universal claim.

Build only what can be demonstrated.
