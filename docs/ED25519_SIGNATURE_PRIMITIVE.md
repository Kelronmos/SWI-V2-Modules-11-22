# Ed25519 signature primitive

**Status:** IMPLEMENTED / TESTED (crypto helper only)

**Not:** CRTG · certificate chain validation · key rotation · Foundation Seal 5

## API (`swi_v2.kernel.ed25519_sig`)

- `verify_ed25519(public_key, message, signature) -> True` or raises `SignatureVerificationError`
- `verify_canonical_mapping(public_key, material, signature)`
- `canonical_message(mapping) -> bytes`
- `sign_ed25519` / `generate_keypair` — tests and controlled exporters only

Private keys must never be committed to Git.
