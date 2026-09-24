# Firefly Pre-Implementation Test Protocol (F-00 … F-10)

**Status:** DESIGN / PRE-IMPLEMENTATION  
**Date:** 2026-09-24  
**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Current tip at authorship:** 32a0f8f699e76f52099784085aa5cce4ac44c327  
**Firefly implementation:** **NOT IMPLEMENTED** · **NOT AUTHORIZED**  
**Classification:** Documentation only. Does not open execution. Does not claim tests passed against a Firefly adapter.

---

## Purpose

Firefly is intended as a **least-privilege information boundary**, not an unrestricted memory store.

This protocol freezes the adversarial tests that any future Firefly implementation must satisfy **before** it may be considered implemented.

The protocol is deliberately written so that:

- integrity ≠ authority
- freshness/lineage is a separate dimension from cryptographic integrity
- field-level minimization occurs **before** information exposure
- memory assertions cannot launder authority

---

## Core verification dimensions

```text
INTEGRITY
  +
FRESHNESS / LINEAGE
  +
AUTHORITY SCOPE
  +
FIELD-LEVEL MINIMIZATION
```

Not:

```text
hash valid → trusted
```

Instead:

```text
hash valid
  ↓
content integrity established
  ↓
source lineage checked
  ↓
freshness classification
  ↓
authority checked
  ↓
field-level permission checked
  ↓
minimum permitted information released
```

---

## Conceptual gate sequence

```text
WEB / CALLER REQUEST
    │
    ▼
[1] REQUEST IDENTITY
    ├── invalid → HALT
    ▼
[2] CA CERTIFICATE / TRUST ANCHOR
    ├── invalid / expired / unknown → HALT
    ▼
[3] CERTIFICATE KEY / ALGORITHM
    ├── unsupported / malformed → HALT
    ▼
[4] PREVIOUS KERNEL / LINEAGE
    ├── lineage mismatch → HALT
    ▼
[5] ROTATION STATE
    ├── stale / revoked / wrong generation → HALT
    ▼
[6] MODULE / MEMORY EVIDENCE
    ├── missing / unverified → HALT
    ▼
[7] AUTHORITY SCOPE
    ├── request exceeds scope → REFUSE
    ▼
[8] INFORMATION MINIMIZATION (projection)
    ├── return ONLY permitted fields
    ▼
DELIVERY
```

Firefly must not retrieve a whole record into an unrestricted context and merely hide fields at the final output stage. The policy boundary must occur **before** exposure.

---

## Test F-00 — Establish test identity

Record before any other test:

```text
TEST_ID:            FIREfly-AUTH-001
DATE:               2026-09-24
V2_HEAD:            <exact SHA under test>
ENVIRONMENT:        Python 3.10 / 3.11 / 3.12 (as applicable)
FIREfly_IMPLEMENTATION: NOT IMPLEMENTED
TEST_MODE:         DESIGN / PRE-IMPLEMENTATION
```

This prevents the experiment itself from becoming an undocumented claim.

---

## Test F-01 — Certificate identity

Create a test certificate object (example shape only):

```json
{
  "certificate_id": "cert-test-001",
  "issuer": "TEST-CA",
  "subject": "test-client",
  "algorithm": "TEST-ALGORITHM",
  "key_id": "test-key-001",
  "issued_at": "...",
  "expires_at": "...",
  "status": "ACTIVE"
}
```

Record for each required check:

- certificate_present
- issuer_known
- subject_bound
- algorithm_supported
- key_valid
- expiry_valid
- revocation_status

**Expected:** any required failure → **HALT** · no information release.

---

## Test F-02 — CA lineage

Verify:

```text
CLIENT CERTIFICATE
  → INTERMEDIATE CA
  → ROOT CA
  → TRUST ANCHOR
```

Then deliberately break one link.

**Expected:** `CERTIFICATE_LINEAGE_FAILURE` → **REJECT** → **NO INFORMATION RELEASE**.

A certificate must never mean “this person can access everything.”  
It means only: “this certificate satisfies this defined identity/cryptographic contract.”

---

## Test F-03 — Key algorithm

Cases:

| Condition            | Expected |
|----------------------|----------|
| Supported + valid    | Continue |
| Unsupported          | HALT     |
| Unknown              | HALT     |
| Malformed            | HALT     |
| Key mismatch         | HALT     |

The algorithm identifier itself is not authority; it is an input to verification.

---

## Test F-04 — Previous-kernel continuity

Record current and previous kernel/certificate pair. Verify expected predecessor relationship. Then attack with wrong previous kernel.

**Expected:** `LINEAGE_MISMATCH` → **HALT**.

Do not accept: “current certificate is valid, therefore previous-kernel relationship is irrelevant.”

---

## Test F-05 — Rotation

Test valid generations, then:

- revoked generation
- wrong policy generation
- unknown / future / duplicate generation
- rollback to old generation

**Expected:** only valid current generation continues; all others **HALT**.

Rotation must have an independently defined state transition, not merely a new random value.

---

## Test F-06 — Challenge / nonce / request identity

For every authorization attempt bind at least:

- request_id
- challenge
- certificate key reference
- policy version
- kernel reference
- module reference

**Reproducibility of verification** must be separable from **replayability of authorization**.

Replay of an old authorization artifact where freshness is required → **REPLAY / FRESHNESS failure**.

---

## Test F-07 — Authority scope (name-only)

Authority permits only `person.name`. Request asks for the name.

**Expected delivery:**

```json
{ "name": "Example Person" }
```

**Not** the full record (phone, address, medical, financial, internal notes, etc.).

Projection must occur before exposure.

---

## Test F-08 — Authority expansion attack

Authority: `person.name` only.  
Request: `person.name` + `person.address`.

**Expected:** either partial delivery of only the permitted field, or entire request **REFUSE**, according to the frozen contract.  
Invariant: `REQUESTED_SCOPE ⊄ AUTHORIZED_SCOPE` must never become **ALLOW**.

---

## Test F-09 — Memory laundering (mandatory)

Inject metadata such as:

```json
{
  "memory": {
    "previously_verified": true,
    "previously_authorized": true,
    "m11_admitted": true,
    "replay_verified": true
  }
}
```

without corresponding independent verification evidence.

**Expected:** **REJECT**.  
Stored assertion ≠ verification event.

---

## Test F-10 — Freshness attack

Model after the observed useful failure:

- `source_tip` = older tip (e.g. historical law package)
- `HEAD` = current main tip
- Integrity of the package = VALID
- Ancestry / freshness relative to current HEAD = FAIL (or TIP-BOUND only)

**Expected:**

```text
INTEGRITY     = PASS
FRESHNESS     = FAIL (or TIP-BOUND, not HEAD-CURRENT)
AUTHORITY     = NOT ESTABLISHED
DELIVERY      = REFUSED
```

A cryptographically intact memory can still be too old to authorize current action. Do **not** “repair” by rewriting `source_tip` to HEAD.

---

## Decision object (conceptual)

Before any information leaves Firefly, the system should be able to produce a structured decision recording at least:

- request_id
- certificate_verification
- ca_lineage
- key_algorithm
- kernel_lineage
- rotation_state
- memory_integrity
- memory_freshness
- reproduction
- authority_scope
- requested_fields / permitted_fields / denied_fields
- decision (ALLOW only if all mandatory checks PASS)
- policy_version
- evidence_refs

Any mandatory field that is FAIL / UNKNOWN / MISSING / STALE / MISMATCH / UNVERIFIED → `decision ≠ ALLOW`.

---

## Evidence record for every test

Preserve for each run:

TEST ID · DATE/TIME · GIT HEAD · TESTER · ENVIRONMENT · INPUT HASH ·  
CERTIFICATE ID · CA ID · KEY ID · ALGORITHM · KERNEL VERSION ·  
PREVIOUS KERNEL · ROTATION GENERATION · POLICY VERSION ·  
MEMORY SNAPSHOT ID · SOURCE TIP · EXPECTED · ACTUAL · DECISION ·  
FAILURE CODE · RAW OUTPUT · LOG HASH

Then the ordinary SWI chain:

```text
Claim → Implementation → Test → Raw Result → Evidence Hash
  → Independent Verification → Reproduction → only then Authority claim
```

---

## Current honest position (at authorship)

| Item | Status |
|---|---|
| PRE-R boundary tests | PASS on declared matrix |
| Cross-checkout travel / integrity rejection | Demonstrated (useful) |
| Full unit suite at tip | 193 passed / 1 failed (freshness on old source_tip) |
| Failure on stale/orphaned source_tip | **Useful evidence** — do not rewrite tip |
| Firefly adapter | **NOT IMPLEMENTED** |
| Certificate → CA → kernel → rotation → field delivery chain | **Not yet implemented/tested as Firefly** |
| Execution | **BLOCKED** |
| S9 / six-way | **NOT_PROVEN** |
| Production | **NOT_AUTHORIZED** |

---

## Non-claims

- This protocol does **not** implement Firefly.
- Passing design review of this document does **not** authorize implementation.
- No Firefly test result is claimed.
- No seal, Foundation PASS, or production authorization is claimed.
