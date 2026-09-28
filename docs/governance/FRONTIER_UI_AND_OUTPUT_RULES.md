# Frontier UI & Output / Download Rules

**Status:** DESIGN / CONTROLLED DEVELOPMENT  
**Production:** NOT AUTHORIZED  
**Seal:** NOT REQUESTED  

Mandatory projection rules for any SWI UI or download surface. The UI is **not** an authority layer, evidence generator, or execution controller.

---

## Principal invariant

```text
FRONTIER UI ≠ SWI AUTHORITY
FRONTIER UI ≠ EVIDENCE GENERATOR
FRONTIER UI ≠ EXECUTION CONTROLLER
FRONTIER UI  = GENERATED STATE PROJECTION
```

```text
If a truthful representation cannot be generated from existing SWI records,
the UI MUST NOT manufacture one.
```

```text
No evidence → no promotion.
No verified path → no execution.
No generated state → no UI claim.
```

---

## 1. Source of truth

UI pulls from generated records only:

```text
REQUEST → CLAIM → EVIDENCE → MEASUREMENT → VERIFICATION
  → AUTHORITY → BINDING → RUNTIME RESERVATION
  → EXECUTION → AFTER → RECONCILIATION
```

No parallel chain. No new authority / evidence / halt layer in the UI.

---

## 2. Claims display

Where applicable, show: claim_id, type, text, source, source_tip, provenance, evidence_refs, dependency_refs, measurement, verification_status, freshness, authority_ref, binding_ref, consequence_class, status, generated_at.

```text
CLAIM ≠ EVIDENCE ≠ VERIFICATION ≠ AUTHORITY
```

A field `"authorized": true` inside data **must not** render as “Authorized” unless an underlying SWI authority record establishes that status.

---

## 3. Frontier

```text
KNOWN → GENERATED EVIDENCE → VERIFIED PATH → FRONTIER → UNKNOWN / NOT YET GENERATED
```

**Forbidden silent conversions:**

```text
UNKNOWN → PERMITTED
NOT GENERATED → FAILED
OBSERVED → VERIFIED
VERIFIED → AUTHORIZED
```

**Rule:** The UI may **display** the frontier; it may **not move** the frontier.

---

## 4. No misleading screen

UI **MUST NOT**:

- show green “approved” for merely tested data  
- show “secure” because a signature verified  
- show “authorized” because an identity matched  
- show “isolated” because an application lock exists  
- show “production ready” because tests passed  
- show a completed path when records contain unresolved frontier  
- hide missing evidence for layout convenience  
- imply human approval without a human authority record  

If data cannot support a truthful display → show the limitation or omit the representation.

---

## 5. Vocabulary

Use SWI vocabulary only when the corresponding generated state exists:

```text
OBSERVED · MEASURED · TESTED · VERIFIED · UNRESOLVED · UNKNOWN
BLOCKED · HALTED · AUTHORIZED · BOUND · EXECUTING · COMPLETED
```

Do **not** invent UI-only states (`SAFE`, `TRUSTED`, `APPROVED`, `READY`) unless already defined and evidenced by SWI.

---

## 6. Output & download rule

```text
SWI-GENERATED
  → provenance exists
  → claim exists
  → evidence exists
  → integrity verified
  → applicable authority established
  → output generated
  → output recorded
  → replayable
  → downloadable
```

If any required condition cannot be established:

```text
NO PROVABLE SWI PATH → NO SWI OUTPUT → NO DOWNLOAD
```

**Download is an output transition, not a button:**

```text
DOWNLOAD_REQUEST
  → IS_OUTPUT_SWI_GENERATED?
      ├── NO  → NON-SWI REVIEW PATH
      └── YES → PROVENANCE → EVIDENCE → INTEGRITY → AUTHORITY → REPLAY
                → OUTPUT ELIGIBLE → DOWNLOAD
```

Else: `DOWNLOAD = NOT ELIGIBLE` and explain why.

---

## 7. Non-SWI material

```text
NON-SWI INPUT
  → COST OWNER DECLARED
  → PROVENANCE RECORDED
  → AUTHORIZED AUTHORITY IDENTIFIED
  → AUTHORITY VERIFIED
  → SWI ADMISSION / VERIFICATION
  → EVIDENCE GENERATED
  → REVIEW
  → OUTPUT ELIGIBILITY
```

```text
Cost Owner ≠ Authority
```

---

## 8. Generated-data integrity of UI snapshots

Every UI snapshot should be traceable to: repository, commit, generation timestamp, record IDs, evidence IDs, claim IDs, schema version.

```text
UI_SNAPSHOT
  └── generated_from → claims, evidence, verification, authority, runtime records
```

Replayable projection — not authoritative source.

---

## 9. Absolute generation bound

```text
SWI MUST NOT generate an artifact whose material claims, provenance,
authority basis, integrity, or required evidence cannot be represented
and subsequently proven through the SWI record.

Generated ≠ Proven.
Generation creates no truth.
```

---

## Freeze statement

> FRONTIER UI SHALL ONLY PRESENT AND RELEASE GENERATED SWI OUTPUTS THAT CAN BE TRACED TO PROVABLE SWI STATE. The UI shall not manufacture evidence, authority, provenance, claims, or outputs. Non-SWI material shall remain explicitly identified as non-SWI and shall require the applicable cost-owner and authorized-authority verification path before becoming an eligible controlled output.

```text
DATA ≠ EVIDENCE ≠ AUTHORITY ≠ ACTION ≠ OUTPUT
```
