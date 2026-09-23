# Ed25519 signature primitive

**Status:** IMPLEMENTED / TESTED (crypto helper only)

**Role:** Cryptographic integrity / signature primitive.

It can establish:

> This exact canonical byte sequence verifies under this public key.

It cannot establish: truth · legality · ethics · authorization · identity legitimacy ·
production readiness · **replay completeness** · governance approval.

**Not:** CRTG · certificate chain validation · key rotation · Foundation Seal 5 by itself

## Placement

```text
Payload / Evidence
        ↓
Canonicalization
        ↓
Ed25519 sign / verify   ← integrity evidence only
        ↓
chain / Merkle (where used)
        ↓
scoped seal path (separate contract)
```

## M11 order (immutable)

```text
RAW → ADMISSION → AdmittedInput → commitment → chain → Merkle → Ed25519 → M11 seal evidence
```

Never: `RAW → Ed25519 → therefore trusted/admitted`.

```text
SIGNATURE ≠ TRUTH
SIGNATURE ≠ AUTHORITY
SIGNATURE ≠ ADMISSION
SIGNATURE alone ≠ REPLAY COMPLETENESS
SIGNATURE ≠ PRODUCTION AUTHORIZATION
SIGNATURE ≠ automatic seal of a new SHA
```

A signature may be *part of* a replay/evidence system; it does not by itself prove that the
entire historical sequence was replayed completely, in order, under the same rules.

## API (`swi_v2.kernel.ed25519_sig`)

- `verify_ed25519(public_key, message, signature) -> True` or raises `SignatureVerificationError`
- `verify_canonical_mapping(public_key, material, signature)`
- `canonical_message(mapping) -> bytes`
- `sign_ed25519` / `generate_keypair` — tests and controlled exporters only

Private keys must never be committed to Git. CI uses ephemeral keys where sealing is demonstrated.
