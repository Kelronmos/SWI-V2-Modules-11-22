# pre-R experimental response boundary

Executable experiment derived from the V2 pre-R design specification.

Tested scope is deliberately local: request binding, scoped authority, evidence presence,
canonical SHA-256 integrity, destination checks, expiry, revocation, and non-expansion of authority.

**Not claimed:** production security, semantic truth, network delivery, formal SWI seal, M-module promotion.

Run:

```bash
PYTHONPATH=. python -m pytest -q tests/pre_r/test_response_boundary.py
```
