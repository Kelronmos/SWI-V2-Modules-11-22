# M11 Crypto Threat Matrix

**Scope:** Post-admission seal only. Not CRTG. Not production key governance.

| Threat | Detection |
|--------|-----------|
| Payload tampering | commitment mismatch |
| Evidence ID substitution | commitment mismatch |
| Source substitution | commitment mismatch |
| admitted_by substitution | commitment mismatch |
| Signature alteration | Ed25519 failure |
| Wrong signing key | Ed25519 failure |
| Merkle proof alteration | proof failure |
| Merkle root alteration | root mismatch |
| Chain alteration | chain hash mismatch |
| Unsupported seal input type | canonicalization rejection |
| Version/domain confusion | version/domain rejection |
| V1 import leakage | isolation tests (separate) |
| Private key in repo | secret scanning / review |
| Replay of valid sealed evidence | **NOT solved by signature alone** — needs sequence/nonce/policy |

## Replay note

A valid signature can be resubmitted. Replay controls require separate event IDs, nonces, expiry, or deduplication — not claimed by M11 seal alone.
