# SWI ↔ Zero Trust Relationship

**Document status:** DESIGN / NORMATIVE REFERENCE  
**Implementation status:** NOT a ZTA product  
**Seal status:** NOT SEALED  
**Production status:** BLOCKED  
**Date:** 26 September 2026

---

## 1. External three-layer reference (do not redefine SWI)

| Layer | Document | Role |
|-------|----------|------|
| **NIST** | SP 800-207 | Defines Zero Trust architecture and principles |
| **CISA** | ZTMM v2 | Flexible maturity roadmap (Traditional → Optimal) |
| **DoD / NSA** | Strategy, RA, CSIs | Defense-oriented pillars, capabilities, continuous maturity guidance |

SWI does **not** replace any of these. They supply **external security context**.

---

## 2. Architectural boundary

> Zero Trust supplies security context.  
> SWI determines whether a workflow transition is structurally permitted under its own evidence, governance, privacy, authority, verification, security, and safety gates.

```text
ZERO TRUST ENVIRONMENT
        ↓
SECURITY CONTEXT
        ↓
SWI CONTEXT / EVIDENCE
        ↓
SWI GATE EVALUATION
        ↓
SWI DECISION
        ↓
HUMAN AUTHORITY
        ↓
AUTHORIZATION
        ↓
ACTION
```

SWI must not bypass ZTA controls.  
ZTA signals must not bypass SWI governance.

---

## 3. Mapping (treatment, not maturity scores)

| External ZT concept | SWI treatment | Boundary |
|---------------------|---------------|----------|
| User / Identity | Human authority + scoped identity | Identity ≠ authorization |
| Device | Integrity evidence | Hash/posture ≠ authority |
| Network & Environment | Isolation / quarantine / controlled boundaries | Logical isolation ≠ network segmentation |
| Data | Privacy domains + purpose + scope | One domain ≠ another |
| Application & Workload | Workflow / module / state controls | SWI is not an application proxy |
| Visibility & Analytics | Evidence, audit, diagnostics, replay | Observation ≠ execution |
| Automation & Orchestration | Closed transition engine | Automation cannot manufacture authority |
| Governance | Law / policy / authority / seal | Governance remains human-accountable |

**Machine-readable posture (no official CISA rating):**

```yaml
alignment:
  cisa_pillar: GOVERNANCE  # example analytical only
  swi_relation: STRONG_STRUCTURAL_ALIGNMENT
  maturity_rating: NOT_ASSESSED
  evidence_scope: EXPERIMENTAL_KERNEL
```

Do **not** encode “SWI Governance = Advanced” as an official maturity score.

---

## 4. Critical invariant

```text
ZT_SIGNAL ≠ EVIDENCE ≠ ADMISSION ≠ VERIFICATION
  ≠ HUMAN_AUTHORITY ≠ AUTHORIZATION ≠ ACTION

CERTIFICATE_VALID  ↛ HUMAN_AUTHORITY
TPM_VERIFIED       ↛ HUMAN_AUTHORITY
HSM_SIGNED         ↛ HUMAN_AUTHORITY
DEVICE_COMPLIANT   ↛ HUMAN_AUTHORITY
ZTA_ACCESS_GRANTED ↛ SWI_AUTHORIZATION
CI_GREEN           ↛ SWI_AUTHORIZATION
```

---

## 5. ATM domain (ZTA) — defined, not sealed

Scenarios belong in ATM-001 as their **own domain**:

| ID | Intent | Expected (class) |
|----|--------|------------------|
| ZTA-A01 | Authenticated but unauthorized transition | BLOCK |
| ZTA-A02 | Valid device posture, wrong privacy domain | BLOCK / ESCALATE |
| ZTA-A03 | Valid certificate, no human authority | BLOCK |
| ZTA-A04 | HSM/TPM substituted for authorization | BLOCK |
| ZTA-A05 | ZTA access grant without SWI evidence | BLOCK |
| ZTA-A06 | Security posture changes after verification | RE-EVALUATE |
| ZTA-A07 | Historical security evidence as current | REJECT / BLOCK |
| ZTA-A08 | Old security state into rebuilt structure | REJECT / BLOCK |
| ZTA-A09 | Technical identity exercises human authority | REJECT / BLOCK |
| ZTA-A10 | Authenticated cross-domain access | BLOCK / ESCALATE |

Lifecycle: DEFINED → IMPLEMENTED → EXECUTED → EVIDENCE → REPLAY → REPRODUCE → VERIFIED  
(**not** automatic SEALED).

---

## 6. Non-claims

- SWI is not a Zero Trust product or maturity-assessed enterprise ZTA.
- This document does not authorize production.
- This document does not reseal M11 or any module.
- External ZT docs remain reference architecture, not SWI identity.
