# SWI PRE Module Registry

**Date:** 2026-09-19  
**Type:** Documentation-only architectural map  
**Runtime impact:** NONE — does not rename modules, change imports, or alter APIs  

## Doctrine

```text
PRE-Mxx  = architectural / pre-seal identity (metadata)
Mxx      = production identifier used by the repository
Category = primary architectural responsibility

Name everything. Categorise everything.
Contract what is ready. Test what is implemented.
Seal only what is evidenced. Block what is not ready.

Registry completeness ≠ implementation completeness
TESTED ≠ SEALED · DATA ≠ AUTHORITY
```

## Status vocabulary

| Status | Meaning |
|--------|--------|
| PROPOSED | Concept only |
| CONTRACTED | Interface defined |
| DESIGNED | Behaviour documented |
| IMPLEMENTED | Code exists |
| TESTED | Relevant tests pass |
| CI-VERIFIED | Required CI green |
| AUDITED | Evidence reviewed |
| SEALED | Explicit seal criteria satisfied |
| NOT IMPLEMENTED | No executable code |
| BLOCKED | Intentionally stopped |
| NOT AUTHORIZED | Must not promote |
| DEFERRED | Postponed |
| EXPERIMENTAL | Outside formal module chain |

---

## V1 map (foundation / evidence) — repo `SWI-V1-Module-1-10`

| PRE ID | Prod | Name | Category | Status (honest) | Notes |
|--------|------|------|----------|-----------------|-------|
| PRE-M00 | M00 | Trainer Pipeline | FOUNDATION / TRAINING | IMPLEMENTED / TESTED | Orchestration; not renamed |
| PRE-M01 | M01 | Foundation / input boundary | FOUNDATION / INPUT | IMPLEMENTED / TESTED | Document actual contract only |
| PRE-M02 | M02 | Pattern / encoding | VALIDATION / NORMALIZATION | SEALED (bounded contract) | regex/base64/etc. per V1 docs |
| PRE-M03 | M03 | Temporal evidence | EVIDENCE / TIME | SEALED (bounded) | Timestamp ≠ truth |
| PRE-M04 | M04 | Cryptographic protection | CRYPTOGRAPHY | IMPLEMENTED / TESTED | Primitive ≠ key governance |
| PRE-M05 | M05 | Sensitive data detection | PRIVACY / CLASSIFICATION | SEALED (bounded) | Detection ≠ complete privacy |
| PRE-M06 | M06 | Drift detection | DRIFT / BEHAVIOURAL | SEALED (bounded) | Score ≠ malice/truth |
| PRE-M07 | M07 | Integrity chain | INTEGRITY / EVIDENCE | IMPLEMENTED / TESTED | Tamper-evident ≠ tamper-proof |
| PRE-M08 | M08 | Token boundary | AUTH / TOKEN | IMPLEMENTED / TESTED | HMAC ≠ authorization |
| PRE-M09 | M09 | Evidence / persistence | INTEGRITY / PERSISTENCE | IMPLEMENTED / TESTED | Persistence ≠ authority |
| PRE-M10 | M10 | Execution isolation | EXECUTION / CONTAINMENT | IMPLEMENTED / TESTED | RLIMIT ≠ full sandbox |

V1 PRE-R runtime: **NOT AUTHORIZED** · design docs only.

---

## V2 map — repo `SWI-V2-Modules-11-22`

| PRE ID | Prod | Name | Category | Status (honest) | Notes |
|--------|------|------|----------|-----------------|-------|
| PRE-M11 | M11 | Continuity Lock | CONTINUITY / STATE | **SEALED** (see `docs/M11_SEAL_RECORD.md`) | Do not reopen for taxonomy |
| PRE-M12 | M12 | Next continuity / admission | CONTINUITY / ADMISSION | CONTRACT / controlled | Stage after M11; no bulk build |
| PRE-M13 | M13 | Scrubber | SANITIZATION | PROPOSED / DEFERRED | Transform ≠ authority |
| PRE-M14 | M14 | Agentic loop | EXECUTION / AGENT | PROPOSED / DEFERRED | Loop ≠ authority source |
| PRE-M15 | M15 | Summarization | TRANSFORM | PROPOSED / DEFERRED | Summary ≠ original evidence |
| PRE-M16 | M16 | Reserved | SLOT / DEFERRED | PROPOSED · NOT IMPLEMENTED | |
| PRE-M17 | M17 | Reserved | SLOT / DEFERRED | PROPOSED · NOT IMPLEMENTED | |
| PRE-M18 | M18 | Identity graph | IDENTITY | PROPOSED / DEFERRED | Relationship ≠ authorization |
| PRE-M19 | M19 | Governance access | GOVERNANCE / ACCESS | PROPOSED / DEFERRED | principal+resource+operation |
| PRE-M20 | M20 | Reserved | SLOT / DEFERRED | PROPOSED · BLOCKED | |
| PRE-M21 | M21 | Transform / summary | TRANSFORM | PROPOSED / DEFERRED | Transform ≠ authority |
| PRE-M22 | M22 | Reserved final | SLOT / DEFERRED | PROPOSED · BLOCKED | Not a dump slot |

---

## Experimental (not formal M-series)

| ID | Location | Category | Status |
|----|----------|----------|--------|
| pre-R01…pre-R10 | `experimental/response_boundary/` | RESPONSE BOUNDARY | EXPERIMENTAL · gate **TESTED** (20) · fail-safe **NOT PROVEN** |
| PR-009 | *(planned)* | RESPONSE ENFORCEMENT | **NOT IMPLEMENTED** — next executable gate |

### PR-009 — Response Rejection Enforcement (planned only)

```text
Response → ReturnGate → REJECT → ENFORCEMENT → NON-EXECUTING
  → privileged action blocked (T20)
```

- Do **not** rewrite ReturnGate into a full runtime.  
- Keep gate (admission) separate from enforcement.  
- Prefer existing V2 `HaltedWorkflow` / `require_admitted` where contracts match.  
- Do **not** invent APIs only to greenwash tests.

---

## Evidence ledger (narrow claims)

| Claim | Evidence | Status |
|-------|----------|--------|
| ReturnGate rejects invalid fixtures | 20 unit tests | TESTED |
| Gate fail-closed under those fixtures | same | TESTED |
| REJECT prevents privileged execution | T20 | **PENDING** |
| M11 sealed | `M11_SEAL_RECORD.md` | SEALED (record) |
| PRE-M12+ implemented | — | NOT YET |
| CRTG production-ready | — | NOT ESTABLISHED |
| Fail-safe beyond pre-R gate | PR-009 | NOT ESTABLISHED |

---

## Categories (primary pillars)

FOUNDATION · VALIDATION · EVIDENCE · INTEGRITY · CRYPTOGRAPHY · PRIVACY · DRIFT · AUTHORITY · EXECUTION · ISOLATION · CONTINUITY · TRANSFORM · IDENTITY · GOVERNANCE · RESPONSE BOUNDARY

One primary responsibility per module.

---

## Next controlled sequence

```text
PRE REGISTRY (this doc)     ← done (docs only)
      ↓
PR-009 ENFORCEMENT          ← executable, narrow
      ↓
T20 FAIL-SAFE PROOF
      ↓
FULL REGRESSION (V1+V2+two-checkout)
      ↓
M12 CONTRACT (if opening next)
```

No shortcut: naming → implementation · testing → seal · evidence → authority.
