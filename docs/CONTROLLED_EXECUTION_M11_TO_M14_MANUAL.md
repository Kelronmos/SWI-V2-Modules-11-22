SWI V2 — Controlled Execution Manual

M11 Closure → M12 → M13 → M14

Repository: "Kelronmos/SWI-V2-Modules-11-22"
Branch: "main"
Document: Controlled execution and verification manual
Scope: Modules 11–14
Status: Execution guidance — not evidence of implementation

«DO NOT CLAIM WHAT THE CODE CANNOT DEMONSTRATE.»

---

0. Constitutional Development Rule

SWI V2 development follows this sequence:

QUESTION
↓
CONTRACT
↓
BOUNDARY
↓
IMPLEMENTATION
↓
TEST
↓
CI
↓
EVIDENCE
↓
AUDIT
↓
SEAL
↓
NEXT DEPENDENCY

A module number does not authorize implementation.

The existence of M12, M13 or M14 in the roadmap does not mean the module is ready to build.

A later module may begin only when its predecessor has produced the evidence required by the next dependency.

Therefore:

SEAL BEFORE DEPENDENCY
DEPENDENCY BEFORE NEXT MODULE

Never implement a future capability merely because the architecture anticipates it.

---

1. Status Vocabulary

SWI uses three separate status levels.

1.1 TESTED

"TESTED" means relevant automated tests exist and pass.

It does not mean:

- universally correct
- secure against every threat
- production ready
- mathematically proven
- identity verified
- truthful
- safe in every environment

---

1.2 CI_VERIFIED

"CI_VERIFIED" means the exact audited commit was executed through the defined CI workflow and the required evidence is observable.

This includes the specific:

- commit SHA
- workflow
- runtime
- dependency environment
- test results
- relevant artifacts

A previous green workflow does not automatically prove a new commit.

OLD GREEN RUN ≠ NEW TIP VERIFIED

---

1.3 SEALED

"SEALED" means the defined audit criteria for that module have passed against recorded evidence.

A seal is scoped.

It does not automatically prove:

TRUTH
ORIGIN
IDENTITY
UNIVERSAL SAFETY
CRTG
WHOLE-SYSTEM COMPLETION
FUTURE MODULE COMPLETION

Therefore:

SEALED ≠ PERFECT
SEALED ≠ UNIVERSALLY SAFE
SEALED ≠ EVERYTHING IMPLEMENTED

---

2. Current Development Position

M11 must be closed before M12 begins.

The current known sequence is:

M11 evidence gap
↓
Documentation reconciliation
↓
Exact-tip two-checkout CI
↓
M11 A–G audit
↓
M11 seal record
↓
M11 SEALED
↓
M12 contract

Do not skip the M11 closure stage.

Do not begin M12 implementation merely because the two-checkout workflow is green.

A green two-checkout workflow is important evidence, but it is only one part of the M11 audit.

---

3. M11 Closure — Remaining Evidence

3.1 D6 — Malformed JSON

M11 must explicitly demonstrate rejection of malformed serialized input.

Required behavior:

Malformed JSON
↓
M11 admission boundary
↓
REJECT

The test must demonstrate that malformed serialized material cannot become an admitted input.

Do not:

- repair the JSON automatically
- substitute an empty object
- silently create a fixture
- bypass admission
- convert malformed input into a valid envelope
- weaken the parser merely to pass the test

The test should prove the boundary.

Example test intent:

given malformed serialized input
when admission is attempted
then admission fails
and no AdmittedInput is produced

The exact implementation must follow the existing code and contract.

---

4. M11 Documentation Reconciliation

After D6 is implemented and tested, reconcile the documentation.

Any documentation that still says:

two-checkout verification = PENDING

must be reviewed against the latest actual CI evidence.

If the exact audited tip has a green two-checkout workflow, documentation may state:

two-checkout travel = CI_VERIFIED

But this must not automatically change M11 to SEALED.

Correct intermediate state:

M11 = TESTED / NOT SEALED

until A–G have independently passed.

Documentation must never run ahead of evidence.

---

5. M11 Exact-Tip CI

After D6 and documentation changes:

1. Commit the changes.
2. Record the new V2 commit SHA.
3. Run the two-checkout workflow.
4. Confirm the actual V1 producer is used.
5. Confirm the serialized artifact crosses the repository boundary.
6. Confirm V2 receives serialized evidence.
7. Confirm V1 runtime import is unavailable in the V2 environment.
8. Confirm tampered evidence is rejected.
9. Confirm invalid integrity references are rejected.
10. Confirm admission/isolation tests pass.
11. Record the workflow run ID.
12. Record the runtime matrix.
13. Record the V1 producer SHA.
14. Record the V2 audited SHA.
15. Record the resulting artifact identity.

The audited commit must be explicit.

AUDITED V2 SHA = the exact commit tested

Do not use:

latest
main
current
probably the same

as audit evidence.

---

6. M11 A–G Audit

The M11 audit must evaluate every category.

A — Contract Freeze
B — Architectural Boundary
C — Real Producer
D — Admission Behaviour
E — Kernel Isolation
F — Reproducibility
G — Documentation Honesty

Every category must pass.

"NOT PROVEN" is not equivalent to "PASS".

---

7. M11 A — Contract Freeze

Verify that the integrity-covered fields are exactly:

payload
foundation_version
evidence_schema_version
evidence_id
source_reference

Verify:

created_at

is explicitly outside the digest if that is what the frozen contract and tests establish.

Verify that tests agree with the documented contract.

Verify supported:

- foundation versions
- evidence schema versions
- verification statuses

are explicitly defined.

Unknown or unsupported values must be rejected.

There must be no silent contract changes.

---

8. M11 B — Architectural Boundary

M11 must consume serialized evidence.

The boundary is:

V1 runtime
↓
serialized evidence
↓
M11 admission
↓
AdmittedInput
↓
V2 processing

V2 must not depend on V1 runtime objects.

Verify:

V2 admission does not import V1

Verify that:

import swi_core

is unavailable in the V2 admission environment where isolation requires it.

Do not solve isolation using:

- "PYTHONPATH"
- "sys.path"
- path injection
- hidden local packages
- shared runtime objects

M10 is not the repository handoff.

The serialized evidence boundary is the handoff.

The V1 envelope must not be mutated in place.

V2 derived state must remain distinguishable from original evidence.

---

9. M11 C — Real Producer

The primary happy path must use the actual V1 producer.

The producer must create serialized evidence through the real export mechanism.

Example conceptual path:

V1 pipeline
↓
export_foundation_evidence
↓
serialized artifact
↓
transfer
↓
V2 admission

Fixtures are permitted for:

- unit tests
- negative tests
- malformed input tests
- contract tests

But fixtures must not be represented as evidence of the real cross-repository travel path.

Therefore:

fixture ≠ real producer evidence

---

10. M11 D — Admission Behaviour

The following cases must be tested.

Input| Expected result
Valid serialized V1-shaped evidence| ACCEPT
Payload changed| REJECT
Integrity reference changed| REJECT
Required field removed| REJECT
Malformed JSON| REJECT
Unsupported schema version| REJECT
Unsupported foundation version| REJECT
Unsupported verification status| REJECT
Raw dictionary| REJECT
PipelineResult-shaped raw object| REJECT

Valid admission must produce the defined typed boundary:

AdmittedInput

Rejected input must not produce an admitted object.

---

11. M11 E — Kernel Isolation

The kernel must not accept arbitrary raw input.

Required conceptual flow:

RAW
↓
M11
↓
AdmittedInput
↓
Kernel
↓
Downstream

Forbidden paths include:

RAW
↓
Kernel

and:

Rejected M11 input
↓
Kernel

and:

RAW DICT
↓
M12

Tests must prove that bypass attempts fail.

The purpose is not merely type elegance.

The purpose is to make the boundary enforceable.

---

12. M11 F — Reproducibility

The two-checkout workflow must prove repository separation.

Conceptually:

CHECKOUT 1
V1
↓
real producer
↓
serialized artifact

CHECKOUT 2
V2
↓
artifact admission
↓
verification

The V2 environment must not require the V1 runtime package to be installed beside it.

The workflow must demonstrate:

- real V1 production
- serialized transfer
- V2-only admission
- V1 import unavailable
- tamper rejection
- integrity rejection
- relevant isolation tests

Record:

V1 SHA
V2 SHA
Python version
workflow name
workflow run ID
artifact identity
test matrix
result

---

13. M11 G — Documentation Honesty

Documentation must match actual code and evidence.

Review:

README
MODULE_STATUS
CROSS_REPO_TRAVEL
RELEASE_GATE
ROADMAP
M11 audit worksheet

The following limitations must remain explicit:

Integrity ≠ Origin

Integrity ≠ Truth

Verification status ≠ Truth

Ed25519 ≠ CRTG

M11 admission ≠ Universal Safety

M11 seal ≠ V2 completion

M11 seal ≠ Foundation Seal 5

M11 seal ≠ Identity Verification

Do not allow documentation to imply capabilities that the implementation does not demonstrate.

---

14. M11 Seal Decision

M11 becomes eligible for sealing only when:

A = PASS
B = PASS
C = PASS
D = PASS
E = PASS
F = PASS
G = PASS
+
Exact-tip two-checkout CI = GREEN

Then:

SEAL ELIGIBLE

Only after the audit evidence is recorded should:

docs/M11_SEAL_RECORD.md

be created.

Then and only then:

M11 = SEALED

There is no:

ALMOST SEALED
NEARLY SEALED
PRACTICALLY SEALED

If one criterion is "NOT PROVEN":

M11 = NOT SEALED

---

15. M11 Seal Record

The seal record must contain actual evidence, not intentions.

Minimum record:

M11 Seal Record

Module:
M11

Status:
SEALED

V1 Producer SHA:
<actual SHA>

V2 Audited SHA:
<actual SHA>

Workflow:
<actual workflow>

Workflow Run:
<actual run ID>

Runtime:
<actual runtime>

A — Contract Freeze:
PASS

B — Architectural Boundary:
PASS

C — Real Producer:
PASS

D — Admission:
PASS

E — Kernel Isolation:
PASS

F — Reproducibility:
PASS

G — Documentation:
PASS

Scope:
Serialized foundation-evidence admission only.

Limitations:
Integrity does not establish truth, origin or identity.
M11 does not establish CRTG.
M11 does not establish Foundation Seal 5.
M11 does not establish universal system safety.
M11 does not establish V2 completion.

Never fabricate missing values.

---

16. M12 Entry Gate

M12 implementation is blocked until:

M11_SEAL_RECORD.md exists
AND
M11 = SEALED
AND
A–G = PASS
AND
two-checkout CI = CI_VERIFIED
AND
documentation agrees

If any condition fails:

M12 = BLOCKED

This is intentional.

A blocked dependency is safer than a fabricated dependency.

---

17. M12 Contract First

Before writing M12 implementation code, create:

docs/M12_CONTRACT.md

The contract must define:

Purpose

What M12 actually does.

Input

Exact accepted input type and structure.

Output

Exact output type and structure.

Preconditions

What must already be true.

Postconditions

What M12 guarantees after successful execution.

Rejection

What M12 must reject.

Halt

What conditions require a controlled halt rather than continuation.

Authority

What M12 is allowed to decide and what it is not allowed to decide.

Integrity

What integrity checks are required.

Provenance

What evidence must remain linked to the source.

State

Valid state transitions.

Dependencies

Exact predecessor evidence required.

Non-goals

Explicitly list what M12 does not claim to provide.

---

18. M12 Failure Vocabulary

Where applicable, define explicit failure categories:

INVALID_INPUT
CONTRACT_FAILURE
INTEGRITY_FAILURE
AUTHORITY_FAILURE
CONSTRAINT_FAILURE
EXECUTION_FAILURE
OUTPUT_FAILURE
STATE_FAILURE
HALT

The exact vocabulary must be frozen by the contract before implementation.

Do not introduce labels merely for appearance.

Each failure state must correspond to an observable behavior.

---

19. M12 Implementation Rule

M12 must implement only its bounded responsibility.

Development order:

CONTRACT
↓
MINIMUM IMPLEMENTATION
↓
POSITIVE TESTS
↓
NEGATIVE TESTS
↓
BYPASS TESTS
↓
ISOLATION TESTS
↓
INTEGRATION
↓
CI
↓
AUDIT
↓
SEAL

Do not implement M13 functionality inside M12.

Do not create speculative infrastructure merely because M13 may eventually need it.

---

20. M12 Required Tests

At minimum, test the following according to the frozen contract:

AdmittedInput → M12 → expected result

Must also test:

Raw input → M12 → REJECT

Raw input → Kernel → M12 → REJECT

M11 rejected input → M12 → REJECT

Invalid state → REJECT

Invalid authority → REJECT

Integrity failure → REJECT

Invalid output condition → REJECT

HALT condition → HALT

Add contract-specific tests after the M12 contract is frozen.

The goal is not simply to test the happy path.

The goal is to prove that the boundary cannot be casually bypassed.

---

21. M12 Provenance and Cryptographic Boundaries

M12 must preserve the distinction between:

ORIGINAL EVIDENCE

and:

DERIVED STATE

Do not mutate source evidence merely to make downstream processing convenient.

Cryptographic terminology must remain precise.

Hash
=
detects changes relative to an expected digest

Signature
=
cryptographic verification under defined key assumptions

Ed25519
=
cryptographic primitive

None of these independently proves:

truth
identity
authority
human intent
institutional legitimacy
CRTG

CRTG remains:

DESIGN PENDING

unless separately implemented, tested, audited and sealed.

Foundation Seal 5 remains a V1 architectural decision.

Do not silently introduce it into M12.

---

22. M12 CI Verification

After implementation and tests:

1. Commit the exact code.
2. Record SHA.
3. Run the required CI.
4. Record runtime.
5. Record dependencies.
6. Record test commands.
7. Record workflow ID.
8. Record all required results.
9. Verify no hidden local dependency.
10. Verify isolation.
11. Verify negative paths.

Then:

TESTED
↓
CI_VERIFIED
↓
AUDIT
↓
SEALED

Create:

docs/M12_SEAL_RECORD.md

only after the M12 audit passes.

---

23. M12 → M13 Architecture Review

Do not automatically begin M13 after writing M12 code.

First review:

What exactly did M12 prove?

What exactly did M12 NOT prove?

What evidence does M13 require?

What exact M12 output becomes M13 input?

Is that output actually demonstrated?

Are there unresolved assumptions?

Are there security or authority boundaries?

Is any dependency only theoretical?

If M13 depends on an unproven capability:

M13 = BLOCKED

Do not approximate the missing capability.

---

24. M13 Contract

Before implementation:

docs/M13_CONTRACT.md

Define:

Purpose
Input
Output
Preconditions
Postconditions
Rejection
Halt
Authority
Integrity
Provenance
State
Dependencies
Non-goals

The contract must identify the exact M12 dependency.

Do not say:

depends on M12

without defining what part of M12 is actually required.

Example:

M13 requires:
<exact typed output>
from:
M12
under:
<defined state>
with:
<defined integrity/provenance conditions>

---

25. M13 Implementation

M13 receives only the contractually permitted predecessor output.

Development sequence:

CONTRACT
↓
BOUNDARY
↓
MINIMUM IMPLEMENTATION
↓
POSITIVE TEST
↓
NEGATIVE TEST
↓
BYPASS TEST
↓
PROVENANCE TEST
↓
INTEGRATION
↓
CI
↓
AUDIT
↓
SEAL

Required negative categories include:

missing input
wrong type
wrong state
unauthorized input
integrity failure
provenance failure
predecessor bypass
raw-input bypass
invalid output
HALT condition

No M14 functionality should be implemented inside M13.

---

26. M13 Dependency Protection

M13 must prove that it cannot simply be invoked independently of its required predecessor where the architecture requires predecessor enforcement.

Test:

Valid M12 output
↓
M13
↓
ACCEPT

Then test:

Raw input
↓
M13
↓
REJECT

and:

Forged M12-shaped input
↓
M13
↓
REJECT

where the contract requires provenance/integrity enforcement.

Do not create a fake predecessor object merely to make the architecture appear complete.

---

27. M13 CI, Audit and Seal

Record:

M13 SHA
M12 dependency SHA
Runtime
Dependencies
Workflow
Workflow Run ID
Test Results
Relevant Artifacts

Then:

TESTED
↓
CI_VERIFIED
↓
AUDIT
↓
SEALED

Create:

docs/M13_SEAL_RECORD.md

only after the defined audit passes.

The M13 seal is limited to the defined M13 contract.

It does not seal M14.

---

28. M13 → M14 Architecture Review

Before M14 implementation, answer:

What did M13 prove?

What did M13 not prove?

What exact M13 output does M14 consume?

What state is required?

What authority is required?

What integrity evidence is required?

What provenance is required?

Are any assumptions unresolved?

Does M14 require a capability that does not yet exist?

If a required capability is not demonstrated:

M14 = BLOCKED

Do not fill the gap with placeholder logic and describe it as implementation.

---

29. M14 Contract

Create:

docs/M14_CONTRACT.md

before implementation.

The contract must define:

Purpose
Input
Output
Preconditions
Postconditions
Rejection
Halt
Authority
Integrity
Provenance
State
Dependencies
Non-goals

The M14 contract must explicitly identify:

M13 dependency

and the evidence required to satisfy it.

If M14 requires CRTG and CRTG is still design-pending:

M14 must stop at the dependency boundary.

Do not create a simulated CRTG implementation merely to unblock M14.

---

30. M14 Implementation

Follow:

INSPECT
↓
CONTRACT
↓
BOUNDARY
↓
MINIMUM IMPLEMENTATION
↓
TEST
↓
NEGATIVE TEST
↓
BYPASS TEST
↓
INTEGRATION
↓
CI
↓
AUDIT
↓
SEAL

M14 must remain within its defined responsibility.

No M15 functionality should be introduced inside M14.

No speculative “future-proofing” should be presented as implemented capability.

---

31. M14 Test Matrix

At minimum, after the contract is frozen:

Scenario| Expected
Valid contract input| ACCEPT
Missing required input| REJECT
Wrong type| REJECT
Invalid state| REJECT
Invalid authority| REJECT
Integrity failure| REJECT
Provenance violation| REJECT
Raw bypass| REJECT
Predecessor bypass| REJECT
Invalid output condition| REJECT
HALT condition| HALT

Expand this matrix according to the actual M14 contract.

Tests must correspond to real behavior.

---

32. M14 CI Verification

Record:

M14 SHA
M13 dependency SHA
Runtime
Dependency environment
Workflow
Workflow Run ID
Test matrix
Test results
Artifacts

Verify that the exact commit being sealed is the commit tested.

Then:

TESTED
↓
CI_VERIFIED
↓
AUDIT
↓
SEALED

Create:

docs/M14_SEAL_RECORD.md

only after the audit passes.

---

33. M14 Exit Gate

If and only if each module has independently passed its defined audit:

M11 SEALED
↓
M12 SEALED
↓
M13 SEALED
↓
M14 SEALED

This means only that the defined scope of M11–M14 has been independently audited and sealed.

It does not mean:

M15 complete
M16 complete
...
M22 complete
CRTG complete
Foundation Seal 5 complete
Universal safety proven
Whole SWI proven

The next action is an architecture review.

---

34. Global Stop Conditions

Immediately stop development if any of the following occurs:

Documentation contradicts code

HALT

Tests contradict implementation

HALT

CI evidence is unknown

HALT

V1 runtime appears inside V2 admission

HALT

Raw input bypasses M11

HALT

Rejected material continues downstream

HALT

Fixtures are presented as real producer evidence

HALT

Cryptographic primitives are presented as governance

HALT

A seal is created without audit evidence

HALT

Future capability is described as implemented

HALT

Unproven dependency is treated as available

HALT

Recovery sequence:

HALT
↓
DOCUMENT
↓
ISOLATE
↓
FIX
↓
RETEST
↓
REVERIFY

---

35. No Bulk M15–M22 Implementation

Do not implement M15–M22 as a batch merely because M11–M14 are complete.

Each future module must follow:

ARCHITECTURE REVIEW
↓
DEPENDENCY PROOF
↓
BOUNDED CONTRACT
↓
IMPLEMENTATION
↓
NEGATIVE TESTS
↓
BYPASS TESTS
↓
CI
↓
AUDIT
↓
SEAL

Module number is not evidence.

Roadmap position is not evidence.

Architecture diagrams are not evidence of implementation.

A document describing a capability is not evidence that the capability exists in code.

---

36. Master Execution Checklist

M11

- [ ] D6 malformed JSON rejection implemented
- [ ] D6 test passes
- [ ] Documentation reconciled
- [ ] Exact audited V2 SHA recorded
- [ ] Real V1 producer verified
- [ ] Serialized transfer verified
- [ ] V1 import unavailable in V2 environment
- [ ] Tamper rejection verified
- [ ] Integrity rejection verified
- [ ] Kernel isolation verified
- [ ] Two-checkout CI green
- [ ] A PASS
- [ ] B PASS
- [ ] C PASS
- [ ] D PASS
- [ ] E PASS
- [ ] F PASS
- [ ] G PASS
- [ ] M11 seal record created
- [ ] M11 marked SEALED

M12

- [ ] M11 SEALED
- [ ] M12 architecture entry review complete
- [ ] M12 contract created
- [ ] Contract frozen
- [ ] Minimum implementation complete
- [ ] Positive tests pass
- [ ] Negative tests pass
- [ ] Bypass tests pass
- [ ] Isolation tests pass
- [ ] Integration tests pass
- [ ] CI verified
- [ ] Audit complete
- [ ] M12 seal record created
- [ ] M12 marked SEALED

M13

- [ ] M12 SEALED
- [ ] M13 dependency review complete
- [ ] M13 contract created
- [ ] Contract frozen
- [ ] Minimum implementation complete
- [ ] Positive tests pass
- [ ] Negative tests pass
- [ ] Bypass tests pass
- [ ] Provenance tests pass
- [ ] Integration tests pass
- [ ] CI verified
- [ ] Audit complete
- [ ] M13 seal record created
- [ ] M13 marked SEALED

M14

- [ ] M13 SEALED
- [ ] M14 dependency review complete
- [ ] M14 contract created
- [ ] Contract frozen
- [ ] Minimum implementation complete
- [ ] Positive tests pass
- [ ] Negative tests pass
- [ ] Bypass tests pass
- [ ] Authority tests pass
- [ ] Integrity tests pass
- [ ] Provenance tests pass
- [ ] Integration tests pass
- [ ] CI verified
- [ ] Audit complete
- [ ] M14 seal record created
- [ ] M14 marked SEALED

---

37. Development Law

The following is the controlling principle for M11–M14:

EVIDENCE BEFORE CLAIM.

BOUNDARY BEFORE EXPANSION.

CONTRACT BEFORE CODE.

CODE BEFORE CONFIDENCE.

TEST BEFORE STATUS.

CI BEFORE REPRODUCIBILITY.

AUDIT BEFORE SEAL.

SEAL BEFORE DEPENDENCY.

DEPENDENCY BEFORE NEXT MODULE.

AND NEVER CLAIM WHAT THE CODE CANNOT DEMONSTRATE.

---

38. Immediate Execution Order

The immediate order is:

1. Finish M11 D6
↓
2. Reconcile M11 documentation
↓
3. Run exact-tip two-checkout CI
↓
4. Complete M11 A–G audit
↓
5. Create M11 seal record only if every gate passes
↓
6. Mark M11 SEALED
↓
7. Create M12 contract
↓
8. Implement M12
↓
9. Test M12
↓
10. CI verify M12
↓
11. Audit M12
↓
12. Seal M12
↓
13. Review M13 dependency
↓
14. Contract M13
↓
15. Implement and test M13
↓
16. CI verify M13
↓
17. Audit and seal M13
↓
18. Review M14 dependency
↓
19. Contract M14
↓
20. Implement and test M14
↓
21. CI verify M14
↓
22. Audit and seal M14
↓
23. Architecture review before M15

No step should be skipped because the next module appears architecturally obvious.

The architecture may describe the destination.
The evidence determines how far SWI has actually travelled.
