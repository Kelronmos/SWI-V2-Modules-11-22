SWI V2 — NEXT STAGE EXECUTION MANUAL

M11 FINAL AUDIT → CONTROLLED SEAL

Governing principle

«Evidence before claim. Boundary before expansion. Contract before implementation. Tests before confidence. CI before reproducibility. Audit before seal. Seal before dependency. Dependency before the next module.»

And above all:

«Never claim what the code cannot demonstrate.»

---

1. CURRENT POSITION

The V2 architecture has reached the point where M11 can be subjected to its formal closing audit.

The current architecture is:

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
M12 CI Verification
        ↓
M12 Audit / Seal
        ↓
Next Controlled Module

Do not skip the seal boundary.

Do not begin substantive M12 work merely because M11 tests pass.

"TESTED" is not "SEALED".

"CI_VERIFIED" is not "SEALED".

"SEALED" is a scoped architectural decision based on the completed audit evidence.

---

2. FREEZE THE AUDITED TIP

Before making any changes:

Record:

V2 audited SHA:
V1 producer SHA:
Workflow:
Workflow run:
Python versions:
Artifact identity:

The previous verified two-checkout evidence was:

V2:
061a47ff23705684179cb48836051c8b097e1b65

V1:
be31dd733e7fba17ceddb0b142a075abcfca890a

Workflow:
two_checkout_travel.yml

Run:
34987307390

Status:
GREEN

Do not silently substitute a new SHA for the audited SHA.

If the repository has moved since that evidence, establish a new audited tip and rerun the required verification.

---

3. COMPLETE THE M11 AUDIT WORKSHEET

Open:

docs/M11_SEAL_AUDIT_WORKSHEET.md

Evaluate every requirement A–G.

Every item must receive one of:

PASS
FAIL
NOT PROVEN

There is no:

almost
probably
effectively
should pass

A seal requires evidence.

---

4. AUDIT A — CONTRACT FREEZE

Verify that the integrity-covered fields remain exactly:

payload
foundation_version
evidence_schema_version
evidence_id
source_reference

Verify:

created_at

remains explicitly outside the digest.

Verify that tests and implementation agree.

Verify supported foundation/schema versions.

Verify unsupported versions reject.

Verify verification-status values distinguish fixture/test data from the actual:

v1_trainer_pipeline_completed

Verify unknown statuses reject.

No silent contract expansion.

No new integrity-covered field may be introduced during this audit.

If the contract has changed, stop and restart contract review.

---

5. AUDIT B — ARCHITECTURAL BOUNDARY

The V2 boundary must remain:

V1 runtime
    ↓
serialized evidence
    ↓
V2 admission

NOT:

V1 runtime object
    ↓
V2

Verify:

- no V1 Python import is required by V2;
- "import swi_core" is unavailable in the isolated admission environment;
- no "PYTHONPATH" manipulation is being used;
- no "sys.path" manipulation is being used;
- M10 is not treated as the V2 handoff;
- V1 evidence is not mutated in place;
- V2 derives its own admitted state;
- admission works without V1 being installed beside V2.

The rule is:

«Serialization is the boundary.»

---

6. AUDIT C — REAL PRODUCER

Verify that the happy path originates from the actual V1 producer.

The expected conceptual path remains:

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

Fixtures may exist for negative/unit tests.

Fixtures must not secretly replace the real producer in the primary cross-repository path.

The distinction must remain visible:

REAL PRODUCER

versus:

TEST FIXTURE

---

7. AUDIT D — ADMISSION BEHAVIOUR

The following behaviours must remain demonstrated.

Valid evidence

Valid serialized V1 evidence
        ↓
ACCEPT
        ↓
AdmittedInput

Tampered payload

Changed payload
        ↓
REJECT

Changed integrity reference

Changed integrity_reference
        ↓
REJECT

Unsupported verification status

Unsupported status
        ↓
REJECT

Missing required field

Missing required field
        ↓
REJECT

Malformed JSON

Malformed JSON
        ↓
REJECT

Unsupported schema/foundation version

Unsupported version
        ↓
REJECT

Raw/non-envelope input

PipelineResult-shaped dict
        ↓
REJECT

The important boundary is:

RAW
 ↓
M11
 ↓
AdmittedInput

Not:

RAW
 ↓
Kernel

---

8. AUDIT E — KERNEL ISOLATION

The kernel must only receive the admitted type.

Required:

AdmittedInput
        ↓
Kernel

Forbidden:

dict
JSON
raw envelope
rejected evidence
        ↓
Kernel

The enforcement mechanism must therefore reject raw values before they can cross the kernel boundary.

A rejected M11 input must not continue downstream.

---

9. AUDIT F — TWO-CHECKOUT REPRODUCIBILITY

The two-checkout test must demonstrate the architecture rather than merely run two folders.

Required model:

CHECKOUT 1
V1
 ↓
real producer
 ↓
serialized artifact


CHECKOUT 2
V2
 ↓
receives artifact
 ↓
M11 admission
 ↓
tamper tests
 ↓
isolation tests

The test must establish:

- V1 producer works;
- artifact is actually produced;
- V2 receives the serialized artifact;
- V1 import is unavailable;
- valid evidence is admitted;
- tampered evidence is rejected;
- integrity alteration is rejected;
- unit/isolation tests pass.

Record the exact:

V1 SHA
V2 SHA
Python matrix
workflow run
artifact identity
result

A previous green run is evidence for that exact audited state.

If code changes after that run, rerun CI.

---

10. AUDIT G — DOCUMENTATION HONESTY

Review:

docs/MODULE_STATUS.md
docs/M11_SEAL_AUDIT_WORKSHEET.md
docs/M11_EVIDENCE_COLLECTION_AND_SEAL_VERIFICATION.md
docs/CROSS_REPO_TRAVEL.md
docs/V2_CLOSING_EXECUTION_MANUAL.md
docs/V2_CLOSING_AND_M11_SEAL_MANUAL.md
docs/CONTROLLED_EXECUTION_M11_TO_M14_MANUAL.md

Remove or reconcile stale claims such as:

Two-checkout CI PENDING

if the exact audited tip is now CI verified.

However, do NOT turn:

CI_VERIFIED

into:

SEALED

merely by editing documentation.

Documentation follows evidence.

It does not create evidence.

---

11. M11 SEAL DECISION

M11 becomes seal-eligible only if:

A PASS
B PASS
C PASS
D PASS
E PASS
F PASS
G PASS

AND

exact audited two-checkout CI = GREEN

Then:

SEAL ELIGIBLE

Only at that point create:

docs/M11_SEAL_RECORD.md

---

12. M11 SEAL RECORD

The seal record must state:

Module:
M11

Scope:
Serialized V1 evidence admission

Audited V1 SHA:
<exact SHA>

Audited V2 SHA:
<exact SHA>

Workflow:
<workflow>

Workflow Run:
<run>

Python Matrix:
<versions>

Audit:
A PASS
B PASS
C PASS
D PASS
E PASS
F PASS
G PASS

Status:
SEALED

It must also explicitly state what the seal does NOT prove.

At minimum:

This seal does not prove truth.

This seal does not prove origin.

This seal does not prove identity.

This seal does not prove universal safety.

This seal does not constitute CRTG.

This seal does not constitute Foundation Seal 5.

This seal does not constitute completion of V2.

This seal authorizes only the defined downstream dependency boundary.

---

13. UPDATE MODULE STATUS

Only after the seal record exists may:

M11

change from:

TESTED / NOT SEALED

to:

SEALED

The wording must remain scoped.

Do not write:

V2 COMPLETE

Do not write:

Foundation VERIFIED

Do not write:

AI SAFETY PROVEN

Do not write:

CRTG COMPLETE

None of those conclusions follow from an M11 admission seal.

---

14. RUN CI AGAIN AFTER THE SEAL COMMIT

This step matters.

If the seal record and status files create a new commit, the old CI run does not automatically prove the new commit.

Therefore:

Seal commit
   ↓
CI
   ↓
GREEN

Record the new verification.

The final state should therefore have evidence attached to the actual repository tip.

---

15. STOP CONDITION

Once M11 is sealed and the post-seal commit has green CI:

STOP.

Do not immediately implement M12 in the same change.

Do not bulk-create M13–M22.

Do not introduce CRTG.

Do not introduce Foundation Seal 5.

Do not alter the frozen M11 contract.

Do not redesign V1.

The purpose of this stop is controlled dependency.

---

16. ONLY THEN BEGIN M12

The next development stage is:

M12 — CONTRACT DESIGN

Not:

M12 implementation

Not:

M12 production-ready

Not:

M12 complete

First define what M12 is allowed to receive and what it is allowed to produce.

The current M12 code is only a controlled type-boundary scaffold.

That is acceptable.

Do not pretend it is normalization.

---

17. M12 CONTRACT-FIRST LOOP

The next module follows:

M11 SEALED
      ↓
M12 PRE-NAME
      ↓
M12 PURPOSE
      ↓
M12 INPUT CONTRACT
      ↓
M12 OUTPUT CONTRACT
      ↓
M12 INVARIANTS
      ↓
M12 FAILURE STATES
      ↓
M12 SECURITY BOUNDARY
      ↓
M12 IMPLEMENTATION
      ↓
M12 TESTS
      ↓
M12 CI
      ↓
M12 AUDIT
      ↓
M12 SEAL

Only after M12 is sealed does the next controlled dependency begin.

---

18. THE REPEATING SWI DEVELOPMENT LAW

Every subsequent module follows the same discipline:

PRE-NAME
   ↓
PURPOSE
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
AUDIT
   ↓
SEAL
   ↓
NEXT DEPENDENCY

The module's Pre-Name should remain visible because it teaches the architecture in human language.

The technical module name establishes implementation authority.

The Pre-Name establishes conceptual understanding.

Neither should be allowed to replace the other.

---

19. FINAL GOVERNANCE RULE

SWI must never become a system where documentation gets ahead of implementation.

Therefore:

If documentation says it,
the code must demonstrate it.

If the code demonstrates it,
tests must verify it.

If tests verify it,
CI must reproduce it.

If CI reproduces it,
the audit must establish its scope.

If the audit passes,
the module may be sealed.

If the module is sealed,
the next dependency may begin.

And:

«Three years of architecture cannot honestly be compressed into three months by simply renaming unfinished work as completed work.»

The objective is not to move quickly by skipping evidence.

The objective is to make each step strong enough that the next step can safely depend on it.

M11 first. Then M12. One controlled boundary at a time.
