# Evidence Freshness Contract

**STATUS:** CONTRACT / FROZEN (doctrine)  
**EVIDENCE:** WP-01 location + classification (`docs/WP01_SOURCE_TIP_LOCATION_2026-09-24.md`, `docs/WP01_CLASSIFICATION_CLOSURE_2026-09-24.md`); tip-bound vs HEAD distinction.  
**LIMITATIONS:** Contract text is not a verifier implementation. Local freshness tests implement only the ancestor+blob subset today.  
**NEXT GATE:** Optional machine classifier + scoped HEAD-CURRENT law attestation at a controlled SHA (WP-02); never by rewriting `source_tip`.

This contract does **not** authorize execution, reseal M11, or claim Foundation PASS.

---

## 1. Three evidence layers

```text
                    CURRENT HEAD
                         |
             +-----------+-----------+
             |                       |
      HEAD-CURRENT              TIP-BOUND
      evidence                  evidence
             |                       |
       proves HEAD              proves source_tip
             |                       |
             +-----------+-----------+
                         |
                         v
                 HISTORICAL RECORD
```

| Layer | Proves | May support seal row? |
|-------|--------|------------------------|
| **HEAD-CURRENT** | Declared scope at **this** HEAD | Yes, for that scope only |
| **TIP-BOUND** | Declared scope at **source_tip** | Only if seal explicitly accepts tip-bound for that claim |
| **HISTORICAL** | Past tip; excluded from current proof | No (unless cited as history) |

Preserve tip-bound packages. **Do not “repair” them** by changing `source_tip` to HEAD.

---

## 2. Vocabulary (enforced)

| Class | Meaning |
|-------|--------|
| **ORPHANED** | `source_tip` is not HEAD and not an ancestor of HEAD |
| **TIP_BOUND** | Ancestor (or equal); attests **source_tip**, not necessarily HEAD |
| **HEAD_CURRENT** | `source_tip == HEAD` **and** blobs match **and** run bound to HEAD **and** scope declared |
| **HISTORICAL** | Deliberately retained; **not** used as current proof |
| **REFRESH_REQUIRED** | Project **needs** HEAD_CURRENT (or a new tip attestation) for a claim and does not have it |

**REFRESH_REQUIRED** ≠ automatic ORPHANED.  
**TIP_BOUND** ≠ failure.  
**TIP_BOUND** ≠ **HEAD_CURRENT**.

---

## 3. Machine rules (normative)

```text
AncestorPass(E, H)  iff  tip(E) = H  OR  tip(E) is ancestor of H

HeadCurrent(E, H)   iff  tip(E) = H
                         AND blobs_match(E, tree)
                         AND run_bound_to_head(E, H)
                         AND scope_declared(E)
```

Implications:

```text
AncestorPass(E, H)  =/=>  HeadCurrent(E, H)
HeadCurrent(E, H)   =>    AncestorPass(E, H)
```

**Forbidden operation:** setting `source_tip = head` as a corrective edit without a new generation run.

Allowed: generate a **new** evidence package with new identity whose `source_tip` is the tip actually tested.

---

## 4. Conceptual types (design; not yet required to exist in tree)

```python
class FreshnessClass(Enum):
    ORPHANED = "ORPHANED"
    TIP_BOUND = "TIP_BOUND"
    HEAD_CURRENT = "HEAD_CURRENT"
    HISTORICAL = "HISTORICAL"
    REFRESH_REQUIRED = "REFRESH_REQUIRED"

@dataclass(frozen=True)
class FreshnessResult:
    source_tip: str
    observed_head: str
    ancestry_pass: bool
    blobs_match: bool
    run_bound_to_head: bool
    classification: FreshnessClass

@dataclass(frozen=True)
class EvidenceScope:
    components: tuple[str, ...]
    tests: tuple[str, ...]
    claims: tuple[str, ...]
    exclusions: tuple[str, ...]
```

Existing implementation note: `tests/law/test_evidence_freshness.py` checks **AncestorPass** (+ authority/registry blob SHAs when present). It does **not** alone establish **HeadCurrent**.

---

## 5. Scope discipline

HEAD_CURRENT is always **scoped**.

Running `tests/law/` at HEAD may justify:

> Law evidence is HEAD_CURRENT **for the declared law-test scope**.

It does **not** justify:

> Entire SWI V2 is HEAD_CURRENT.

Every package should declare (or inherit a contract for) components, tests, claims, and exclusions.

---

## 6. Instance: law package `8245e3f`

| Field | Value |
|-------|--------|
| Artifacts | `evidence/law/manifest.json`, `formal-results.json`, `test-results.json` |
| source_tip | `8245e3f03d8673c966abf9c63be9d838073159b0` |
| Ancestor of main HEAD (post PR #2) | true |
| Blobs match | true |
| Classification | **TIP_BOUND** |
| HeadCurrent for full repo | **false** (not claimed) |
| Action | **Preserve**; do not rewrite tip |

When a controlled SHA `X` is ready: re-run **declared law scope** only; write a **new** package with `source_tip = X` and `classification = HEAD_CURRENT` for that scope.

---

## 7. Seal composition rule

```text
SEAL CANDIDATE
  foreach component claim:
    if only TIP_BOUND -> keep label TIP_BOUND (or exclude from seal scope)
    if HEAD_CURRENT for declared scope -> eligible for that row
    if ORPHANED / REFRESH_REQUIRED for required row -> seal blocked
  then independent audit
  then SEAL (still ≠ PRODUCTION AUTHORIZED)
```

No silent promotion TIP_BOUND → HEAD_CURRENT.

---

## 8. Audit question (mandatory)

For every claim:

> What exact commit, code blobs, tests, run, and evidence package prove this claim?

Answers that name `8245e3f` mean tip-bound proof of that tip.  
Answers that name current HEAD require HeadCurrent criteria.  
Answers that blur the two **fail** this contract.

---

## 9. Placement in programme

```text
WP-01  classification closed (tip-bound doctrine applied)
   |
   +-- EVIDENCE_FRESHNESS_CONTRACT (this file)  FROZEN
   |
WP-02  inheritance matrix + optional scoped HEAD_CURRENT attestation
   |
WP-03+ contracts / authority / binding / ...
   |
WP-21  seal only with per-row freshness class explicit
```

«Do not claim what the code cannot demonstrate.»  
«Do not rewrite source_tip to manufacture HEAD_CURRENT.»
