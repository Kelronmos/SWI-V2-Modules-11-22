# M11 Seal Record

## Seal Status

**SEALED** — post-admission cryptographic continuity path under the evidence below.

Date (UTC): 2026-09-17  
Governance act: this record  
Not claimed: CRTG · Foundation Seal 5 · production key custody · factual truth of payloads · M12 auto-complete

---

## Frozen commits

| Repo | SHA |
|------|-----|
| **V2** (seal + travel consumer) | `1d6d7dc250df80f39aa60bd8da812c9ae3efebec` |
| **V1** (producer tip at seal time; CI checks out V1 `main`) | `e0c6a521d7965c46c18464edc5dc6fbd8f9e254c` |

Workflow file: `.github/workflows/two_checkout_travel.yml`  
Workflow run: **#50**  
Run ID: `35253244912`  
URL: https://github.com/Kelronmos/SWI-V2-Modules-11-22/actions/runs/35253244912  
Event: `push` · Conclusion: **success** · Completed: 2026-09-17T17:31:57Z

---

## Contract

| Item | Value |
|------|--------|
| Foundation / schema versions | `1.0-proposed` |
| Seal domain | `SWI-M11-SEAL-V1` |
| Seal version | `1.0-proposed` |
| Admission | schema + integrity + verification_status; produces `AdmittedInput` only |
| Seal input | **`AdmittedInput` only** (envelope/dict rejected) |

---

## Cryptographic algorithms (post-admission)

| Layer | Algorithm / rule |
|-------|------------------|
| Commitment | SHA-256 over `SWI-M11-SEAL-COMMITMENT-V1:` ‖ strict-canonical admitted material |
| Chain | SHA-256 over `SWI-M11-CHAIN-V1:` ‖ previous ‖ commitment; documented genesis |
| Merkle | Dense domain-separated tree; verifier **reconstructs** expected tree/proof |
| Signature | Ed25519 over strict-canonical signing material |
| Keys | Ephemeral test keys in CI; **no production private keys in repo** |

---

## CI matrix (run #50)

| Gate | Result |
|------|--------|
| V1 produce evidence (Python 3.12) | **PASS** |
| V2 admit without V1 tree (Python 3.10 / 3.11 / 3.12) | **PASS** |
| `swi_core` not importable on V2 | **PASS** |
| Admit valid / reject tampered / reject bad integrity | **PASS** |
| Post-admission seal + verify + tamper reject | **PASS** (all three Pythons) |
| V2 unit tests in isolation job | **PASS** |

---

## Explicit limitations

| Topic | Status |
|-------|--------|
| CRTG / certificate chain | **NOT IMPLEMENTED** |
| Production key management / HSM / rotation | **NOT IMPLEMENTED** |
| Replay as sealed policy | Signature ≠ replay proof |
| Factual truth of payload | **Not established by cryptography** |
| Sparse Merkle | **RESEARCH ONLY — not part of this seal** |

---

## Decision

```text
M11 CONTINUITY LOCK / STATE PRESERVATION
  → SEALED
  under V2 SHA 1d6d7dc250df80f39aa60bd8da812c9ae3efebec
  and GitHub Actions run 35253244912
```

M12 may proceed only under controlled module manuals (claim → implementation → test → result → limitation).
