# Volume 2 Modules 11–15 Consolidated Guide — Handling Note

**Date:** 16 September 2026

An externally compiled document titled *SWI Volume 2 — Modules 11 Through 15* (Consolidated Guide) was supplied. It claims to reproduce the real contents of this repository for Modules 11–15: architecture, contracts, kernel source, module implementation state, and tests.

## Honest status table in the guide (aligned with live repo)

| Module | Guide status | Live repo |
|--------|--------------|-----------|
| **11** Foundation Admission | IMPLEMENTED, TESTED, **NOT SEALED** | Matches (`AUDIT_PARTIAL` / NOT SEALED) |
| **12** Evidence Normalization | TYPE-BOUNDARY STUB ONLY | Matches (`accepted_placeholder`) |
| **13** | EMPTY PLACEHOLDER | Matches |
| **14** | EMPTY PLACEHOLDER | Matches |
| **15** | EMPTY PLACEHOLDER | Matches |

The guide correctly states that nothing in its body should be read as claiming more than this table.

## Decision

- The live repository remains the **authoritative** source of code, tests, CI, and audit evidence.
- The compilation is treated as a **reference / rebuild aid only**.
- **No bulk overwrite** of `swi_v2/`, `test/`, workflows, or existing audit artifacts from the compilation.
- **No** promotion of M11 to SEALED, **no** M12 implementation, **no** M13–15 logic from this step.

## Current controlled position (unchanged)

- M11: **AUDIT_PARTIAL / NOT SEALED** (see `docs/M11_SEAL_AUDIT_WORKSHEET.md`, `docs/M11_AUDIT_SUMMARY.json`)
- Real producer + local two-venv admission demonstrated; Python 3.10/3.11 and independent GitHub Actions verification still pending for full seal eligibility
- M12: DESIGN PENDING / type-boundary scaffold only
- M13–22: BLOCKED
- CRTG: DESIGN PENDING

## Rationale (SWI discipline)

> Evidence before claim.  
> Code → test → result → documentation.  
> Never documentation → assume → implemented / sealed.

Replacing live, audited files with a static compilation would invert that order.

## Next controlled step (if desired)

If the compilation is to be retained in-repo, store it as a clearly labelled reference artifact without altering runtime code, seal status, or MODULE_STATUS.
