# V2 Known Limitations

## M11 admission

- Validates schema, integrity digest, and allowed `verification_status` only.
- Does **not** prove origin, identity, truth, or action safety.
- `created_at` is optional metadata; **not** in the integrity digest.
- Unexpected envelope fields are **rejected** (`UnexpectedFieldError`).
- Default `admit_foundation_input` does **not** prevent replay of the same
  `evidence_id`. Use opt-in `ReplayGuard` for in-process, in-memory replay
  rejection only (no durable/cross-machine cache). Not CRTG.

## ReplayGuard

- In-process / in-memory only.
- Not production replay defense.
- `scripts/admit_travel_evidence.py` still calls `admit_foundation_input`
  directly unless explicitly updated.

## CRTG / Seal 5 / M12–22

- CRTG: DESIGN PENDING
- M11: TESTED / **NOT SEALED** until tip CI + full audit
- M12–22: BLOCKED until M11 sealed
