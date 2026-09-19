# Response Envelope — Field Review (pre-freeze)

**Status:** REVIEW / PROVISIONAL  
**Date:** 2026-09-19  
**Parent:** `docs/SWI_BIDIRECTIONAL_VERIFIED_RETURN_PATH_BUILD_MANUAL.md`  
**Implementation:** NOT AUTHORIZED  
**Schema id (proposed):** `swi.response.v1-proposed`

## Required fields (candidate)

schema, response_id, request_id, subject_id, result, authority_scope, verification, integrity, provenance, policy, limitations[], created_at, expires_at.

## Verification factors

identity, request_binding, integrity, authority, policy, provenance; semantic_correctness default **NOT_ESTABLISHED**.

## Excluded

Boolean authorized-only, truth/trusted/m11_admitted flags, executable instruction channels.

## Integrity material (conceptual)

Digest over schema, ids, canonical result, authority_scope, evidence_id, policy.decision, previous_digest.

## Checklist

- [ ] Sufficient for binding, authority ≤ request, destination, expiry
- [ ] No semantic truth implication
- [ ] Limitations required on admitted envelopes
- [ ] Aligned with adversarial acceptance doc

Do not implement until authorization is explicit.
