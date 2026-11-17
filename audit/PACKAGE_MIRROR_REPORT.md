# Package Mirror Report

**Local full commit (not yet force-synced via git push):** `3ecc8aad50efcef6160bc8221253efe82952bda2`

| Metric | Value |
|--------|-------|
| Original ZIP files | 88 |
| Restored to working tree | 87 + mismatches fixed |
| PACKAGE_MIRROR | PASS (local) |
| PACKAGE_HASH_VERIFICATION | PASS (local) |
| Remote feature branch before this note | incomplete (~17 files) |

## Acceptance (local)

```
PACKAGE_INVENTORY=PASS
PACKAGE_MIRROR=PASS
PACKAGE_HASH_VERIFICATION=PASS
```

## GitHub publication

`git push` from this environment failed (no HTTPS credentials).
To publish the complete tree from a credentialed machine:

```bash
# After obtaining local clone with commit 3ecc8aa, or re-running the mirror steps:
git checkout feature/swi-iso-evidence-replay-lab
git push -u origin feature/swi-iso-evidence-replay-lab
```

## Governance

```
PROVEN=NO
SEALED=NO
AUTHORIZED=NO
PRODUCTION_AUTHORIZED=NO
ISO_COMPATIBILITY=NOT_ASSESSED
```
