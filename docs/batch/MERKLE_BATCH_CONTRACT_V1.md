# SWI Merkle Batch Contract V1

**Document:** `docs/batch/MERKLE_BATCH_CONTRACT_V1.md`  
**Status:** SPECIFIED (B1)  
**Date:** 2026-09-29  
**Scope:** Post-M11 bounded batching layer  
**Does not modify:** M11 post-admission seal path  

---

## 1. Purpose

This contract defines a deterministic, evidence-accountable mechanism for committing a set of already-sealed evidence receipts into a single Merkle root with inclusion proofs, while guaranteeing complete accounting of every submitted item.

The batch root is a cryptographic commitment to the **INCLUDED** leaves under the rules of this contract.

It is **not**:
- authority
- factual truth
- approval / authorization
- legal compliance
- production trust
- execution rights
- a blockchain anchor (unless a later, separate stage explicitly adds one)

---

## 2. Architectural Position

```text
M11 AdmittedInput
      ↓
existing M11 seal          ← UNCHANGED / SEALED
      ↓
individual sealed evidence receipt
      ↓
BATCH BUILDER (this contract)
      ↓
GateResult + Decision + Control + Disposition for every submitted item
      ↓
ONLY disposition = INCLUDED become Merkle leaves
      ↓
deterministic dense Merkle tree
      ↓
ONE BATCH ROOT + inclusion proofs + batch manifest
      ↓
independent verifier
```

The batch layer sits strictly downstream of the sealed M11 path.  
It consumes sealed receipts; it does not re-open or re-seal M11 material.

---

## 3. Core Invariants

1. **No silent omission**  
   Every item presented to the batch builder must receive an explicit terminal disposition.  
   Unexplained disappearance → HALT.

2. **Deterministic construction**  
   Identical ordered set of INCLUDED leaves + identical contract parameters → identical root.

3. **Verifier reconstruction**  
   An independent verifier must reconstruct the expected tree and proofs from the declared leaves and contract parameters.  
   Proof substitution is rejected.

4. **Disposition completeness (central invariant)**  
   ```text
   submitted_count = included_count
                   + rejected_count
                   + deferred_count
                   + not_applicable_count
                   + other explicitly contracted terminal states
   ```  
   Any imbalance → RECONCILIATION_FAILURE → HALT.

5. **Semantic separation**  
   ```text
   PASS      ≠ INCLUDED
   APPROVED  ≠ INCLUDED
   DENY      ≠ REJECTED
   HALT      ≠ REJECTED
   ```  
   Gate outcomes and batch disposition are distinct dimensions.

6. **Non-claims**  
   Batch root proves only integrity of the committed set under this contract.  
   It never upgrades to authority, truth, approval, or execution rights.

---

## 4. Multi-Dimensional Outcome Model (required)

Every submitted item carries four independent dimensions:

### GateResult
- `PASS`
- `FAIL`
- `REVIEW_REQUIRED`
- `UNKNOWN`

### Decision
- `APPROVED`
- `DENY`

### Control
- `CONTINUE`
- `HALT`

### Batch Disposition
- `INCLUDED`
- `REJECTED`
- `DEFERRED`
- `NOT_APPLICABLE`
- (plus any additional states explicitly contracted)

**Critical rule:** these dimensions must never be collapsed.

Examples of valid combinations:

| GateResult | Decision  | Control  | Disposition     | Meaning |
|------------|-----------|----------|----------------|---------|
| PASS       | APPROVED  | CONTINUE | INCLUDED       | Accepted into the tree |
| PASS       | DENY      | CONTINUE | REJECTED       | Structurally valid but not permitted |
| UNKNOWN    | —         | HALT     | DEFERRED       | Cannot decide; do not include |
| FAIL       | DENY      | CONTINUE | REJECTED       | Failed gate and denied |
| PASS       | APPROVED  | HALT     | DEFERRED       | Control failure blocks inclusion |

Only items whose final Disposition is `INCLUDED` become Merkle leaves.

---

## 5. Leaf Schema

Each leaf that enters the tree is the canonical hash of a sealed evidence receipt (or an explicit leaf payload defined by the batch).

Minimum leaf identity:

```json
{
  "leaf_version": "1.0",
  "receipt_id": "string",
  "receipt_hash": "hex-encoded SHA-256",
  "source_seal_domain": "SWI-M11-SEAL-V1",
  "source_seal_version": "1.0-proposed"
}
```

Additional application-specific fields may be included only if they are themselves deterministically canonicalized and covered by the leaf hash.

Raw sensitive payload values are never required in the leaf; the receipt hash is the primary commitment.

---

## 6. Batch Identity & Ordering

- `batch_id`: unique opaque identifier for the batch instance  
- `batch_version`: contract version string (`1.0`)  
- `ordering_rule`: must be deterministic (e.g., ascending `receipt_id` lexicographic, or ascending `receipt_hash`)  
- Leaves are ordered strictly according to the declared rule before tree construction.  
- Reordering after commitment is a mutation and must fail verification.

---

## 7. Tree Construction

- Algorithm: dense binary Merkle tree  
- Hash function: SHA-256  
- Domain separation (mandatory):

  ```text
  Leaf  = SHA-256( b"SWI-BATCH-LEAF-V1\x00"  || leaf_bytes )
  Node  = SHA-256( b"SWI-BATCH-NODE-V1\x00"  || left || right )
  ```

- Odd number of leaves: duplicate the last leaf (same rule as M11 dense tree).  
- Empty batch (zero INCLUDED leaves) is forbidden unless the contract explicitly permits a documented empty-root sentinel (default: forbidden).

The tree is built **only** over leaves whose disposition is `INCLUDED`.

---

## 8. Inclusion Proof

For every INCLUDED leaf the batch must produce:

```text
MerkleProof {
  leaf_hash,
  index,
  siblings[],
  root
}
```

Verification procedure (independent):

1. Recompute leaf hash under the domain-separated rule.  
2. Walk the sibling path using the same parent rule.  
3. Accept only if the recomputed root equals the declared batch root.  
4. Reject any proof that does not reconstruct correctly or that claims a different root.

Proof substitution or foreign proofs are rejected.

---

## 9. Batch Manifest

Every batch produces a machine-readable manifest:

```json
{
  "schema": "SWI-BATCH-MANIFEST-V1",
  "batch_id": "...",
  "batch_version": "1.0",
  "contract_hash": "...",
  "ordering_rule": "...",
  "submitted_count": 0,
  "included_count": 0,
  "rejected_count": 0,
  "deferred_count": 0,
  "not_applicable_count": 0,
  "root": "hex",
  "leaves": [
    {
      "index": 0,
      "receipt_id": "...",
      "receipt_hash": "...",
      "disposition": "INCLUDED",
      "gate_result": "PASS",
      "decision": "APPROVED",
      "control": "CONTINUE"
    }
  ],
  "dispositions": [
    {
      "receipt_id": "...",
      "disposition": "REJECTED|DEFERRED|NOT_APPLICABLE|...",
      "gate_result": "...",
      "decision": "...",
      "control": "...",
      "reason_code": "...",
      "rule": "...",
      "policy_ref": "..."
    }
  ],
  "reconciliation": {
    "submitted": 0,
    "included": 0,
    "non_included": 0,
    "balanced": true
  },
  "created_at": "ISO-8601 (informational only)",
  "swi_commit_sha": "...",
  "manifest_hash": "..."
}
```

`manifest_hash` is computed over the canonical form of the manifest (excluding the hash field itself).

---

## 10. Reason Codes (minimum set for non-inclusion)

| Code   | Meaning                        |
|--------|--------------------------------|
| BM-001 | Contract exclusion             |
| BM-002 | Duplicate                      |
| BM-003 | Expired                        |
| BM-004 | Unavailable material           |
| BM-005 | Policy / control block         |
| BM-006 | Explicit deferral              |
| BM-007 | Schema / format rejection      |
| BM-015 | Unknown (must not auto-PASS)   |

`BM-015 UNKNOWN` forces `REVIEW_REQUIRED` or `HALT` according to the governing gate; it never silently becomes inclusion.

---

## 11. Reconciliation Rule (central)

```text
submitted_count = included_count
                + rejected_count
                + deferred_count
                + not_applicable_count
                + other explicitly contracted terminal states
```

Any imbalance → `RECONCILIATION_FAILURE` → HALT.  
The batch is not considered successfully constructed until reconciliation balances and every disposition is recorded.

**Principle:**  
> The Merkle root accounts for what was included; the batch manifest accounts for what was not.

A Merkle root alone cannot tell an auditor that something was never included in the first place.

---

## 12. Independent Verification Requirements

An independent verifier (S9-style) given only:

- the batch manifest  
- the declared INCLUDED leaves (or their hashes)  
- the inclusion proofs  
- this contract  

must be able to:

1. Confirm every submitted item has a disposition and the four outcome dimensions.  
2. Confirm reconciliation balances.  
3. Reconstruct the Merkle root from the INCLUDED leaves under the domain-separated rules.  
4. Verify each inclusion proof against the root.  
5. Detect any mutation of leaf, order, proof, root, or disposition record.

If the verifier merely re-invokes the original batch builder, independence is **not** established.

---

## 13. Explicit Non-Claims

This contract and any batch produced under it **do not claim**:

- that the underlying evidence is factually true  
- that any party is authorized  
- that any action is approved for execution  
- that the batch root is a blockchain or external notary proof (unless a later stage adds anchoring)  
- production readiness or production trust  
- universal interoperability  

A valid batch root is solely evidence of integrity of the committed set under the declared rules.

---

## 14. Status Progression (evidence-driven only)

```text
SPECIFIED          ← current (this document)
    ↓
IMPLEMENTED
    ↓
TESTED
    ↓
REPLAYABLE_BOUNDED
    ↓
INDEPENDENTLY_VERIFIED
```

Never automatically advance to PRODUCTION, TRUSTED, AUTHORIZED, COMPLIANT, or SAFE.

Logical evidence-continuity chain for early stages:

B1 Contract → B2 Deterministic batch → B3 Inclusion proofs → B4 Complete inclusion/omission accounting

Only after B1–B4 are evidenced may B5 (mutation) and B7 (S9) be used to upgrade status.

---

## 15. Completion Gate for B1

B1 is complete when:

- This contract document exists and is versioned.  
- Leaf schema, multi-dimensional outcome model, disposition states, tree rules, proof rules, manifest structure, reconciliation rule, and non-claims are fully specified.  
- No code that modifies the sealed M11 path has been introduced.  
- Status remains SPECIFIED until subsequent stages produce evidence.

---

## 16. Relationship to Other Work

- M11 seal remains the sole post-admission cryptographic continuity path for individual evidence.  
- This batch layer is optional downstream aggregation.  
- Interoperability / loss-ledger work (separate controlled stages) may feed sealed receipts into this batch builder; the two layers remain distinct.  
- External anchoring (blockchain or otherwise) is explicitly deferred to a later optional stage (B8).

---

**End of SWI Merkle Batch Contract V1**
