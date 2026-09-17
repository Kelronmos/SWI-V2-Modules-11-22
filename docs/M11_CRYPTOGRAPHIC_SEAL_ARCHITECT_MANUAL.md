# M11 Cryptographic Seal — Architect Manual

**Date:** 2026-09-17  
**M11 status:** CRYPTO SEAL IMPLEMENTED + TESTED / **NOT SEALED**

## 1. Purpose

Bind a cryptographic seal to real `AdmittedInput` after M11 admission.

## 2. Scope

Strict canonicalize · SHA-256 commitment · chain · dense Merkle · Ed25519 · independent verify.

## 3. Non-goals

CRTG · production KMS · factual truth · action safety · consensus · ZK · claiming SEALED without release gate.

## 4–6. Architecture / contract / admission

```
Envelope (serialized) → admit_foundation_input → AdmittedInput → create_seal → verify_seal
```

Admission integrity contract unchanged (`default=str` remains on admission path).  
Seal path uses **strict** JSON types only (no `default=str`).

## 7–11. Layers

| Layer | Mechanism |
|-------|-----------|
| Canonical | `seal_canonicalize` — null/bool/int/float/str/list/object only |
| Commitment | SHA-256(`SWI-M11-SEAL-COMMITMENT-V1:` ‖ canonical) |
| Chain | SHA-256(`SWI-M11-CHAIN-V1:` ‖ prev ‖ commitment); genesis documented |
| Merkle | Domain-separated dense tree over commitment materials |
| Signature | Ed25519 over strict-canonical signing material |

## 12–13. Verification / fail-closed

Recompute all layers; any mismatch → `False`. No internal `self.valid = True`.

## 14. Key management

Ephemeral test keys via `generate_keypair()`. Never commit private keys.

## 15–16. Threats / tests

See `M11_CRYPTO_THREAT_MATRIX.md` and `test/test_m11_post_admission_seal.py`.

## 17–18. Demo / independent verification

```bash
python scripts/demo_m11_crypto_seal.py   # exit 0
```

## 21. Release gate

Two-checkout CI · Python matrix · frozen SHAs · `M11_SEAL_RECORD.md` **before** SEALED.

## 22. Known limitations

Replay not solved by signature alone. CRTG DESIGN PENDING. Production key rotation NOT IMPLEMENTED.

## 23. Future CRTG boundary

Separate from this seal. Requires identity, issuance, revocation, rotation, trust roots.
