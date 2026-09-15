SWI V2 — CONTROLLED MODULE DEVELOPMENT & SEALING MANUAL

M11 → M12 → M13 → M14

Repository: "Kelronmos/SWI-V2-Modules-11-22"
Branch: "main"
Scope: Controlled development, teaching, verification, audit and sealing of Modules 11–14
Status: Execution guidance + teaching convention — not evidence of implementation

«DO NOT CLAIM WHAT THE CODE CANNOT DEMONSTRATE.»

---

0. PURPOSE OF THIS MANUAL

This manual defines how SWI V2 moves from one controlled module to the next without repeating the central failure of many AI projects:

«Describing what a system should be able to do as though it has already demonstrated that capability.»

SWI development must distinguish:

ARCHITECTURAL IDEA
        ≠
CONTRACT
        ≠
IMPLEMENTATION
        ≠
TEST
        ≠
CI EVIDENCE
        ≠
AUDIT
        ≠
SEAL

A module may have a powerful architectural purpose and still be:

DESIGN PENDING

A module may have working code and still be:

TESTED

A module may have passed CI and still not be:

SEALED

A module becomes "SEALED" only after the defined audit evidence exists.

---

1. THE SWI PRE-NAME CONVENTION

SWI historically used conceptual names for parts of the architecture.

Those names should not be discarded merely because the numbered module structure is being formalized.

Instead, use:

M11 — CONTINUITY LOCK (STATE PRESERVATION)
M12 — THE MASTERY ARCHIVE (KNOWLEDGE ANCHOR)
M13 — SEMANTIC SCRUBBER (CLEAN DATA PROTOCOL)
M14 — THE AGENTIC LOOP (TASK AUTONOMY GOVERNOR)

(Source: SWI Architecture Volume 2 — Technical Codex, Modules 11–14.)

The Pre-Name is the teaching and architectural identity.

The module number is the controlled implementation identity.

The key rule:

> Pre-Name explains what the module means. The contract, code, tests and seal determine what the module actually does.

Do not invent a new Pre-Name merely to fill a blank.
Do not treat a Pre-Name as permission to implement functionality that has not been contracted and demonstrated.

---

1.1 Why keep the Pre-Names?

The original names often explain the reasoning behind the architecture better than a number alone.

For teaching:

M12

tells us where something sits.

THE MASTERY ARCHIVE (KNOWLEDGE ANCHOR)

tells us:

why it exists
what problem it was intended to address
how it relates conceptually to SWI

Therefore both should remain visible.

---

2. PRE-NAME DOES NOT CREATE AUTHORITY

A Pre-Name is not permission to implement functionality.

For example:

M13 — SEMANTIC SCRUBBER (CLEAN DATA PROTOCOL)

does not mean:

M13 is complete.

It means:

This is the conceptual identity assigned to M13.

The implementation must still prove itself.

Therefore:

PRE-NAME
↓
TEACHING CONTEXT

MODULE NUMBER
↓
ARCHITECTURAL LOCATION

CONTRACT
↓
IMPLEMENTATION AUTHORITY

TEST
↓
BEHAVIOURAL EVIDENCE

CI
↓
REPRODUCIBILITY

AUDIT
↓
SEAL AUTHORITY

---

3. THE SWI CONTROL LAW

Every module follows:

QUESTION
↓
PRE-NAME / CONCEPT
↓
DEPENDENCY REVIEW
↓
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
INTEGRATION TEST
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

No module skips directly from:

CONCEPT → CODE

---

4. STATUS DEFINITIONS

DESIGN_PENDING

The concept exists but implementation has not been sufficiently defined or demonstrated.

---

IMPLEMENTED

Code exists.

This is intentionally a weak status.

It does not mean the code is correct.

---

TESTED

Relevant tests pass.

It does not mean universal correctness.

---

CI_VERIFIED

The exact audited commit passed the required CI workflow.

The evidence must identify:

- commit SHA
- workflow
- runtime
- environment
- tests
- results

---

AUDITED

The defined audit criteria have been reviewed against evidence.

---

SEALED

The module has passed the defined audit and its seal record has been created.

---

5. THE FUNDAMENTAL RULE

Never write:

M12 guarantees safety.

unless the contract and evidence actually demonstrate that exact claim.

Prefer:

M12 enforces <specific defined boundary>
under <specific tested conditions>.

Precision is part of the architecture.

---

6. M11 — CONTINUITY LOCK (STATE PRESERVATION)

PURPOSE

M11 is the controlled admission boundary between serialized V1 evidence and V2 processing.

In the SWI Pre-Name, CONTINUITY LOCK (STATE PRESERVATION) expresses the architectural intent to preserve controlled state across the repository boundary.

The critical architectural principle is:

V1 RUNTIME
     ↓
SERIALIZED EVIDENCE
     ↓
M11 ADMISSION
     ↓
ADMITTED INPUT
     ↓
V2

M11 does not consume V1 runtime objects.

M11 consumes serialized evidence.

The Pre-Name explains continuity and state preservation.
The contract, tests and seal determine the exact admission behaviour that is demonstrated.

---

7. M11 TEACHING MODEL

Teach M11 using this analogy:

«V1 may produce the document.
M11 checks whether the document satisfies the admission contract.
V2 then works from the admitted representation.»

The document crossing the boundary is not the same thing as shared memory.

Therefore:

TRANSFER
≠
SHARED RUNTIME

---

8. M11 CONTRACT

The M11 contract must freeze the integrity-covered fields.

Current required fields:

payload
foundation_version
evidence_schema_version
evidence_id
source_reference

"created_at" must remain explicitly outside the digest if that is what the frozen contract and tests establish.

The contract must also define:

supported foundation versions
supported schema versions
supported verification statuses
rejection behaviour
admitted representation

Unknown values must not silently pass.

---

9. M11 REAL PRODUCER

The happy path must use the actual V1 export.

Conceptually:

V1 pipeline
↓
export_foundation_evidence
↓
serialized artifact
↓
transfer
↓
M11
↓
AdmittedInput

Fixtures are permitted for unit and negative testing.

But:

fixture
≠
real cross-repository evidence

Documentation must never describe a fixture as a live producer.

---

10. M11 REQUIRED TESTS

At minimum:

Scenario | Expected
Valid serialized envelope | ACCEPT
Payload modified | REJECT
Integrity modified | REJECT
Required field removed | REJECT
Malformed JSON | REJECT
Unsupported schema | REJECT
Unsupported foundation version | REJECT
Unsupported status | REJECT
Raw dictionary | REJECT
PipelineResult-shaped object | REJECT

---

11. M11 D6 — MALFORMED JSON

This is a specific evidence requirement.

Test:

MALFORMED SERIALIZED INPUT
↓
M11
↓
REJECT

The implementation must not:

- repair the input
- substitute an empty object
- silently convert it
- create a fixture
- bypass the admission boundary

The test must demonstrate genuine rejection.

---

12. M11 KERNEL ISOLATION

Required conceptual path:

RAW
↓
M11
↓
AdmittedInput
↓
KERNEL

Forbidden:

RAW
↓
KERNEL

Also forbidden:

REJECTED M11 INPUT
↓
KERNEL

The kernel must not become an alternative admission route.

---

13. M11 ARCHITECTURAL ISOLATION

V2 must not depend on V1 runtime installation.

Verify:

V2 admission
+
V1 unavailable
=
M11 still operates on serialized evidence

Do not use:

PYTHONPATH
sys.path manipulation
hidden local packages
runtime object sharing

to create an artificial dependency.

M10 is not the repository handoff.

The serialized evidence boundary is the handoff.

---

14. M11 TWO-CHECKOUT CI

The required proof is conceptually:

CHECKOUT A
V1
↓
REAL PRODUCER
↓
SERIALIZED ARTIFACT

CHECKOUT B
V2
↓
M11 ADMISSION
↓
RESULT

The two environments must remain independently meaningful.

Record:

V1 SHA
V2 SHA
Python version
workflow
workflow run
artifact identity
test results

A previous green workflow does not automatically certify a new commit.

---

15. M11 A–G AUDIT

Audit:

A — Contract Freeze
B — Architectural Boundary
C — Real Producer
D — Admission Behaviour
E — Kernel Isolation
F — Reproducibility
G — Documentation Honesty

Every category must be:

PASS

"NOT PROVEN" means:

NOT SEALED

---

16. M11 LIMITATIONS

The seal record must preserve these distinctions:

Integrity ≠ Origin

Integrity ≠ Truth

Verification Status ≠ Truth

Ed25519 ≠ CRTG

M11 Admission ≠ Universal Safety

M11 Seal ≠ V2 Completion

M11 Seal ≠ Foundation Seal 5

M11 Seal ≠ Identity Verification

These are not disclaimers added for legal appearance.

They are architectural boundaries.

---

17. M11 SEAL

M11 can become seal-eligible only when:

A PASS
B PASS
C PASS
D PASS
E PASS
F PASS
G PASS

AND

exact-tip two-checkout CI = GREEN

Then create:

docs/M11_SEAL_RECORD.md

The record must identify the exact evidence.

Only then:

M11 = SEALED

---

18. M11 EXIT GATE

Before M12:

M11_SEAL_RECORD.md exists
AND
M11 = SEALED
AND
documentation agrees
AND
exact-tip CI is verified

If not:

M12 = BLOCKED

---

19. M12 — THE MASTERY ARCHIVE (KNOWLEDGE ANCHOR)

PURPOSE

M12 begins only after M11 has been independently sealed.

M12 must not be designed as:

"everything M11 didn't do"

It must have a bounded responsibility.

The SWI Pre-Name THE MASTERY ARCHIVE (KNOWLEDGE ANCHOR) provides the teaching identity from the Technical Codex.

The contract defines the exact input, output, rejection and halt behaviour that will be demonstrated.

---

20. M12 ARCHITECTURE REVIEW

Before writing code, answer:

What does M12 receive?

From exactly where?

What does M12 produce?

Who is allowed to consume that output?

What state is required?

What authority is required?

What integrity evidence is required?

What provenance must travel?

What does M12 explicitly NOT do?

If any critical dependency is unproven:

HALT

---

21. M12 CONTRACT

Create:

docs/M12_CONTRACT.md

before implementation.

Required sections:

1. Module Identity
2. SWI Pre-Name: THE MASTERY ARCHIVE (KNOWLEDGE ANCHOR)
3. Purpose
4. Scope
5. Inputs
6. Outputs
7. Preconditions
8. Postconditions
9. State Model
10. Authority Model
11. Integrity Requirements
12. Provenance Requirements
13. Rejection Conditions
14. HALT Conditions
15. Failure Vocabulary
16. Dependencies
17. Non-Goals
18. Test Requirements
19. CI Requirements
20. Seal Criteria

---

22. M12 FAILURE MODEL

Use explicit failure categories where applicable:

INVALID_INPUT
CONTRACT_FAILURE
INTEGRITY_FAILURE
AUTHORITY_FAILURE
CONSTRAINT_FAILURE
EXECUTION_FAILURE
OUTPUT_FAILURE
STATE_FAILURE
HALT

Do not introduce a failure class simply because it sounds sophisticated.

Every failure state must correspond to observable behaviour.

---

23. M12 IMPLEMENTATION

Implementation order:

CONTRACT
↓
BOUNDARY
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

No M13 functionality belongs inside M12.

---

24. M12 POSITIVE TEST

Demonstrate the valid path:

M11 AdmittedInput
↓
M12
↓
DEFINED VALID RESULT

The expected result must come from the contract.

Do not define the test expectation after seeing what the implementation happens to produce.

---

25. M12 NEGATIVE TESTS

At minimum, test:

raw input
missing input
wrong type
invalid state
invalid authority
integrity failure
invalid output condition
HALT condition

Where applicable:

M11 rejection
↓
M12
↓
REJECT

---

26. M12 BYPASS TESTING

Try to defeat the intended boundary.

Examples:

RAW → M12

RAW → Kernel → M12

Forged M11-shaped object → M12

Modified evidence → M12

The exact tests depend on the contract.

The principle remains:

«A security boundary is more meaningful when its bypass paths are tested.»

---

27. M12 PROVENANCE

M12 must distinguish:

SOURCE EVIDENCE

from:

DERIVED STATE

Never mutate source evidence simply because downstream processing wants a different representation.

Prefer:

Original Evidence
+
Derived State

rather than:

Original Evidence overwritten by Derived State

---

28. M12 CRYPTOGRAPHIC LANGUAGE

Keep terminology exact.

HASH
=
change detection relative to an expected digest

SIGNATURE
=
cryptographic verification under defined key assumptions

Ed25519
=
cryptographic primitive

These do not independently establish:

truth
identity
human intent
institutional legitimacy
CRTG

Do not convert cryptography into governance claims.

---

29. M12 CI

The CI record must include:

commit SHA
runtime
dependency environment
test command
workflow
workflow run ID
test results
artifacts

The exact commit being sealed must be the exact commit tested.

Then:

TESTED
↓
CI_VERIFIED
↓
AUDITED
↓
SEALED

Create:

docs/M12_SEAL_RECORD.md

only after the audit.

---

30. M12 SEAL CRITERIA

M12 cannot be sealed merely because:

tests pass

Required:

contract frozen
implementation matches contract
positive tests pass
negative tests pass
bypass tests pass
isolation tests pass
integration passes
CI verified
evidence recorded
audit passes
documentation reconciled

Then:

M12 = SEALED

---

31. M12 → M13 DEPENDENCY REVIEW

Before M13 begins:

What did M12 actually prove?

What did M12 not prove?

What exact output does M13 require?

Is that output contractually defined?

Is it actually produced?

Is its provenance preserved?

Is its integrity preserved?

Does M13 require authority M12 does not provide?

If the answer exposes an unproven dependency:

M13 = BLOCKED

---

32. M13 — SEMANTIC SCRUBBER (CLEAN DATA PROTOCOL)

M13 receives only the exact dependency demonstrated by M12.

The Pre-Name SEMANTIC SCRUBBER (CLEAN DATA PROTOCOL) remains visible for teaching.

The contract remains authoritative for implementation.

---

33. M13 CONTRACT

Create:

docs/M13_CONTRACT.md

Required:

Module Identity
SWI Pre-Name: SEMANTIC SCRUBBER (CLEAN DATA PROTOCOL)
Purpose
Scope
Input
Output
Preconditions
Postconditions
State
Authority
Integrity
Provenance
Rejection
HALT
Dependencies
Non-Goals
Tests
CI
Seal Criteria

---

34. M13 DEPENDENCY

Do not write:

M13 depends on M12.

That is insufficient.

Define:

M13 requires:
<exact M12 output>

produced under:
<exact state>

with:
<exact integrity conditions>

and:
<exact provenance>

A module number alone is not a dependency contract.

---

35. M13 IMPLEMENTATION

Use:

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

Do not implement M14 inside M13.

Do not create speculative M14 interfaces unless the M13 contract genuinely requires an interface for its own defined output.

---

36. M13 NEGATIVE TESTS

At minimum:

missing input → REJECT

wrong type → REJECT

wrong state → REJECT

unauthorized input → REJECT

integrity failure → REJECT

provenance failure → REJECT

predecessor bypass → REJECT

raw-input bypass → REJECT

invalid output → REJECT

HALT condition → HALT

Expand based on the actual contract.

---

37. M13 PROVENANCE TEST

Prove that M13 cannot silently treat unrelated material as valid M12 output where provenance is contractually required.

Conceptual test:

M12 output
↓
M13
↓
ACCEPT

versus:

unrelated/forged output
↓
M13
↓
REJECT

Do not manufacture a fake M12 dependency merely to make the test pass.

---

38. M13 CI AND AUDIT

Record:

M13 SHA
M12 dependency SHA
runtime
environment
workflow
run ID
test matrix
results
artifacts

Then:

TESTED
↓
CI_VERIFIED
↓
AUDITED
↓
SEALED

Create:

docs/M13_SEAL_RECORD.md

only after the audit.

---

39. M13 SEAL LIMIT

The M13 seal proves only the defined M13 scope.

It does not automatically prove:

M14
M15
CRTG
Foundation Seal 5
universal safety
whole-system correctness

---

40. M13 → M14 ARCHITECTURE REVIEW

Before M14:

M13 capability
↓
M13 limitations
↓
M14 required dependency
↓
dependency evidence
↓
M14 contract

Ask:

What exactly does M14 need?

Does M13 really provide it?

Under what state?

Under what authority?

With what integrity?

With what provenance?

Can the dependency be independently tested?

Is any part still design-pending?

---

41. M14 — THE AGENTIC LOOP (TASK AUTONOMY GOVERNOR)

M14 is the fourth controlled stage in this sequence.

Its Pre-Name remains visible throughout:

M14 — THE AGENTIC LOOP (TASK AUTONOMY GOVERNOR)

(Source: SWI Architecture Volume 2 — Technical Codex.)

The contract defines the bounded responsibility that will be demonstrated.

---

42. M14 CONTRACT

Create:

docs/M14_CONTRACT.md

before implementation.

Required sections:

Module Identity
SWI Pre-Name: THE AGENTIC LOOP (TASK AUTONOMY GOVERNOR)
Purpose
Scope
Input
Output
Preconditions
Postconditions
State
Authority
Integrity
Provenance
Rejection
HALT
Dependencies
Non-Goals
Test Matrix
CI Requirements
Audit Criteria
Seal Criteria

---

43. M14 DEPENDENCY RULE

M14 must explicitly identify its M13 dependency.

Example structure:

M14 consumes:
<exact M13 output>

provided that:
<state>

and:
<integrity condition>

and:
<provenance condition>

If M14 needs a capability that has not been demonstrated:

M14 = BLOCKED

Do not approximate the missing capability.

---

44. M14 IMPLEMENTATION

Sequence:

INSPECT
↓
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
AUTHORITY TEST
↓
INTEGRITY TEST
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

No M15 functionality inside M14.

---

45. M14 TEST MATRIX

Minimum:

Scenario | Expected
Valid contract input | ACCEPT
Missing required input | REJECT
Wrong type | REJECT
Invalid state | REJECT
Invalid authority | REJECT
Integrity failure | REJECT
Provenance violation | REJECT
Raw bypass | REJECT
Predecessor bypass | REJECT
Invalid output | REJECT
HALT condition | HALT

The final test matrix must be expanded after the contract is frozen.

---

46. M14 AUTHORITY TESTING

Where M14 contains an authority boundary, explicitly test:

authorized request
↓
ALLOW

and:

unauthorized request
↓
REJECT

Do not infer authority merely from:

- a username
- a string
- a field named "role"
- a locally supplied flag

unless the contract explicitly defines that mechanism and its limitations.

---

47. M14 INTEGRITY TESTING

Where integrity is part of M14:

valid integrity
↓
continue

and:

modified evidence
↓
REJECT

Do not describe integrity validation as proof of truth.

---

48. M14 PROVENANCE TESTING

Where provenance is required:

valid predecessor evidence
↓
M14
↓
ACCEPT

versus:

unrelated or forged predecessor representation
↓
M14
↓
REJECT

The implementation must follow the actual contract.

---

49. M14 CI

Record:

M14 SHA
M13 dependency SHA
runtime
environment
workflow
run ID
test matrix
test results
artifacts

Verify that:

SHA BEING SEALED
=
SHA TESTED

Then:

TESTED
↓
CI_VERIFIED
↓
AUDITED
↓
SEALED

---

50. M14 SEAL RECORD

Create:

docs/M14_SEAL_RECORD.md

only after all required audit criteria pass.

The record must contain actual values.

Never write:

<future SHA>
<expected run>
<will pass>

A seal record is evidence, not a plan.

---

51. THE SEAL RECORD STANDARD

Every module seal record should answer five questions:

1. What was sealed?

Exact module and Pre-Name.

2. What commit was sealed?

Exact SHA.

3. What evidence was used?

Tests, CI, artifacts, dependencies.

4. What was NOT proven?

Explicit limitations.

5. What dependency does the seal authorize?

Only the dependency explicitly defined by the architecture.

---

52. MASTER SEAL CHAIN

The controlled progression is:

M11 — CONTINUITY LOCK (STATE PRESERVATION)
↓
M11 CONTRACT
↓
M11 IMPLEMENTATION
↓
M11 TESTED
↓
M11 CI_VERIFIED
↓
M11 AUDITED
↓
M11 SEALED

        ↓

M12 DEPENDENCY AUTHORIZED
↓
M12 — THE MASTERY ARCHIVE (KNOWLEDGE ANCHOR)
↓
M12 CONTRACT
↓
M12 IMPLEMENTATION
↓
M12 TESTED
↓
M12 CI_VERIFIED
↓
M12 AUDITED
↓
M12 SEALED

        ↓

M13 DEPENDENCY AUTHORIZED
↓
M13 — SEMANTIC SCRUBBER (CLEAN DATA PROTOCOL)
↓
M13 CONTRACT
↓
M13 IMPLEMENTATION
↓
M13 TESTED
↓
M13 CI_VERIFIED
↓
M13 AUDITED
↓
M13 SEALED

        ↓

M14 DEPENDENCY AUTHORIZED
↓
M14 — THE AGENTIC LOOP (TASK AUTONOMY GOVERNOR)
↓
M14 CONTRACT
↓
M14 IMPLEMENTATION
↓
M14 TESTED
↓
M14 CI_VERIFIED
↓
M14 AUDITED
↓
M14 SEALED

---

53. WHAT A SEAL AUTHORIZES

A seal authorizes only the next defined dependency.

For example:

M11 SEALED

means:

M11's defined admission boundary has passed its defined audit.

It does not mean:

all V2 is safe

Likewise:

M14 SEALED

does not mean:

M15–M22 are complete.

---

54. GLOBAL HALT CONDITIONS

Stop immediately if:

documentation contradicts implementation

test expectation contradicts contract

CI evidence is missing

V1 runtime becomes an undocumented V2 dependency

raw input bypasses an admission boundary

rejected material reaches downstream processing

fixtures are represented as real evidence

cryptographic primitives are represented as governance

future functionality is represented as implemented

a seal is created without an audit

an unproven dependency is treated as available

Then:

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

55. CRTG BOUNDARY

CRTG must remain explicitly separated from ordinary cryptographic primitives.

If CRTG is still:

DESIGN PENDING

then no M11–M14 implementation may silently behave as though CRTG already exists.

Do not rename an existing mechanism as CRTG merely to satisfy a roadmap requirement.

If a future module requires CRTG:

CRTG dependency
↓
DESIGN PENDING
↓
MODULE BLOCKED

until the dependency is properly designed and demonstrated.

---

56. FOUNDATION SEAL 5 BOUNDARY

Foundation Seal 5 remains a V1 architectural decision unless independently changed through the proper V1 process.

M11–M14 must not silently redefine it.

Therefore:

M11 SEALED
≠
Foundation Seal 5

M14 SEALED
≠
Foundation Seal 5

---

57. TEACHING FORMAT FOR EVERY MODULE

When teaching a module, use this structure:

MODULE NUMBER
+
SWI PRE-NAME
+
WHY IT EXISTS
+
WHAT IT RECEIVES
+
WHAT IT PRODUCES
+
WHAT IT IS ALLOWED TO DO
+
WHAT IT IS NOT ALLOWED TO DO
+
BOUNDARY
+
CONTRACT
+
IMPLEMENTATION
+
TESTS
+
CI
+
AUDIT
+
SEAL
+
LIMITATIONS

This keeps the architecture relatable without confusing conceptual language with demonstrated capability.

---

58. THE THREE-LAYER TEACHING MODEL

Every SWI concept should be explainable at three levels.

Layer 1 — Human explanation

What problem are we solving?

Layer 2 — Architectural explanation

Where does the responsibility live?

Layer 3 — Evidence explanation

What code, test and CI result demonstrates it?

Example:

Human:
"We don't want untrusted material entering the next stage."

Architecture:
"M11 — CONTINUITY LOCK is the admission boundary."

Evidence:
"These tests reject these specific invalid inputs,
and this CI run demonstrates the boundary in the defined environment."

This is the preferred SWI teaching method.

---

59. NO MAGIC MODULES

A module should never be described using words such as:

intelligent
self-validating
fully secure
trustworthy
autonomous
tamper-proof
truth-producing
identity-proving
human-safe

unless those claims are specifically defined, bounded and demonstrated.

Prefer technical descriptions.

For example:

tamper-evident

rather than:

tamper-proof

when the system only detects alteration.

---

60. NO MAGIC CRYPTOGRAPHY

Never teach:

HASH = TRUST

or:

SIGNATURE = TRUTH

or:

ENCRYPTION = SAFETY

Instead:

HASH
→ detects change relative to expected digest

SIGNATURE
→ verifies cryptographic relation under key assumptions

ENCRYPTION
→ protects confidentiality under defined cryptographic assumptions

System-level trust requires more than cryptographic primitives.

---

61. NO MAGIC AI

SWI must not depend on the assumption that an AI model is:

conscious
truthful
self-governing
morally responsible
infallible

The workflow must enforce boundaries independently of the model's personality or confidence.

The model may produce an output.

SWI determines what the workflow permits that output to do.

---

62. MODULE COMPLETION DEFINITION

A module is complete only within its defined scope when:

CONTRACT
+
IMPLEMENTATION
+
TESTS
+
CI
+
AUDIT
+
SEAL

all exist and agree.

Therefore:

CODE EXISTS
≠
MODULE COMPLETE

---

63. FUTURE MODULE RULE

After M14:

DO NOT BULK IMPLEMENT M15–M22

Instead:

M15 ARCHITECTURE REVIEW
↓
M15 DEPENDENCY PROOF
↓
M15 CONTRACT
↓
M15 IMPLEMENTATION
↓
M15 TEST
↓
M15 CI
↓
M15 AUDIT
↓
M15 SEAL

Then repeat.

---

64. FINAL SWI DEVELOPMENT LAW

EVIDENCE BEFORE CLAIM.

BOUNDARY BEFORE EXPANSION.

PRE-NAME FOR UNDERSTANDING.

CONTRACT FOR AUTHORITY.

CODE FOR IMPLEMENTATION.

TEST FOR BEHAVIOUR.

CI FOR REPRODUCIBILITY.

AUDIT FOR CONFIDENCE.

SEAL FOR CONTROLLED DEPENDENCY.

DEPENDENCY BEFORE THE NEXT MODULE.

AND NEVER CLAIM WHAT THE CODE CANNOT DEMONSTRATE.

---

65. CURRENT EXECUTION ORDER

The immediate work must remain:

M11 — CONTINUITY LOCK (STATE PRESERVATION)
↓
D6 malformed JSON
↓
documentation reconciliation
↓
exact-tip two-checkout CI
↓
A–G audit
↓
M11 seal record
↓
M11 SEALED

Only then:

M12 — THE MASTERY ARCHIVE (KNOWLEDGE ANCHOR)
↓
contract
↓
implementation
↓
tests
↓
CI
↓
audit
↓
seal

Only then:

M13 — SEMANTIC SCRUBBER (CLEAN DATA PROTOCOL)
↓
dependency review
↓
contract
↓
implementation
↓
tests
↓
CI
↓
audit
↓
seal

Only then:

M14 — THE AGENTIC LOOP (TASK AUTONOMY GOVERNOR)
↓
dependency review
↓
contract
↓
implementation
↓
tests
↓
CI
↓
audit
↓
seal

Then:

M14 SEALED
↓
ARCHITECTURE REVIEW
↓
M15 DECISION

---

66. FINAL TEACHING PRINCIPLE

SWI should be understandable without pretending it is finished.

The Pre-Names preserve the story of the architecture.

The numbered modules preserve the discipline of implementation.

The contracts preserve the boundaries.

The tests preserve the behavioural evidence.

CI preserves reproducibility.

The audit preserves accountability.

The seal preserves controlled progression.

Therefore:

THE NAME TELLS US WHAT WE WERE TRYING TO SOLVE.

THE CONTRACT TELLS US WHAT WE AGREED TO BUILD.

THE CODE TELLS US WHAT WE ACTUALLY BUILT.

THE TESTS TELL US WHAT WE OBSERVED.

CI TELLS US WHETHER WE CAN REPRODUCE IT.

THE AUDIT TELLS US WHETHER THE EVIDENCE SATISFIES THE GATE.

THE SEAL TELLS US WHETHER THAT DEFINED DEPENDENCY MAY BE USED.

NOTHING MORE.
NOTHING LESS.

SWI moves forward because evidence allows it to move forward — not because the roadmap says the next number is waiting.
