# CROSS-REPOSITORY MECHANISM

## Accurate Description & Claim-Language Correction Guide

*A working reference for describing the V1 ↔ V2 evidence handoff precisely — grounded in the actual workflow file and code in both repositories, not in how the mechanism is sometimes described informally.*

# 1. Why This Guide Exists

The phrase “the repositories are talking” — or softer variants like “V1 and V2 communicate,” “cross-repository trust is working,” or “the evidence travels between the systems” — can be read as implying something the current implementation does not do: two live systems perceiving, negotiating with, or authenticating each other.

What actually exists is real and independently verified (see this project’s audit trail), but it is a narrower thing than “communication.” This guide exists to keep every future description — in docs, in conversation, in any public statement — anchored to the mechanism as it actually runs, not to a more impressive-sounding paraphrase of it.

This is the same discipline this project already applies to seal records and audit worksheets (Stage 15, Item G — documentation honesty): a claim is only as good as the evidence under it, and the fix belongs in the wording, not just in a private understanding of what was “really” meant.

# 2. What Actually Happens, Mechanically

This is a step-by-step account of `.github/workflows/two_checkout_travel.yml`, read directly from the file — not a summary of intent.

**Job 1 — produce (runs once, checks out V1 only)**

1. GitHub Actions checks out Kelronmos/SWI-V1-Module-1-10 into a fresh, disposable virtual machine, into a folder named `v1`.
2. A Python virtual environment is created and V1’s `requirements.txt` is installed into it.
3. `v1/scripts/export_travel_evidence.py` runs inside that VM and writes a file, `evidence.json`, to local disk.
4. That file is uploaded to GitHub’s artifact storage under the name `v1-foundation-evidence`, with a 14-day retention.
5. **The VM is then destroyed.** Nothing about it persists except the uploaded file.

**Job 2 — admit (runs after Job 1, checks out V2 only, on a separate matrix of Python versions)**

1. A **different**, independent virtual machine checks out SWI-V2-Modules-11-22 only. V1’s code is not present anywhere on this machine.
2. A separate virtual environment is built from V2’s `requirements.txt` only.
3. The workflow **downloads** `evidence.json` from GitHub’s artifact storage — the same bytes Job 1 uploaded, fetched over GitHub’s own storage API, not received directly from Job 1.
4. It explicitly tests that `import swi_core` fails, to prove V1’s code is genuinely absent.
5. `scripts/admit_travel_evidence.py` reads `evidence.json` off local disk and calls `admit_foundation_input()`, which checks schema, supported versions, and a SHA-256 integrity digest against the file’s own declared fields.
6. Two more copies of the file, deliberately corrupted, are fed through the same script to confirm each is rejected.
7. The full V2 test suite runs, in isolation, once per Python version (3.10, 3.11, 3.12).

**The only thing that moves between the two jobs is a JSON file, via GitHub’s artifact storage, in one direction, after Job 1 has already finished.**

# 3. What This Is Not

- **Not a live channel.** Job 1 and Job 2 never run at the same time. There is no point at which both systems are “up” simultaneously.
- **Not a negotiation.** Nothing in either job asks the other a question and gets an answer back. Job 2 cannot request different data, retry against Job 1, or affect what Job 1 produced.
- **Not authentication of a sender.** V2 checks that the *file’s contents* are internally consistent (the hash matches the declared fields). It does not check *who* produced the file. Anyone with write access to the workflow, or anyone who could place a correctly-hashed file into that artifact slot, would pass the same check. That gap is explicitly named in `CROSS_REPOSITORY_TRUST_SPECIFICATION.md` as unimplemented — see Section 7.
- **Not emergent.** Every step above exists because a person wrote it into a YAML file, in that exact order, naming that exact artifact. Remove the YAML file and nothing “finds its way” between the repositories on its own.

# 4. What This Is

**An authored CI handoff**: a human-designed pipeline in which one automated job produces a file, a storage layer holds it, and a second automated job — running later, elsewhere, and in isolation from the first — consumes that file and checks it against a fixed set of rules.

A useful non-technical analogy: this is closer to **one office mailing a sealed, tamper-evident envelope to a second office, which checks the seal before opening it**, than to two offices being on a phone call. The seal check is real and meaningful — it genuinely proves the envelope’s *contents* weren’t altered in transit — but it says nothing about who is on the other end of the line, because there is no line.

# 5. Correct Vocabulary

| If describing this mechanism, prefer… | Instead of… | Because |
| --- | --- | --- |
| “V2 admits a serialized evidence artifact V1 produced earlier, via a CI-orchestrated handoff” | “V1 and V2 communicate” / “the repos talk” | No live exchange occurs; only a file moves, after the fact |
| “V2 verifies the artifact’s schema and integrity” | “V2 verifies V1” | V2 checks the *file*, not the identity or trustworthiness of whatever produced it |
| “Evidence travel is CI-verified” (matches this repo’s own term) | “Cross-repository trust is verified” | “Trust” is reserved in this project’s own docs for the CRTG signer-identity layer, which is explicitly not implemented |
| “The evidence handoff is authored and scripted” | “The evidence handoff is automatic” or “native” | It runs automatically once triggered, but only because a person wrote every step; “native” implies it’s an inherent property of the two systems, which it isn’t |
| “Integrity-verified” | “Authenticated” | Integrity confirms the bytes weren’t altered; authentication would confirm *who* sent them, which nothing here does yet |

# 6. Where This Distinction Actually Matters

- **In the M11 seal record** (once written): Part G of the seal audit exists specifically to catch language that claims more than the evidence supports. “The repositories communicate” would fail that check the same way “SWI V2 is safe” would.
- **In any public description of SWI**: a reader who hears “cross-repository trust” or “the repos talk” reasonably pictures something closer to live authentication than a scripted file handoff. When the real mechanism is described precisely, the same underlying result — real, independently reproducible artifact verification — still sounds credible, because it is; it just doesn’t invite a bigger claim than what was tested.
- **In distinguishing M11 from CRTG**: M11’s job (integrity + schema admission) and CRTG’s job (signer identity) are different problems. Blurring them into “the repos trust each other” makes it sound like both are solved when only one is.

# 7. What Would Actually Need to Exist for This to Become Real Cross-Repo Trust (CRTG)

This section restates — it does not extend — the existing, already-written `CROSS_REPOSITORY_TRUST_SPECIFICATION.md`, which is explicitly marked PROPOSED / DESIGN PENDING and Not implemented. No private keys in this repository. Per Stage 15, Item 1, CRTG work is currently frozen until M11 is sealed — nothing below is a new design, and nothing below should be built yet.

The proposed hierarchy, verbatim from that spec:

```text
Trusted CA → Repository certificate → Public key
Private signing key → Task signature → Envelope → CRTG → M11 → AdmittedInput
```

For the current mechanism to graduate from “authored CI handoff” to “verified cross-repository trust,” each of these would need to genuinely exist and be tested, in order:

1. **A real private signing key**, held by whatever produces evidence on the V1 side — not present in either repository today.
2. **A signature over the evidence envelope**, made with that key, added as a field V2 can check.
3. **A repository certificate and trusted CA relationship**, so V2 has a basis for trusting *which* public key is allowed to sign V1 evidence at all — not just that some signature is present.
4. **CRTG itself**: the verification step that checks the signature against a trust policy before the envelope is allowed to reach M11.
5. **Tests proving the negative case**: an evidence file signed by an untrusted or absent key must be rejected, the same rigor already applied to M11’s tamper tests in Section 2.

Until all five exist and are independently tested the way M11’s admission logic already has been, “cross-repository trust” remains an accurate label only for the *design*, not for anything currently running.

# 8. Concrete Documentation Edits (applied)

These edits were applied to the live repository:

- `docs/CROSS_REPO_TRAVEL.md` — mechanism note under Rule
- `docs/KNOWN_LIMITATIONS.md` — handoff is pipeline not native; integrity ≠ identity; stale fixture-only lines corrected
- `docs/CROSS_REPOSITORY_TRUST_SPECIFICATION.md` — left unchanged (already correctly scoped PROPOSED / DESIGN PENDING)

# 9. A Five-Question Check for Any Future Description of This Mechanism

Before publishing or repeating a sentence about the V1/V2 relationship, run it through:

1. Does it imply the two systems run, or are “up,” at the same time? *(They never are.)*
2. Does it imply either system can ask the other something and get a live answer? *(Neither can.)*
3. Does it name or imply a *sender’s identity* being verified? *(Only integrity/schema is verified — see Section 7 for what identity verification would require.)*
4. Does it use “trust” to describe something other than the CRTG design? *(Reserve “trust” for CRTG until CRTG exists.)*
5. Would a reader be surprised, after reading Section 2 of this guide, to learn the actual mechanism is a scripted CI handoff? *(If yes, the sentence overclaims — revise it.)*

If a sentence passes all five, it’s describing what’s actually running.
