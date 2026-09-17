# M12 Contract — THE MASTERY ARCHIVE

**Pre-Name:** Knowledge Anchor  
**Module ID:** M12  
**Status:** **CONTRACT FROZEN** · Implementation: **NOT STARTED** · Seal: **NOT CLAIMED**  
**Date (UTC):** 2026-09-17  
**Dependency:** M11 **SEALED** (`docs/M11_SEAL_RECORD.md`)  
**Next dependency unlocked only after M12 seal:** M13

Governing doctrine: evidence before claim · contract before implementation · never claim what the code cannot demonstrate.

---

## 1. Purpose (narrow)

Given valid `AdmittedInput`, produce a deterministic `NormalizedEvidence` representation while preserving source identity, provenance, integrity reference, and admission marker.

M12 may reorganize representation. M12 must not silently change meaning or invent truth.

---

## 2. Non-goals

M12 must **NOT** implement: truth verification, semantic interpretation, identity/authorization, AI safety evaluation, memory/retrieval, embeddings, vector search, LLM summarization, knowledge confidence, CRTG, key management, certificates, database persistence, external network calls, or M13+ functionality.

If any of these appears in implementation — **stop**.

---

## 3. Data flow

```text
V1 FoundationEvidenceEnvelope (serialized)
        ↓
M11 admission → AdmittedInput
        ↓
M12 → NormalizedEvidence
        ↓
M13 (blocked until M12 sealed)
```

Raw input → M12 = **REJECT**. Only M11 → `AdmittedInput` → M12 is valid.

---

## 4. Input — `AdmittedInput` (actual kernel type)

Source of truth: `swi_v2/kernel/contracts.py`

| Field | Required |
|-------|----------|
| `payload` | yes |
| `foundation_version` | yes |
| `evidence_schema_version` | yes |
| `evidence_id` | yes |
| `integrity_reference` | yes |
| `source_reference` | yes |
| `admitted_by` | yes (default on type: `module_11_foundation_admission`) |

**Note:** `verification_status` exists on `FoundationEvidenceEnvelope`, not on `AdmittedInput`. M12 must not invent a verification upgrade. If future admission carries status into `AdmittedInput`, amend this contract explicitly.

**Reject:** `dict`, `str`, `bytes`, `list`, `tuple`, `None`, arbitrary objects, fake lookalikes that are not `AdmittedInput`.

---

## 5. Output — `NormalizedEvidence` (frozen shape)

### 5.1 Preserved exactly (value-equal to input; no reinterpretation)

| Field |
|-------|
| `evidence_id` |
| `foundation_version` |
| `evidence_schema_version` |
| `source_reference` |
| `integrity_reference` |
| `admitted_by` |

Absent required field on input → **REJECT** (do not default).

### 5.2 Derived (deterministic only)

| Field | Rule |
|-------|------|
| `normalized_payload` | Pure function of `payload` + published rules for this M12 version |
| `normalization_version` | Explicit string, initial: `1.0-proposed` |
| `module_id` | Constant `"M12"` |

### 5.3 Forbidden in output

Truth/factuality claims · meaning/summary as “knowledge” · identity/authorization decisions · confidence/safety scores · random IDs · wall-clock timestamps · host/env fingerprints · mutation of preserved fields · upgrading verification/admission status by side effect.

---

## 6. Normalization rules (ten)

1. Admission required — only `AdmittedInput`.
2. Raw objects rejected — no silent coercion.
3. Evidence identity preserved — no replacement `evidence_id`.
4. Provenance preserved — `source_reference` survives.
5. Integrity reference preserved — `integrity_reference` survives.
6. Admission marker preserved — `admitted_by` survives; M12 does not “re-admit.”
7. No silent invention — absent data → REJECT or explicit absence per published rules; never guess.
8. No semantic cleaning — structure only; not correct/incorrect/safe/trustworthy.
9. Determinism — same input + same `normalization_version` + same rules → identical output.
10. No mutation — original `AdmittedInput` unchanged.

**Initial payload rule (v1.0-proposed):** If `payload` is a `Mapping`, emit a deterministic canonical form (sorted keys, JSON-serializable values only; reject unsupported types). If `payload` is a JSON-serializable scalar/list under the same constraints, preserve structure deterministically. Otherwise **REJECT**. No network, no I/O, no randomness.

---

## 7. Error boundary

M11 rejection of foundation evidence ≠ M12 rejection of admitted input. Audits must label which module failed.

---

## 8. Limitations

| Topic | Status |
|-------|--------|
| Truth of payload | **NOT ESTABLISHED** |
| Foundation Seal 5 (V1 signed export) | **NOT READY** — M12 does not fix origin signing |
| CRTG / production keys | **OUT OF SCOPE** |
| Memory / retrieval / embeddings | **OUT OF SCOPE** |
| Replay policy | **OUT OF SCOPE** |

---

## 9. Build sequence

| Pass | Deliverable | Status |
|------|-------------|--------|
| **1** | This contract | **FROZEN** |
| **2** | `models` + `normalization` + remove `accepted_placeholder` | NOT STARTED |
| **3** | Contract / rejection / determinism / immutability / isolation tests | NOT STARTED |
| **4** | M11→M12 integration + CI | NOT STARTED |
| **5** | Audit worksheet + independent rediscovery → **M12 SEALED** | NOT STARTED |

M13 unlocks only after Pass 5.

---

## 10. Scaffold vs contract

```text
Today:  process() → accepted_placeholder
Target: process() → NormalizedEvidence
```

Until Pass 2–5 complete, “M12 normalizes evidence” is **false**.

---

## 11. Seal meaning (when earned)

An M12 seal means only: the audited implementation satisfied this contract at the identified commit and CI boundary.

It does **not** mean truth, AI safety, production readiness, knowledge correctness, or global compliance.

---

## 12. One-sentence freeze

**M12 accepts only M11 `AdmittedInput`, emits deterministic `NormalizedEvidence` that preserves identity/provenance/integrity/admission fields exactly, derives payload without invention, and claims nothing beyond that boundary.**
