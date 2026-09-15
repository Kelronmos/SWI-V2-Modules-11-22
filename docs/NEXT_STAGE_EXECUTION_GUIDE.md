SWI V2 — NEXT STAGE EXECUTION GUIDE

Stage: M11 Final Audit → M11 Seal

Current position

Work from the current V2 repository state.

Known evidence:

- V2 audited tip: "061a47ff23705684179cb48836051c8b097e1b65"
- V1 producer tip: "be31dd733e7fba17ceddb0b142a075abcfca890a"
- Two-checkout workflow: "two_checkout_travel.yml"
- Green workflow run: "34987307390"
- M11: "TESTED / NOT SEALED"
- M12: "DESIGN PENDING / type boundary only"

The objective of this stage is not new functionality.

The objective is to convert existing evidence into a formally auditable M11 seal.

---

STEP 1 — FREEZE THE CURRENT TIP

Do not change:

- M11 contract;
- M11 admission behaviour;
- kernel boundary;
- existing passing tests;
- V1 producer;
- two-checkout architecture.

The audited implementation must remain stable while the audit is performed.

---

STEP 2 — OPEN THE M11 AUDIT WORKSHEET

Open:

docs/M11_SEAL_AUDIT_WORKSHEET.md

Work through:

A
B
C
D
E
F
G

Do not mark anything PASS because the code "looks correct."

Each PASS needs observable evidence.

---

STEP 3 — AUDIT A: CONTRACT

Confirm:

payload
foundation_version
evidence_schema_version
evidence_id
source_reference

are exactly the integrity-covered fields.

Confirm:

created_at

is outside the digest.

Confirm unsupported versions reject.

Confirm unknown verification states reject.

Decision:

A = PASS

only if the code, tests and documentation agree.

---

STEP 4 — AUDIT B: BOUNDARY

Prove:

V1 runtime
↓
serialized evidence
↓
V2 M11

and NOT:

V1 runtime object
↓
V2

Confirm:

import swi_core

is unavailable in the V2 admission environment.

Confirm there is no:

PYTHONPATH
sys.path
local path injection

being used to create a false separation.

Confirm M10 is not being represented as the V2 handoff.

Decision:

B = PASS

only with evidence.

---

STEP 5 — AUDIT C: REAL PRODUCER

Verify that the happy path uses the real V1 producer.

Expected:

Trainer
↓
PipelineResult
↓
export_foundation_evidence()
↓
serialized evidence
↓
V2 M11

Fixtures are acceptable for negative/unit tests.

Fixtures must not be the only evidence of cross-repository travel.

Decision:

C = PASS

---

STEP 6 — AUDIT D: ADMISSION

Confirm all important rejection paths.

Minimum matrix:

valid evidence                 → ACCEPT
payload modified               → REJECT
integrity modified             → REJECT
unsupported status             → REJECT
required field removed         → REJECT
malformed JSON                 → REJECT
unsupported schema             → REJECT
unsupported foundation         → REJECT
raw dictionary                 → REJECT
PipelineResult-shaped object   → REJECT

Confirm malformed JSON is actually tested.

Decision:

D = PASS

---

STEP 7 — AUDIT E: KERNEL

Prove that only admitted evidence can enter the kernel.

Required:

RAW
 ↓
M11
 ↓
AdmittedInput
 ↓
Kernel

Rejected M11 input must not continue.

Raw dictionaries must not bypass admission.

Decision:

E = PASS

---

STEP 8 — AUDIT F: TWO-CHECKOUT CI

Use the actual green workflow evidence.

Record:

V1 SHA
V2 SHA
workflow
run number
Python versions
producer result
admission result
tamper result
bad-integrity result
import-isolation result
unit-test result

Current known evidence:

V1:
be31dd733e7fba17ceddb0b142a075abcfca890a

V2:
061a47ff23705684179cb48836051c8b097e1b65

Run:
34987307390

Do not replace these with a branch name.

The seal must attach to the exact audited commits.

Decision:

F = PASS

---

STEP 9 — AUDIT G: DOCUMENTATION

Search the repository for contradictory current-state language.

Especially search:

Two-checkout CI PENDING
M11 PENDING
M11 SEALED
M11 COMPLETE
V2 COMPLETE
CRTG IMPLEMENTED
Foundation Seal 5

Correct only statements that are objectively stale.

Do not rewrite historical procedures simply because they contain the word PENDING.

Historical instructions may remain historical.

Current status must reflect current evidence.

Decision:

G = PASS

---

STEP 10 — FINAL DECISION

Only proceed if:

A = PASS
B = PASS
C = PASS
D = PASS
E = PASS
F = PASS
G = PASS

AND:

exact audited two-checkout CI = GREEN

If even one is:

FAIL

stop.

If evidence is insufficient:

NOT PROVEN

stop.

There is no:

almost sealed

state.

---

STEP 11 — CREATE THE SEAL RECORD

Create:

docs/M11_SEAL_RECORD.md

Use the exact audited evidence.

The record must state:

M11 SEALED

only after A–G pass.

The seal is scoped to M11 admission.

It does not mean:

SWI is universally safe
SWI is fully verified
V2 is complete
CRTG exists
Foundation Seal 5 exists
identity is verified
evidence is necessarily true

---

STEP 12 — UPDATE CURRENT STATUS

After the seal record exists, update the current module status from:

M11 = TESTED / NOT SEALED

to:

M11 = SEALED

Only if the seal record genuinely exists and A–G passed.

Do not update the status first.

The evidence record comes first.

---

STEP 13 — RUN CI AGAIN

Because the documentation/status changed, run the repository CI again.

This creates a new exact tip.

Do not accidentally claim the old CI run proves the new commit.

Record:

old audited implementation SHA
↓
documentation/seal commit
↓
new CI result
↓
final audited SHA

If the final seal commit is the commit being represented as the sealed state, its required CI must also be green.

---

STEP 14 — STOP

Once M11 is genuinely sealed:

STOP.

Do not implement M12 in the same change.

Do not modify M11 to prepare for M12.

Do not add CRTG.

Do not introduce V1 dependencies.

Do not create M13–M22 implementation.

Do not bulk-generate modules.

The next stage begins only after M11 is independently closed.

---

STEP 15 — NEXT STAGE AFTER M11

Only then begin:

M12 CONTRACT DESIGN

Not:

M12 implementation

First answer:

What exactly enters M12?

What exactly leaves M12?

What does M12 transform?

What must M12 preserve?

What causes rejection?

What is deterministic?

What does M12 NOT prove?

Then freeze the contract.

Then implement.

Then test.

Then CI.

Then audit.

Then seal.

---

CONTROLLED LOOP

Every module follows:

CONTRACT
↓
IMPLEMENT
↓
TEST
↓
CI
↓
AUDIT
↓
SEAL
↓
DEPENDENCY
↓
NEXT MODULE

Never:

IMPLEMENT
↓
IMPLEMENT
↓
IMPLEMENT
↓
AUDIT EVERYTHING LATER

That is exactly the failure mode this process is designed to prevent.

FINAL RULE

For this stage, the only objective is:

«Turn M11's existing technical evidence into a defensible, scoped M11 seal.»

Nothing more.
