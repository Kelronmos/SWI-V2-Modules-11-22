# Verifier Hardening Pass 1

**Date:** 2026-09-17  
**Goal:** Live CI resolution + property-level mapping for historical M11 seal.  
**Does not:** rewrite M11 seal · implement M12 · claim standalone verifier repo.

## Acceptance path

```text
VALID SEALED M11
  → LIVE GitHub run 35253244912
  → head_sha == 1d6d7dc…
  → conclusion == success · status == completed
  → real source + real tests present
  → e4_eligible_live
```

## Adversarial (must fail eligibility)

wrong SHA · wrong run ID · self-attested alone · audit JSON alone

## Commands

```bash
python scripts/v47_ci_resolver.py --owner Kelronmos --repo SWI-V2-Modules-11-22 \
  --run-id 35253244912 --seal-commit 1d6d7dc250df80f39aa60bd8da812c9ae3efebec

python scripts/v47_live_m11_verify.py --adversarial
```

## Next gate

Standalone verifier repository (no import of sealer verification logic).
