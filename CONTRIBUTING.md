# Contributing to SWI V2

SWI is open for collaboration.

Collaboration does **not** rewrite provenance.

Permission is **not** required to contribute.  
Evidence **is** required before claims are accepted.

---

## Philosophy

> Open the code, not the history.

Governing technical doctrine:

> EVIDENCE BEFORE CLAIM.  
> BOUNDARY BEFORE EXPANSION.  
> CONTRACT BEFORE IMPLEMENTATION.  
> TEST FOR BEHAVIOUR.  
> CI FOR REPRODUCIBILITY.  
> AUDIT FOR CONFIDENCE.  
> SEAL FOR CONTROLLED DEPENDENCY.

---

## M11 / M12 protection

- **Do not** rewrite, regenerate, or alter the historical M11 seal or its CI binding merely because documentation or licence files changed.
- **Do not** implement or “complete” M12 under a collaboration/governance PR.
- M12 remains gated: M11 sealed → M12 contract → implementation → tests → CI → audit → seal.
- New technical work produces **new** evidence events; historical evidence stays historical.

---

## Contribution workflow

```text
Issue / Proposal → Understand boundary → Define claim → Implement
→ Write tests → Run tests → Document result → Document limitation
→ CI → Review → Merge
```

---

## Pull request standard

### Claim
What property is this change intended to demonstrate?

### Implementation
What code changed?

### Tests
What tests were added or changed?

### Result
What actually happened?

### Limitation
What remains unproven?

### CI
Which CI run demonstrates reproducibility?

### Risk
What existing behaviour (including M11) could this affect?

### Evidence
What repository evidence supports the claim?

---

## Evidence Before Claims

Distinguish: **Proposed → Implemented → Tested → CI-verified → Audited → Sealed → Independently verified.**

Do not represent experimental or partial work as established SWI functionality.

---

## Attribution

Original SWI architecture: Keletso Ronald Mosidila / Trusts Motion.  
Contributors are credited for their own contributions.  
Contribution does not constitute endorsement, certification, or co-ownership of the original architecture.

---

## Security

See [SECURITY.md](SECURITY.md).

---

## Licence of contributions

By submitting a contribution, you agree it is provided under the Apache License 2.0 unless you explicitly state otherwise in the PR.
