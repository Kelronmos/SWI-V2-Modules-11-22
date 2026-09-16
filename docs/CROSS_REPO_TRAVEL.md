# Cross-Repository Travel (V2)

## Status (locked)

| Gate | State |
|------|--------|
| Local serialized travel → M11 | **PROVEN** (`a58e5b2`+) |
| Live two-checkout with real V1 producer | **CI_VERIFIED** (run 34987307390 · V2 `061a47f` · V1 `be31dd7`) |
| CRTG | DESIGN PENDING |
| M11 SEAL | NOT READY |

## Rule

> V1 produces a versioned evidence contract. V2 consumes the **serialized** contract independently of the V1 implementation.

**Do not** depend on `import` of SWI-V1. M10 is not the handoff.

```text
JSON / bytes
  → M11 (schema + integrity + status)
  → AdmittedInput
  → Kernel
```

Rejection must not reach M12+.

**Mechanism note:** this is a CI-orchestrated artifact handoff (one job produces a file, a second job consumes it after the first has finished), not a live channel between running systems. Nothing described here implies the two repositories communicate, negotiate, or authenticate each other at runtime. See also `docs/CROSS_REPOSITORY_TRUST_SPECIFICATION.md` (PROPOSED / DESIGN PENDING — signer identity not implemented).

## Provenance

Do not mutate V1 evidence in place. Create **derived** V2 state and keep it distinct.

## Integrity

Five covered fields only; **`created_at` not in digest**.

## Next

Complete A–G (including D6 malformed-JSON evidence) · M11 seal only if all PASS · then controlled M12 — not bulk 13–22.
