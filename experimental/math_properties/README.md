# Experimental Mathematical Properties

**Status:** EXPERIMENTAL · RESEARCH ONLY  
**Seal:** NOT AUTHORIZED  
**Production:** NOT AUTHORIZED  
**M11:** UNTOUCHED

This directory holds property-scoped verification material for existing
SWI contracts. It does **not** introduce parallel authorization mechanisms.

## MATH-002 — Authority Containment

- **Property:** Envelope / delegated authority must be contained by the originating authority.
- **Implementation:** `experimental.response_boundary.core.AuthorityScope.contains`
- **Scope:** Property-level only. Does **not** prove process-wide enforcement.
- **Tests:** `tests/pre_r/test_math_002_authority_containment.py`

## Rules

- MATH-* labels are audit/property identifiers, not formal SWI modules.
- Evidence determines status.
- TESTED ≠ AUDITED ≠ SEALED ≠ PRODUCTION.
