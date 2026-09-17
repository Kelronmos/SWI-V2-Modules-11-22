# SCAR → Firefly Documentation Index

**Status:** DESIGN / DEFERRED — **NO IMPLEMENTATION AUTHORIZED**  
**Date:** 17 September 2026  
**M11:** SEALED (do not modify) · **M12:** FROZEN · **Firefly code:** not present

---

## Read order

| Order | Document | Role |
|-------|----------|------|
| 1 | V1 `docs/SCAR_STATUS.md` | What SCAR actually is (IMPLEMENTED / TESTED) |
| 2 | `SCAR_FIREFLY_CONSUME_REFUSE_CONTRACT.md` | MAY / MUST PRESERVE / MUST REJECT / MUST NEVER INFER |
| 3 | `SCAR_FIREFLY_ADAPTER_CONTRACT.md` | Adapter I/O shape, REJECT/HALT |
| 4 | `SCAR_FIREFLY_CONTRACT_AUDIT.md` | Audit vs real `scar.py` fields |
| 5 | `SCAR_FIREFLY_ADAPTER_TEST_SPEC.md` | Positive / negative / mutation / authority vectors |
| 6 | `SCAR_FIREFLY_TEACHING_MANUAL.md` | Teaching exercises for the seam |
| 7 | `SWI_TEACHING_GUIDE_MEMORY_BOUNDARY_AUDIT.md` | How to audit any memory boundary |
| 8 | `SCAR_FIREFLY_BUILD_MANUAL.md` | Build path when authorized; **STOP** before seal |
| 9 | `V2_MEMORY_WEB_STATUS.md` | CURRENT architecture status table |

---

## Hard facts

| Fact | Detail |
|------|--------|
| SCAR content_hash covers | `scar_class`, `title`, `description`, `trigger_context`, `failure_signature`, `recommended_response`, `embedding_model` only |
| Not hash-covered | e.g. `priority_score`, `status`, `tags`, `metadata`, `created_by`, embeddings payload |
| Valid hash | ≠ entire Scar unchanged |
| Embeddings | Out of adapter v1 |
| metadata | Allowlist only; unknown → REJECT |
| Authority injection | Must REJECT/HALT |
| M11 / M12 | No bypass via Firefly |

---

## Implementation gate (still open)

- [ ] metadata allowlist frozen in writing  
- [ ] forbidden keys frozen  
- [ ] suspect/pruned policy frozen (default in test spec: accept-as-status)  
- [ ] empty title/description policy frozen (default: allow)  
- [ ] embeddings excluded confirmed  
- [ ] provenance requirements frozen  
- [ ] failure semantics frozen  
- [ ] adversarial vectors accepted  
- [ ] contract version assigned (`scar-firefly-0.1` proposed)  
- [ ] **explicit project authorization to implement**  

Until every box is checked: no `swi_v2/firefly/` package.

---

## Honest status line

```text
SCAR (V1)                    IMPLEMENTED / TESTED
SCAR → Firefly contracts     DESIGN FROZEN
Firefly adapter              NOT IMPLEMENTED
Firefly                      DESIGN / DEFERRED
M11                          SEALED (historical)
Replay                       NOT SEALED
M12                          IMPLEMENTATION FROZEN
M13–22                       BLOCKED
```
