# M12 Contract — THE MASTERY ARCHIVE

**Pre-Name:** Knowledge Anchor  
**Module ID:** M12  
**Status:** **CONTRACT FROZEN** · Implementation: **NOT STARTED** · Seal: **NOT CLAIMED**  
**Date (UTC):** 2026-09-17  
**Dependency:** M11 **SEALED** (`docs/M11_SEAL_RECORD.md`)  
**Next dependency unlocked only after M12 seal:** M13

---

## 1. Purpose (narrow)

M12 owns **controlled evidence normalization** only.

It turns M11 `AdmittedInput` into a deterministic `NormalizedEvidence` representation that later modules may consume.

M12 is **not**:

- memory / retrieval / vector store
- embeddings / LLM summarization / semantic ranking
- “knowledge confidence” or truth scoring
- identity, authorization, or safety policy
- CRTG or a new cryptographic trust layer
- mutation of the original admitted evidence

Current scaffold (`swi_v2/module12/process`) remains a **type-boundary placeholder** until implementation matches this contract.

---

## 2. Ownership

| Role | Owner |
|------|--------|
| Controlled evidence normalization | **M12** |
| Admission + post-admission continuity seal | M11 (already sealed) |
| Scrubbed / controlled representation beyond normalization | M13 (blocked until M12 sealed) |

---

## 3. Data flow

```text
V1 FoundationEvidenceEnvelope (serialized)
        ↓
M11 admission → AdmittedInput (+ optional post-admission seal)
        ↓
M12 normalization → NormalizedEvidence
        ↓
M13 (not in scope)
```

---

## 4. Input

**Type:** `AdmittedInput` only (M11 product).

**Rejection (fail closed):**

| Input | Required behaviour |
|-------|--------------------|
| `dict` / raw envelope | **REJECT** |
| non-`AdmittedInput` object | **REJECT** |
| missing required admitted fields | **REJECT** |
| sealed/unsealed is orthogonal | M12 consumes admitted structure; does not re-define M11 seal |

Existing V2 principle stands: raw material must not bypass M11 into M12.

---

## 5. Output — `NormalizedEvidence`

### 5.1 Preserved exactly (copy, do not invent)

These fields MUST appear in the output with values **byte-for-byte / value-equal** to the corresponding `AdmittedInput` fields (no reinterpretation):

| Field |
|-------|
| `evidence_id` |
| `foundation_version` |
| `evidence_schema_version` |
| `source_reference` |
| `source_integrity_reference` |
| `verification_status` |

If a required preserved field is absent on input → **REJECT** (do not default).

### 5.2 Derived (deterministic only)

| Field | Rule |
|-------|------|
| `normalized_payload` | Pure function of admitted payload + published normalization rules for this M12 version |
| `normalization_version` | Explicit version string of the M12 rule set (e.g. `1.0-proposed`) |
| `module_id` | Constant `"M12"` |

### 5.3 Forbidden in output (never silently generated)

| Forbidden |
|-----------|
| truth / factuality claims |
| meaning / interpretation / summary text as “knowledge” |
| identity / principal / authorization decisions |
| confidence / safety scores |
| random IDs, wall-clock timestamps, host/env fingerprints in the normalized result |
| mutation of preserved provenance fields |

---

## 6. Primary property

**Deterministic normalization without loss or silent invention.**

### 6.1 Determinism

```text
same AdmittedInput
+ same normalization_version
+ same published rules
= same NormalizedEvidence
```

No hidden process state, locale, or time dependence in the normalized result.

### 6.2 No loss of required provenance

Required preserved fields MUST survive normalization unchanged.

### 6.3 No silent invention

Missing evidence MUST NOT be filled with plausible defaults for forbidden categories (§5.3).

### 6.4 Immutability of source

```text
AdmittedInput ──preserved──→ provenance fields on NormalizedEvidence
AdmittedInput ──derived───→ normalized_payload
AdmittedInput is not modified in place
```

---

## 7. Rejection rules (summary)

| Condition | Result |
|-----------|--------|
| Not `AdmittedInput` | REJECT |
| Missing required preserved field | REJECT |
| Payload cannot be normalized under published rules | REJECT (explicit error; no partial invention) |
| Attempt to attach forbidden semantics | REJECT / out of contract |

---

## 8. Limitations (permanent for this contract)

| Limitation | Status |
|------------|--------|
| Semantic understanding | **OUT OF SCOPE** |
| Long-term memory / retrieval | **OUT OF SCOPE** |
| CRTG / production keys | **OUT OF SCOPE** |
| Replay policy | **OUT OF SCOPE** (M11 signature ≠ replay) |
| Factual truth of payload | **NOT ESTABLISHED** |
| Foundation Seal 5 (V1 signed export) | **NOT READY** — M12 does not fix origin signing |

---

## 9. Build sequence (mandatory)

| Pass | Deliverable | Status |
|------|-------------|--------|
| **1** | This contract frozen | **THIS DOCUMENT** |
| **2** | Minimal implementation (`normalization.py`, models, errors) | NOT STARTED |
| **3** | Contract / determinism / immutability / bypass / isolation tests | NOT STARTED |
| **4** | M11→M12 evidence path + CI | NOT STARTED |
| **5** | Independent rediscovery → audit → **M12 SEALED** | NOT STARTED |

**M13 unlocks only after Pass 5.**

---

## 10. Relationship to scaffold

```text
Today:  process() → accepted_placeholder  (boundary only)
Target: process() → NormalizedEvidence   (this contract)
```

Until Pass 2–5 complete, any claim that “M12 normalizes evidence” is **false**.

---

## 11. Governance cross-links

- `docs/M11_SEAL_RECORD.md` — dependency seal
- `docs/GOVERNANCE_LOCK.md` — M12 controlled development only
- `docs/V47_GATE_FREEZE.md` — claim → contract → implementation → test → CI → seal
- Pre-Name retained: **Knowledge Anchor** / **The Mastery Archive**

---

## 12. One-sentence freeze

**M12 accepts only M11 `AdmittedInput`, emits deterministic `NormalizedEvidence` that preserves provenance exactly, derives payload without invention, and does not claim memory, truth, or trust beyond that boundary.**
