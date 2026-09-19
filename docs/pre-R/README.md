# V2 pre-R Return Boundary

**Status:** DESIGN ONLY  
**Target:** SWI V2 only  
**V1 dependency:** NONE  
**Formal module promotion:** NOT AUTHORIZED  
**Implementation:** NOT AUTHORIZED  
**Security claim:** NONE  

## Question (narrow)

> Can a result cross a return boundary while preserving defined evidence, integrity, identity, destination and authority scope, without the return path, intermediary backend, or UI creating new authority?

## Doctrine

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
RESULT ≠ RESPONSE ≠ AUTHORITY ≠ NEW ACTION
INTEGRITY ≠ TRUTH · TESTED ≠ SEALED · RETURN ≠ AUTHORITY ESCALATION
Aᵣ ⊆ A₀ · UNKNOWN ⇏ ALLOW
```

## Components

pre-R01 RequestBinding · pre-R02 AuthorityScope · pre-R03 EvidenceCarrier · pre-R04 IntegrityVerifier · pre-R05 ResponseEnvelope · pre-R06 ReturnGate · pre-R07 DestinationGate · pre-R08 TransformationGuard · pre-R09 DeliveryAdapter · pre-R10 BoundaryAudit

## Documents

| File | Role |
|------|------|
| `RETURN_BOUNDARY_SPEC.md` | Full build & verification guide |
| `TEST_MATRIX.md` | Mutation → expected |
| `LIMITATIONS.md` | Limitation register |
| `PROMOTION_CRITERIA.md` | When (not) to promote |
| `IMPLEMENTATION_AUTHORIZATION.md` | **NOT AUTHORIZED** |

## Next

Freeze contract & seams → **AUTHORIZED FOR IMPLEMENTATION** → then code. No code before that.
