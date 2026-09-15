# Cross-Repository Travel (V2)

## Status (locked)

| Gate | State |
|------|--------|
| Local serialized travel → M11 | **PROVEN** (`a58e5b2`+) |
| Live two-checkout with real V1 producer | **PENDING** |
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

## Provenance

Do not mutate V1 evidence in place. Create **derived** V2 state and keep it distinct.

## Integrity

Five covered fields only; **`created_at` not in digest**.

## Next

Two-checkout proof · M11/Kernel isolation evidence · then controlled M12 — not bulk 13–22.
