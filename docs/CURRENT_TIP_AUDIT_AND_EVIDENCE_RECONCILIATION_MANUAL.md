SWI V2 — CURRENT-TIP AUDIT & EVIDENCE RECONCILIATION MANUAL

Repository: "Kelronmos/SWI-V2-Modules-11-22"
Audit date: 2026-09-22
Audited branch: "main"
Current tip: "8a5c533b514c13eff575b6822d79f0889d8a5664"
Project status: RESEARCH / EXPERIMENTAL
Production authorization: NONE

---

0. PURPOSE

This manual defines the controlled procedure for auditing the current SWI V2 repository before making further implementation changes.

The purpose is not to make the repository appear more complete.

The purpose is to establish:

WHAT EXISTS
WHAT WAS TESTED
WHAT PASSED
WHAT FAILED
WHAT IS SEALED
WHAT IS NOT SEALED
WHAT REMAINS UNPROVEN
WHAT SHOULD BE DONE NEXT

The governing rule is:

DO NOT FIX A REMEMBERED PROBLEM.

VERIFY THE CURRENT TIP.

THEN FIX ONLY THE DEMONSTRATED GAP.

---

1. GOVERNING SWI EVIDENCE LAW

All work in this manual follows:

CLAIM
  ↓
IMPLEMENTATION
  ↓
TEST
  ↓
RESULT
  ↓
LIMITATION
  ↓
NEXT ITERATION

No step may silently substitute for another.

In particular:

DOCUMENTATION ≠ IMPLEMENTATION

IMPLEMENTATION ≠ PROOF

TEST PASS ≠ SEAL

CI GREEN ≠ PRODUCTION AUTHORIZATION

TAMPER-EVIDENT ≠ TAMPER-PROOF

EVIDENCE ≠ AUTHORITY

ADMISSION ≠ AUTHORIZATION

AUTHORIZATION ≠ ACTION

---

2. CORE AUTHORITY INVARIANT

SWI V2 maintains the separation:

DATA
  ↓
EVIDENCE
  ↓
ADMISSION
  ↓
AUTHORIZATION
  ↓
ACTION

Therefore:

DATA ≠ EVIDENCE
EVIDENCE ≠ ADMISSION
ADMISSION ≠ AUTHORIZATION
AUTHORIZATION ≠ ACTION

A successful test at one layer does not automatically prove the next layer.

---

3. CURRENT-TIP IDENTITY

The audit MUST begin by establishing repository identity.

Required:

Repository:
Kelronmos/SWI-V2-Modules-11-22

Branch:
main

HEAD:
8a5c533b514c13eff575b6822d79f0889d8a5664

The current HEAD commit is:

docs: SWI CEK God's-Eye Flow Observability Manual (architecture freeze)

The commit explicitly preserves the following boundaries:

CEK = architecture freeze

No CEK runtime implementation.

M11 unchanged.

PRE-CONSEQUENCES separate.

CEK does not authorize execution.

CEK does not replace ReturnGate.

CEK does not replace PR-009.

CEK does not create a seal.

Therefore CEK must remain classified as:

ARCHITECTURE
NOT RUNTIME

---

4. CURRENT-TIP CI EVIDENCE

The current tip has successful workflow evidence associated with:

HEAD SHA:
8a5c533b514c13eff575b6822d79f0889d8a5664

pre-R boundary experiment

Workflow:
pre-R boundary experiment

Run:
35598054694

Run number:
27

Conclusion:
SUCCESS

two-checkout travel

Workflow:
two-checkout-travel

Run:
35598054688

Run number:
126

Conclusion:
SUCCESS

Both runs point to the current HEAD.

Therefore the following claim is supportable:

CURRENT TIP HAS SUCCESSFUL CI EVIDENCE

Do not expand that claim into:

SYSTEM SECURE
SYSTEM SAFE
PRODUCTION READY
UNIVERSALLY ENFORCED

Those are different propositions.

---

5. M11 STATUS

M11 must be treated separately from PR-009 and CEK.

Current documentation records M11 as:

SEALED

The current CEK commit also explicitly states:

M11 unchanged

Therefore this audit does not reopen M11.

Rule

M11 SEALED
      ↓
NO CASUAL REOPEN
      ↓
NO DEPENDENCY INFERENCE
      ↓
NO RETROACTIVE MODIFICATION

Any future M11 change requires its own controlled seal/reseal procedure and evidence chain.

---

6. PR-009 CURRENT STATE

PR-009 is located at:

experimental/response_boundary/enforcement.py

Tests:

tests/pre_r/test_pr009_enforcement.py

Current documented status:

IMPLEMENTED
TESTED
EXPERIMENTAL
NOT SEALED
NOT PRODUCTION AUTHORIZED

This is the correct classification.

---

7. PR-009 RESPONSIBILITY

PR-009 exists to bind an admission decision to executable authority.

Conceptually:

Response
   ↓
ReturnGate
   ↓
REJECT / HALT ─────→ HaltedWorkflow
                          ↓
                     may_execute = False

ADMIT ─────────────→ AdmittedResponse
                          ↓
                     may_execute = True
                          ↓
                 privileged_action()

The important distinction is:

ReturnGate = admission

PR-009 = enforcement binding for the protected experimental API

PR-009 does not turn the entire operating environment into a universally enforced security boundary.

---

8. CURRENT PR-009 TEST EVIDENCE

Current tests document successful coverage for the protected experimental API.

Evidence includes:

VALID ADMIT
→ AdmittedResponse
→ may_execute = True

REJECT
→ privileged_action blocked

HALT
→ may_execute = False

HaltedWorkflow
→ require_executable rejects

RAW ENVELOPE
→ require_executable rejects

REJECT
→ no privileged output

ADMIT
→ privileged read permitted

Additional adversarial coverage includes:

serialize → deserialize
raw/mutated object attempts
copied halted objects
altered halted objects
raw REJECT conversion attempts
mutated admitted-object attempts

These tests materially strengthen the current PR-009 evidence.

---

9. T20 INTERPRETATION

The earlier problem was described as:

T20 caller ignores REJECT

The current implementation now contains enforcement tests that exercise the protected privileged path.

Therefore the old statement:

T20 not tested

must no longer be treated as the current implementation state without qualification.

The accurate distinction is:

T20 / protected enforcement API
                ↓
              TESTED

but:

ARBITRARY CALLER / EVERY POSSIBLE EXECUTION PATH
                ↓
             NOT PROVEN

These are not contradictory.

They operate at different proof levels.

---

10. THE REMAINING ENFORCEMENT GAP

The current limitation is structural scope.

PR-009 protects calls that use:

enforce()
require_executable()
privileged_action()

The repository documentation explicitly limits the claim.

Therefore:

PROTECTED API ENFORCEMENT
        = DEMONSTRATED

while:

PROCESS-WIDE ENFORCEMENT
        = NOT PROVEN

and:

OS-WIDE ENFORCEMENT
        = NOT PROVEN

and:

EVERY POSSIBLE CALLER
        = NOT PROVEN

and:

STRUCTURAL IMPOSSIBILITY OF BYPASS
        = NOT PROVEN

This is a limitation, not something that should be hidden by stronger wording.

---

11. FAIL-CLOSED VS FAIL-SAFE

These must remain separate.

FAIL-CLOSED

Question:

Can this request be admitted?

Rule:

PROVEN
    → ADMIT

NOT PROVEN
    → REJECT / HALT

This is the admission boundary.

---

FAIL-SAFE

Question:

What happens after the system cannot safely proceed?

Required behaviour:

FAILURE
  ↓
STOP
  ↓
NON-EXECUTING STATE
  ↓
NO PRIVILEGED SIDE EFFECT
  ↓
NO UNVALIDATED OUTPUT RELEASE
  ↓
EXPLICIT RECOVERY

Therefore:

REJECT = decision

FAIL-SAFE = enforced behaviour after the decision

Do not treat the words as interchangeable.

---

12. RECOVERY BOUNDARY

Automatic recovery is not currently established as a production-authorized capability.

The repository documents:

AUTHORIZED RECOVERY
= NOT IMPLEMENTED

Therefore:

HALT
≠
RECOVER
≠
AUTHORIZE

A halt-clearing operation must never be treated as authorization by implication.

Required conceptual separation:

record_halt()
      ≠
clear_halt()
      ≠
authorize_execution()

---

13. CEK — CURRENT STATUS

CEK / “God's-Eye” is currently an architecture layer.

The current tip establishes:

CEK geometry
CEK terminology
CEK observability architecture
CEK evidence path

But does not establish:

CEK runtime implementation
CEK authorization
CEK execution
CEK sealing

Therefore:

CEK = ARCHITECTURE FREEZE

NOT:

CEK = IMPLEMENTED RUNTIME

No runtime implementation should be added merely because the architecture has been documented.

---

14. PRE-CONSEQUENCES

PRE-CONSEQUENCES remains a separate architectural concern.

Current state:

SEPARATED
NOT ABSORBED INTO PR-009
NOT IMPLEMENTED AS A UNIVERSAL RUNTIME

This separation must be preserved.

Do not create false equivalence:

PR-009
≠
PRE-CONSEQUENCES

and:

CEK
≠
PRE-CONSEQUENCES

---

15. HISTORICAL DOCUMENT RECONCILIATION

Some repository documents describe earlier states.

Example:

Historical state:
adversarial tests still planned

Current state:

adversarial tests now present

Therefore the correct procedure is not to delete history.

Instead:

HISTORICAL RECORD
        +
CURRENT-TIP STATUS
        +
DATE / SHA
        ↓
RECONCILED EVIDENCE

Historical records should remain identifiable as historical.

Never rewrite history to make the current repository appear cleaner than it was.

---

16. DOCUMENTATION STATUS RULE

Every security or architecture document should identify:

DATE
COMMIT / SHA
SCOPE
STATUS
WHAT WAS TESTED
WHAT PASSED
WHAT WAS NOT TESTED
LIMITATIONS
NEXT STEP

Recommended status vocabulary:

DESIGNED
IMPLEMENTED
TESTED
CI-VERIFIED
SEALED
PRODUCTION AUTHORIZED

These are independent states.

Example:

IMPLEMENTED + TESTED
≠
SEALED

and:

SEALED
≠
PRODUCTION AUTHORIZED

unless an explicit authorization process establishes that relationship.

---

17. EVIDENCE TABLE

The audit record should use a table like this:

Proposition| Evidence| Current state
Current HEAD identified| Git commit| PROVEN
Current pre-R workflow passes| CI run on HEAD| PROVEN
Two-checkout travel passes| CI run on HEAD| PROVEN
PR-009 implementation exists| Source inspection| PROVEN
Protected privileged path blocks REJECT| Tests| PROVEN
HALT is non-executable in protected path| Tests| PROVEN
Raw envelope cannot directly execute| Tests| PROVEN
Arbitrary caller cannot bypass all enforcement| No universal proof| NOT PROVEN
Process-wide enforcement| No evidence| NOT PROVEN
OS-wide enforcement| No evidence| NOT PROVEN
CEK runtime implementation| Explicitly absent| NOT IMPLEMENTED
PRE-CONSEQUENCES runtime| Explicitly separate| NOT IMPLEMENTED
PR-009 seal| No| NOT SEALED
Production authorization| No| NOT AUTHORIZED

---

18. DO NOT DUPLICATE EXISTING WORK

Before writing code, perform:

SEARCH
  ↓
INSPECT
  ↓
COMPARE
  ↓
TEST EXISTING IMPLEMENTATION
  ↓
IDENTIFY ACTUAL GAP
  ↓
ONLY THEN IMPLEMENT

The following are specifically prohibited as automatic next steps:

duplicate T20
duplicate enforcement.py
rebuild ReturnGate
rebuild M11
implement CEK runtime prematurely
merge PRE-CONSEQUENCES into PR-009
create a new seal without a seal gate

---

19. CONTROLLED NEXT-EXPERIMENT OPTION

If a new technical experiment is justified, it should target the actual remaining question:

«Can an arbitrary caller bypass the protected enforcement boundary?»

That experiment must be defined independently.

Potential proof structure:

PROTECTED CALLER
      ↓
EXPECTED BLOCK
      ↓
PASS

UNPROTECTED CALLER
      ↓
ATTEMPT BYPASS
      ↓
OBSERVE RESULT
      ↓
CLASSIFY

Possible results:

BLOCKED

or:

BYPASS CONFIRMED

or:

TEST OUT OF SCOPE

or:

ENVIRONMENTAL LIMITATION

Do not predetermine the result.

---

20. ADVERSARIAL TEST PRINCIPLE

Every new test must specify:

ATTACK
PRECONDITION
ENTRY POINT
EXPECTED RESULT
OBSERVED RESULT
ARTIFACT
COMMIT
CI RUN
LIMITATION

Example:

ATTACK:
caller attempts to execute without AdmittedResponse

EXPECTED:
no privileged side effect

OBSERVED:
???

CONCLUSION:
only after execution

A test name is not evidence.

A green test is evidence of the tested proposition—not of every proposition around it.

---

21. INDEPENDENT AUDIT GATE

Before changing the security boundary, perform an independent audit.

The auditor should ask:

1. Is this the current HEAD?

2. Does the implementation actually exist?

3. Do the tests exercise the implementation?

4. Does CI test the same commit?

5. Are historical results being confused with current results?

6. Does the claim exceed the test scope?

7. Is a limitation being disguised as a success?

8. Does the proposed change duplicate existing functionality?

9. Does the change cross an authority boundary?

10. Would the change affect M11's seal?

11. Does the change affect CEK's architecture boundary?

12. Does the change affect PRE-CONSEQUENCES?

13. Is production authorization being implied?

Any unresolved answer:

PAUSE

---

22. M11 REASSESSMENT GATE

M11 must not be reassessed merely because another experiment passes.

Required logic:

PR-009 evidence
      ↓
PR-009 limitation
      ↓
independent audit
      ↓
M11 dependency analysis
      ↓
only if required
      ↓
M11 reassessment

Never:

PR-009 PASS
      ↓
M11 automatically promoted

---

23. SEAL RULE

A seal must correspond to an explicit evidence package.

Minimum conceptual chain:

SEALED RECORD
+
EXACT SOURCE SHA
+
TEST EVIDENCE
+
CI RUN
+
COMMIT MATCH
+
INDEPENDENT VERIFICATION
+
REPLAY / RECONSTRUCTION

If any required element is absent:

SEAL = NOT PROVEN

The seal is a conclusion from evidence.

It is not a replacement for evidence.

---

24. PRODUCTION BOUNDARY

The current research repository must continue to state:

NOT PRODUCTION AUTHORIZED

This remains true even when:

tests pass
CI passes
M11 is sealed
PR-009 is implemented
CEK architecture is frozen

Those facts do not independently constitute production authorization.

---

25. REPOSITORY CHANGE PROTOCOL

For any future implementation:

STEP 01
Record current SHA.

STEP 02
Identify exact proposition to prove.

STEP 03
Inspect existing implementation.

STEP 04
Inspect existing tests.

STEP 05
Inspect existing documentation.

STEP 06
Define smallest required change.

STEP 07
Create isolated change.

STEP 08
Run focused tests.

STEP 09
Run full relevant suite.

STEP 10
Run CI.

STEP 11
Verify CI SHA equals intended commit.

STEP 12
Record result.

STEP 13
Record limitations.

STEP 14
Update status documentation.

STEP 15
Independent audit.

STEP 16
Only then consider seal/promotion.

---

26. STOP CONDITIONS

The workflow must HALT if:

CURRENT SHA UNKNOWN

TEST RESULT NOT TRACEABLE

CI RESULT BELONGS TO ANOTHER COMMIT

IMPLEMENTATION CLAIM EXCEEDS SOURCE

TEST CLAIM EXCEEDS TEST SCOPE

HISTORICAL RESULT PRESENTED AS CURRENT

SEAL DEPENDENCY UNKNOWN

AUTHORITY BOUNDARY UNCLEAR

PROPOSED CHANGE DUPLICATES EXISTING WORK

PRODUCTION STATUS AMBIGUOUS

The correct response to an unresolved security proposition is:

NOT PROVEN

not:

PROBABLY SAFE

---

27. CURRENT-TIP DECISION RECORD

At the conclusion of the 2026-09-22 audit:

CURRENT TIP
8a5c533b514c13eff575b6822d79f0889d8a5664

        ↓

CI
PASS

        ↓

PR-009
IMPLEMENTED

        ↓

PROTECTED-PATH TESTS
PRESENT / PASSING

        ↓

PR-009
EXPERIMENTAL / NOT SEALED

        ↓

UNIVERSAL ENFORCEMENT
NOT PROVEN

        ↓

CEK
ARCHITECTURE FREEZE / NO RUNTIME

        ↓

PRE-CONSEQUENCES
SEPARATE

        ↓

M11
UNCHANGED / RECORDED SEALED STATE

        ↓

PRODUCTION
NOT AUTHORIZED

---

28. NEXT ACTION

The next action is not automatically coding.

The next controlled action is:

RECONCILE CURRENT EVIDENCE
        ↓
UPDATE HISTORICAL STATUS LANGUAGE
        ↓
INDEPENDENT AUDIT
        ↓
IDENTIFY WHETHER A REAL TECHNICAL GAP REMAINS
        ↓
ONLY THEN IMPLEMENT

If no demonstrated gap remains:

STOP.

Stopping is a valid research result.

---

29. SWI RESEARCH DISCIPLINE

The repository is the experiment.

Not the announcement.

Not the memory.

Not the intention.

Not the diagram.

Not the claim.

The evidence chain is:

CLAIM
 ↓
CODE
 ↓
TEST
 ↓
RESULT
 ↓
CI
 ↓
REPLAY
 ↓
LIMITATION
 ↓
AUDIT
 ↓
NEXT ITERATION

The objective is not to make every box green.

The objective is to make every box truthful.

---

30. FINAL OPERATING RULE

DO NOT BUILD BECAUSE WE REMEMBERED IT.

DO NOT FIX BECAUSE WE EXPECT IT TO BE BROKEN.

DO NOT SEAL BECAUSE CI IS GREEN.

DO NOT CALL EXPERIMENTAL CODE PRODUCTION.

DO NOT TURN ARCHITECTURE INTO IMPLEMENTATION BY WORDING.

DO NOT TURN TESTED INTO UNIVERSAL.

DO NOT TURN EVIDENCE INTO AUTHORITY.

VERIFY THE TIP.

TEST THE CLAIM.

RECORD THE RESULT.

RECORD THE LIMITATION.

THEN MOVE THE BOUNDARY.

CURRENT SWI POSITION

                 SWI V2

       ┌───────────────────────┐
       │ CURRENT TIP VERIFIED │
       └──────────┬───────────┴
                  ↓
       ┌───────────────────────┐
       │ PR-009 IMPLEMENTED   │
       │ + PROTECTED TESTS    │
       └──────────┬───────────┴
                  ↓
       ┌───────────────────────┐
       │ LIMITATION REMAINS:  │
       │ UNIVERSAL BYPASS     │
       │ NOT PROVEN           │
       └──────────┬───────────┴
                  ↓
       ┌───────────────────────┐
       │ CEK = ARCHITECTURE   │
       │ NO RUNTIME           │
       └──────────┬───────────┴
                  ↓
       ┌───────────────────────┐
       │ M11 = UNCHANGED      │
       │ SEALED STATE RECORDED│
       └──────────┬───────────┴
                  ↓
       ┌───────────────────────┐
       │ PRODUCTION = NO      │
       └───────────────────────┐

Status vocabulary:

PROVEN       = evidence exists for the defined proposition
TESTED       = defined test executed successfully
CI-VERIFIED  = matching CI evidence exists for the exact commit
SEALED       = explicit seal gate satisfied
AUTHORIZED   = explicit authorization exists

Nothing above should be inferred from another status.

End of manual.
