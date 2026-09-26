# Experimental: Privacy domain boundary

**Status:** RESEARCH / EXPERIMENTAL  
**Implemented:** boundary gate only  
**Seal:** NOT SEALED  
**Production:** NOT AUTHORIZED  
**Branch:** `experimental/privacy-domain`

## What this is

Fail-closed privacy-domain access check:

- Domains (e.g. IDENTITY, MEDICAL, EDUCATION, FAMILY, …) are separate.
- Decisions: ALLOW | BLOCK | ESCALATE | REDACT
- Purpose and scope binding required where applicable.

## What this is not

- Not a state-transition permission registry (that is the transition engine).
- Not human authority.
- Not a Zero Trust product.
- Not production authorization.

## Rule

```text
Privacy is a gate. It is not a state-transition permission by itself.
IDENTITY_ACCESS ↛ MEDICAL_ACCESS
```

## Primary API

See `domain_boundary.py` — `check_privacy_access(...)`.

## Tests

Adversarial suite under `tests/law/test_privacy_domain.py` (on this branch).  
Independent evidence capture required before any promotion claim.
