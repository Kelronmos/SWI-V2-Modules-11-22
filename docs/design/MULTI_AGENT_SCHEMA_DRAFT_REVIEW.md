# Multi-Agent Distributed Schema Draft — SWI Fit Review

**Date:** 2026-09-19  
**Source:** Proposed optimised multi-agent envelopes, BaseSWIModule, async batch, DLQ/NATS/S3 stack  
**Status:** **DESIGN / EXPERIMENTAL** · **NOT IMPLEMENTED** in V1/V2 runtime · **NOT SEALED** · **NOT PRODUCTION AUTHORIZED**

## Verdict (short)

| Question | Answer |
|----------|--------|
| Can ideas *inform* future SWI work? | **Yes** (contracts, deltas, state_hash, fail-closed) |
| Can this stack *replace* current V1/V2 as-is? | **No** |
| Should it be merged into main modules now? | **No** |
| Is “production-ready” supported by SWI evidence? | **No** |

Working SWI remains:

```text
V1 evidence producer → serialized envelope → V2 M11 admission → seal
pre-R ReturnGate (experimental, gate-tested)
```

The draft is a **parallel research architecture** (orchestrator + agents + bus + DLQ). It must not silently become M11–M22 or claim CRTG/Seal 5.

---

## What aligns with SWI doctrine

| Draft idea | SWI analogue | Fit |
|------------|--------------|-----|
| Zero-base / `extra="forbid"` | Admission + canonical contracts; no implicit fields | Strong |
| Explicit input contracts | M11 schema/integrity admission | Strong |
| SHA-256 continuity (`state_hash`) | Integrity reference / chain / seal digests | Strong *if* fail-closed on mismatch |
| Delta-only updates | Append-only / hash-chain style evidence | Conceptual fit |
| Structured status enums | ADMIT/REJECT/HALT, CONTRACT_VIOLATION | Partial (map carefully) |
| Claim → schema → test | SWI Claim→Impl→Test→Result→Limitation | Strong |
| Deterministic mode | Existing deterministic admission preference | Strong |

---

## What conflicts or overclaims

| Draft claim | SWI problem |
|-------------|-------------|
| “Production-grade / production-ready” | Not evidenced in V1/V2 tip; violates TESTED≠SEALED |
| Step ID `SWI-MOD-NN-NNN` | Does not match M00–M22 / PRE-Mxx registry |
| Free `origin_agent` / `target_agent` strings | Risk of agent names as implicit authority |
| `assertions_verified: list[str]` | Strings are not proofs; can launder “authority” |
| **`RECALCULATE_HASH_AND_REPLAY`** | **High risk:** hash mismatch often means *stop*, not rewrite hash and continue |
| Payload patch + auto-replay | Can become authority/data laundering without new admission |
| NATS / Temporal / Redis / S3 as required runtime | Not part of sealed SWI path; optional future lane |
| Async batch + high concurrency | Race vs single-writer hash chain; needs separate contract |
| MyPy strict + ruff on `modules/` | Paths don’t exist in current V2 layout (`swi_v2/`, `experimental/`) |
| Full suite requires live NATS | CI would skip or fail; not drop-in for existing workflows |

### Critical security note (SWI)

```text
STATE_HASH_MISMATCH  →  prefer REJECT/HALT / DLQ without auto-mutation
NOT
STATE_HASH_MISMATCH  →  rewrite state_hash to current → replay as if continuous
```

Silent hash rewrite breaks the continuity claim M11 and integrity chains are built to protect. Remediation may **diagnose** and escalate; **replay** requires a **new** admission decision and explicit policy, not hash patching.

Same for:

```text
evidence ≠ authority
model output ≠ authority
delta ≠ permission
SUCCESS status ≠ truth
```

---

## Fit to current repos

| Layer | Current SWI | Draft |
|-------|-------------|-------|
| V1 | Trainer → FoundationEvidenceEnvelope | Not agent-orchestrator |
| V2 M11 | admit → AdmittedInput → seal | Not multi-agent bus |
| pre-R | ReturnGate REJECT/ADMIT | Gate only; no NATS/DLQ |
| Deps | stdlib + cryptography where needed | pydantic, nats, aioboto3, … |
| CI | two-checkout, pre-r, V2 verify | Proposed `swi-ci.yml` paths mismatch |

**Patch policy:** do **not** replace `admission.py`, seal path, or pre-R core with this stack. Optional future: `experimental/distributed_schema/` **after** contract freeze and PR-009-style enforcement rules.

---

## Recommended adaptation (if pursued later)

1. **Rename to design IDs** — e.g. `DESIGN-DA-01` (distributed agent), not M11–M22.  
2. **Map statuses** — SUCCESS→only after gate; CONTRACT_VIOLATION→REJECT/HALT; never auto-ADMIT.  
3. **Hash mismatch** — fail-closed; DLQ for human/policy path; no default recalculate-and-replay.  
4. **Authority** — keep principal/resource/action (or node/resource/operation); agents are not authorities.  
5. **Deltas** — merge only after admission + integrity; ledger is evidence, not permission.  
6. **CI** — unit-test pure functions without NATS first; mark NATS/S3 tests optional/`skip if unavailable`.  
7. **PR-009 first** — enforcement that REJECT cannot be ignored, before distributed workers.  

---

## Test review of the draft suite

| Test class | What it shows | Gap |
|------------|---------------|-----|
| Envelope field shape / SHA-256 length | Structural | Not full jsonschema reject of extras |
| Delta does not mutate original dict | Shallow immutability | Not concurrent ledger safety |
| NATS remediate + republish | Integration *if* NATS up | Skips offline; not SWI CI |
| Escalation metric / no primary publish | Useful fail-safe *idea* | Daemon-local only |
| Local escalation file write | Audit artifact | Not SWI seal evidence |

**None** of these prove: V1→V2 travel, M11 seal, or pre-R fail-safe beyond the gate.

---

## Explicit non-claims

- Not a replacement for FoundationEvidenceEnvelope / AdmittedInput  
- Not multi-agent production SWI  
- Not CRTG, Seal 5, or complete key lifecycle  
- Not automatic distributed lockdown  
- Not authorized to change M11 seal status  

---

## Next gate (consistent with PRE registry)

```text
PRE REGISTRY (done)
  → PR-009 enforcement (still primary executable gap)
  → optional DESIGN-DA contract freeze (this doc)
  → experimental implementation only under explicit authorization
  → unit tests without external brokers first
  → never auto-merge into sealed path
```

**Summary:** The draft is useful as a **bounded design study** (zero-base contracts, deltas, hash continuity, DLQ taxonomy). It does **not** pass SWI’s evidence bar for production or for patching sealed modules. Treat as **PROPOSED / NOT IMPLEMENTED** until contracted, implemented in an experimental lane, tested, and limited honestly.
