# SWI Online Test Rebuild — V1 + V2

Controlled **TEST-ONLY** bootstrap for Structured Workflow Intelligence.

```
ONLINE SOURCE → MATERIALIZE → REBUILD → TEST → INVENTORY → HASH → REPORT
```

## What this does

From a clean computer:

1. Obtains both repositories directly from GitHub
2. Synchronizes safely (fast-forward only)
3. Rebuilds V1 using its own declared mechanism
4. Rebuilds V2 using its existing `tools/rebuild_swi.*` (or equivalent)
5. Runs the actual test suites
6. Records exact commit SHAs
7. Produces a rebuild report and basic inventory
8. Explicitly states that the system remains incomplete and unauthorized

## What this does **not** do

- Does not claim SWI is complete
- Does not claim the system is proven or sealed
- Does not establish production authorization
- Does not manufacture missing nodes or fixtures
- Does not perform destructive Git operations
- Does not import V1 runtime code into V2

## Quick start

### macOS / Linux

```bash
chmod +x start.sh
./start.sh
```

### Windows

```bat
start.bat
```

## Workspace layout created at runtime

```
swi-test-workspace/
├── v1/                 # SWI-V1-Module-1-10 checkout
├── v2/                 # SWI-V2-Modules-11-22 checkout
├── artifacts/          # commit SHAs, manifests
├── reports/            # JSON + Markdown rebuild reports
├── logs/               # rebuild / test logs
└── downloads/          # reserved (currently unused)
```

## Evidence discipline

| Claim                    | Value          |
|--------------------------|----------------|
| System completion        | INCOMPLETE     |
| Proven                   | NO             |
| Sealed                   | NO             |
| Production authorized    | **NO**         |

```
TESTED ≠ PROVEN
PROVEN ≠ SEALED
SEALED ≠ PRODUCTION AUTHORIZED
```

Rebuild success and test results are recorded as observed evidence only.

## Requirements

- Git
- Python 3.10+ (3.12 recommended)

## Licence note

This bootstrap is provided for controlled testing of the public SWI repositories.
It does not alter the licences or seals of those repositories.
