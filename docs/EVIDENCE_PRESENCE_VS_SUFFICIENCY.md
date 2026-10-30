# Evidence presence vs sufficiency

**PROVEN=NO · SEALED=NO · PRODUCTION_AUTHORIZED=NO**

## Rule

```text
E(a) ≠ ∅     ≠     E_SUFFICIENT
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

## Governing permit

`evaluate_governing_permit` checks **presence** only (`_evidence_exists`).
Empty evidence → REJECTED (`evidence_empty`).
Non-empty evidence satisfies the formula conjunct; it does **not** mean evidence is sufficient.

## Empty conditions

Empty `C` must never PERMIT via vacuous subset truth (`∅ ⊆ X`).
See `empty_conditions_never_permit` and `test/test_empty_capability_regression.py`.

## Execution integrity

`bind_evidence_sufficiency(sufficient=...)` records an explicit sufficiency flag.
`None` or `False` → fail closed (`EVIDENCE_INSUFFICIENT`).
Binding `True` is an assertion input, not an independent sufficiency proof.

## TESTED ≠ PROVEN

Passing tests do not set `proven=true`. Evaluation records keep `proven=false`.
