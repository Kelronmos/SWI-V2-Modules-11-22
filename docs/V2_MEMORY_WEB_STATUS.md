# V2 Memory Web Status — CURRENT freeze

**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Date:** 17 September 2026  
**Doctrine:** BUILD THE WEB · VERIFY THE STRANDS · PRESERVE THE HISTORY · NEVER CONFUSE MEMORY WITH TRUTH

This is a **CURRENT** status document. It does not rewrite `docs/M11_SEAL_RECORD.md`.

---

## Status table

| Component | Current status |
|-----------|----------------|
| V1 SCAR / ScarStore | **IMPLEMENTED / TESTED** (V1 repo; canonical: V1 `docs/SCAR_STATUS.md`) |
| V1 M07 SCAR integrity | **IMPLEMENTED / TESTED** |
| **V2 M11** | **SEALED** — historical seal preserved |
| Independent verification | **REQUIRED / CONTINUING** |
| Replay (full) | **REQUIRED / NOT SEALED** |
| ReplayGuard | **PARTIAL** — in-process, in-memory only |
| Sparse Merkle | **EXPERIMENTAL / RESEARCH ONLY** |
| Cross-node M11 | **NOT YET PROVEN** |
| **Firefly** | **DESIGN / DEFERRED** |
| Firefly distributed memory | **BLOCKED** |
| M12 scaffold | **SCAFFOLD** (if present) |
| M12 substantive implementation | **FROZEN** |
| M12 seal | **DOES NOT EXIST** |
| M13–22 | **BLOCKED** |

---

## Web diagram (contracts, not automatic authority)

```text
                    GOVERNANCE
                        │
                        ▼
                    EVIDENCE
                        │
          ┌─────────────┼─────────────┐
          │             │             │
         SCAR          M11          REPLAY
          │             │             │
          └─────────────┼─────────────┘
                        │
                     FIREFLY   (design)
                        │
                        ▼
                       M12   (frozen)
                        │
                        ▼
                       M13+
```

Strands mean: a defined contract may exist for a specific exchange.  
They do **not** mean every node has authority over every other node.

---

## Hard rules

1. **Do not edit the M11 seal record** to fit new architecture. New evidence → new records.  
2. **SCAR ≠ M11.** SCAR is V1 memory/integrity; M11 is V2 admission/continuity.  
3. **Firefly ≠ implemented.** Concept / architecture / contract / implementation / tests / CI / audit / seal are distinct stages.  
4. **MEMORY ≠ TRUTH.** Stored record ≠ factual truth.  
5. **SIGNATURE ≠ REPLAY.** Replay results: `REPLAY_MATCH` | `REPLAY_MISMATCH` | `REPLAY_REJECTED` | `REPLAY_UNAVAILABLE` — never `TRUTH_CONFIRMED`.  
6. **No Firefly bypass of M11.** No raw bypass of admission.  
7. **No fake M12.** Placeholder ≠ NormalizedEvidence implementation.  
8. **Canonical spelling:** **Firefly** (not Firelfy / Firely).

---

## Repair sequence (next)

1. Freeze M11 (done — do not rewrite)  
2. Reconcile CURRENT docs (this commit)  
3. Independent M11 verification continuity  
4. Deterministic replay beyond in-memory guard  
5. Adversarial replay tests  
6. SCAR status already frozen on V1  
7. Firefly memory contract (consume/refuse from SCAR) — design only  
8. Local SCAR→Firefly tests only after contract freeze  
9. Firefly + replay  
10. Failure/bypass paths  
11. Then reassess distributed memory  
12. Controlled module schema → M12 contract freeze → implement → test → CI → audit → seal  

---

## Related

- `docs/M11_SEAL_RECORD.md` — historical seal (immutable intent)  
- `docs/MODULE_STATUS.md`  
- `docs/M12_CONTRACT.md` / `docs/M12_IMPLEMENTATION_MANUAL.md`  
- V1 `docs/SCAR_STATUS.md`  
- `docs/SWI_TRUST_SEQUENCE.md` / `docs/SWI_CONTROLLED_SEQUENCE_MANUAL.md`  
