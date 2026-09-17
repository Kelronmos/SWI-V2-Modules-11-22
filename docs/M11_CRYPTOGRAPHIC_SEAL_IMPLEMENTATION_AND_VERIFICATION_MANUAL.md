# M11 Cryptographic Seal — Implementation and Verification Manual

**Date:** 2026-09-17  
**Status of this document:** Describes implementation when present on the branch.  
**M11 seal status:** NOT SEALED until CI + tip two-checkout + M11_SEAL_RECORD.md exist.

## 1. Purpose

Attach a cryptographic seal **after** successful Module 11 admission so the seal covers the real `AdmittedInput`, not a parallel demo object.

## 2. Scope

| In scope | Out of scope |
|----------|--------------|
| Merkle commitment | CRTG certificate chain |
| Post-admission Ed25519 seal | Production KMS / HSM |
| Independent verify_seal | Consensus / ZK |
| Adversarial unit/E2E tests | Claiming M11 SEALED without CI |

## 3. Security boundary

```
FoundationEvidenceEnvelope (serialized)
  → admit_foundation_input()   # schema + integrity only
  → AdmittedInput
  → create_seal(AdmittedInput, ...)
  → SealedEvidence
  → verify_seal → True / False
```

`create_seal` rejects non-`AdmittedInput` (no envelope/dict bypass).

## 4–11. Layers

Canonical admitted fields → SHA-256 digest → chain hash → Merkle root/proof → Ed25519 over signing material → independent recompute on verify.

## 12. Fail-closed behaviour

Any covered mutation → `verify_seal` returns False. Wrong key / bad signature → False.

## 13. Replay

Signing does **not** equal replay protection. Use existing ReplayGuard where applicable.

## 14. Key management

Test keys only via `generate_keypair()`. Never commit private keys.

## 15–16. Tests

See `test/test_m11_post_admission_seal.py` and `test/test_m11_end_to_end_seal.py`.

## 17–20. Release gate

Two-checkout CI, Python matrix, frozen tip SHAs, then `M11_SEAL_RECORD.md` — **before** any SEALED status change.

## 21. What this does NOT prove

Production trust infrastructure, CRTG, Seal 5, factual truth of payloads.

## 22. Next stage

M12 remains BLOCKED until M11 is actually sealed under the repository release gate.
