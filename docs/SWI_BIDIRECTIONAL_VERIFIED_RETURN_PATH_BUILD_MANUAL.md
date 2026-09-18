# SWI Bidirectional Verified Return Path

**Manual Build & Verification Guide**

| Field | Value |
|-------|--------|
| Project | Structured Workflow Intelligence (SWI) |
| Repository | Kelronmos/SWI-V2-Modules-11-22 |
| Date | 2026-09-18 |
| Status | **BUILD SPECIFICATION / DESIGN** |
| Implementation | **NOT AUTHORIZED** |
| Module numbers | **pre-R01 … pre-R10** only (not formal M-series) |
| M11 | SEALED — do not modify |
| M12 | FROZEN — do not bypass via return path |
| Claim level | Design → Implementation → Test → Result → Limitation → Next iteration |

---

## 1. Purpose

Establish a controlled path for information in both directions:

```text
USER → REQUEST → AUTHORITY / POLICY → SWI PIPELINE → VERIFICATION
  → EXECUTION → RESULT → RETURN VERIFICATION → AUTHORITY RE-CHECK
  → RESPONSE → USER / UI
```

A successful backend operation does **not** automatically authorize delivery.  
A verified result does **not** automatically authorize every recipient.  
A UI display operation does **not** create authority.

---

## 2. Core design principle

**Forward:** REQUEST → AUTHORITY → POLICY → VERIFICATION → EXECUTION  
**Backward:** RESULT → EVIDENCE → INTEGRITY → AUTHORITY → DELIVERY

The return path must independently establish that the result belongs to the request; came from an admitted path; is unaltered; retains evidence; stays in original authority scope; is permitted for the recipient; and has not acquired authority via UI or intermediate backend.

**Central invariant:** Information may travel backwards; authority does not.

---

## 3. Non-goals

Does not claim: general AI safety; complete system security; tamper-**proof** (use **tamper-evident**); protection against every compromise; proof of semantic correctness or model truthfulness; automatic authorization outside the boundary.

`INTEGRITY ≠ TRUTH` · *verified within the defined contract* ≠ *verified as true*

---

## 4. Zones

| Zone | Role |
|------|------|
| A | USER / CLIENT |
| B | UI — render only; no authority creation |
| C | SWI CONTROL PLANE — response gate |
| D | EXECUTION / BACKEND |

```text
USER → UI (render only) → SWI RETURN GATE
  (identity, binding, integrity, evidence, authority, policy, delivery)
  → VERIFIED RESPONSE
```

---

## 5. Response envelope (conceptual — not frozen)

Illustrative: schema, response_id, request_id, subject_id, authority_scope, result, verification, integrity, provenance, policy, limitations, created_at, expires_at. Freeze only after review.

---

## 6. Request binding

```text
request_id → execution_id → evidence_id → response_id
```

Reject unknown/wrong/expired request. **Test:** result for A returned under B → REJECT.

---

## 7. Authority as scope

```text
RETURNED_RESULT_AUTHORITY ≤ ORIGINAL_REQUEST_AUTHORITY
```

Not a boolean. Represent subject, actions, resources, purpose, times. Result production never expands authority.

---

## 8. Verification state (separated)

IDENTITY / REQUEST_BINDING / INTEGRITY / AUTHORITY / POLICY / PROVENANCE / SEMANTIC_CORRECTNESS (last not implied by integrity).

---

## 9. Evidence and integrity

Result → evidence → hash → envelope. Conceptual digest over content + request_id + evidence_id + authority_scope + previous_digest. Hash = integrity relationship, not truth.

---

## 10. Response gate

`admit_response(request, result, evidence, authority, policy)` in order: schema → binding → identity → evidence ref → evidence integrity → authority → policy → destination → construct → seal → return. Mandatory failure → HALT/REJECT.

---

## 11. Fail-closed

`UNKNOWN ⇏ ALLOW`. Missing evidence/authority/destination → REJECT or PAUSE. Broken integrity → REJECT.

---

## 12–13. UI and backend boundaries

UI may render admitted content and status; must not create authority, change verification, convert REJECT→ALLOW, or silently modify envelopes.

Preferred: `backend → response gate → verified response → UI` — never `backend → UI` as trusted delivery.

Prefer push of admitted response over UI pull of raw backend state.

---

## 14. Transformations

Each hop must declare preserved/lost properties and new claims. Uncontracted transform does not inherit verification.

---

## 15. Negative tests (first)

Authority laundering · UI injection · backend injection · replay · expiry · wrong recipient · evidence removal · hash modification · gate bypass · unknown→ALLOW · receipt-as-permission · key/certificate substitution → REJECT / PAUSE / BLOCKED as defined.

---

## 16. Status model

```text
CREATED → VALIDATING → VERIFIED → ADMITTED → DELIVERED
                 ↘ REJECTED
ADMITTED → EXPIRED | REVOKED
```

Invalid: REJECTED → DELIVERED without a new authorized response.

---

## 17. Pre-modules (experimental only)

pre-R01 Envelope · pre-R02 Binding · pre-R03 Authority re-check · pre-R04 Evidence · pre-R05 Integrity · pre-R06 Provenance · pre-R07 Policy · pre-R08 Destination · pre-R09 Sealer · pre-R10 Delivery adapter.

No formal M-numbers until contracts, tests, CI, and seal decision exist.

---

## 18. Layout when authorized

```text
response_path/{contracts,kernel,validators,adapters,tests,evidence,docs}
```

Isolated; no silent V1 internal imports from V2.

---

## 19. Acceptance (A–J)

Binding · authority ≤ request · integrity on modify · evidence missing · wrong recipient · UI cannot create authority · backend cannot bypass gate · replay · expiry · uncontracted transform.

---

## 20. Invariants I-01 … I-15

Result/UI cannot create authority · backend result not auto-deliverable · verification not upgraded without evidence · integrity ≠ truth · certificate ≠ unrestricted authority · receipt ≠ permission · no silent recipient change · no silent expiry recovery · unverified transform does not inherit verification · unknown ⇏ ALLOW · new privileged action needs new authority · forward authority does not expand on return · UI renders only · response gate is mandatory.

---

## 21. Critical loop

Never: verified response → UI → automatic privileged action.  
Always: verified response → UI → **new request** → authority check.

---

## 22. Defensible claim if suite passes

Within the implemented boundary, defined binding, integrity evidence, and authority scope can be preserved on return, and tested modification/expansion attempts via defined seams are rejected.

Not: AI safety solved; truthful AI guaranteed; whole app secure.

---

## 23. Implementation gate (closed)

Does **not** authorize `response_path/` code, formal modules, CI, or seal.

```text
BUILD SPEC → contract freeze → adversarial criteria → IMPLEMENTATION AUTHORIZATION
  → pre-R code → TEST → CI → AUDIT → STOP → seal decision only if gates pass
```

---

## 24. Core model

```text
FORWARD:  USER → REQUEST → AUTHORITY → POLICY → SWI → EXECUTION → EVIDENCE → RESULT
BACKWARD: RESULT → RETURN GATE → SEALED RESPONSE → UI → USER
NEW ACTION: NEW REQUEST → NEW AUTHORITY CHECK
```

«Build only what can be demonstrated. Test failure paths. Record limitations. Stop at the boundary.»
