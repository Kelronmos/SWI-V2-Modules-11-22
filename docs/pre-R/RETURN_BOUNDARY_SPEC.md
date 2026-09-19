# SWI V2 pre-R Return Boundary — Full Manual Build & Verification Guide

| Field | Value |
|-------|--------|
| Status | **DESIGN ONLY** |
| Target | **SWI V2 only** |
| Namespace | **pre-R** |
| V1 dependency | **NONE** |
| Formal module promotion | **NOT AUTHORIZED** |
| Implementation | **NOT AUTHORIZED** |
| Security claim | **NONE** |

Order: Claim → Contract → Implementation → Test → Result → Limitation → Next iteration.

## Purpose

> Can a result cross a return boundary while preserving defined evidence, integrity, identity, destination and authority scope, without the return path, intermediary backend, or UI creating new authority?

## Why V2 pre-R

V1 has evidence/authority/integrity/canonicalization and **no return-path implementation**. pre-R is a separate V2 experiment — not a formal module until promotion criteria pass.

## Doctrine

DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION  
INTEGRITY ≠ TRUTH · AUTHORIZED_SCOPE ≠ UNLIMITED  
Aᵣ ⊆ A₀ (return may narrow, never enlarge)  
UNKNOWN ⇏ ALLOW

## Flow

```text
USER → REQUEST → BINDING → AUTHORITY → POLICY → EXECUTION → RESULT
  → EVIDENCE → INTEGRITY → AUTHORITY RE-CHECK → POLICY → DESTINATION
  → RESPONSE → DELIVERY → UI
```

Critical loop: RESPONSE → USER → NEW REQUEST → NEW AUTHORITY DECISION  
Never: RESPONSE → AUTOMATIC AUTHORITY → PRIVILEGED ACTION

## Components pre-R01…pre-R10

RequestBinding · AuthorityScope · EvidenceCarrier · IntegrityVerifier · ResponseEnvelope · ReturnGate · DestinationGate · TransformationGuard · DeliveryAdapter · BoundaryAudit

Reuse existing SWI evidence/canonicalization contracts; do not invent a second crypto stack.

## Return gate checks

binding · evidence · integrity · authority · destination · policy · expiry · revocation · transformation → ADMIT/REJECT fail-closed

## Failure examples

Modified authority admitted · changed destination delivered · missing evidence admitted · unknown integrity admitted · UI/backend flag as authorization · old response as new privileged action · certificate as unrestricted action

## Not proof alone

Unit pass · signature OK · hash OK · UI looks right · one integration test · CI green · certificate exists

## Phases (after AUTHORIZED only)

0 Contract freeze → R01…R10 → full chain + reverse path (new request)

## Separation

No V1 modification for pre-R · no hidden V1 dependency · no import of return-path into V1

## Status ladder

DESIGNED → IMPLEMENTED → UNIT → INTEGRATION → CI → ADVERSARIAL → AUDITED → AUTHORIZED → SEALED

## Bounded claim template

> Within the tested scope, mutations to binding, evidence, integrity, authority scope and destination were rejected per recorded results. Subject to limitations. Not promoted to a formal SWI module.

## Final doctrine

```text
RESULT ≠ RESPONSE ≠ AUTHORITY ≠ NEW ACTION
RETURN ≠ AUTHORITY ESCALATION
TESTED ≠ SEALED
```

**Next:** freeze contract/seams. **Do not write return-path code** until AUTHORIZED FOR IMPLEMENTATION.
