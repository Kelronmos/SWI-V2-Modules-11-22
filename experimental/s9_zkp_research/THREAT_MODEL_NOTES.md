# S9 ZKP Research — Threat Model Notes

**Status:** RESEARCH NOTES  
**Implementation:** NOT IMPLEMENTED  

These notes record the adversarial concerns that any future ZKP integration with SWI must address. They are not a formal threat model and do not claim completeness.

## Adversaries of interest

1. **Malicious prover**  
   Attempts to produce a proof for a false statement (soundness attack).

2. **Curious verifier**  
   Attempts to extract witness information from proofs or transcripts (zero-knowledge failure).

3. **Authority forger**  
   Attempts to treat a valid proof as an AuthorityGrant or as admission.

4. **Execution bypasser**  
   Attempts to treat a valid proof as sufficient to pass the ExecutionGate.

5. **Scope escalator**  
   Attempts to reuse a proof bound to one scope for a different command/scope.

6. **Return-path stripper**  
   Removes or replaces binding/proof material on the path back to the gate.

7. **Setup attacker** (if a trusted setup is used)  
   Compromises toxic waste or parameters.

## Required SWI-specific protections

Even if a proving system is sound and zero-knowledge under its own model:

- A valid proof must not be convertible into an AuthorityGrant.
- A valid proof must not satisfy `require_proceed` / ExecutionGate by itself.
- Escalation records must still carry zero authority.
- Command/scope binding must remain independently verifiable.

## Residual risks that cannot be solved by ZK alone

- Implementation bugs in circuit or host code.
- Side-channel leakage outside the proof protocol.
- Incorrect statement / constraint specification.
- Social or operational misuse of a “PASS” result.
- Compromise of keys or setup material (when applicable).

## Current posture

Because no proving system is implemented, none of the above protections have been demonstrated cryptographically. The existing S9 authority-chain provides only structural and deterministic-integrity controls.
