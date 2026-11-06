# ZIP Recovery Integration Report — 2026-11-06

**Source main commit:** `378c856e9081cbaea580a2c433881ea24c54b7e9`  
**Working branch:** `fix/zip-recovery-integration-2026-11-06`  
**Status:** PARTIALLY_COMPLETE  

## Authority ceiling (unchanged)
```
PROVEN=NO
SEALED=NO
PRODUCTION_AUTHORIZED=NO
```

## Archives
| Archive | SHA-256 | Files |
|---------|---------|-------|
| Educational | `32384328…5804e` | 37 |
| Multiplatform | `effab957…699ea` | 25 |
| Firefly | `80aa5fb2…23b032` | 11 |

Content-duplicate groups: 25 (Educational ⊃ Multiplatform).  
Unsafe extraction entries: 0.

## Tests executed
- Educational isolated: **20 passed**
- Multiplatform isolated: **13 passed**
- Firefly small independent replay (100 tx): **PASS**, still `production_authorization=NOT_GRANTED`
- Full main pytest suite: **NOT_RUN**

## Firefly comparison
Original 100k run already declared `independent_reproduction=NOT_ESTABLISHED`.  
New minimal replay does not upgrade any claim.

## Relocation decision
- Keep original ZIP binaries under `Local Independent Tests/`.
- Treat extracted device/education packages as research/demo only.
- Do not merge into `swi_v2/` authorization or execution paths.
- Firefly original evidence remains immutable; new replay output is separate.

## Explicit non-claims
TESTED ≠ PROVEN ≠ SEALED ≠ PRODUCTION AUTHORIZED  
CI green ≠ SWI authorized  
Demonstration ≠ live enforcement
