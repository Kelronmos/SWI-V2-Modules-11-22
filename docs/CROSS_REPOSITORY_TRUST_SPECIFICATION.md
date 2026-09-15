# Cross-Repository Trust (V2 copy of design posture)

**Status:** PROPOSED / DESIGN PENDING

Hierarchy:

```text
Trusted CA → Repository certificate → Public key
Private signing key → Task signature → Envelope → CRTG → M11 → AdmittedInput
```

Requirement: verifiable **signer identity** + **signature under an active key** in the trust policy.

Certificate ≠ task signature. Certificate validity ≠ truth.

Not implemented. No private keys in this repository.
