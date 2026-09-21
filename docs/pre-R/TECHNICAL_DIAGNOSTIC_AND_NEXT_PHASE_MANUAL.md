# SWI / PRE-CONSEQUENCES

## Technical Diagnostic, Separation & Next-Phase Manual

**Document status:** Working manual  
**Date:** 2026-09-21  
**Scope:** V1/V2 documentation, experimental pre-R boundary, PRE-CONSEQUENCES architectural separation  

### Primary doctrine

> Claim → Implementation → Test → Result → Limitation → Next iteration

### Additional invariants

```text
TESTED ≠ SEALED
DATA ≠ AUTHORITY
REGISTRY ≠ IMPLEMENTATION
DOCUMENTATION ≠ PROOF OF RUNTIME BEHAVIOUR
ARCHITECTURAL SEPARATION ≠ INTEROPERABILITY
```

---

## PHASE 0 — Establish the baseline

**Objective**  
Do not modify anything until the repository's actual state is recorded.

### Step 0.1 — Identify repositories

Confirm:

- V1 = SWI-V1-Module-1-10
- V2 = SWI-V2-Modules-11-22

Record:

- Repository
- Branch
- HEAD SHA
- Working tree state
- CI state
- Open PRs
- Relevant documentation
- Relevant experimental code

### Step 0.2 — Establish the V1/V2 boundary

Verify:

- V2 does not import V1 runtime code.
- The permitted relationship is the documented evidence/export travel contract, not a runtime dependency.

### Step 0.3 — Establish M11 state

Do not infer M11 status from filenames.

Check:

- M11 implementation
- M11 tests
- M11 seal record
- CI
- cross-repository tests
- known limitations

Record separately:

- IMPLEMENTED
- TESTED
- AUDITED
- SEALED

Never collapse these into one status.

---

## PHASE 1 — Diagnose the PRE-R documentation

**Objective**  
Determine exactly what the repository currently means by pre-R.

Inspect:

- docs/pre-R/README.md
- docs/pre-R/PRE_MODULE_REGISTRY.md
- docs/pre-R/PR009_ENFORCEMENT.md
- docs/pre-R/TEST_MATRIX.md
- docs/pre-R/LIMITATIONS.md
- docs/pre-R/IMPLEMENTATION_AUTHORIZATION.md

Then search the entire repository for:

- PRE
- pre-R
- PRE-M
- ReturnGate
- PR-009
- standing
- authority
- authorization
- ALLOW
- DENY
- CONSEQUENCE
- PRE-CONSEQUENCES

**Diagnostic question**  
For every occurrence ask:

> Is this describing an existing SWI implementation, an architectural proposal, or another architecture entirely?

Label each occurrence:

- [S] SWI existing
- [E] SWI experimental
- [D] documentation/design only
- [P] PRE-CONSEQUENCES
- [AMBIGUOUS] requires correction

Anything [AMBIGUOUS] becomes a documentation repair candidate.

---

## PHASE 2 — Establish the architectural separation

**Objective**  
Prevent PRE-CONSEQUENCES from being accidentally absorbed into SWI.

Create:

`docs/pre-R/PRE_CONSEQUENCES_SURFACE_SEPARATION.md`

Use this architectural statement:

> PRE-CONSEQUENCES is not a renamed SWI gate.  
> It is not ReturnGate.  
> It is not standing.  
> It is not authorization.  
> It is not PR-009.  
> It is not stronger ALLOW/DENY.  
> It is not an SWI module.  
>  
> It represents a separate architectural surface beginning from a different computational starting condition.  
>  
> That architecture is not implemented in this repository.

---

## PHASE 3 — Define the two surfaces

The documentation should contain two independent paths.

### Surface A — Existing SWI

```text
Existing computational substrate
        ↓
Admission
        ↓
Authority
        ↓
Enforcement
        ↓
Execution
        ↓
Evidence
        ↓
Continuity
```

This is the surface SWI is currently rebuilding.

### Surface B — PRE-CONSEQUENCES

```text
Different computational starting condition
        ↓
PRE-CONSEQUENCES
        ↓
Future architecture
```

Status:

- NOT IMPLEMENTED
- NOT AN SWI MODULE
- NOT A SWI DEPENDENCY
- NOT PROVEN INTEROPERABLE

**Critical diagnostic**  
Do not write:

- SWI → PRE-CONSEQUENCES
- ReturnGate → PRE-CONSEQUENCES
- PR-009 implements PRE-CONSEQUENCES

The separation is architectural, not merely semantic.

---

## PHASE 4 — Diagnose ReturnGate

Treat ReturnGate independently.

Locate its actual implementation.

Determine:

```text
Input
↓
Decision
↓
Output
↓
Caller
↓
Enforcement point
↓
Execution possibility
```

Document exactly what it proves.

For example:

> ReturnGate = admission decision

It must not automatically become:

- lawfulness
- standing
- corrected computational condition
- formation/non-formation
- ultimate authority

**Test categories** (minimum):

- valid admission
- invalid admission
- malformed input
- missing evidence
- ambiguous state
- fail-closed state

Record:

- Expected
- Actual
- Pass/Fail
- Limitation

---

## PHASE 5 — Diagnose PR-009

PR-009 has a different question:

> What happens after rejection?

Trace:

```text
ReturnGate
      ↓
REJECT
      ↓
enforce()
      ↓
HaltedWorkflow
      ↓
may_execute = false
      ↓
privileged action prevented
```

The important distinction is:

- ReturnGate = admission
- PR-009 = enforcement of the rejection boundary

Do not merge their identities.

---

## PHASE 6 — Verify T20

T20 must prove the documented property rather than merely exercise an API.

Required conceptual test:

> Given: privileged operation  
> And: admission = REJECT  
> Then: privileged operation cannot proceed through the enforced PR-009 path.

Record:

```text
T20
Expected: rejection prevents privileged execution
Observed: ______
Result: PASS/FAIL
```

Then explicitly document the limitation:

> Process-wide API bypass remains outside the current proof scope.

That distinction is essential.

---

## PHASE 7 — Diagnose enforcement depth

Ask:

> Is rejection enforced only because the caller voluntarily respects the API?

Compare:

| Level | Description |
|-------|-------------|
| 1 | Caller receives REJECT; caller behaves correctly |
| 2 | enforce() rejects execution |
| 3 | Privileged execution path requires an admissible capability/token |
| 4 | Every relevant execution path is structurally subject to enforcement |
| 5 | Independent verification demonstrates that unauthorized paths cannot escape the defined enforcement boundary |

Do not claim Level 4 or 5 merely because Level 2 or 3 works.

---

## PHASE 8 — Audit laundering paths

Diagnostic:

> Can rejected state be transformed into apparently valid state?

Test:

```text
REJECT
 ↓
serialization
 ↓
deserialization
 ↓
copy
 ↓
wrapper
 ↓
new object
 ↓
privileged operation
```

Also test:

```text
REJECT
 ↓
metadata modification
 ↓
new request
```

and:

```text
REJECT
 ↓
alternate API
 ↓
privileged action
```

Expected invariant:

> REJECTED authority cannot become ADMITTED authority merely through representation changes.

If this is not proven, document it as a limitation.

---

## PHASE 9 — Evidence model diagnosis

For every evidence object determine:

- Who created it?
- What does it attest?
- When was it created?
- What input produced it?
- What operation produced it?
- What integrity mechanism protects it?
- Who can verify it?
- What authority does it actually carry?

Central rule:

> Evidence ≠ Authority

A hash can demonstrate integrity.  
A signature can authenticate provenance.  
Neither automatically proves that an operation was authorized.

Document independently:

- integrity
- provenance
- authorization
- execution
- continuity

---

## PHASE 10 — Certificate / key-rotation diagnosis

Do not begin by assuming one universal certificate.

Diagnose each seam:

```text
Mxx
 ↓
Evidence generated
 ↓
Evidence transferred
 ↓
Evidence verified
 ↓
Authority decision
 ↓
Execution
```

For each seam ask:

1. What exactly is being certified?
2. Who issues it?
3. Who verifies it?
4. What key is used?
5. What happens when the key rotates?
6. Can old evidence still be verified?
7. Can revoked evidence be replayed?
8. Can evidence be copied into another context?
9. Does the certificate prove integrity, identity, authorization, or all three?
10. What happens when verification fails?

Then design the common contract only where the evidence requirements are genuinely equivalent.

---

## PHASE 11 — Key rotation

If certificates eventually become part of the evidence architecture, establish:

- key_id
- algorithm
- issuer
- valid_from
- valid_until
- status
- rotation_version
- evidence_timestamp
- verification policy

Test:

- old key + old evidence
- old key + new evidence
- new key + new evidence
- revoked key + evidence
- unknown key
- expired key
- wrong key
- tampered certificate
- replayed certificate

Expected result should be explicit for every case.

Do not claim "key rotation solved" until those cases have evidence.

---

## PHASE 12 — Continuity diagnosis

Only after the boundary and evidence behaviour are understood should continuity be examined.

For M11 ask:

- What state is being continued?
- How is continuity represented?
- What proves that state belongs to the previous state?
- What happens when continuity breaks?
- Can an invalid continuation be admitted?
- Can state be replayed?
- Can state be forked?

Distinguish:

- continuity evidence
- from authorization evidence

A continuity mechanism does not automatically become an authorization mechanism.

---

## PHASE 13 — M11 seal gate

M11 should not be sealed merely because tests pass.

Sequence:

```text
Implementation
      ↓
Unit tests
      ↓
Boundary tests
      ↓
Adversarial tests
      ↓
Two-checkout regression
      ↓
Evidence documentation
      ↓
Independent audit
      ↓
Seal decision
```

And explicitly:

> TESTED ≠ SEALED

---

## PHASE 14 — M12 opening gate

Only after M11 is genuinely sealed should M12 be opened.

Before implementation:

- M12 contract
- M12 inputs
- M12 outputs
- M12 authority
- M12 dependencies
- M12 evidence
- M12 failure behaviour
- M12 limitations

Then:

```text
contract
 ↓
implementation
 ↓
tests
 ↓
integration
 ↓
audit
```

Do not bulk-implement M12–M22 simply because the registry contains their names.

---

## PHASE 15 — Cross-repository regression

Run the complete travel path:

```text
V1 producer
      ↓
V1 evidence export
      ↓
V2 admission
      ↓
integrity verification
      ↓
valid evidence accepted
```

Then adversarially:

```text
tampered evidence → REJECT
invalid integrity → REJECT
missing V1 import → expected unavailable/failure state
```

Architectural rule:

> V2 consumes the defined V1 evidence contract.  
> V2 does not become dependent on V1 runtime internals.

---

## PHASE 16 — Documentation consistency audit

Run repository-wide searches for contradictory terminology.

Look specifically for claims such as:

- PRE-CONSEQUENCES is implemented
- PRE-CONSEQUENCES is a module
- ReturnGate is PRE-CONSEQUENCES
- PR-009 is PRE-CONSEQUENCES
- standing = authorization
- authorization = corrected starting condition
- tested = sealed
- registry = implementation
- tamper-evident = tamper-proof

Every contradiction gets corrected or explicitly attributed as historical/design material.

---

## PHASE 17 — Independent audit package

Prepare an audit bundle:

1. 01_REPOSITORY_BASELINE.md
2. 02_ARCHITECTURE_BOUNDARIES.md
3. 03_RETURNGATE_EVIDENCE.md
4. 04_PR009_EVIDENCE.md
5. 05_TEST_MATRIX.md
6. 06_CROSS_REPO_EVIDENCE.md
7. 07_LIMITATIONS.md
8. 08_SEAL_CRITERIA.md
9. 09_PRE_CONSEQUENCES_SEPARATION.md

The auditor should be able to answer:

- What exists?
- What was tested?
- What was not tested?
- What is experimental?
- What is sealed?
- What is merely proposed?
- What cannot currently be claimed?

---

## PHASE 18 — Only then consider sealing

Decision tree:

```text
START
                   │
                   ▼
             Diagnose state
                   │
                   ▼
           Define exact contract
                   │
                   ▼
             Implement change
                   │
                   ▼
              Unit tests
                   │
                   ▼
           Boundary/adversarial
                   │
                   ▼
        Cross-repository regression
                   │
                   ▼
          Evidence documentation
                   │
                   ▼
          Independent audit
                   │
             ┌────┴────┐
             │           │
           PASS         FAIL
             │           │
             ▼           ▼
        Seal review    Document gap
             │           │
             ▼           ▼
        SEAL / NO SEAL  Next iteration
```

---

## Final architectural position

The repository should ultimately make this distinction impossible to miss:

```text
SWI
                  │
      existing computational substrate
                  │
       admission / authority
                  │
          enforcement
                  │
             execution
                  │
              evidence
                  │
             continuity
                  │
        M11 → M12 → future


        ─────────────────────
          ARCHITECTURAL GAP
        ─────────────────────


          PRE-CONSEQUENCES
                  │
     different computational
        starting condition
                  │
          future architecture
                  │
             NOT BUILT
```

---

## Recommended next-phase order

| Phase | Focus |
|-------|--------|
| 0 | Baseline diagnosis |
| 1 | PRE-R terminology audit |
| 2 | PRE-CONSEQUENCES separation documentation |
| 3 | ReturnGate audit |
| 4 | PR-009 enforcement audit |
| 5 | T20 + adversarial enforcement tests |
| 6 | Laundering/bypass analysis |
| 7 | Evidence-contract audit |
| 8 | Certificate/key-rotation design |
| 9 | Continuity/M11 final audit |
| 10 | Two-checkout V1/V2 regression |
| 11 | Independent audit |
| 12 | M11 seal decision |
| 13 | M12 contract |
| 14 | M12 implementation/testing |
| 15 | Repeat boundary → evidence → audit cycle |

**Most important:** PRE-CONSEQUENCES should remain at Phase 2 as architectural separation. It must not be dragged into Phases 3–15 as another SWI mechanism. Its own implementation, if ever pursued, needs a separate specification and independent proof path.
