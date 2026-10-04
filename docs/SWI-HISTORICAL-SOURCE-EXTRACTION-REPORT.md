# SWI Historical Source Extraction Report

**Status:** EXTRACTION ONLY · NOT A RESTORE · NOT A SEAL  
**Date:** 2026-10-04  
**Repository:** Kelronmos/SWI-V2-Modules-11-22  

```text
HISTORICAL SOURCE = LINEAGE EVIDENCE
≠ CURRENT IMPLEMENTATION
≠ TESTED
≠ PROVEN
≠ SEALED
≠ AUTHORIZED
```

---

## 1. Current HEAD

| Field | Value |
|-------|--------|
| Branch | `main` |
| **HEAD** | `27981fba65979712876165d7b847bc18d4f3550e` |
| Subject | SWI: add trusted-source spine_inspector module (read-only, fail-closed) |
| Worktree at inspection | clean |

### Current files under inspection

| File | Size | Blob (HEAD) | Assessment |
|------|------|-------------|------------|
| `swi_v2/execution_integrity.py` | **1114** bytes | `031a22c8d99861c4c1ef3a25feb65a1a95077f5a` | **TRUNCATED** — docstring + imports only |
| `swi_v2/trusted_source/spine_inspector.py` | **44** bytes | `fa7d0709ee14a1072d8dd40def8da74e61ceb9f4` | **PLACEHOLDER** string only |

---

## 2. Historical candidates — `swi_v2/execution_integrity.py`

### 2.1 Symbol matrix (selected commits)

| Commit | Date | Size | Blob | Gate | HumanAuthority | validate_human_authority | execute | bind_authority | _mint_permit | Placeholder/trunc |
|--------|------|------|------|------|----------------|--------------------------|---------|----------------|--------------|-------------------|
| `27981fb` HEAD | 2026-10-04 | 1114 | `031a22c8…` | no | no | no | no | no | no | **TRUNCATED** |
| `1faec5b` | 2026-10-04 | 1114 | `031a22c8…` | no | no | no | no | no | no | **TRUNCATED** |
| `6875cfb` | 2026-10-04 | 23 | `f5fe3d08…` | no | no | no | no | no | no | **SEE_FILE_…** |
| `088bcb8` | 2026-10-04 | 24 | `987bf95f…` | no | no | no | no | no | no | **PLACEHOLDER_WILL_REPLACE** |
| `7da044d` | 2026-10-04 | 11743 | `82c3a6eb…` | **yes** | no | no | **yes** | no | **yes** | real but **pre-HA** |
| `9215984` | 2026-10-03 | 45 | `24f6bb2e…` | no | no | no | no | no | no | **SEE_ARTIFACTS_…** |
| `fc640c8` | 2026-10-03 | 21 | `a00ca383…` | no | no | no | no | no | no | placeholder wipe |
| **`fb39a51`** | 2026-10-03 | **21564** | **`9e996555a583…`** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **COMPLETE** |
| **`77ee326`** | 2026-09-30 | **21564** | **`9e996555a583…`** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **COMPLETE (same blob)** |
| `28961cb` | 2026-09-30 | 12882 | `1e35e1c5…` | yes | no | no | yes | no | yes | HaltRecord era |
| `358eeef` | 2026-09-30 | 11743 | `82c3a6eb…` | yes | no | no | yes | no | yes | hardened permit gate |
| `3827d0f` | 2026-09-30 | 10057 | `159d87b0…` | yes | no | no | yes | no | no | initial bounded gate |

### 2.2 Newest complete authority-gate candidate

| Field | Value |
|-------|--------|
| **COMMIT** | `fb39a51823572dcca60ad9ffd0eba9f085d2f7aa` |
| **DATE** | 2026-10-03 21:51:07 +0200 |
| **PARENT** | `658500008997b9675ee5ac12bee51834498adc04` |
| **FILE** | `swi_v2/execution_integrity.py` |
| **BLOB** | `9e996555a5831208970b31b91fefb367e1f52cb7` |
| **FILE SIZE** | **21564** bytes |
| **SYMBOLS FOUND** | `ExecutionIntegrityGate`, `HumanAuthority`, `validate_human_authority`, `execute`, `bind_authority`, `_mint_permit`, `NewInformation`, `apply_new_information`, `to_halt_record`, `Decision.UNKNOWN` |
| **NOT FOUND as identifiers** | `FLOW_BIND`, `RUNTIME_MATCH` (conceptual invariant names; not required string tokens in this source) |
| **RELATED TESTS** | `test/adversarial/test_execution_integrity.py`, `test/adversarial/test_new_information_boundary_attacks.py`, `test/adversarial/test_gate_pass_fail_matrix.py`, `test/adversarial/test_universal_halt.py` |
| **Same blob also at** | `77ee32602ee6262b7c4a740125d922f0742febd1` (2026-09-30) |
| **Blob reachable** | YES (`git cat-file -t/-s`) |

**Note:** `fb39a51` is the **parent of** `fc640c8` (the first wipe). Chronologically it is the last commit whose tree still carries blob `9e996555…` before placeholder replacement.

### 2.3 Secondary (incomplete for HA tests) candidate

| Field | Value |
|-------|--------|
| COMMIT | `7da044dd44ff7bb64254bde1f369044e58da0363` (also blob at `358eeef`) |
| BLOB | `82c3a6eb720fdb9276bee050a4e9f0f0605708fc` |
| SIZE | 11743 bytes |
| SYMBOLS | Gate + execute + permit; **no** `HumanAuthority` / `validate_human_authority` |
| Use | Lineage of pre–authority-gate hardened boundary only — **not** sufficient for current HA-oriented tests |

---

## 3. Historical candidates — `swi_v2/trusted_source/spine_inspector.py`

| Field | Value |
|-------|--------|
| **COMMIT** | `27981fba65979712876165d7b847bc18d4f3550e` (only appearance) |
| **FILE** | `swi_v2/trusted_source/spine_inspector.py` |
| **BLOB** | `fa7d0709ee14a1072d8dd40def8da74e61ceb9f4` |
| **FILE SIZE** | **44** bytes |
| **CONTENT** | `PLACEHOLDER_LOAD_FROM_LOCAL_FILE_20747_BYTES` |
| **SYMBOLS FOUND** | **none** of: FieldStatus, inspect_record, format_report, SPINE_STAGES, fail-closed exit logic |
| **RELATED TESTS** | `test/test_trusted_source_spine_inspector.py` (expects real implementation) |
| **Prior real implementation in git** | **NONE** |

Scaffolding present on `main` without a real inspector body:

- `swi_v2/trusted_source/__init__.py` (imports missing symbols)
- `docs/SWI_TRUSTED_SOURCE_BOUNDARY_PLACEHOLDER.md`
- `evidence/trusted_source_boundary_placeholder.json`
- `scripts/swi_trusted_source_spine_inspect.py`
- `scripts/swi_trusted_source_spine_manual.sh`
- `test/fixtures/trusted_source/*`
- `.github/workflows/trusted_source_boundary.yml`

---

## 4. Compare lineage vs HEAD

| File | EXACT SOURCE FOUND | CURRENT FILE CORRUPTED | HISTORICAL FILE COMPLETE | RECOVERY WITHOUT RECONSTRUCTION | TESTS MATCH SOURCE |
|------|--------------------|------------------------|---------------------------|----------------------------------|--------------------|
| `execution_integrity.py` (HA gate) | **YES** (`9e996555…`) | **YES** | **YES** (at `fb39a51`/`77ee326`) | **YES** | **UNKNOWN** (tests exist; connection **DISCONNECTED** on HEAD) |
| `execution_integrity.py` (pre-HA) | YES (`82c3a6eb…`) | YES (HEAD not this blob) | YES but incomplete vs HA tests | YES | DISCONNECTED from HA tests |
| `spine_inspector.py` | **NO** | **YES** | **NO** (never committed as real source) | **NO** | DISCONNECTED |

---

## 5. Destructive / disconnecting commits (evidence only)

No assignment of intent. Observed tree changes only.

| Commit | Observed effect on `execution_integrity.py` |
|--------|-----------------------------------------------|
| `fc640c8ebe509f978ffa2f3ba22fcd76e3e38ca6` | Replaced full source (parent `fb39a51` / blob `9e996555…`) with **~21-byte placeholder** |
| `921598492fc72c604b63ec780322bd104069c139` | **SEE_ARTIFACTS_LOCAL_FILE_TOO_LARGE_FOR_INLINE** placeholder |
| `7da044dd44ff7bb64254bde1f369044e58da0363` | Restored **pre-HA** blob `82c3a6eb…` (11743 B) — real code, **missing** HumanAuthority surface |
| `088bcb866e6e67ae8c764d5f291a7553ce9c4c15` | **PLACEHOLDER_WILL_REPLACE** |
| `6875cfbc58007af0a2e0338bd2ef4367f8607c44` | **SEE_FILE_/tmp/c_impl.py** |
| `1faec5b383b2b8311160bd8dde407a6fb5c47c6c` | **Truncated header** (1114 B) — docstring/imports only |
| `27981fb` (HEAD) | Still carries **truncated** `execution_integrity.py` (1114 B) |

| Commit | Observed effect on `spine_inspector.py` |
|--------|------------------------------------------|
| `27981fba65979712876165d7b847bc18d4f3550e` | **Created** file as placeholder string only (44 B); no prior real blob in history |

**Test disconnection:** adversarial and trusted-source tests on `main` still **name** symbols (`HumanAuthority`, `inspect_record`, etc.) that **HEAD files do not define**.

---

## 6. Recovery candidate (extraction result only)

### A. Execution integrity — exact recovery candidate

```text
PATH:   swi_v2/execution_integrity.py
COMMIT: fb39a51823572dcca60ad9ffd0eba9f085d2f7aa
BLOB:   9e996555a5831208970b31b91fefb367e1f52cb7
SIZE:   21564 bytes
ALSO:   77ee32602ee6262b7c4a740125d922f0742febd1 (identical blob)
```

Exact extraction command (not executed as restore in the extraction pass):

```bash
git show fb39a51823572dcca60ad9ffd0eba9f085d2f7aa:swi_v2/execution_integrity.py
git rev-parse fb39a51:swi_v2/execution_integrity.py
# → 9e996555a5831208970b31b91fefb367e1f52cb7
```

### B. Trusted-source spine inspector

```text
NO exact historical implementation blob in repository history.
RECOVERY WITHOUT RECONSTRUCTION: NO
```

---

## 7. Recovery risks

1. Restoring `9e996555…` restores **lineage**, not automatic TESTED/PROVEN/SEALED status.
2. Tests after `9a8ce95` may still contain **post-wipe drift** (`execute(..., action_id=...)`) relative to historical `execute(incoming, attempt_retry=...)` — must be evaluated in VERIFY stage, not assumed.
3. Diagnostic/architecture commits on `main` after the wipe must remain; restore must be **file-exact**, not a squash of history.
4. `spine_inspector.py` cannot be recovered from git; any later introduction is **new delivery**, not historical extraction.
5. HEAD truncation may break broader CI until exact restore + import/test stages complete.

---

## 8. Unknowns

- Whether every test in the adversarial suite passes against blob `9e996555…` on current `main` tip (not run in the extraction pass).
- Whether intermediate diagnostic modules assume APIs only present in `9e996555…` or in `82c3a6eb…`.
- Content of any **out-of-repo** copy of the real spine inspector (not in object store).
- Whether string tokens `FLOW_BIND` / `RUNTIME_MATCH` were ever source identifiers (not found in candidate blob).

---

## 9. Final extraction verdict

```text
HISTORICAL SOURCE FOUND:
  execution_integrity.py (HA gate): YES
  spine_inspector.py (real):          NO

EXACT RECOVERY POSSIBLE:
  execution_integrity.py: YES (blob 9e996555a5831208970b31b91fefb367e1f52cb7)
  spine_inspector.py:     NO

RECONSTRUCTION REQUIRED:
  execution_integrity.py: NO (if restoring exact blob)
  spine_inspector.py:     YES (no historical source in git)

CURRENT IMPLEMENTATION INTACT:
  execution_integrity.py: NO
  spine_inspector.py:     NO
```

```text
IMPLEMENTED: NO
TESTED: NO
PROVEN: NO
SEALED: NO
PRODUCTION_AUTHORIZED: NO
```

---

## 10. STOP

Extraction complete. **No restore of implementation files in the extraction pass.**

Next stages (not performed by extraction alone):

```text
EXTRACT (done)
→ VERIFY
→ RESTORE EXACT SOURCE
→ IMPORT CHECK
→ TEST
→ SECOND-EYE INSPECTION
→ SCAR REFLEX / BEFORE-DURING-AFTER RECORDING
→ EVIDENCE REVIEW
```

Locked principle (context only; not implemented by this report):

```text
SCAR / SHARED MEMORY → EVIDENCE + CONTEXT + REFLEX → INSPECTION / ROUTING
→ SWI BINDING → HUMAN AUTHORITY → AUTHORIZATION → ACTION

EVIDENCE AVAILABLE ≠ AUTHORIZED TO ACT
MEMORY ≠ AUTHORITY
RECALL ≠ AUTHORIZATION
OBSERVATION ≠ AUTHORITY
```
