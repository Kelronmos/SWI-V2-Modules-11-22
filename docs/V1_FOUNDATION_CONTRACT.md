# V1 Foundation Evidence Contract

**STATUS: PROPOSED / IMPLEMENTATION PENDING**

V1: https://github.com/Kelronmos/SWI-V1-Module-1-10  
V2: https://github.com/Kelronmos/SWI-V2-Modules-11-22

## What V1 provides today

- Modules 00–10 under `swi_core/`
- ModuleKernel on 02, 03, 05, 06
- Trainer fail-closed halt on kernel contract failure
- Tests, verify.sh, CI, seal/evidence docs

## What V1 does NOT yet provide

- Versioned exportable cross-repository foundation evidence object
- Production integrity reference emitted for downstream volumes

## Proposed envelope

payload · foundation_version · evidence_schema_version · evidence_id · integrity_reference · verification_status · source_reference

## Version support (V2 skeleton)

| Contract | Support |
|----------|---------|
| 1.0-proposed | SUPPORTED (fixtures only) |
| unknown | REJECT |

V1 producer: **NOT IMPLEMENTED**. V2 verifier: **IMPLEMENTED** against fixtures only.
