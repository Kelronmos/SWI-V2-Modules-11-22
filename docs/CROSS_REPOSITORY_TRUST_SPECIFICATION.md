# SWI Cross-Repository Certificate, Identity & Key-Rotation Trust Manual

**Version:** 1.0 — Design Specification  
**Date:** 15 September 2026  
**Author:** Keletso Ronald Mosidila — Trusts Motion  
**Status:** **PROPOSED / DESIGN PENDING**

> Canonical design shared with V1. Not implementation. See also `docs/CROSS_REPOSITORY_TRUST_INTEGRATION.md`.

## Purpose

No cross-repository task crosses the SWI trust boundary until signer identity, certificate chain, key state, signature, and task envelope are verified.

## Distinctions

Valid certificate ≠ valid signature ≠ valid task ≠ valid evidence ≠ true claim ≠ safe action.

## Status

| Component | Status |
|-----------|--------|
| CRTG | **PROPOSED** |
| CA / cert profile / trust store | DESIGN PENDING |
| Envelope / sign / verify | DESIGN PENDING |
| Rotation / revocation / replay | DESIGN PENDING |
| CI / production | NOT IMPLEMENTED |

## Intended V2 path

```text
External Task → CRTG → Verified Envelope → M11 → AdmittedInput → V2 Kernel → M12+
```

CRTG does **not** replace M11. M12 must **not** accept raw input because a certificate check passed.

## Private keys

Never in Git, fixtures, or payloads.

## Crypto

Established standards only (profile freeze before code). No custom crypto.

## Fail-closed

Missing/invalid identity material → REJECT / HALT. Unknown is not compatible.

## Not claimed

Universal security · truth of payload · production CRTG · certificates implemented in this repo.
